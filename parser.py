import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.cloud import generativelanguage

SCOPES = ['https://www.googleapis.com/auth/drive']
TO_BE_PROCESSED_FOLDER_ID = 'REMOVED'

def get_google_drive_service():
  creds: None
  if os.path.exists('service_account.json'):
    creds = service_account.Credentials.from_service_account_file('service_account.json', scopes=SCOPES)
  return build('drive', 'v3', credentials=creds)
    
    
def main():
  service = get_google_drive_service()
  
  full_results = []
  results = service.files().list(q=f"'{TO_BE_PROCESSED_FOLDER_ID}' in parents", pageSize=1000, fields="files(id, name)", supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
  next_page_token = results.get('nextPageToken')
  full_results = (results.get('files', []))
  
  while (next_page_token != None):
      results = service.files().list(q=f"'{TO_BE_PROCESSED_FOLDER_ID}' in parents", pageSize=1000, pageToken=next_page_token, fields="files(id, name)", supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
      next_page_token = results.get('nextPageToken')
      full_results.extend(results.get('files', []))
  
if __name__ == '__main__':
    main()