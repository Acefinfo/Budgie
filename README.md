# 🪙 Budgie  
**Version:** Beta v0.1.0-alpha  

A modern **desktop productivity and finance application** that helps you manage expenses, organize notes, chat with friends, and interact with an AI assistant — all in one unified platform.

---

## 🎯 Goal
Build a **smart, all-in-one personal desktop app** that combines financial tracking, note-taking, communication, and AI assistance for a seamless, efficient, and enjoyable experience.

---

## ✨ Features

### 💰 Expense Tracker
- Add, edit, delete, and view transactions  
- Categorize expenses (Food, Travel, Bills, etc.)  
- Visualize spending with interactive charts  
- Store data locally with optional backend sync  

### 🗒️ Notes *(Planned)*
- Create, edit, and delete notes  
- Search and organize with tags  
- Local storage with optional cloud sync  
- AI-assisted summarization *(future)*  

### 💬 Chat *(Planned)*
- Real-time messaging between users  
- Friend list with online/offline status  
- Store chat history locally or via backend  
- Group chat, file sharing, and encryption *(future)*  

### 🤖 AI Assistant *(Planned)*
- Answer finance and productivity queries  
- Summarize or analyze notes automatically  
- Provide smart suggestions and reminders  
- Learn user habits for personalized insights  

### 🖥️ Desktop Interface
- **Flow:** Login → Dashboard → Expense / Notes / Chat / AI sections  
- Clean, responsive UI using **PySide6 (Qt for Python)**  
- Interactive data visualization and analytics  
- Consistent theme and smooth navigation  

---

## 🧩 Tech Stack

**Language:** Python 3.10+  

**Frontend (Desktop App):**
- PySide6 — UI creation and navigation  
- requests — API communication  
- matplotlib — Data visualization  
- os, pathlib, datetime — File and date management  

**Backend:**
- FastAPI — REST API and route handling  
- uvicorn — Local development server  
- SQLAlchemy — ORM for database models  
- passlib, jwt — Authentication and security  
- PostgreSQL — Database  
- requests-oauthlib — Google OAuth integration  

---

## ⚙️ Setup Instructions

### 🖥️ Backend

1. Create a `.env` file inside the `backend` folder with:
   Find the file .env.example in 
   [Backend env file example](backend\.env.example)
   **If not found:**
   ```
   # Database
   DATABASE_URL=Your_Database_URL_Here

   # JWT Settings
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60

   # Google OAuth
   GOOGLE_CLIENT_ID=your_google_client_id_here
   GOOGLE_CLIENT_SECRET=your_google_client_secret_here


   GOOGLE_REDIRECT_URI=your_google_redirect_uri_here
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the backend server:
   ```
   uvicorn main:app --reload
   ```

---

### 💻 Frontend (Desktop App)

1. Install dependencies:
   ```
   pip install PySide6 requests matplotlib
   ```

2. Launch the app:
   ```
   python main.py
   ```

---

## 🚀 Release

**Budgie Beta v0.1.0-alpha** is available as a pre-release on GitHub:  
🔗 [Budgie Releases](https://github.com/Acefinfo/Budgie/releases)

**Included in this beta:**
- Dashboard navigation  
- Expense tracker (basic logic + UI)  
- Google OAuth login  

**Known limitations:**  
Notes, Chat, and AI modules are under active development.

---

## 📁 Project Structure
```
Budgie/
├─ backend/
│  ├─ main.py
│  ├─ models/
│  ├─ services/
│  └─ .env
├─ desktop_app/
│  ├─ main.py
│  ├─ ui/
│  └─ services/
└─ README.md
```

---

## 🤝 Contributing
Contributions are welcome!  
Fork the repo, open issues, or submit pull requests.  
Help is especially appreciated for the **Notes**, **Chat**, and **AI Assistant** modules.

---

## 📜 License
This project is licensed under the **MIT License**.  
See the [LICENSE](./LICENSE) file for more details.

---

## 🪶 Author
**Acefinfo**  
💻 [GitHub Profile](https://github.com/Acefinfo)
