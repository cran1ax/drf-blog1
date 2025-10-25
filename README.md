# Django Blog Project (Decoupled Django Frontend + DRF Backend)

This project demonstrates a blog application built with a decoupled architecture using two separate Django projects:
1.  **Backend (`drf_blog1`)**: A Django REST Framework (DRF) application serving a JSON API for posts and authentication using JWT. Runs on port 8001.
2.  **Frontend (`django_frontend`)**: A traditional Django application serving HTML templates. It fetches data by making HTTP requests to the Backend API. Runs on port 8000.

## 🚀 Architecture Overview

+-----------------+ +-----------------------+ +---------------------+ | User's Browser | ---> | Django Frontend (8000)| ---> | Django Backend (8001)| | (Views HTML) | | (Templates + Views) | | (DRF API + Database)| +-----------------+ | | | +---------------------+ | (requests library) | +-----------------------+


1.  The user interacts with the **Django Frontend** server running on port 8000.
2.  The Frontend's Django views receive the request.
3.  Instead of accessing a database directly, the Frontend views use the `requests` library to call the **Django Backend API** running on port 8001.
4.  The Backend API processes the request (fetches/updates data in its database) and returns JSON data.
5.  The Frontend view receives the JSON data and passes it to its Django templates.
6.  The Frontend server renders the final HTML and sends it to the user's browser.

## 📁 Project Structure

drf_blog1_main/ # Main project folder ├── drf_blog1/ # Backend API Django Project (Port 8001) │ ├── blog/ # - Blog API app │ ├── blog_project/ # - Backend settings/URLs │ ├── venv/ │ ├── db.sqlite3 # - Backend database │ ├── manage.py │ └── requirements.txt ├── django_frontend/ # Frontend Django Project (Port 8000) │ ├── frontend_config/ # - Frontend settings/URLs │ ├── pages/ # - Frontend views app │ ├── templates/ # - HTML templates │ ├── venv/ │ ├── db.sqlite3 # - Frontend database (mostly for sessions) │ ├── manage.py │ └── requirements.txt # - (Should include 'requests') └── README.md # This file


---
## 🔧 Installation & Setup

You need to set up **both** projects separately.

### 1. Backend API Setup (`drf_blog1`)

1.  **Navigate to the backend folder:**
    ```bash
    cd drf_blog1
    ```
2.  **Create and activate virtual environment:**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate
    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run migrations:**
    ```bash
    python manage.py migrate
    ```
5.  **Create a superuser** (optional, for admin access):
    ```bash
    python manage.py createsuperuser
    ```

### 2. Frontend Django Setup (`django_frontend`)

1.  **Navigate to the frontend folder:**
    ```bash
    # From the main project folder (drf_blog1_main)
    cd django_frontend
    ```
2.  **Create and activate virtual environment:**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate
    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies** (Make sure `requests` is in its `requirements.txt` file):
    ```bash
    # Create requirements.txt if it doesn't exist, add 'django' and 'requests'
    pip install django requests
    pip freeze > requirements.txt
    # Or just install directly:
    # pip install django requests
    ```
4.  **Run migrations** (important for the session framework used for storing login tokens):
    ```bash
    python manage.py migrate
    ```

---
## ▶️ Running the Project

You must run **both** servers simultaneously in **separate terminals**.

1.  **Terminal 1: Start Backend API (Port 8001)**
    * Navigate to the `drf_blog1` folder.
    * Activate its `venv`.
    * Run:
      ```bash
      python manage.py runserver 8001
      ```

2.  **Terminal 2: Start Frontend Django (Port 8000)**
    * Navigate to the `django_frontend` folder.
    * Activate its `venv`.
    * Run:
      ```bash
      python manage.py runserver 8000
      ```

Now you can access the **frontend website** in your browser at:
➡️ **`http://127.0.0.1:8000/`**

The **backend API** is running at `http://127.0.0.1:8001/api/`.

---
## 📚 Key Technologies

* **Backend:** Django, Django REST Framework, DRF Simple JWT
* **Frontend:** Django, Django Templates, Python `requests` library
* **Database:** SQLite (separate instance for each project)

---
## 🔐 Authentication

* The **Backend** uses JWT for stateless API authentication (`/api/token/`).
* The **Frontend** simulates a stateful login:
    * It calls the backend's `/api/token/` endpoint.
    * It stores the received JWT `access_token` in its own **Django session**.
    * Frontend views check `request.session.get('access_token')` to see if a user is "logged in".
    * Protected frontend views add the stored token to the `Authorization: Bearer <token>` header when calling protected backend API endpoints.

---
## 🧪 Testing & Development

* Test backend API endpoints using tools like Postman or Insomnia targeting `http://127.0.0.1:8001/api/...`.
* Develop the frontend by modifying views and templates in the `django_frontend` project and accessing `http://127.0.0.1:8000/`.

---
## 📄 License



---

**Happy Coding! 🎉**
