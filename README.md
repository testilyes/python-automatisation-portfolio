# 🕷️ Scraper Python + Base de données SQLite

Script Python de scraping automatisé avec stockage en base de données et rapport automatique.

---

## 🎯 Ce que fait ce script

| Avant | Après |
|---|---|
| Copier-coller manuellement des données depuis le web → **2-3h/semaine** | Script automatisé → **5 minutes** |

Concrètement :
- **Scrape** automatiquement des données depuis un site web
- **Stocke** tout proprement dans une base SQLite (sans doublons)
- **Génère** un rapport avec les données les plus pertinentes

---

## 🛠️ Stack technique

- **Python 3.10+**
- **requests** — appels HTTP
- **BeautifulSoup4** — parsing HTML
- **SQLite** — stockage local léger et portable

---

## 🚀 Installation & lancement

```bash
# 1. Cloner le repo
git clone https://github.com/ton-profil/scraper-demo.git
cd scraper-demo

# 2. Installer les dépendances
pip install requests beautifulsoup4

# 3. Lancer le script
python scraper_demo.py
```

---

## 📊 Exemple de résultat

```
🚀 Démarrage du scraper

✅ Base de données prête : actualites.db
📡 Scraping page 1...
📡 Scraping page 2...
🔍 60 articles récupérés

═══════════════════════════════════════════════════════
  📊 RAPPORT — 60 articles en base
═══════════════════════════════════════════════════════
  TITRE                                  SCORE  COMMENTS
───────────────────────────────────────────────────────
  Show HN: I built a tool to...            842       231
  Ask HN: How do you manage...             634       187
  The future of open source AI             521       143
═══════════════════════════════════════════════════════
  💾 Données sauvegardées dans : actualites.db
═══════════════════════════════════════════════════════

✅ Terminé !
```

---

## 🔧 Adaptable à votre besoin

Ce script peut être adapté pour scraper n'importe quelle source :
- 🏪 Prix de produits e-commerce
- 🏠 Annonces immobilières (SeLoger, Leboncoin)
- 📋 Appels d'offres publics
- ⭐ Avis clients (Google, Trustpilot)
- 👥 Leads et contacts professionnels

---

## 📩 Besoin d'un script sur mesure ?

**Développeur Python freelance basé à Paris — livraison en 48-72h**

👉 https://www.malt.fr/profile/ilyesbenyahia1 | 📧 ilyesbenyahia92@gmail.com
