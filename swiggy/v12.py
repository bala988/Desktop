import requests
import time
import json
import os
import csv
from datetime import datetime, timedelta, timezone

# Define the output directory
OUTPUT_DIR = r"C:\Users\DELL\Desktop"

# Ensure the directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to get OAuth token
def get_access_token():
    url = "https://auth.apps.paloaltonetworks.com/oauth2/access_token"
    payload = {
        "grant_type": "client_credentials",
        "scope": "tsg_id:1894915075"
    }
    auth = ("swiggyit@1894915075.iam.panserviceaccount.com", "88bbdad6-38c8-4893-a86f-f756804c309e")
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=payload, auth=auth, headers=headers)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("❌ Error getting token:", response.text)
        return None

# Function to fetch and filter data
def fetch_and_save_json(token):
    url = "https://api.sase.paloaltonetworks.com/seb-api/v1/users"
    now = datetime.now(timezone.utc)
    
    # Add a buffer of 4 hours to cover potential data delays
    start_time = (now - timedelta(hours=28)).strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    params = {
        "limit": 2000,
        "user.last_seen_gte": start_time,
        "user.last_seen_lte": end_time,
        "sort": "user.last_seen",
        "order": "desc"
    }

    headers = {"Accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if not data.get("data"):
            print("No user records found in JSON.")
            return
        
        save_to_json(data.get("data"))
    else:
        print("Error fetching data:", response.text)

# Function to save JSON with unique filename
def save_to_json(data):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"user_data_{timestamp}.json"
        file_path = os.path.join(OUTPUT_DIR, filename)

        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)

        print(f"Data saved successfully: {file_path}")
        convert_json_to_csv(file_path)
    except Exception as e:
        print(f"Error saving JSON: {e}")

# Function to convert JSON to CSV
def convert_json_to_csv(json_file_path):
    try:
        with open(json_file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        users = data if isinstance(data, list) else data.get("data", [])
        if not users:
            print("No user data found in JSON for CSV conversion.")
            return

        csv_filename = json_file_path.replace(".json", ".csv")
        csv_path = os.path.join(OUTPUT_DIR, csv_filename)

        with open(csv_path, "w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["id", "externalId", "email", "lastSeen", "firstSeen", "name", "provider"])
            for user in users:
                writer.writerow([user.get("id"), user.get("externalId"), user.get("email"), user.get("lastSeen"), user.get("firstSeen"), user.get("name"), user.get("provider")])

        print(f"JSON converted to CSV successfully: {csv_path}")
    except Exception as e:
        print(f"Error converting JSON to CSV: {e}")

# Run script every 24 hours (No Overwrite)
while True:
    token = get_access_token()
    if token:
        fetch_and_save_json(token)
    
    print("Waiting 24 hours for the next run...")
    time.sleep(24 * 60 * 60)  # Sleep for 24 hours
