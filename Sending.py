# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 10:15:28 2024

@author: qxiao3
"""

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaFileUpload
import pandas as pd
import numpy as np
import time
import random
import io

# Google Drive API Setup
SERVICE_ACCOUNT_FILE = 'path_to_service_account.json'  # Replace with your service account key file
SCOPES = ['https://www.googleapis.com/auth/drive']

# Initialize Google Drive API
def initialize_drive_api():
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=credentials)

# Upload file to Google Drive
def upload_file(drive_service, file_id, file_path):
    try:
        file_metadata = {'name': 'shared_file.csv'}  # Update file name if necessary
        media = MediaFileUpload(file_path, mimetype='text/csv')
        updated_file = drive_service.files().update(
            fileId=file_id, 
            media_body=media,
            fields="id"
        ).execute()
        print(f"File uploaded successfully: {updated_file.get('id')}")
    except Exception as e:
        print(f"Error uploading file: {e}")

# Generate and write data to a local file before uploading to Google Drive
def collect_data(load, index):
    timestamp = time.time() - 1732571461
    measurements = [random.randint(0, 10000) for _ in range(500)]  # Simulated random measurements
    return [timestamp] + [load.iloc[0][index * 30]] + measurements

def write_data(data, file_path):
    try:
        df = pd.DataFrame([data])
        df.to_csv(file_path, index=False, header=False)
        print(f"Data written to {file_path} successfully!")
    except Exception as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    # Initialize the Google Drive API
    drive_service = initialize_drive_api()
    shared_file_id = 'your_shared_file_id'  # Replace with the actual file ID of the shared file
    local_file_path = 'shared_file.csv'  # Temporary local file for uploading
    # Load profile data
    df0 = pd.read_csv('load_profile.csv')
    record = np.zeros((1, 502))
    index = 0

    while True:
        try:
            # Collect and write data
            data = collect_data(df0, index)
            write_data(data, local_file_path)

            # Upload updated file to Google Drive
            upload_file(drive_service, shared_file_id, local_file_path)

            # Save record locally for additional purposes
            temp = np.array(data).reshape(1, 502)
            record = np.append(record, temp, axis=0)
            if index % 10 == 0:
                pd.DataFrame(record).to_csv('Sent_data.csv', index=False, header=False)
                print("Local cumulative data saved.")

            time.sleep(30)  # Adjust time interval to read and send data as needed

        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(5)