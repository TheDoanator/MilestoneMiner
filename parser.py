import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.cloud import generativelanguage

SCOPES = ['https://www.googleapis.com/auth/drive']

def get_google_drive_service():
  creds: None
  if os.path.exists('service_account.json'):
    creds = service_account.Credentials.from_service_account_file('service_account.json', scopes=SCOPES)
  return build('drive', 'v3', credentials=creds)
    

def main():
  service = get_google_drive_service();