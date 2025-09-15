# 📚 Book Reviews Web Application

**Дипломный проект выпускника 4 курса колледжа** по специальности "Информационные системы и программирование".

*This web application is a Final Year Diploma Project developed to fulfill the graduation requirements.*

---

### Description
This college diploma project is a full-stack web application for book enthusiasts to share and discover reviews. Users can create accounts, log in, and manage their reviews while also browsing books and authors. The project demonstrates skills in backend development (FastAPI, Python), frontend development (React), database design (SQLite), and asynchronous task processing (Celery, Redis).

### 🎓 Academic Notice
This project was developed for educational purposes as a final assignment in the college curriculum. Some features (email notifications, web scraping) are implemented with a focus on demonstrating technical capability and may require specific configuration to work in a production environment.

---

### Features
- **User Management**
  - User registration and authentication
  - Profile management
  - Admin privileges system

- **Book & Review System**
  - Browse books and authors
  - Add, edit, and delete reviews
  - View reviews from other users
  - Automatic book cover & book description retrieval from Bookvoed.com

- **Email Notifications**
  - Notification about review deletion
  - Notification of Receipt of Administrator Position

- **Responsive Design**
  - Mobile-(kind of)friendly interface
  - Clean, modern UI

---

### 📧 Email Configuration
For email functionality to work properly, configure an SMTP provider:

#### For Mail.ru (recommended for Russian users):
1. Log in to your Mail.ru account.
2. Go to Settings → Security → App passwords.
3. Generate a new app password.
4. Use this password in your `.env` file as `PASSWORD`.

#### For Gmail:
1. Enable 2-factor authentication on your Google account.
2. Generate an app password at [Google App Passwords](https://myaccount.google.com/apppasswords).
3. Use the generated password in your `.env` file.
4. Update `MAIL_SERVER` to `smtp.gmail.com`.

### 🗂️ Project Structure
```
BookReviews/
├── .venv/                       # Virtual environment
├── backend/                      # Backend application
│   ├── celery/                  # Celery configuration and tasks
│   ├── email/                   # Email sending configuration
│   ├── parsing/                 # Web scraping and parsing logic
│   └── src/                     # Main source code
│       ├── DAO/                 # Data Access Object layer
│       ├── database/            # Database models and logic
│       ├── helpers/             # Helper functions
│       ├── repository/          # Data repositories
│       └── routes/              # API routes
│       └── main.py              # main python file
├── frontend/                    # Frontend application (React)
├── .env                         # Environment variables
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

### 🚀 Quick Start

#### Prerequisites
- Python 3.11+
- Redis server
- SMTP email account (Gmail, Mail.ru, etc.)
- Node.js (version 14.x or higher recommended)

#### Installation & Setup
1. **Clone the repository and checkout on stable local version:**
   ```bash
   git clone https://github.com/Iwlj4s/BookReviews.git
   cd BookReviews
   git fetch origin
   git checkout -t origin/local-stable-version
   git checkout local-stable-version
   ```

2. **Set up the backend:**
   - Create a virtual environment:
     ```bash
     python -m venv .venv
     ```
   - Activate the virtual environment:
     - Windows:
       ```bash
       .venv\Scripts\Activate
       ```
     - macOS/Linux:
       ```bash
       source .venv/bin/activate
       ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Set up environment variables:**
   - Create a `.env` file in the root directory with the following contents:
     ```bash
     DB_LITE="sqlite+aiosqlite:///BookReviews.db"
     DB_LITE_FOR_ALEMBIC="sqlite:///BookReviews.db"
     SECRET_KEY=your_secret_key_here
     ALGORITHM=HS256
     LOGIN="your_email@mail.ru"
     PASSWORD=your_app_password
     ```

4. **Start Redis server:**
   - Download and run Redis from Redis Installation Guide (for Windows).
   - For macOS:
     ```bash
     brew install redis
     brew services start redis
     ```
   - For Linux:
     ```bash
     sudo apt install redis-server
     sudo systemctl start redis
     ```

#### Run the Backend Application
- Open a terminal and run:
  ```bash
  uvicorn backend.src.main:app --reload
  ```

#### Run the Celery Worker
- Open another terminal and run:
  ```bash
  celery -A backend.celery.celery_app worker --loglevel=info
  ```

#### Swagger docs:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Setting Up the Frontend
1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   - Make sure you have Node.js (version 14.x or higher) installed. Check your Node.js version:
     ```bash
     node -v
     ```

   If you need to install or update Node.js, refer to the [Node.js official website](https://nodejs.org/) and download the latest version.

   Then, run:
   ```bash
   npm install
   ```

3. **Run the Frontend Application:**
   ```bash
   npm run dev
   ```

### Access the Application
Open your browser and navigate to:
- **Backend:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Frontend:** [http://localhost:5173](http://localhost:5173)

---

### 🛠️ Troubleshooting
#### Common Issues
- **Celery authentication errors:** Ensure you're using an app password, not your regular email password. Verify SMTP settings in your `.env` file.
- **Redis connection issues:** Make sure Redis server is running: `redis-cli ping` should return "PONG".

---

### 📝 License
This project is developed as part of a college curriculum. Please check with the authors for usage permissions.

---

### &#x1F4D6; Preview

#### Register Page


#### Login Page


#### Profile Page


#### Home Page


#### Reviews Page


#### Books Page


#### Authors Page


#### Users Page


#### User Page
