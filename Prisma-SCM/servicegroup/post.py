import http.client
import json
import csv

# Mapping folder numbers to API folder names
FOLDER_MAP = {
    "1": "Shared",
    "2": "Mobile Users",
    "3": "Remote Networks",
    "4": "Service Connections",
    "5": "Mobile Users Container",
    "6": "Mobile Users Explicit Proxy"
}

# API Token (Replace with your actual token)
AUTH_TOKEN = "Bearer eyJ0eXAiOiJKV1QiLCJraWQiOiJyc2Etc2lnbi1wa2NzMS0yMDQ4LXNoYTI1Ni8xIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJjdHMiOiJPQVVUSDJfU1RBVEVMRVNTX0dSQU5UIiwiYXVkaXRUcmFja2luZ0lkIjoiYWM4MDk1MTgtZDMyMS00ZWEyLTgyNjgtODVmZGFhYjA4NjU0LTMxNDg1NTg1Iiwic3VibmFtZSI6IjI3YTY5ZDM0LTdhMTUtNGY1NC04NjRmLWVlYWI3OTY1OGUwNCIsImlzcyI6Imh0dHBzOi8vYXV0aC5hcHBzLnBhbG9hbHRvbmV0d29ya3MuY29tOjQ0My9hbS9vYXV0aDIiLCJ0b2tlbk5hbWUiOiJhY2Nlc3NfdG9rZW4iLCJ0b2tlbl90eXBlIjoiQmVhcmVyIiwiYXV0aEdyYW50SWQiOiJlSlA0N1J3ckdBczdZTjk2RUZMU2pjWEZxQ0UiLCJhdWQiOiJ1c2VyMUAxNjkyMTgzMjA1LmlhbS5wYW5zZXJ2aWNlYWNjb3VudC5jb20iLCJuYmYiOjE3NDE1OTEyOTYsImdyYW50X3R5cGUiOiJjbGllbnRfY3JlZGVudGlhbHMiLCJzY29wZSI6WyJwcm9maWxlIiwidHNnX2lkOjE2OTIxODMyMDUiLCJlbWFpbCJdLCJhdXRoX3RpbWUiOjE3NDE1OTEyOTYsInJlYWxtIjoiLyIsImV4cCI6MTc0MTU5MjE5NiwiaWF0IjoxNzQxNTkxMjk2LCJleHBpcmVzX2luIjo5MDAsImp0aSI6IkpyT0dMaS1zMzRtSVVtV09UQWVDbFhiXzlmdyIsInRzZ19pZCI6IjE2OTIxODMyMDUiLCJhY2Nlc3MiOnsicHJuOjE2OTIxODMyMDU6Ojo6IjpbInN1cGVydXNlciIsImJhc2UiXX19.PFdMJVabVcv-rY_nDVaeLyzH2Dk_BdWKlqm5BbyssBvdWinJLhEIaAXlFi0YGzDpiSGQl5jtWJnrvmnITo9se-nuwcoSOtGBJlMkEsOR-ap5NHPXmVtdow6nLo5T2fioGyKTj6vnvvAFvkSDBY9Z1HBLUQvL49zw-jJEYvr3CFVUm8RLtccsqXs8P7WQxXBwijxkqehWsHtf8-p2fCdYY_-_tHk8KfHQfafnuVUC95fwLFR686huqAGEqocSejX0_ZGMp5Iq34Ow5A2SOhmo82lrCx109PBGvsQTmTz3BEqHvcYxqnsUMC9HJbU3aDUmshhOup3FXBZUdqgl1JHLDA"

# Function to process CSV and send API requests
def process_csv(csv_file, folder):
    with open(csv_file, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row.get("Name", "").strip()
            members = row.get("Members", "").strip().split(";")  # Split members by semicolon
            tags = row.get("Tags", "").strip().split(";") if row.get("Tags") else []

            # Validate necessary fields
            if not name or not members or all(m.strip() == "" for m in members):
                print(f"Skipping row due to missing name or service group members: {row}")
                continue

            # Prepare payload
            payload = {
                "name": name,
                "members": members,
                #"tag": tags
            }

            send_request(payload, folder)

# Function to send API request
def send_request(payload, folder):
    conn = http.client.HTTPSConnection("api.sase.paloaltonetworks.com")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': AUTH_TOKEN
    }

    endpoint = f"/sse/config/v1/service-groups?folder={folder.replace(' ', '%20')}"
    conn.request("POST", endpoint, json.dumps(payload), headers)

    res = conn.getresponse()
    data = res.read()
    print(f"Response for {payload['name']}: {data.decode('utf-8')}")

# Get user input for folder selection
print("Select the target folder:")
for key, value in FOLDER_MAP.items():
    print(f"{key}. {value}")

folder_choice = input("Enter the number corresponding to the folder: ").strip()
selected_folder = FOLDER_MAP.get(folder_choice)

if not selected_folder:
    print("Invalid selection. Exiting.")
else:
    csv_file = "C:\\Users\\DELL\\Desktop\\output\\export_objects_service_groups1.csv"  # Update path as needed
    process_csv(csv_file, selected_folder)
