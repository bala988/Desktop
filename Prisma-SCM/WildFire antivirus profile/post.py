import http.client
import json
import csv

# API Connection Setup
conn = http.client.HTTPSConnection("api.sase.paloaltonetworks.com")

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJraWQiOiJyc2Etc2lnbi1wa2NzMS0yMDQ4LXNoYTI1Ni8xIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJjdHMiOiJPQVVUSDJfU1RBVEVMRVNTX0dSQU5UIiwiYXVkaXRUcmFja2luZ0lkIjoiOWU2MzdkODUtNGFmNS00ZDMxLTk1ODEtY2ExYWY4Nzc1YjRiLTEzMDE1Mjk0OSIsInN1Ym5hbWUiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJpc3MiOiJodHRwczovL2F1dGguYXBwcy5wYWxvYWx0b25ldHdvcmtzLmNvbTo0NDMvYW0vb2F1dGgyIiwidG9rZW5OYW1lIjoiYWNjZXNzX3Rva2VuIiwidG9rZW5fdHlwZSI6IkJlYXJlciIsImF1dGhHcmFudElkIjoiVUFUZGF0Y0pqZlNGS2w2QkoyLWZsLXpJWHcwIiwiYXVkIjoidXNlcjFAMTY5MjE4MzIwNS5pYW0ucGFuc2VydmljZWFjY291bnQuY29tIiwibmJmIjoxNzQwMTMzNDQ4LCJncmFudF90eXBlIjoiY2xpZW50X2NyZWRlbnRpYWxzIiwic2NvcGUiOlsicHJvZmlsZSIsInRzZ19pZDoxNjkyMTgzMjA1IiwiZW1haWwiXSwiYXV0aF90aW1lIjoxNzQwMTMzNDQ4LCJyZWFsbSI6Ii8iLCJleHAiOjE3NDAxMzQzNDgsImlhdCI6MTc0MDEzMzQ0OCwiZXhwaXJlc19pbiI6OTAwLCJqdGkiOiI3U21hdlViQzh2bjQtRGNCclFlOFBHelhtN1kiLCJ0c2dfaWQiOiIxNjkyMTgzMjA1IiwiYWNjZXNzIjp7InBybjoxNjkyMTgzMjA1Ojo6OiI6WyJzdXBlcnVzZXIiLCJiYXNlIl19fQ.gr53HI97xmOl0jIiJC-UzUgwOG_k3WGQtZsF062e61fMRlM_HTpPcPXTHMuB-71qix4Y_-Z0rDgEzetvkoLC7_nCf9loG20fzt7uEtTPP0ckJAMfoKeUe7OTOyPNCyUgjDwZwKKXDU1uSD0yewUdLa9gmyNwGavTClHrIt3CxJSM1GRnGdcQyDnnYTQKjJGnjuvqYmZ7fw0fllW_bbWv6TqU8U3vxdeZdLeRwU1PfQLiYHkO1E2huRL87s4Z7xHjR4n5MhyPnNwZgystLKmC_7Es6cEs7ay6EfQqXdXseIJ6mSk6UD75EGIG_RCsk5lIN_IYrWpOPjoh87nNb_xq5g'
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
folder = folder_options.get(folder_choice, "Shared")

print(f"\nUsing Folder: {folder}\n")

# CSV File Path
csv_file_path = r"C:\Users\DELL\Desktop\output\export_objects_security_profiles_wildfire-analysis.csv" # Update if necessary

# Read CSV and send API requests
with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        name = row.get("Name", "").strip()  # Ensure column name is correct
        
        if not name:
            print(f"Skipping row due to missing name: {row}")
            continue
        
        payload = json.dumps({
            "name": name
        })
        
        # Send API request with correct endpoint
        api_url = f"/sse/config/v1/wildfire-anti-virus-profiles?folder={folder.replace(' ', '%20')}"
        conn.request("POST", api_url, payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(f"Response for {name}: {data.decode('utf-8')}")

# Close the connection
conn.close()
