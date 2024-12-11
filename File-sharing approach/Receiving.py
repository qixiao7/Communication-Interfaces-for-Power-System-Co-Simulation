# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 17:59:31 2024

@author: qixiao
"""

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials
import io
import logging
import os
import pandas as pd
import numpy as np
import time

# Google Drive API Setup
SERVICE_ACCOUNT_FILE = 'path_to_service_account.json'  # Path to your service account key file
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Initialize Google Drive API
def initialize_drive_api():
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=credentials)

# Download file from Google Drive
def download_file(drive_service, file_id, output_file_path):
    request = drive_service.files().get_media(fileId=file_id)
    with io.BytesIO() as file_stream:
        downloader = MediaIoBaseDownload(file_stream, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        file_stream.seek(0)
        with open(output_file_path, 'wb') as f:
            f.write(file_stream.read())
    print(f"File downloaded successfully to {output_file_path}")

# Monitor file for updates (simple polling method)
def monitor_and_record_data(drive_service, file_id, local_file_path, output_file_path):
    """Monitor changes to the file on Google Drive and download updates."""
    last_modified = None
    record = []

    while True:
        try:
            # Request metadata with specific fields
            file_metadata = (
                drive_service.files()
                .get(fileId=file_id, fields="id, name, modifiedTime")
                .execute()
            )

            # print("File metadata:", file_metadata)  # Debugging aid

            # Check if the file has been updated
            current_modified = file_metadata.get("modifiedTime")
            if current_modified != last_modified:
                print("File updated. Downloading...")
                download_file(drive_service, file_id, local_file_path)
                # Read and process the file
                data = pd.read_csv(local_file_path, header=None).values
                if data.size > 0:
                    timestamp =time.time()-1732571461  # Current timestamp
                    timestamped_data = np.hstack((np.full((data.shape[0], 1), timestamp), data))  # Add timestamp as a column
                    record.append(timestamped_data)

                    # Save all recorded data to output file
                    all_data = np.vstack(record)
                    pd.DataFrame(all_data).to_csv(output_file_path, index=False, header=False)
                    print(f"Data saved to {output_file_path}")
                last_modified = current_modified

            time.sleep(10)  # Wait before checking again

        except Exception as e:
            print(f"Error monitoring file: {e}")
            time.sleep(5)


# Store the last modified time locally for comparison
def get_file_last_modified(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return f.readline().strip()
    return None

def set_file_last_modified(file_path, last_modified):
    with open(file_path, 'w') as f:
        f.write(last_modified)

if __name__ == "__main__":
    # Initialize the Google Drive API
    drive_service = initialize_drive_api()
    shared_file_id = 'your_shared_file_id'  # Replace with the actual file ID from Google Drive
    local_file_path = 'local_file.csv'  # Local file path to save the downloaded file
    output_file_path = 'received_data.csv'  # File to save cumulative received data

    print("Starting to monitor file and record data...")
    monitor_and_record_data(drive_service, shared_file_id, local_file_path, output_file_path)
