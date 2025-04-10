import http.client
import json
import csv

# API Connection Setup
conn = http.client.HTTPSConnection("api.sase.paloaltonetworks.com")

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJraWQiOiJyc2Etc2lnbi1wa2NzMS0yMDQ4LXNoYTI1Ni8xIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJjdHMiOiJPQVVUSDJfU1RBVEVMRVNTX0dSQU5UIiwiYXVkaXRUcmFja2luZ0lkIjoiNGZiYTJiMzItY2E0OC00YTE5LWIwMmMtYjYxNjFmNzQ1NDUwLTEyOTYxOTczMyIsInN1Ym5hbWUiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJpc3MiOiJodHRwczovL2F1dGguYXBwcy5wYWxvYWx0b25ldHdvcmtzLmNvbTo0NDMvYW0vb2F1dGgyIiwidG9rZW5OYW1lIjoiYWNjZXNzX3Rva2VuIiwidG9rZW5fdHlwZSI6IkJlYXJlciIsImF1dGhHcmFudElkIjoiWXBjU1Z0a1lERzBWbFRIaV95QnlWS2hWYktvIiwiYXVkIjoidXNlcjFAMTY5MjE4MzIwNS5pYW0ucGFuc2VydmljZWFjY291bnQuY29tIiwibmJmIjoxNzQwMTMwODk5LCJncmFudF90eXBlIjoiY2xpZW50X2NyZWRlbnRpYWxzIiwic2NvcGUiOlsicHJvZmlsZSIsInRzZ19pZDoxNjkyMTgzMjA1IiwiZW1haWwiXSwiYXV0aF90aW1lIjoxNzQwMTMwODk5LCJyZWFsbSI6Ii8iLCJleHAiOjE3NDAxMzE3OTksImlhdCI6MTc0MDEzMDg5OSwiZXhwaXJlc19pbiI6OTAwLCJqdGkiOiJpd0pHTU1VYTkyMThEZXRUamhENjNVYXA4dUEiLCJ0c2dfaWQiOiIxNjkyMTgzMjA1IiwiYWNjZXNzIjp7InBybjoxNjkyMTgzMjA1Ojo6OiI6WyJzdXBlcnVzZXIiLCJiYXNlIl19fQ.EPW81hePfL22cNIoKzK9AVMS4Ly_U5Z6Kok3jJwQXIZWRrjHBzF4nwE2-gSuxLNAAB6870cWmRb_m2R_6i6-OxXXrGNXLbArhnw6wFA_rzje0yEFIRgJFS-RxHIb9wQ876I1lgd3YQXyb7SoGFHXLU_IkXiosUOtgwkVn5zruFdswug52-2grNC3fMJg_YbiH0H4x0WZ-3UV8V4fB_El1QC-1ojM7TaqSiTHWXCrC2cdThsIVbH1gfPfqxtlz5L6qZXmq2y9oeqIxDcEII3jbxy3CLvoDPOVFaBGokZ9oQFjt1phr0_zIQE8tmLnO6ZgWRYQUS64HFRLS5tMtBH-7A'
}

# Folder Menu
folder_options = {
    "1": "Shared",
    "2": "Mobile Users",
    "3": "Remote Networks",
    "4": "Service Connection",
    "5": "Mobile User Container",
    "6": "Mobile User Explicit Proxy"
}

# User selects Folder
print("\nSelect Folder:")
for key, value in folder_options.items():
    print(f"{key}. {value}")

folder_choice = input("Enter the number for Folder: ").strip()
folder = folder_options.get(folder_choice, "Shared")

print(f"\nUsing Folder: {folder}\n")

# CSV File Path
csv_file = r"C:\Users\DELL\Desktop\output\export_objects_security_profiles_anti-spyware.csv"

# Read CSV & Send API Requests
with open(csv_file, mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)

    for row in reader:
        name = row.get("Name", "").strip()
        #description = row.get("Description", "").strip()

        if not name:
            print(f"Skipping row due to missing name: {row}")
            continue

        payload = json.dumps({
            #"description": description,
            "name": name,
            #"rules": [],
            #"threat_exception": []
        })

        # API request
        api_url = f"/sse/config/v1/anti-spyware-profiles?folder={folder.replace(' ', '%20')}"
        conn.request("POST", api_url, payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(f"Response for {name}: {data.decode('utf-8')}")

# Close the connection
conn.close()
