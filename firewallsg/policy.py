import requests
from urllib.parse import urlparse
import csv
import io

# Function to update the WildFire profile without overwriting existing profiles
def update_wildfire_profile(base_url, api_key, policy_name, wildfire_profile):
    # Ensure the base URL has a scheme
    parsed_url = urlparse(base_url)
    if not parsed_url.scheme:
        base_url = 'http://' + base_url

    # Retrieve the current security profile configuration
    get_url = f"{base_url}/api/?type=config&action=get&xpath=/config/devices/entry/vsys/entry/rulebase/security/rules/entry[@name='{policy_name}']/profile-setting/profiles&key={api_key}"
    response = requests.get(get_url, verify=False)

    if response.status_code != 200 or "<response status=\"error\"" in response.text:
        return f"Failed to retrieve profiles for policy: {policy_name}. Error: {response.text}"

    # Check if WildFire Analysis is already present
    if wildfire_profile in response.text:
        return f"WildFire Analysis already exists for policy: {policy_name}. No update needed."

    # Add WildFire Analysis to the existing profiles
    set_url = f"{base_url}/api/?type=config&action=set&xpath=/config/devices/entry/vsys/entry/rulebase/security/rules/entry[@name='{policy_name}']/profile-setting/profiles/wildfire-analysis"
    set_url += f"&element=<member>{wildfire_profile}</member>&key={api_key}"

    set_response = requests.get(set_url, verify=False)
    if set_response.status_code == 200 and "<response status=\"success\"" in set_response.text:
        return f"Successfully updated WildFire Analysis for policy: {policy_name}"
    else:
        return f"Failed to update WildFire Analysis for policy: {policy_name}. Error: {set_response.text}"

# Read the CSV and update policies
def process_policies(csv_file_path, base_url, api_key, wildfire_profile):
    results = []

    # Read the CSV file
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            policy_name = row['Policy Name'].strip()

            # Update the WildFire Analysis profile for each policy
            result = update_wildfire_profile(base_url, api_key, policy_name, wildfire_profile)
            results.append(result)

    return results
