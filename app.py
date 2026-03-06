#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Intentionally Vulnerable Flask Application
DO NOT USE IN PRODUCTION - FOR SECURITY TESTING ONLY
"""

from flask import Flask, request, render_template_string, redirect, session, jsonify, send_file
import os
import subprocess
import pickle
import yaml
import xml.etree.ElementTree as ET
import sqlite3
import hashlib
import jwt
import random
import string
from werkzeug.utils import secure_filename

app = Flask(__name__)

# VULNERABILITY: Hardcoded secrets (CWE-798)
app.config['SECRET_KEY'] = 'super_secret_flask_key_12345'
JWT_SECRET = 'jwt_secret_key_12345'
ADMIN_PASSWORD = 'admin123'
DB_PASSWORD = 'password123'

# VULNERABILITY: Debug mode enabled in production
app.config['DEBUG'] = True

# In-memory user store (simulating database)
users = [
    {'id': 1, 'username': 'admin', 'password': 'hashed_password', 'email': 'admin@example.com', 'role': 'admin'},
    {'id': 2, 'username': 'user', 'password': 'hashed_password', 'email': 'user@example.com', 'role': 'user'}
]

@app.route('/')
def index():
    return '''
    <html>
        <head><title>Vulnerable Python App</title></head>
        <body>
            <h1>Intentionally Vulnerable Flask Application</h1>
            <p>This application contains numerous security vulnerabilities for testing purposes.</p>
            <h2>Available Endpoints:</h2>
            <ul>
                <li>POST /api/login - SQL Injection</li>
                <li>GET /api/ping?host=example.com - Command Injection</li>
                <li>GET /api/files?filename=test.txt - Path Traversal</li>
                <li>POST /api/upload - Unrestricted File Upload</li>
                <li>GET /api/search?query=test - XSS</li>
                <li>GET /api/proxy?url=http://example.com - SSRF</li>
                <li>POST /api/calculate - RCE via eval</li>
                <li>POST /api/deserialize - Insecure Deserialization</li>
                <li>DELETE /api/admin/users/&lt;id&gt; - Missing Authentication</li>
                <li>GET /api/users/&lt;id&gt; - IDOR</li>
                <li>POST /api/parse-xml - XXE Injection</li>
                <li>POST /api/parse-yaml - YAML Deserialization</li>
                <li>POST /api/register - Mass Assignment</li>
                <li>GET /api/debug - Sensitive Data Exposure</li>
                <li>GET /redirect?url= - Open Redirect</li>
            </ul>
        </body>
    </html>
    '''

# VULNERABILITY: SQL Injection (CWE-89)
@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username', '')
    password = request.json.get('password', '')

    # Vulnerable: Direct string formatting simulating SQL injection
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print(f'Query: {query}')  # This would be vulnerable in real SQL

    user = next((u for u in users if u['username'] == username), None)
    if user:
        # VULNERABILITY: Weak JWT signing with predictable secret (CWE-327)
        token = jwt.encode({'id': user['id'], 'username': user['username']}, JWT_SECRET, algorithm='HS256')
        return jsonify({'success': True, 'token': token, 'user': user})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

# VULNERABILITY: Command Injection (CWE-78)
@app.route('/api/ping')
def ping():
    host = request.args.get('host', '')
    # Vulnerable: User input directly in shell command
    try:
        output = subprocess.check_output(f'ping -c 3 {host}', shell=True, stderr=subprocess.STDOUT)
        return jsonify({'success': True, 'output': output.decode('utf-8')})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': e.output.decode('utf-8')})

# VULNERABILITY: Path Traversal (CWE-22)
@app.route('/api/files')
def get_file():
    filename = request.args.get('filename', '')
    # Vulnerable: No sanitization of file path
    try:
        file_path = os.path.join(os.getcwd(), 'uploads', filename)
        with open(file_path, 'r') as f:
            content = f.read()
        return jsonify({'content': content})
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

# VULNERABILITY: Unrestricted File Upload (CWE-434)
@app.route('/api/upload', methods=['POST'])
def upload_file():
    # Vulnerable: No file type validation, no size limits
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    # Using secure_filename but still vulnerable due to no type checking
    filename = secure_filename(file.filename)
    file_path = os.path.join(os.getcwd(), 'uploads', filename)
    file.save(file_path)
    return jsonify({'success': True, 'filename': filename, 'path': file_path})

# VULNERABILITY: Cross-Site Scripting (XSS) (CWE-79)
@app.route('/api/search')
def search():
    query = request.args.get('query', '')
    # Vulnerable: Reflects user input without sanitization
    return f'<h1>Search Results for: {query}</h1>'

# VULNERABILITY: Server-Side Request Forgery (SSRF) (CWE-918)
@app.route('/api/proxy')
def proxy():
    url = request.args.get('url', '')
    # Vulnerable: No URL validation, allows internal network access
    try:
        import requests
        response = requests.get(url)
        return jsonify({'data': response.text, 'status': response.status_code})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# VULNERABILITY: Remote Code Execution via eval() (CWE-94)
@app.route('/api/calculate', methods=['POST'])
def calculate():
    expression = request.json.get('expression', '')
    try:
        # Vulnerable: Direct eval of user input
        result = eval(expression)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# VULNERABILITY: Insecure Deserialization (CWE-502)
@app.route('/api/deserialize', methods=['POST'])
def deserialize():
    data = request.data
    try:
        # Vulnerable: Pickle deserialization can execute arbitrary code
        obj = pickle.loads(data)
        return jsonify({'result': str(obj)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# VULNERABILITY: Missing Authentication (CWE-862)
@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Vulnerable: No authentication or authorization check!
    global users
    users = [u for u in users if u['id'] != user_id]
    return jsonify({'success': True, 'message': 'User deleted'})

# VULNERABILITY: Insecure Direct Object Reference (IDOR) (CWE-639)
@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    # Vulnerable: No authorization check - any user can view any user's data
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404

# VULNERABILITY: XML External Entity (XXE) Injection (CWE-611)
@app.route('/api/parse-xml', methods=['POST'])
def parse_xml():
    xml_data = request.data
    try:
        # Vulnerable: XML parser without XXE protection
        tree = ET.fromstring(xml_data)
        return jsonify({'result': ET.tostring(tree).decode('utf-8')})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# VULNERABILITY: YAML Deserialization (CWE-502)
@app.route('/api/parse-yaml', methods=['POST'])
def parse_yaml():
    yaml_content = request.json.get('yamlContent', '')
    try:
        # Vulnerable: YAML parsing can execute arbitrary code
        parsed = yaml.load(yaml_content)
        return jsonify({'result': parsed})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# VULNERABILITY: Mass Assignment (CWE-915)
@app.route('/api/register', methods=['POST'])
def register():
    # Vulnerable: Directly assigning all properties from user input
    new_user = {
        'id': len(users) + 1,
        **request.json  # Attacker could set role: 'admin'
    }
    users.append(new_user)
    return jsonify({'success': True, 'user': new_user})

# VULNERABILITY: Sensitive Data Exposure (CWE-200)
@app.route('/api/debug')
def debug():
    # Vulnerable: Exposes sensitive environment variables
    return jsonify({
        'environment': dict(os.environ),
        'secret': app.config['SECRET_KEY'],
        'jwt_secret': JWT_SECRET,
        'admin_password': ADMIN_PASSWORD,
        'users': users,
        'config': {
            'db_password': DB_PASSWORD
        }
    })

# VULNERABILITY: Insecure Randomness (CWE-330)
@app.route('/api/token')
def get_token():
    # Vulnerable: random is not cryptographically secure
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    return jsonify({'token': token})

# VULNERABILITY: Open Redirect (CWE-601)
@app.route('/redirect')
def redirect_url():
    url = request.args.get('url', '')
    # Vulnerable: No validation of redirect URL
    return redirect(url)

# VULNERABILITY: Server-Side Template Injection (SSTI) (CWE-94)
@app.route('/api/template')
def template():
    name = request.args.get('name', 'Guest')
    # Vulnerable: User input directly in template
    template = f'<h1>Hello {{{{ name }}}}!</h1>'
    return render_template_string(template, name=name)

# VULNERABILITY: Regex Denial of Service (ReDoS) (CWE-1333)
@app.route('/api/validate-email', methods=['POST'])
def validate_email():
    email = request.json.get('email', '')
    # Vulnerable: Complex regex that can cause ReDoS
    import re
    email_regex = r'^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$'
    is_valid = bool(re.match(email_regex, email))
    return jsonify({'valid': is_valid})

# VULNERABILITY: Information Disclosure through Error Messages (CWE-209)
@app.route('/api/error-test')
def error_test():
    try:
        raise Exception('Database connection failed: mysql://admin:password@localhost:3306/mydb')
    except Exception as e:
        # Vulnerable: Exposes sensitive information in error message
        import traceback
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/health')
def health():
    return jsonify({'status': 'running', 'vulnerabilities': 'many'})

# Error handler that exposes stack traces
@app.errorhandler(Exception)
def handle_error(e):
    # VULNERABILITY: Stack trace exposure (CWE-209)
    import traceback
    return jsonify({
        'error': str(e),
        'type': type(e).__name__,
        'traceback': traceback.format_exc()
    }), 500

if __name__ == '__main__':
    # VULNERABILITY: Running with debug=True and publicly accessible
    app.run(host='0.0.0.0', port=5000, debug=True)
