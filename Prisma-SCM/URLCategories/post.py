import http.client
import json
import csv

# API Connection Setup
conn = http.client.HTTPSConnection("api.sase.paloaltonetworks.com")
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJraWQiOiJyc2Etc2lnbi1wa2NzMS0yMDQ4LXNoYTI1Ni8xIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJjdHMiOiJPQVVUSDJfU1RBVEVMRVNTX0dSQU5UIiwiYXVkaXRUcmFja2luZ0lkIjoiNGZiYTJiMzItY2E0OC00YTE5LWIwMmMtYjYxNjFmNzQ1NDUwLTEyOTQ4NzgzOCIsInN1Ym5hbWUiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJpc3MiOiJodHRwczovL2F1dGguYXBwcy5wYWxvYWx0b25ldHdvcmtzLmNvbTo0NDMvYW0vb2F1dGgyIiwidG9rZW5OYW1lIjoiYWNjZXNzX3Rva2VuIiwidG9rZW5fdHlwZSI6IkJlYXJlciIsImF1dGhHcmFudElkIjoiendpbldUeUZuNU5tOGVCNzV2RTNiU2UzRERjIiwiYXVkIjoidXNlcjFAMTY5MjE4MzIwNS5pYW0ucGFuc2VydmljZWFjY291bnQuY29tIiwibmJmIjoxNzQwMTI4MzA0LCJncmFudF90eXBlIjoiY2xpZW50X2NyZWRlbnRpYWxzIiwic2NvcGUiOlsicHJvZmlsZSIsInRzZ19pZDoxNjkyMTgzMjA1IiwiZW1haWwiXSwiYXV0aF90aW1lIjoxNzQwMTI4MzA0LCJyZWFsbSI6Ii8iLCJleHAiOjE3NDAxMjkyMDQsImlhdCI6MTc0MDEyODMwNCwiZXhwaXJlc19pbiI6OTAwLCJqdGkiOiJDUzU5OUdJRkgzSFdvRDJmMkd4U3VuZVlDUVUiLCJ0c2dfaWQiOiIxNjkyMTgzMjA1IiwiYWNjZXNzIjp7InBybjoxNjkyMTgzMjA1Ojo6OiI6WyJzdXBlcnVzZXIiLCJiYXNlIl19fQ.rPATvDT89MLj2Zs1q4bhY2jFOl3a9b0OrafbJ-O-kGY1Yrn3t1Dx5uMni6DKGXSjKviuV9QOFO4dMMM9uQutdUIqgjGEyBduvz4BexwBRujNyCVLzEIUQY05nVvXY0QCTRo9LuBDtaBANfbyhw4f_do3AMtAPQYyAEtWiEn2iv6ZnLv9skSQs-KuohNiIWrYImHLHOiTGyc11nhulO0rIzn23RahSaPlf5_KqKKJjg_37SREOktp-6Pi_-COhOwSrO3O9Z5orLS5ulbNcpIWhFIStuQ-SyWPDghAGgK1XzNvPl4AwLo6aM1TZz5yvMCpX6YZClNNL3XukHDAyVZgtQ'  # Replace with actual token
}

# Folder Menu
folder_options = {
    "1": "Shared",
    "2": "Mobile Users",
    "3": "Remote Networks",
    "4": "Service Connection",
    "5": "Mobile User Container",
    "6": "Mobile Users Explicit Proxy"
}

# User selects Folder
print("\nSelect Folder:")
for key, value in folder_options.items():
    print(f"{key}. {value}")
folder_choice = input("Enter the number for Folder: ").strip()
selected_folder = folder_options.get(folder_choice, "Shared")
print(f"\nUsing Folder: {selected_folder}\n")

# CSV File Path
csv_file = r"C:\\Users\\DELL\\Desktop\\output\\export_objects_custom_objects_url-category.csv"

# Read CSV and process data
with open(csv_file, mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        name = row.get("Name", "").strip()
        url_list = [url.strip() for url in row.get("Match", "").split(';') if url.strip()]
        
        if not name or not url_list:
            print(f"Skipping row due to missing name or URLs: {row}")
            continue
        
        payload = json.dumps({
            "description": f"Auto-imported URL category {name}",
            "name": name,
            "list": url_list,
            "type": "URL List"
        })
        
        # Send API request to create URL category
        api_url = f"/sse/config/v1/url-categories?folder={selected_folder.replace(' ', '%20')}"
        conn.request("POST", api_url, payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(f"Response for {name}: {data.decode('utf-8')}")

# Close connection
conn.close()
