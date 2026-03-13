"""
🕷️ DÉMO PORTFOLIO — Scraper Python + SQLite
============================================
Scrape les dernières actualités tech de Hacker News
et les stocke dans une base de données SQLite.

Auteur  : Ton Nom
Stack   : Python 3 · requests · BeautifulSoup4 · SQLite
Usage   : python scraper_demo.py
"""

import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime


# ── 1. BASE DE DONNÉES ───────────────────────────────────────────────────────

def init_db(db_path: str = "actualites.db") -> sqlite3.Connection:
    """Crée la base et la table si elles n'existent pas encore."""
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            titre       TEXT    NOT NULL,
            lien        TEXT    UNIQUE,
            score       INTEGER,
            commentaires INTEGER,
            scraped_at  TEXT    NOT NULL
        )
    """)
    conn.commit()
    print(f"✅ Base de données prête : {db_path}")
    return conn


# ── 2. SCRAPING ──────────────────────────────────────────────────────────────

def scrape_hacker_news(pages: int = 1) -> list[dict]:
    """Scrape les articles depuis Hacker News."""
    articles = []
    headers = {"User-Agent": "Mozilla/5.0 (portfolio demo scraper)"}

    for page in range(1, pages + 1):
        url = f"https://news.ycombinator.com/?p={page}"
        print(f"📡 Scraping page {page}...")

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"❌ Erreur réseau : {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.select("tr.athing")

        for row in rows:
            # Titre + lien
            title_tag = row.select_one("span.titleline > a")
            if not title_tag:
                continue
            titre = title_tag.get_text(strip=True)
            lien  = title_tag.get("href", "")

            # Score + commentaires (ligne suivante dans le DOM)
            subrow = row.find_next_sibling("tr")
            score = commentaires = 0
            if subrow:
                score_tag = subrow.select_one("span.score")
                if score_tag:
                    score = int(score_tag.text.split()[0])

                links = subrow.select("a")
                for a in links:
                    if "comment" in a.text or "discuss" in a.text:
                        try:
                            commentaires = int(a.text.split()[0])
                        except ValueError:
                            commentaires = 0

            articles.append({
                "titre":        titre,
                "lien":         lien,
                "score":        score,
                "commentaires": commentaires,
                "scraped_at":   datetime.now().isoformat(),
            })

    print(f"🔍 {len(articles)} articles récupérés")
    return articles


# ── 3. STOCKAGE ──────────────────────────────────────────────────────────────

def save_articles(conn: sqlite3.Connection, articles: list[dict]) -> int:
    """Insère les articles (ignore les doublons via UNIQUE sur lien)."""
    inserted = 0
    for art in articles:
        try:
            conn.execute("""
                INSERT OR IGNORE INTO articles
                    (titre, lien, score, commentaires, scraped_at)
                VALUES
                    (:titre, :lien, :score, :commentaires, :scraped_at)
            """, art)
            if conn.total_changes > inserted:
                inserted = conn.total_changes
        except sqlite3.Error as e:
            print(f"⚠️  Erreur insertion : {e}")

    conn.commit()
    return inserted


# ── 4. RAPPORT CONSOLE ───────────────────────────────────────────────────────

def print_report(conn: sqlite3.Connection) -> None:
    """Affiche un résumé des données stockées."""
    total = conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
    top   = conn.execute("""
        SELECT titre, score, commentaires
        FROM   articles
        ORDER  BY score DESC
        LIMIT  5
    """).fetchall()

    print("\n" + "═" * 55)
    print(f"  📊 RAPPORT — {total} articles en base")
    print("═" * 55)
    print(f"  {'TITRE':<38} {'SCORE':>5}  {'COMMENTS':>8}")
    print("─" * 55)
    for titre, score, comments in top:
        titre_court = (titre[:35] + "…") if len(titre) > 35 else titre
        print(f"  {titre_court:<38} {score:>5}  {comments:>8}")
    print("═" * 55)
    print("  💾 Données sauvegardées dans : actualites.db")
    print("═" * 55 + "\n")


# ── 5. MAIN ──────────────────────────────────────────────────────────────────

def main():
    print("\n🚀 Démarrage du scraper Hacker News\n")
    conn     = init_db()
    articles = scrape_hacker_news(pages=2)
    save_articles(conn, articles)
    print_report(conn)
    conn.close()
    print("✅ Terminé !")


if __name__ == "__main__":
    main()
