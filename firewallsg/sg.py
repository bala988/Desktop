from flask import Flask, request, render_template_string, jsonify
from urllib.parse import urlparse
import requests
import csv
import io

app = Flask(__name__)

html_template = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Firewall Policy Updater</title>
  </head>
  <body>
    <div style="margin: 50px;">
      <h2>Firewall Policy Updater</h2>
      <form id="upload-form" method="post" enctype="multipart/form-data">
        <label for="base_url">Firewall Base URL:</label><br>
        <input type="text" id="base_url" name="base_url" required><br><br>

        <label for="api_key">API Key:</label><br>
        <input type="text" id="api_key" name="api_key" required><br><br>

        <label for="security_profile_group">Security Profile Group (if profile is 'none'):</label><br>
        <input type="text" id="security_profile_group" name="security_profile_group"><br><br>

        <label for="wildfire_profile">WildFire Profile (if not already set):</label><br>
        <input type="text" id="wildfire_profile" name="wildfire_profile"><br><br>

        <label for="csv_file">Upload CSV File:</label><br>
        <input type="file" id="csv_file" name="csv_file" accept=".csv" required><br><br>

        <button type="submit">Submit</button>
      </form>
      <div id="response" style="margin-top: 20px;"></div>
    </div>
  </body>
</html>
"""

def update_policy(base_url, api_key, policy_name, security_profile_group=None, wildfire_profile=None, append_wildfire=False):
    # Check if the base_url has a scheme, if not, prepend 'http://'
    parsed_url = urlparse(base_url)
    if not parsed_url.scheme:
        base_url = 'http://' + base_url

    url = f"{base_url}/api/?type=config&action=set&xpath=/config/devices/entry/vsys/entry/rulebase/security/rules/entry[@name='{policy_name}']"

    if security_profile_group:
        url += f"&element=<profile-setting><group><member>{security_profile_group}</member></group></profile-setting>"
    
    if wildfire_profile:
        if append_wildfire:
            url += f"&element=<profile-setting><profiles><wildfire-analysis><member>{wildfire_profile}</member></wildfire-analysis></profiles></profile-setting>"
        else:
            url += f"&element=<profile-setting><profiles><wildfire-analysis><member>{wildfire_profile}</member></wildfire-analysis></profiles></profile-setting>"

    headers = {
        'X-PAN-KEY': api_key
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return f"Successfully updated policy: {policy_name}"
    else:
        return f"Failed to update policy: {policy_name}. Error: {response.text}"

@app.route('/', methods=['GET'])
def home():
    return render_template_string(html_template)

@app.route('/', methods=['POST'])
def upload():
    base_url = request.form.get('base_url')
    api_key = request.form.get('api_key')
    security_profile_group = request.form.get('security_profile_group')
    wildfire_profile = request.form.get('wildfire_profile')
    csv_file = request.files.get('csv_file')

    if not csv_file:
        return jsonify({"error": "No CSV file uploaded."}), 400

    try:
        csv_content = csv_file.read().decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(csv_content))

        results = []
        for row in csv_reader:
            policy_name = row['Name'].strip()
            security_profile = row['Profile'].strip().lower()

            if security_profile == 'none':
                result = update_policy(base_url, api_key, policy_name, security_profile_group=security_profile_group)
                results.append(result)

            elif "profile group" in security_profile:
                results.append(f"Skipping policy: {policy_name}, contains 'Profile Group'.")

            elif "wildfire analysis" in security_profile:
                results.append(f"Skipping policy: {policy_name}, contains 'WildFire Analysis'.")

            elif wildfire_profile and "wildfire analysis" not in security_profile:
                result = update_policy(base_url, api_key, policy_name, wildfire_profile=wildfire_profile, append_wildfire=True)
                results.append(result)

            else:
                results.append(f"Skipping policy: {policy_name}, no update needed.")

        return jsonify({"results": results}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
