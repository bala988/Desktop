from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
import csv
import requests

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Folder for uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home Route - Show form to input token details and upload files
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Token generation details
        client_id = request.form['client_id']
        client_secret = request.form['client_secret']
        folder = request.form['folder']
        rule_position = request.form['rule_position']

        # File uploads
        address_file = request.files['address_file']
        service_file = request.files['service_file']
        security_rules_file = request.files['security_rules_file']

        # Save files to upload folder
        if address_file:
            address_path = os.path.join(app.config['UPLOAD_FOLDER'], address_file.filename)
            address_file.save(address_path)
        if service_file:
            service_path = os.path.join(app.config['UPLOAD_FOLDER'], service_file.filename)
            service_file.save(service_path)
        if security_rules_file:
            security_rules_path = os.path.join(app.config['UPLOAD_FOLDER'], security_rules_file.filename)
            security_rules_file.save(security_rules_path)

        # Call token fetch and push logic
        token = fetch_token(client_id, client_secret)
        if token:
            # Process the uploaded files and push converted rules
            address_data = read_file(address_path)
            service_data = read_file(service_path)
            security_rules_data = read_file(security_rules_path)

            push_converted_rules(address_data, service_data, security_rules_data, token, folder, rule_position)
            flash('Rules successfully converted and pushed to Prisma Access!', 'success')
        else:
            flash('Error generating token, please check your details', 'error')

        return redirect(url_for('index'))

    return render_template('index.html')

def fetch_token(client_id, client_secret):
    """Fetch a new token using the provided client_id and client_secret."""
    url = "https://auth.apps.paloaltonetworks.com/oauth2/access_token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        token_data = response.json()
        return token_data.get("access_token")
    else:
        print(f"Error fetching token: {response.status_code}, {response.text}")
        return None

def read_file(file_path):
    """Read CSV or JSON files."""
    try:
        if file_path.endswith(".csv"):
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                return [row for row in reader]
        elif file_path.endswith(".json"):
            with open(file_path, mode='r') as file:
                return json.load(file)
        else:
            raise ValueError("Unsupported file format")
    except Exception as e:
        raise ValueError(f"Error reading file: {str(e)}")

def push_converted_rules(address_data, service_data, security_rules_data, token, folder, rule_position):
    """Simulate pushing converted rules to Prisma Access (this should send API requests)."""
    print(f"Address data: {address_data}")
    print(f"Service data: {service_data}")
    print(f"Security rules data: {security_rules_data}")
    print(f"Pushing converted rules to Prisma Access in folder: {folder} as {rule_position}")
    # In this step, use the token to send the converted data to Prisma Access API

if __name__ == '__main__':
    app.run(debug=True)
