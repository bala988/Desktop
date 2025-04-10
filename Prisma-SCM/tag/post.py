import http.client
import json
import csv

# API Connection Setup
conn = http.client.HTTPSConnection("api.sase.paloaltonetworks.com")

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJraWQiOiJyc2Etc2lnbi1wa2NzMS0yMDQ4LXNoYTI1Ni8xIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJjdHMiOiJPQVVUSDJfU1RBVEVMRVNTX0dSQU5UIiwiYXVkaXRUcmFja2luZ0lkIjoiOWU2MzdkODUtNGFmNS00ZDMxLTk1ODEtY2ExYWY4Nzc1YjRiLTExMjkzODY1MiIsInN1Ym5hbWUiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJpc3MiOiJodHRwczovL2F1dGguYXBwcy5wYWxvYWx0b25ldHdvcmtzLmNvbTo0NDMvYW0vb2F1dGgyIiwidG9rZW5OYW1lIjoiYWNjZXNzX3Rva2VuIiwidG9rZW5fdHlwZSI6IkJlYXJlciIsImF1dGhHcmFudElkIjoiSHA3U01XVjlZcVJCQjZtNVpoWXg2dFFvYkNVIiwiYXVkIjoidXNlcjFAMTY5MjE4MzIwNS5pYW0ucGFuc2VydmljZWFjY291bnQuY29tIiwibmJmIjoxNzM5NzkwOTE1LCJncmFudF90eXBlIjoiY2xpZW50X2NyZWRlbnRpYWxzIiwic2NvcGUiOlsicHJvZmlsZSIsInRzZ19pZDoxNjkyMTgzMjA1IiwiZW1haWwiXSwiYXV0aF90aW1lIjoxNzM5NzkwOTE1LCJyZWFsbSI6Ii8iLCJleHAiOjE3Mzk3OTE4MTUsImlhdCI6MTczOTc5MDkxNSwiZXhwaXJlc19pbiI6OTAwLCJqdGkiOiJHODdCRWljXy1ZTWtDVVlZbWc5b0RhY001bWsiLCJ0c2dfaWQiOiIxNjkyMTgzMjA1IiwiYWNjZXNzIjp7InBybjoxNjkyMTgzMjA1Ojo6OiI6WyJzdXBlcnVzZXIiLCJiYXNlIl19fQ.R80z4tso-g6U0Yh2AiS9uqfpZEuhTnR1M3-kvM9QQ16wlgIhb3DGrMQjhZUL8lDg0G-SK5VBviOLiDpUu2H9jzQhVey1hpVJgjc6wb9Mivz4ua_nWK3VZoRmXUsWyJ2-uNG45Sn-PtJ_cJwGTveF6sKKeMw1enqdWGrU-yA7FXyML1xQXUfvw9LBx-xvHCnzu-gPKN3BZTeDpT0dZGpIPsuggQvLwVpxqelWm1ePOOhSY7h2f6R9jDkYFhtu5SkblrGDwySWmw6RDndFdTBiHHnWfg-jF6wSwPL4B9SoTgzplZ63CikRCutz2WrX2f5Uwp8Uvut9-er092u0aD8UMQ'  # Replace with actual token
}

# Folder Menu
folder_options = {
    "1": "Shared",
    "2": "Mobile Users",
    "3": "Remote Networks",
    "4": "Service Connections",
    "5": "Mobile Users Container",
    "6": "Mobile Users Explicit Proxy"
}

# User selects Folder
print("\nSelect Folder:")
for key, value in folder_options.items():
    print(f"{key}. {value}")

folder_choice = input("Enter the number for Folder: ").strip()
folder = folder_options.get(folder_choice, "Shared")  # Default to "Shared" if invalid

print(f"\nUsing Folder: {folder}\n")

# CSV File Path
csv_file = r"C:\Users\DELL\Desktop\output\export_objects_tags.csv"

# Read CSV and Upload Tags
with open(csv_file, mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        tag_name = row.get("Name", "").strip()
        tag_color = row.get("Color", "Red").strip()
        tag_comments = row.get("Comments", "").strip()

        if not tag_name:
            print("Skipping row with missing tag name.")
            continue

        payload = {
            "name": tag_name,
            "color": tag_color,
            "comments": tag_comments
        }

        json_payload = json.dumps(payload)
        print(f"Sending tag: {tag_name}")

        # API Request with Selected Folder
        api_url = f"/sse/config/v1/tags?folder={folder.replace(' ', '%20')}"
        conn.request("POST", api_url, json_payload, headers)
        res = conn.getresponse()
        data = res.read()
        
        response = data.decode("utf-8")
        print(f"Response for {tag_name}: {response}")
