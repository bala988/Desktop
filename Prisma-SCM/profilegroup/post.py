import http.client
import json
import csv

# API Connection Setup
conn = http.client.HTTPSConnection("api.sase.paloaltonetworks.com")

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJraWQiOiJyc2Etc2lnbi1wa2NzMS0yMDQ4LXNoYTI1Ni8xIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJjdHMiOiJPQVVUSDJfU1RBVEVMRVNTX0dSQU5UIiwiYXVkaXRUcmFja2luZ0lkIjoiYWM4MDk1MTgtZDMyMS00ZWEyLTgyNjgtODVmZGFhYjA4NjU0LTMxMzE4MzY4Iiwic3VibmFtZSI6IjI3YTY5ZDM0LTdhMTUtNGY1NC04NjRmLWVlYWI3OTY1OGUwNCIsImlzcyI6Imh0dHBzOi8vYXV0aC5hcHBzLnBhbG9hbHRvbmV0d29ya3MuY29tOjQ0My9hbS9vYXV0aDIiLCJ0b2tlbk5hbWUiOiJhY2Nlc3NfdG9rZW4iLCJ0b2tlbl90eXBlIjoiQmVhcmVyIiwiYXV0aEdyYW50SWQiOiJKUXYtanllVXljQmxTRjZKZDU2ZDUxcURubWsiLCJhdWQiOiJ1c2VyMUAxNjkyMTgzMjA1LmlhbS5wYW5zZXJ2aWNlYWNjb3VudC5jb20iLCJuYmYiOjE3NDE1ODg0NzIsImdyYW50X3R5cGUiOiJjbGllbnRfY3JlZGVudGlhbHMiLCJzY29wZSI6WyJwcm9maWxlIiwidHNnX2lkOjE2OTIxODMyMDUiLCJlbWFpbCJdLCJhdXRoX3RpbWUiOjE3NDE1ODg0NzIsInJlYWxtIjoiLyIsImV4cCI6MTc0MTU4OTM3MiwiaWF0IjoxNzQxNTg4NDcyLCJleHBpcmVzX2luIjo5MDAsImp0aSI6IkN5U3A5ZExSNnBXemFkVDI5OTRVWkZJR2NGbyIsInRzZ19pZCI6IjE2OTIxODMyMDUiLCJhY2Nlc3MiOnsicHJuOjE2OTIxODMyMDU6Ojo6IjpbInN1cGVydXNlciIsImJhc2UiXX19.hhQ0l3FnJsLeL1PISI_Q_HHyMn_G5rLAj1LJjWrd1Gny0uqn5dAsHXf5CsQGbaAZKucg-N58ukGOvloxv0JqrOenldOcRUYzhxcTw9NhJZ7qSpMMfKN5wJdgO6m_Dw9MCxHGeRD74aXSQiOMMjYnMBoaNa-V8xqPoW21Bx5rOrAgjK8QejJ0JHx80i9xdA1GvQ0NRglgPG-Qvfhl30so9n7vBYoknmjeBM65sHqRCSz31h97e-5VdtwqqaxjdhIiC7Gl8xICyvcvF-Vzpfk5QfoLFolBuZOuClj-NGolfgEwgGAjeigikOJ0c9u9ooipzgDfK1ZSSz24RNsg1_KBzQ'
}

# Folder Menu
folder_options = {
    "1": "Shared",
    "2": "Mobile Users",
    "3": "Remote Networks",
    "4": "Mobile Users Container",
    "5": "Mobile Users Explicit Proxy"
}

# User selects Folder
print("\nSelect Folder:")
for key, value in folder_options.items():
    print(f"{key}. {value}")

folder_choice = input("Enter the number for Folder: ").strip()
folder = folder_options.get(folder_choice, "Shared")

print(f"\nUsing Folder: {folder}\n")

# CSV File Path
csv_file_path = r"C:\Users\DELL\Desktop\output\export_objects_security_profile-groups.csv"

# Read CSV and send API requests
with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        name = row.get("Name", "").strip()
        #spyware = row.get("Anti Spyware Profile", "").strip()  # Ensure column name is correct
        
        if not name:
            print(f"Skipping row due to missing name: {row}")
            continue
        
        payload = json.dumps({
            #"dns_security": row.get("dns_security", "").split(','),
            "file_blocking": row.get("File Blocking Profile", "").split(','),
            "name": name,
            #"saas_security": row.get("saas_security", "").split(','),
            "Spyware": row.get("Anti Spyware Profile", "").split(','),
            #"url_filtering": row.get("url_filtering", "").split(','),
            #"virus_and_wildfire_analysis": row.get("virus_and_wildfire_analysis", "").split(','),
            "vulnerability": row.get("Vulnerability Protection Profile", "").split(',')
        })
        
        # Send API request with correct endpoint
        api_url = f"/sse/config/v1/profile-groups?folder={folder.replace(' ', '%20')}"
        conn.request("POST", api_url, payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(f"Response for {name}: {data.decode('utf-8')}")

# Close the connection
conn.close()
