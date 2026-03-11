# Web Vulnerability Scanner

Script Python permettant de detecter automatiquement les vulnerabilites web les plus courantes sur un site cible.

Developpe dans le cadre du projet **SN-AT-002 | Semaine 7** — Writing Efficient Python Code.

---

## Site cible

Le script est configure pour analyser [testphp.vulnweb.com](http://testphp.vulnweb.com/), un site volontairement vulnerable cree par Acunetix pour l'entrainement a la securite. Ne jamais utiliser ce script sur un site sans autorisation explicite.

---

## Vulnerabilites detectees

- **SQL Injection** : injection de payloads SQL dans les champs de formulaire, detection des erreurs retournees par la base de donnees
- **XSS (Cross-Site Scripting)** : injection de code JavaScript, verification si le payload est refleti dans la reponse sans echappement HTML
- **CSRF (Cross-Site Request Forgery)** : detection de l'absence de token CSRF dans les formulaires POST

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
2. Recuperer tous les formulaires de la page
3. Tester chaque formulaire avec les payloads d'injection
4. Generer un fichier `report.txt` avec les vulnerabilites trouvees

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

## Exemple de rapport genere

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

## Bibliotheques utilisees

| Bibliotheque | Role |
|---|---|
| `requests` | Envoi des requetes HTTP (GET, POST) |
| `BeautifulSoup` | Parsing du HTML et extraction des formulaires |
| `urllib.parse` | Reconstruction des URLs relatives en URLs completes |

---

## Avertissement

Ce script est developpe a des fins educatives uniquement. L'utilisation de cet outil sur un site sans autorisation est illegale. Toujours tester dans un environnement controle.
