import http.client
import json
import csv

# API Connection Setup
conn = http.client.HTTPSConnection("api.sase.paloaltonetworks.com")

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJraWQiOiJyc2Etc2lnbi1wa2NzMS0yMDQ4LXNoYTI1Ni8xIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJjdHMiOiJPQVVUSDJfU1RBVEVMRVNTX0dSQU5UIiwiYXVkaXRUcmFja2luZ0lkIjoiNGZiYTJiMzItY2E0OC00YTE5LWIwMmMtYjYxNjFmNzQ1NDUwLTE1NDAzMjE2OCIsInN1Ym5hbWUiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJpc3MiOiJodHRwczovL2F1dGguYXBwcy5wYWxvYWx0b25ldHdvcmtzLmNvbTo0NDMvYW0vb2F1dGgyIiwidG9rZW5OYW1lIjoiYWNjZXNzX3Rva2VuIiwidG9rZW5fdHlwZSI6IkJlYXJlciIsImF1dGhHcmFudElkIjoiTzBIYVVzOVFQZXpvU1hSYlhGRUh1VDc3TEZVIiwiYXVkIjoidXNlcjFAMTY5MjE4MzIwNS5pYW0ucGFuc2VydmljZWFjY291bnQuY29tIiwibmJmIjoxNzQwNjM3MjEwLCJncmFudF90eXBlIjoiY2xpZW50X2NyZWRlbnRpYWxzIiwic2NvcGUiOlsicHJvZmlsZSIsInRzZ19pZDoxNjkyMTgzMjA1IiwiZW1haWwiXSwiYXV0aF90aW1lIjoxNzQwNjM3MjEwLCJyZWFsbSI6Ii8iLCJleHAiOjE3NDA2MzgxMTAsImlhdCI6MTc0MDYzNzIxMCwiZXhwaXJlc19pbiI6OTAwLCJqdGkiOiI5S2xKaWllakJ6eWJiaXlfSEEwWHUycTE0eWciLCJ0c2dfaWQiOiIxNjkyMTgzMjA1IiwiYWNjZXNzIjp7InBybjoxNjkyMTgzMjA1Ojo6OiI6WyJzdXBlcnVzZXIiLCJiYXNlIl19fQ.Wf9NjxlBBYM22HHNODgK8-sa6K6abswLNNjRBzSUKj3EvHYaWgbANJIj-PH5uHz8cWJjjnIn29JaSp4SeSWa51NA-4Yv7qe8XVsAjfdtK4WCwiRra5P5Twz7WnVKWXy5n425bkSbi4QgJgw5idds1khV9qDQ0JLY7krz5zUFu72dvqwskjz7VgBRoJNnu9f8zG0lMrp6gTu10gXXruTz2EIfJows-qPqUPiucybBRs8lL7UkKdhWoVqCDGE1ExBp9_0OnXeEW0ClOqTGkBfq9_DRPclotxv-1SsGmaYf0NZl5y-xyAHp80AkV5DGMqEx71KvCSsArHvObRkLKrfFKg'
}

# Position Menu
position_options = {
    "1": "pre",
    "2": "post"
}

folder_options = {
    "1": "Shared",
    "2": "Mobile Users",
    "3": "Remote Networks",
    "4": "Service Connections",
    "5": "Mobile Users Container",
    "6": "Mobile Users Explicit Proxy"
}

# User selects Position
print("\nSelect Position:")
for key, value in position_options.items():
    print(f"{key}. {value.capitalize()}")

position_choice = input("Enter the number for Position: ").strip()
position = position_options.get(position_choice, "pre")  # Default to "pre" if invalid

# User selects Folder
print("\nSelect Folder:")
for key, value in folder_options.items():
    print(f"{key}. {value}")

folder_choice = input("Enter the number for Folder: ").strip()
folder = folder_options.get(folder_choice, "Shared")  # Default to "Shared" if invalid

print(f"\nUsing Position: {position}, Folder: {folder}\n")

# File Path
policy_file = r"C:\Users\DELL\Desktop\output\export_policies_security_rulebase3.csv"

# Read CSV and Upload Policies
with open(policy_file, mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)

    seen_names = set()  # Track already processed policy names

    for row in reader:
        policy_name = row.get("Name", "").strip()
        if not policy_name:
            print("Skipping row with missing policy name.")
            continue

        if policy_name in seen_names:
            continue  
        seen_names.add(policy_name)

        # Extract and process Source Address
        raw_source_address = row.get("Source Address", "any").strip()
        source_address_list = [addr.strip() for addr in raw_source_address.split(";") if addr.strip()]

        # Debugging output
        print(f"\nProcessing Policy: {policy_name}")
        print(f"Source Address (Raw): '{raw_source_address}'")
        print(f"Source Address (Processed): {source_address_list}")

        payload = {
            "name": policy_name,
            "action": row.get("Action", "deny").strip(),
            "application": row.get("Application", "any").split(";"),
            "category": row.get("Category", "any").split(";"),
            "destination": row.get("Destination Address", "any").split(";"),
            "service": row.get("Service", "any").split(";"),
            "from": row.get("Source Zone", "any").split(";"),
            "to": row.get("Destination Zone", "any").split(";"),
            "source": row.get("Source", "any").split(";"),
            "source_user": row.get("Source User", "any").split(";"),
            "source_address": source_address_list if source_address_list else ["any"]  # Use "any" if empty
        }

        json_payload = json.dumps(payload)
        print(f"Sending policy: {policy_name}")

        # API Request with Selected Position and Folder
        api_url = f"/sse/config/v1/security-rules?position={position}&folder={folder.replace(' ', '%20')}"
        conn.request("POST", api_url, json_payload, headers)
        res = conn.getresponse()
        data = res.read()

        response = data.decode("utf-8")
        print(f"Response for {policy_name}: {response}")
