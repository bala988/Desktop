import requests
import xml.dom.minidom
from datetime import datetime
import os

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()

# Function to read API key directly from key.env
def load_api_key(file_path="key.env"):
    try:
        with open(file_path, "r") as file:
            for line in file:
                if line.startswith("export API_KEY="):
                    return line.strip().split("=")[1].strip('"')
    except FileNotFoundError:
        print("Error: key.env not found at", file_path)
    except Exception as e:
        print(f"Error reading key.env: {e}")
    return None

# Load API key
api_key = load_api_key()

if not api_key:
    print("Error: API_KEY not found. Please check your key.env file.")
    exit()

print("API Key Loaded Successfully.")

# Variables
firewall_ip = "192.168.29.210"
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M")
filename = f'firewall_config_{current_datetime}.xml'
backup_path = f"C:/Users/DELL/Desktop/firewallbackups/{filename}"
os.makedirs(os.path.dirname(backup_path), exist_ok=True)

# API URL with API key
url = f"https://{firewall_ip}/api/?type=export&category=configuration&key={api_key}"

# Perform API Call
try:
    r = requests.get(url, verify=False)
    if r.status_code != 200:
        print(f"Error: {r.status_code} - {r.text}")
        exit()

    # Format and Save XML
    dom = xml.dom.minidom.parseString(r.text)
    formatted_xml = dom.toprettyxml(indent="  ", newl="\n", encoding="utf-8")

    with open(backup_path, 'wb') as f:
        f.write(formatted_xml)
    
    print(f"Backup successful: {backup_path}")

except requests.exceptions.RequestException as e:
    print(f"Backup failed: {e}")
