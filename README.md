# Web Vulnerability Scanner

Script Python permettant de detecter automatiquement les vulnérabilites web les plus courantes sur un site cible.

Développé dans le cadre du projet **SN-AT-002 | Semaine 7** — Writing Efficient Python Code.

---

## Site cible

Le script est configure pour analyser [testphp.vulnweb.com](http://testphp.vulnweb.com/), un site volontairement vulnérable créé par Acunetix pour l'entrainement à la sécurité. Ne jamais utiliser ce script sur un site sans autorisation explicite.

---

## Vulnérabilités détectées

- **SQL Injection** : injection de payloads SQL dans les champs de formulaire, detection des erreurs retournées par la base de données
- **XSS (Cross-Site Scripting)** : injection de code JavaScript, verification si le payload est refleti dans la reponse sans échappement HTML
- **CSRF (Cross-Site Request Forgery)** : détection de l'absence de token CSRF dans les formulaires POST

---

## Installation

```bash
pip install requests beautifulsoup4 pwntools
```

Il est recommande d'utiliser un environnement virtuel :

```bash
python -m venv env
source env/bin/activate      # Linux / macOS
env\Scripts\activate         # Windows
```

---

## Utilisation

```bash
python final_deliverable.py
```

Le script va :
1. Se connecter au site cible
2. Récupérer tous les formulaires de la page
3. Tester chaque formulaire avec les payloads d'injection
4. Générer un fichier `report.txt` avec les vulnérabilités trouvées

---

## Structure du projet

```
.
├── LIVRABLE_SN-AT-002.pdf   # Script principal (scraping + detection + rapport)
├── report.txt             # Rapport genere automatiquement apres execution
└── test_anthelme (1).py
└── README.md
```

---

## Exemple de rapport généré

```
RAPPORT DE VULNERABILITES - TESTPHP
===================================

Vulnerability: SQL Injection
Endpoint: http://testphp.vulnweb.com/search.php?test=query
Payload: '; DROP TABLE users; --
Recommendation: Use parameterized queries.
--------------------
Vulnerability: XSS
Endpoint: http://testphp.vulnweb.com/search.php?test=query
Payload: <script>alert('XSS')</script>
Recommendation: Escape HTML and use CSP.
--------------------
Vulnerability: CSRF
Endpoint: http://testphp.vulnweb.com/search.php?test=query
Payload: N/A (Missing Token)
Recommendation: Implement CSRF tokens and origin checks.
--------------------
```

---

## Bibliothèques utilisées

| Bibliothèque | Rôle |
|---|---|
| `requests` | Envoi des requêtes HTTP (GET, POST) |
| `BeautifulSoup` | Parsing du HTML et extraction des formulaires |
| `urllib.parse` | Reconstruction des URLs relatives en URLs complètes |

---

## Avertissement

Ce script est dévéloppé à des fins éducatives uniquement. L'utilisation de cet outil sur un site sans autorisation est illegale. Toujours tester dans un environnement controlé.
