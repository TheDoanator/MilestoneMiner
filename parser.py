import os
import io
import csv
import docx
import google.generativeai as genai

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']
TO_BE_PROCESSED_FOLDER_ID = 'REMOVED'

def get_google_drive_service():
  creds: None
  if os.path.exists('service_account.json'):
    creds = service_account.Credentials.from_service_account_file('service_account.json', scopes=SCOPES)
  return build('drive', 'v3', credentials=creds)

def get_file_list(service):
  full_results = []
  results = service.files().list(q=f"'{TO_BE_PROCESSED_FOLDER_ID}' in parents", pageSize=1000, fields="files(id, name)", supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
  next_page_token = results.get('nextPageToken')
  full_results = (results.get('files', []))
  
  while (next_page_token != None):
      results = service.files().list(q=f"'{TO_BE_PROCESSED_FOLDER_ID}' in parents", pageSize=1000, pageToken=next_page_token, fields="files(id, name)", supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
      next_page_token = results.get('nextPageToken')
      full_results.extend(results.get('files', []))
  
  return full_results

def read_word_file_from_drive(service, file_id):
  request = service.files().get_media(fileId=file_id)
  file_stream = io.BytesIO()
  downloader = MediaIoBaseDownload(file_stream, request)
  done = False
  while not done:
    done = downloader.next_chunk()
  file_stream.seek(0)
  return file_stream


def extract_text(document):
  text = []
  for section in document.sections:
    for paragraph in section.header.paragraphs:
      text.append(paragraph.text)
    for paragraph in section.footer.paragraphs:
      text.append(paragraph.text)
  for paragraph in document.paragraphs:
    text.append(paragraph.text)
  for table in document.tables:
    for row in table.rows:
      for cell in row.cells:
        text.append(cell.text)
  return text
  
    
def parse_documents(file_list, service):
  for file in file_list:
      file_id = file['id']
      file_name = file['name']
      word_stream = read_word_file_from_drive(service, file_id)
      document = docx.Document(word_stream)
      document_text = extract_text(document)
      prompt_text = "\n".join(document_text)
  return prompt_text
      

def call_gemini(prompt_text):
  genai.configure(api_key='REMOVED')
  model = genai.GenerativeModel('gemini-2.5-flash-lite')
  # response = model.generate_content("You will be given the full text of a license agreement. Your task is to extract milestone-related data into raw CSV text format only with the following columns in this order: OTC Agreement Number, Milestone Name, Milestone Target Completion Date, Milestone Description, Milestone Set Deadline, Milestone Payment. OTC Agreement Number should be extracted from the agreement text. Milestone Name should be either PERFORMANCE MILESTONES for non-payment milestones or MILESTONE PAYMENTS for milestones requiring payment. Milestone Target Completion Date is the due date of the milestone formatted as YYYY-MM-DD. Milestone Description should include the entire original sentence or phrase describing the milestone or payment as written in the agreement, for example 'By November 30, 2025 Licensee will complete milestone A.' Milestone Set Deadline is the same as the Target Completion Date unless a different administrative deadline is given. Milestone Payment should be a numeric value only, for example 3610, or blank if no payment is specified. Only extract milestones from Section 9 (Performance Milestones) and Section 10.5 (Milestone Payments) of the agreement. Convert any dates or dollar amounts written in words into proper numeric format, for example 'three thousand six hundred ten dollars' should be converted to 3610. Format all dates in YYYY-MM-DD. Do not include royalty payments, annual fees, patent reimbursements, or other unrelated payment terms. Repeat the extracted OTC Agreement Number for each milestone row. Output strictly raw CSV text only with no additional formatting, tables, or explanations. Here is the text: " + prompt_text)
  response = model.generate_content("Hi!")
  return response  
    
def main():
  service = get_google_drive_service()
  file_list = get_file_list(service)
      
  if not file_list:
    print('No files found in "To Be Processed" folder.')
    return

  prompt_text = parse_documents(file_list, service)
  output_raw_text = call_gemini(prompt_text)
  output_text = ''.join(part.text for part in output_raw_text.candidates[0].content.parts)
  print(output_text)
  
  # file_object = io.StringIO(output_text)
  # with open('output.csv', 'w', newline='') as csvfile:
  #   writer = csv.writer
    
  
  

if __name__ == '__main__':
    main()