# 📚 Book Reviews Web Application

**Дипломный проект выпускника 4 курса колледжа** по специальности "Информационные системы и программирование".

*This web application is a Final Year Diploma Project developed to fulfill the graduation requirements.*

---

### Description
This college diploma project is a full-stack web application for book enthusiasts to share and discover reviews. Users can create accounts, log in, and manage their reviews while also browsing books and authors. The project demonstrates skills in backend development (FastAPI, Python), frontend development (React), database design (SQLite / PostgreSQL), and asynchronous task processing (Celery, Redis).

For your reference, screenshots of the pages have been added, you can see them at the very bottom

---

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

- **Data Base Support**
  - PostgreSQL (recommended for production)
  - SQLite (for development and testing)

- **Email Notifications**
  - Notification about review deletion
  - Notification of Receipt of Administrator Position

- **Responsive Design**
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

---

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
- For PostgreSQL: PostgreSQL server installed and running

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

3. **Data Base Configuration**

    **Option A: SQLite**
    - Set up environment variables for SQLite:
    - Update your `.env` file for SQLite:
      ```bash
        DB_LITE="sqlite+aiosqlite:///BookReviews.db"
        DB_LITE_FOR_ALEMBIC="sqlite:///BookReviews.db"
        ```
      
    **Option B: PostgreSQL (Recommended)**
    - Install PostgreSQL if not already installed
      - Windows: Download from PostgreSQL Official Site
      - macOS: brew install postgresql
      - Linux (Ubuntu): sudo apt install postgresql postgresql-contrib
    - Start PostgreSQL service
    - You can created DB in your command line
      ```bash
        psql -U postgres -h localhost -c "CREATE DATABASE bookreviews"
      ```
    - Update your `.env` file for PostgreSQL:
      ```bash
        DB_HOST=localhost
        DB_PORT=5432
        DB_NAME=bookreviews
        DB_USER=your_postgres_username
        DB_PASSWORD=your_postgres_password

        ASYNC_DATABASE_URL_POSTGRE="postgresql+asyncpg://your_username:your_password@localhost:5432/bookreviews"
        DATABASE_URL_POSTGRE="postgresql://your_username:your_password@localhost:5432/bookreviews"
        ```
    - You can check your PostgreSQL connection:
      ```bash
        cd backend
      ```
      ```bash
      python test_postgres.py
      ```

---

4. **Full Set Up environment variables:**
   - Create a `.env` file in the root directory with the following contents:
     ```bash
     # SQLite
     DB_LITE="sqlite+aiosqlite:///BookReviews.db"
     DB_LITE_FOR_ALEMBIC="sqlite:///BookReviews.db"

     # PostgreSQL
      DB_HOST=localhost
      DB_PORT=5432
      DB_NAME=bookreviews
      DB_USER=your_postgres_username
      DB_PASSWORD=your_postgres_password

      ASYNC_DATABASE_URL_POSTGRE="postgresql+asyncpg://your_username:your_password@localhost:5432/bookreviews"
      DATABASE_URL_POSTGRE="postgresql://your_username:your_password@localhost:5432/bookreviews"

     SECRET_KEY=your_secret_key_here
     ALGORITHM=HS256

     # Email set up
     LOGIN="your_email@mail.ru"
     PASSWORD=your_app_password
     ```

5. **Start Redis server:**
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

- **PostgreSQL connection issue:**     
  - Ensure PostgreSQL service is running
  - Verify username/password in ``.env`` file
  - Check if database exists: run ``test_postgres.py`` to test and create database
  - Ensure ``DB_USER`` has necessary permissions

---

### 📝 License
This project is developed as part of a college curriculum. Please check with the authors for usage permissions.

---

### &#x1F4D6; Preview

#### Register Page
<img width="1044" height="690" alt="image" src="https://github.com/user-attachments/assets/efcfa384-9941-4bd0-954e-f88a0dfcef73" />

---

#### Login Page
<img width="1124" height="665" alt="image" src="https://github.com/user-attachments/assets/6d433dd5-5778-4b2c-ba42-127669e257b6" />

---

#### Profile Page
##### Admin profile
<img width="1239" height="923" alt="image" src="https://github.com/user-attachments/assets/34a673a6-992d-40e0-adaa-d110db259c10" />

<img width="1026" height="910" alt="image" src="https://github.com/user-attachments/assets/c553d346-805b-4e63-9c4c-a22bc28e4894" />

<img width="1427" height="918" alt="image" src="https://github.com/user-attachments/assets/cafd3c88-76ec-44b9-b62d-cc9548a5a391" />

<img width="1050" height="697" alt="image" src="https://github.com/user-attachments/assets/3016da58-2087-460b-9e10-cbc3ca6e946f" />

##### Default user profile
<img width="1261" height="918" alt="image" src="https://github.com/user-attachments/assets/e6d01666-0dbf-497e-a81a-76d4438dcec0" />


<img width="1243" height="899" alt="image" src="https://github.com/user-attachments/assets/01274d4f-6a2f-4680-812b-7f82611cf27b" />

<img width="950" height="929" alt="image" src="https://github.com/user-attachments/assets/aa50b9ff-07dd-4553-b8af-4e58cf252cda" />

---

#### Home Page
<img width="1399" height="926" alt="image" src="https://github.com/user-attachments/assets/8f502b14-1d13-4dc1-92a0-49d250af27ad" />


#### Reviews Page
<img width="1779" height="922" alt="image" src="https://github.com/user-attachments/assets/ce61e39b-bbc2-4ea1-ac50-538b4591f893" />

<img width="1775" height="930" alt="image" src="https://github.com/user-attachments/assets/7e55461e-3d7f-4f91-9ccd-5c6cc02cf1dd" />

---

#### Books Page
<img width="1765" height="919" alt="image" src="https://github.com/user-attachments/assets/1a0ba23d-da9f-49c7-af12-1ef4891eac83" />

<img width="1648" height="926" alt="image" src="https://github.com/user-attachments/assets/698b2a2d-bb79-407f-a070-fe7469a6ca0d" />

---

#### Authors Page
<img width="1546" height="631" alt="image" src="https://github.com/user-attachments/assets/d8d3df8e-0bd0-49d7-b173-3e324cf34331" />

---

#### Users Page
<img width="1460" height="558" alt="image" src="https://github.com/user-attachments/assets/ecdecfdc-b850-4374-836e-67c6dc9c76e2" />

---

#### User Page
<img width="1529" height="925" alt="image" src="https://github.com/user-attachments/assets/7b00d4ce-2ba0-435c-bb14-8518f3aa6e66" />

<img width="1461" height="630" alt="image" src="https://github.com/user-attachments/assets/08fec0cd-bead-48ca-b3c4-4aa15797fd86" />

---

#### Email message about deleted review
<img width="978" height="813" alt="image" src="https://github.com/user-attachments/assets/b7317b4a-97dd-41d4-8203-f61cbe637b89" />

<img width="956" height="716" alt="image" src="https://github.com/user-attachments/assets/6c256057-c7de-4c07-a705-412706a240ab" />



