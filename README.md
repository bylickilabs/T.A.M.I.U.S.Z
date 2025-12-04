# T.A.M.I.U.S.Z  
> **Trusted Artificial Memory Interaction & Unified Support Zone**  
  - Powered by **BYLICKILABS – Intelligence Systems & Communications**

---

## 📌 Overview

> **T.A.M.I.U.S.Z** is an advanced AI-inspired memory interaction system that allows you to store, manage, and retrieve personal or organizational knowledge using natural-language questions.

> The platform integrates:

- A **secure administration interface**
- A **public memory assistant**
- Intelligent **AI-like fuzzy matching**
- **Multilingual support** (English & German)
- A modern **Cyberpunk-inspired UI**
- Local, secure **SQLite storage**

> Its mission is simple:
  -  **Preserve knowledge. Enable interaction. Deliver answers.**

---

## ⭐ Core Features

### 🔐 Secure Admin Portal

- Admin login with username and password  
- Central management of all memory entries:
  - **Question / Trigger**
  - **Answer / Memory text**
  - **Tags** (optional)
- Automatic timestamps  
- Password hashing via Werkzeug  

---

### 🧠 AI-Like Memory Interaction

- Natural-language question handling  
- Fuzzy matching evaluates similarity  
- Returns the best matching stored answer  
- Shows fallback when no match is found  
- Preserves formatting via `nl2br` filter  

---

### 🌍 Multilingual Interface (EN/DE)

- Dynamic language switching  
- All system texts maintained in translation dictionaries  
- Easy extension for future languages  

---

### 🎨 Cyberpunk UI

- Modern neon-themed interface  
- Responsive Bootstrap 5 layout  
- Glass-card components  
- GitHub + Info + Language buttons  

---

### 🗄 Local SQLite Database

- Database file: `memory_ai.db`  
- Tables:
  - `facts`
  - `admin_users`  
- Auto-created on first application run  

---

## 🔤 Acronym Definition

```yarn
T.A.M.I.U.S.Z
----------------
T – Trusted
A – Artificial
M – Memory
I – Interaction
U – Unified
S – Support
Z – Zone
```

---

## 🧱 Architecture Overview

### Backend (`app.py`)
- Routing  
- Sessions  
- Language handling  
- Fuzzy matching  
- Database initialization  

### Templates
- base.html  
- index.html  
- login.html  
- admin_list.html  
- admin_edit.html  
- about.html  

### Static
- styles.css  

---

## 📁 Project Structure

```
T.A.M.I.U.S.Z/
├─> app.py
├─> memory_ai.db
├─> requirements.txt
│
├─> static/
│   └─ styles.css
│
└─> templates/
    ├─ base.html
    ├─ index.html
    ├─ login.html
    ├─ admin_list.html
    ├─ admin_edit.html
    └─ about.html
```

---

## 🛠 Installation

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start application
```bash
python app.py
```

---

## 🔑 Default Admin Credentials

> app.py 

| Username | Password |
|:---:|:---:|
| YOUR_NAME_HERE | YOUR_PASSWORD_HERE |

> Change this password immediately.

---

## 🧩 Admin Portal Usage

### Create Entry
- Add Question  
- Add Answer  
- Add Tags  
- Save  

### Edit Entry  
Modify fields → Save

### Delete Entry  
Confirmed deletion  

---

## 🔍 Public Assistant Usage

1. Ask a natural question  
2. System computes similarity  
3. Best match is displayed  
4. Fallback message if no result  

> Example:
  - "When did I graduate?"
  - "Where did I work in 2019?"
  - tags: graduate, 2019, ...

---

## 🧩 Future Enhancements

- Multi-user system  
- Encrypted database layer  
- Semantic search via embeddings  
- JSON/CSV import & export  
- Voice interaction  
- Theming engine  

---

## 📩 Contact

For inquiries or support:  
📧 **bylicki@mail.de**

---

## 📄 License

All rights reserved by  
**BYLICKILABS – Intelligence Systems & Communications**.
[LICENSE](LICENSE)

For commercial use, please request permission:  
📧 **bylicki@mail.de**