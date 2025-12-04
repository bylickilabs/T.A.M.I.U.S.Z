from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    g,
)
import sqlite3
import os
from datetime import datetime
from difflib import SequenceMatcher
from werkzeug.security import generate_password_hash, check_password_hash

APP_NAME = "T.A.M.I.U.S.Z"
APP_TITLE = "Trusted | Artificial | Memory | Interaction | Unified | Support | Zone"
APP_VERSION = "1.0.0"
APP_COMPANY = "©Thorsten Bylicki | ©BYLICKILABS"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "memory_ai.db")

ADMIN_DEFAULT_USER = "YOUR_NAME_HERE"
ADMIN_DEFAULT_PASSWORD = "YOUR_PASSWORD_HERE"

TRANSLATIONS = {
    "de": {
        "nav_home": "Assistent",
        "nav_admin": "Admin-Portal",
        "nav_logout": "Logout",
        "nav_login": "Login",
        "nav_about": "Info",
        "hero_title": "Dein persönlicher Erinnerungs-Assistent",
        "hero_subtitle": "Stelle Fragen an Thorstens Erinnerungen – sicher in einer Datenbank gespeichert.",
        "ask_placeholder": "Zum Beispiel: Wann habe ich meine Frau kennengelernt?",
        "ask_button": "Frage stellen",
        "no_answer": "Dazu wurde bisher keine passende Erinnerung gespeichert.",
        "best_match": "Gefundene Erinnerung:",
        "admin_login_title": "Admin-Login",
        "admin_username": "Benutzername",
        "admin_password": "Passwort",
        "admin_login_button": "Anmelden",
        "admin_dashboard_title": "Erinnerungs-Datenbank",
        "admin_add_fact": "Neue Erinnerung anlegen",
        "admin_edit_fact": "Erinnerung bearbeiten",
        "admin_question": "Frage / Auslöser",
        "admin_answer": "Antwort / Erinnerungstext",
        "admin_tags": "Tags (optional, Komma-getrennt)",
        "admin_save": "Speichern",
        "admin_cancel": "Abbrechen",
        "admin_created": "Erinnerung wurde gespeichert.",
        "admin_updated": "Erinnerung wurde aktualisiert.",
        "admin_deleted": "Erinnerung wurde gelöscht.",
        "admin_actions": "Aktionen",
        "admin_edit": "Bearbeiten",
        "admin_delete": "Löschen",
        "confirm_delete": "Möchtest du diesen Eintrag wirklich löschen?",
        "login_failed": "Login fehlgeschlagen. Bitte Zugangsdaten prüfen.",
        "logged_out": "Du wurdest abgemeldet.",
        "info_title": "Über diese Anwendung",
        "info_body": (
            "T.A.M.I.U.S.Z ist ein persönlicher Erinnerungs-Assistent. "
            "Im geschützten Admin-Portal können individuelle Lebensdaten, Ereignisse und Fakten "
            "hinterlegt werden. Über die öffentliche Oberfläche können diese Informationen später "
            "über natürliche Fragen und gesetzten Tags wieder abgerufen werden."
        ),
        "lang_label": "Sprache",
        "github_label": "GitHub",
        "footer_rights": "Alle Rechte vorbehalten.",
    },
    "en": {
        "nav_home": "Assistant",
        "nav_admin": "Admin Portal",
        "nav_logout": "Logout",
        "nav_login": "Login",
        "nav_about": "Info",
        "hero_title": "Your Personal Memory Assistant",
        "hero_subtitle": "Ask questions to Thorsten's memories – securely stored in a database.",
        "ask_placeholder": "For example: When did I meet my wife?",
        "ask_button": "Ask",
        "no_answer": "No matching memory has been stored yet.",
        "best_match": "Found memory:",
        "admin_login_title": "Admin Login",
        "admin_username": "Username",
        "admin_password": "Password",
        "admin_login_button": "Sign in",
        "admin_dashboard_title": "Memory Database",
        "admin_add_fact": "Create new memory",
        "admin_edit_fact": "Edit memory",
        "admin_question": "Question / Trigger",
        "admin_answer": "Answer / Memory text",
        "admin_tags": "Tags (optional, comma separated)",
        "admin_save": "Save",
        "admin_cancel": "Cancel",
        "admin_created": "Memory entry has been created.",
        "admin_updated": "Memory entry has been updated.",
        "admin_deleted": "Memory entry has been deleted.",
        "admin_actions": "Actions",
        "admin_edit": "Edit",
        "admin_delete": "Delete",
        "confirm_delete": "Do you really want to delete this entry?",
        "login_failed": "Login failed. Please check your credentials.",
        "logged_out": "You have been logged out.",
        "info_title": "About this application",
        "info_body": (
            "T.A.M.I.U.S.Z is a personal memory assistant. "
            "In the protected admin portal you can store individual life events and facts. "
            "Through the public interface these memories can be queried again via natural "
            "language questions and set tags."
        ),
        "lang_label": "Language",
        "github_label": "GitHub",
        "footer_rights": "All rights reserved.",
    },
}

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_SECRET_KEY_FOR_PRODUCTION"

def get_db():
    """Hole DB-Connection pro Request (g.db)."""
    if "db" not in g:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


@app.teardown_appcontext
def close_db(error=None):
    """DB-Connection nach Request schließen."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Tabellen anlegen und Default-Admin sicherstellen."""
    db = get_db()

    db.execute(
        """
        CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            tags TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )

    db.execute(
        """
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        """
    )

    db.commit()

    cur = db.execute(
        "SELECT id FROM admin_users WHERE username = ?",
        (ADMIN_DEFAULT_USER,),
    )
    if cur.fetchone() is None:
        db.execute(
            "INSERT INTO admin_users (username, password_hash) VALUES (?, ?)",
            (ADMIN_DEFAULT_USER, generate_password_hash(ADMIN_DEFAULT_PASSWORD)),
        )
        db.commit()


@app.before_request
def before_request():
    """Vor jedem Request sicherstellen, dass DB-Struktur existiert."""
    init_db()

def get_texts():
    lang = session.get("lang", "de")
    return TRANSLATIONS.get(lang, TRANSLATIONS["de"])


@app.context_processor
def inject_globals():
    """Globale Variablen in jedes Template injizieren."""
    lang = session.get("lang", "de")
    texts = TRANSLATIONS.get(lang, TRANSLATIONS["de"])
    return dict(
        APP_NAME=APP_NAME,
        APP_TITLE=APP_TITLE,
        APP_VERSION=APP_VERSION,
        APP_COMPANY=APP_COMPANY,
        texts=texts,
        current_lang=lang,
    )

@app.template_filter("nl2br")
def nl2br(value: str) -> str:
    """Zeilenumbrüche in <br> umwandeln (für Antwortanzeige)."""
    if not value:
        return ""
    return value.replace("\n", "<br>")

def find_best_answer(question: str):
    """Finde beste passende Antwort per Fuzzy Matching."""
    db = get_db()
    cur = db.execute("SELECT id, question, answer FROM facts")
    rows = cur.fetchall()

    if not rows:
        return None

    q_norm = (question or "").strip().lower()
    best_row = None
    best_score = 0.0

    for row in rows:
        stored_q = (row["question"] or "").strip().lower()
        if not stored_q:
            continue

        score = SequenceMatcher(None, q_norm, stored_q).ratio()

        if q_norm in stored_q or stored_q in q_norm:
            score += 0.3

        if score > best_score:
            best_score = score
            best_row = row

    if best_score < 0.4:
        return None

    return best_row["answer"]

def login_required(view):
    from functools import wraps

    @wraps(view)
    def wrapped_view(**kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("login"))
        return view(**kwargs)

    return wrapped_view

@app.route("/", methods=["GET", "POST"])
def index():
    texts = get_texts()
    answer = None
    question = ""

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if question:
            best = find_best_answer(question)
            if best:
                answer = best
            else:
                answer = texts["no_answer"]

    return render_template("index.html", question=question, answer=answer)

@app.route("/set_lang/<lang_code>")
def set_lang(lang_code):
    """Sprache umschalten (DE/EN)."""
    if lang_code in TRANSLATIONS:
        session["lang"] = lang_code
    return redirect(request.referrer or url_for("index"))

@app.route("/login", methods=["GET", "POST"])
def login():
    texts = get_texts()

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        db = get_db()
        cur = db.execute(
            "SELECT id, username, password_hash FROM admin_users WHERE username = ?",
            (username,),
        )
        row = cur.fetchone()

        if row and check_password_hash(row["password_hash"], password):
            session["admin_logged_in"] = True
            session["admin_username"] = row["username"]
            return redirect(url_for("admin_dashboard"))
        else:
            flash(texts["login_failed"], "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    texts = get_texts()
    session.clear()
    flash(texts["logged_out"], "info")
    return redirect(url_for("index"))

@app.route("/admin")
@login_required
def admin_dashboard():
    db = get_db()
    cur = db.execute(
        """
        SELECT id, question, answer, tags, created_at, updated_at
        FROM facts
        ORDER BY created_at DESC
        """
    )
    facts = cur.fetchall()
    return render_template("admin_list.html", facts=facts)


@app.route("/admin/new", methods=["GET", "POST"])
@login_required
def admin_new():
    texts = get_texts()

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        answer = request.form.get("answer", "").strip()
        tags = request.form.get("tags", "").strip()

        if question and answer:
            now = datetime.utcnow().isoformat()
            db = get_db()
            db.execute(
                """
                INSERT INTO facts (question, answer, tags, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (question, answer, tags, now, now),
            )
            db.commit()
            flash(texts["admin_created"], "success")
            return redirect(url_for("admin_dashboard"))

    return render_template("admin_edit.html", fact=None)


@app.route("/admin/<int:fact_id>/edit", methods=["GET", "POST"])
@login_required
def admin_edit(fact_id):
    texts = get_texts()
    db = get_db()

    cur = db.execute(
        "SELECT id, question, answer, tags FROM facts WHERE id = ?",
        (fact_id,),
    )
    fact = cur.fetchone()
    if not fact:
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        answer = request.form.get("answer", "").strip()
        tags = request.form.get("tags", "").strip()

        if question and answer:
            now = datetime.utcnow().isoformat()
            db.execute(
                """
                UPDATE facts
                SET question = ?, answer = ?, tags = ?, updated_at = ?
                WHERE id = ?
                """,
                (question, answer, tags, now, fact_id),
            )
            db.commit()
            flash(texts["admin_updated"], "success")
            return redirect(url_for("admin_dashboard"))

    return render_template("admin_edit.html", fact=fact)


@app.route("/admin/<int:fact_id>/delete", methods=["POST"])
@login_required
def admin_delete(fact_id):
    texts = get_texts()
    db = get_db()
    db.execute("DELETE FROM facts WHERE id = ?", (fact_id,))
    db.commit()
    flash(texts["admin_deleted"], "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)