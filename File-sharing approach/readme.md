## Communication-Interfaces-for-Power-System-Co-Simulation
********************************************
File-sharing approach via Google Drive
********************************************
## Overview
This approach facilitates data sharing between a local OPAL-RT system and a remote system using Google Drive. The process involves:
1. **Sending Code:** Collecting data periodically from the local OPAL-RT system and uploading it to a shared file in Google Drive via the Google Drive API.
2. **Receiving Code:** Accessing the shared file online from the remote system, detecting updates, downloading the updated file, recording, and processing the data.
## Notes
1. Make sure the service account has Editor access to the shared file.
2. Ensure network connectivity for accessing Google Drive APIs.
3. For additional security, avoid exposing the service account JSON file publicly.
********************************************
## Setup Instructions
1. Install Required Google API Packages
   'pip install google-api-python-client google-auth'
3. Configure the Script: replace 'SERVICE_ACCOUNT_FILE' and 'shared_file_id' with your own path and file id.
   2.1 Provide the Path to Your Service Account JSON File
   To use the Google Drive API, you must set up a service account and obtain its credentials.
   Steps to Obtain the Service Account JSON File:
   1) Navigate to Google Cloud Console.
   2) In the left-hand menu, go to IAM & Admin > Service Accounts.
   3) Select your project (or create a new one if needed).
   4) Click Create Service Account if one does not already exist, and provide a name for it.
   5) Assign an appropriate role (e.g., Project > Owner or Editor) to the service account for accessing Google Drive.
   6) After creating the service account, go to the Keys tab and click Add Key > Create New Key. Select JSON as the key type. This will download the service account JSON file to your computer.
   7) Place the JSON file in a secure location on your computer and provide its path in the script:
      SERVICE_ACCOUNT_FILE = '/path/to/your/service_account_key.json'

   2.2 Provide the Shared File ID
   To access the shared file in Google Drive, you need its unique File ID.
   Steps to Obtain the File ID:
   1) go to Google Drive.
   2) Locate the file you want to share, right-click on it, and select Get link.
   3) Change the file's sharing permissions to grant access to the service account. You can do this by sharing the file with the service account's email address.
   4) Copy the shared file's link. It should look something like this:
      https://drive.google.com/file/d/hsfnjowlfmssnsfnwk154512dgdfgdg/view?usp=sharing
   5) Extract the File ID from the URL. The File ID is the part between /d/ and /view?. For example, in the link above, the File ID is:
      hsfnjowlfmssnsfnwk154512dgdfgdg
   6) Replace the placeholder in the script with your File ID:
      shared_file_id = 'hsfnjowlfmssnsfnwk154512dgdfgdg'
