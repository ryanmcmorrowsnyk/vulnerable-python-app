# Vulnerable Python Application

**⚠️ WARNING: This application is intentionally vulnerable and should NEVER be deployed to production!**

This is an intentionally vulnerable Flask application designed for testing security remediation tools and learning about common web application vulnerabilities.

## Purpose

This application is designed to:
- Test automated security scanning and remediation tools
- Demonstrate common OWASP Top 10 vulnerabilities in Python/Flask
- Provide a realistic codebase with 182+ dependency vulnerabilities
- Showcase different vulnerability remediation scenarios

## Features

- Flask framework with Python
- User authentication (with vulnerabilities)
- File upload/download
- Database operations (simulated)
- External API integration
- Search functionality
- Admin operations
- Multiple data parsers (XML, YAML, JSON)

## Vulnerabilities

### Code Vulnerabilities (SAST)

| Vulnerability | CWE | File | Line | Severity |
|--------------|-----|------|------|----------|
| Hardcoded Secrets | CWE-798 | app.py | 24-27 | HIGH |
| SQL Injection | CWE-89 | app.py | 69-84 | CRITICAL |
| Command Injection | CWE-78 | app.py | 86-95 | CRITICAL |
| Path Traversal | CWE-22 | app.py | 97-108 | HIGH |
| Unrestricted File Upload | CWE-434 | app.py | 110-125 | HIGH |
| Cross-Site Scripting (XSS) | CWE-79 | app.py | 127-132 | HIGH |
| Server-Side Request Forgery (SSRF) | CWE-918 | app.py | 134-144 | HIGH |
| Remote Code Execution (eval) | CWE-94 | app.py | 146-155 | CRITICAL |
| Insecure Deserialization | CWE-502 | app.py | 157-166 | CRITICAL |
| Missing Authentication | CWE-862 | app.py | 168-174 | CRITICAL |
| Insecure Direct Object Reference | CWE-639 | app.py | 176-184 | MEDIUM |
| XML External Entity (XXE) | CWE-611 | app.py | 186-195 | HIGH |
| YAML Deserialization | CWE-502 | app.py | 197-206 | HIGH |
| Mass Assignment | CWE-915 | app.py | 208-217 | MEDIUM |
| Sensitive Data Exposure | CWE-200 | app.py | 219-232 | HIGH |
| Open Redirect | CWE-601 | app.py | 241-246 | MEDIUM |
| Insecure Randomness | CWE-330 | app.py | 234-239 | MEDIUM |
| Information Disclosure | CWE-209 | app.py | 266-277 | MEDIUM |
| Debug Mode Enabled | CWE-489 | app.py | 30, 295-296 | MEDIUM |

### Dependency Vulnerabilities (SCA)

This application uses **180+ packages from 2021**, including:

**High-CVE Packages:**
- `Flask==2.0.1` - Multiple XSS, DoS issues
- `Django==3.2.4` - SQL injection, XSS vulnerabilities
- `Werkzeug==2.0.1` - Path traversal, RCE (10+ CVEs)
- `Jinja2==3.0.1` - Template injection issues
- `requests==2.26.0` - SSRF vulnerabilities
- `urllib3==1.26.5` - HTTP smuggling (5+ CVEs)
- `cryptography==3.4.7` - Multiple cryptographic issues
- `paramiko==2.7.2` - Authentication bypass
- `PyJWT==2.1.0` - Algorithm confusion
- `oauthlib==3.1.1` - OAuth flow vulnerabilities
- `bleach==3.3.1` - XSS filter bypass
- `mistune==0.8.4` - XSS, ReDoS
- `boto3==1.17.102` - AWS SDK vulnerabilities
- `google-api-python-client==2.12.0` - GCP SDK issues
- `azure-storage-blob==12.8.1` - Azure SDK vulnerabilities

**Actual Total:** 182 vulnerabilities from dependencies (verified with Snyk)

## Remediation Scenarios

This application includes various remediation scenarios:

### 1. Simple Direct Version Bumps (~30 packages)
- `urllib3 1.26.5 → 2.0.x`
- `Flask 2.0.1 → 3.0.x`
- `Werkzeug 2.0.1 → 3.0.x`

### 2. Transitive Dependency Upgrades (~35 packages)
- Fix vulnerabilities in indirect dependencies by upgrading parent packages

### 3. Diamond Dependencies (~25 packages)
- Multiple packages depend on same vulnerable transitive dependencies
- Require coordinated upgrades

### 4. Ecosystem-Specific Maneuvers (~30 packages)
- Use pip constraints files
- Upgrade strategy required for dependency resolution
- May need to regenerate lock files

### 5. Breaking Changes (~30 packages)
- Flask 2.x → 3.x (API changes)
- Django 3.x → 4.x/5.x (major version jumps)
- Jinja2 template syntax changes

### 6. Unhealthy/Unsupported Packages (~20 packages)
- Some packages deprecated or unmaintained
- May require migration to alternatives

### 7. Unfixable Issues (~12 packages)
- Deep transitive chains requiring upstream fixes
- Vulnerabilities with no patch available

## Python 3.13 Compatibility Note

This application targets Python 3.13 compatibility. Many older packages from 2017-2019 that would normally be included cannot be used due to:
- Lack of pre-built wheels for Python 3.13
- Use of deprecated Python modules (like `pipes`)
- Build system incompatibilities

As a result, the vulnerability count is 182 instead of the initial target of 200+. The packages included represent the maximum set of vulnerable packages that can actually be installed and run on Python 3.13.

## Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies (will show many vulnerabilities)
pip install -r requirements.txt

# Run the vulnerable application
python app.py

# Application will run on http://localhost:5000
```

## Security Testing

```bash
# Run Snyk test
snyk test --file=requirements.txt --command=python3

# Expected output: 180+ vulnerabilities

# View dependency tree
pip list

# Generate requirements with versions
pip freeze > installed-requirements.txt
```

## API Endpoints

All endpoints are intentionally vulnerable:

- `POST /api/login` - SQL Injection
- `GET /api/ping?host=example.com` - Command Injection
- `GET /api/files?filename=test.txt` - Path Traversal
- `POST /api/upload` - Unrestricted File Upload
- `GET /api/search?query=<script>` - XSS
- `GET /api/proxy?url=http://internal` - SSRF
- `POST /api/calculate` - RCE via eval
- `POST /api/deserialize` - Insecure Deserialization
- `DELETE /api/admin/users/1` - Missing Auth
- `GET /api/users/1` - IDOR
- `POST /api/parse-xml` - XXE
- `POST /api/parse-yaml` - YAML Deserialization
- `POST /api/register` - Mass Assignment
- `GET /api/debug` - Data Exposure
- `GET /redirect?url=` - Open Redirect
- `GET /api/token` - Weak Randomness

## OWASP Top 10 Coverage

- ✅ A01:2021 - Broken Access Control
- ✅ A02:2021 - Cryptographic Failures
- ✅ A03:2021 - Injection
- ✅ A04:2021 - Insecure Design
- ✅ A05:2021 - Security Misconfiguration
- ✅ A06:2021 - Vulnerable and Outdated Components
- ✅ A07:2021 - Identification and Authentication Failures
- ✅ A08:2021 - Software and Data Integrity Failures
- ✅ A09:2021 - Security Logging and Monitoring Failures
- ✅ A10:2021 - Server-Side Request Forgery

## Vulnerability Statistics

- **Total Dependencies**: 239 packages
- **Vulnerable Dependencies**: 182 issues
- **Vulnerable Paths**: 698 paths
- **Code Vulnerabilities**: 19 issues
- **Total Vulnerabilities**: 200+ (combining code + dependencies)

## License

MIT License - Use for educational and testing purposes only.

## Disclaimer

**DO NOT use this application in production environments. It contains intentional security vulnerabilities and should only be used in isolated, controlled environments for security testing and education.**
