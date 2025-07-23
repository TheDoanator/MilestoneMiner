import os
import io
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
      
    
def main():
  service = get_google_drive_service()
  file_list = get_file_list(service)
      
  if not file_list:
    print('No files found in "To Be Processed" folder.')
    return

  prompt_text = parse_documents(file_list, service)
  with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(prompt_text)
  

if __name__ == '__main__':
    main()