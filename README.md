# 📚 FastAPI Bookstore API

## 🚀 Overview
This is a **FastAPI-based Bookstore API** that allows users to register, authenticate using JWT tokens, and perform **CRUD operations** on books. The authentication and authorization mechanism ensures that only logged-in users can manipulate book data.

---

## 🛠️ Setup & Installation

### 1️⃣ Clone the Repository
```sh
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2️⃣ Install Dependencies & Create Virtual Environment
This project uses `uv` for dependency management.
```sh
uv sync
```

### 3️⃣ Run the Application
```sh
uvicorn app.main:app --reload
```

Now, the server should be running at `http://127.0.0.1:8000`

---

## 🔑 Authentication & Authorization

### 1️⃣ Register a User
**Endpoint:** `POST /register`
- Takes `username`, `email`, and `password`
- Stores user credentials in **MongoDB (user_collection)**
- Passwords are securely **hashed** before storage

### 2️⃣ Login & Get JWT Token
**Endpoint:** `POST /token`
- Authenticates users using credentials provided in a **Form**
- If authentication is successful, returns a JWT **access_token**

### 🔐 JWT Token Generation
- **Located in:** `core/auth.py`
- **Functions:**
  - `create_password()`: Hashes passwords securely
  - `verify_password()`: Compares plain and hashed passwords
  - `create_token()`: Generates a JWT token using **HS256** algorithm and a **SECRET_KEY** from `.env`

---

## 📦 Database (MongoDB)
**Database Connection File:** `database.py`
- **Collections Used:**
  - `users_collection` → Stores registered users' data
  - `books_collection` → Stores book records

---

## 📜 API Endpoints

### 🏷️ Authentication (`auth.py`)
| Method | Endpoint     | Description  |
|--------|-------------|--------------|
| POST   | `/register` | User Registration |
| POST   | `/token`    | User Login & Get JWT Token |

### 📚 Book CRUD Operations (`book.py`)
| Method | Endpoint   | Description |
|--------|-----------|-------------|
| GET    | `/books`  | Get all books |
| POST   | `/books`  | Add a new book (Requires Authentication) |
| PUT    | `/books/{id}`  | Update a book (Only by the owner) |
| DELETE | `/books/{id}`  | Delete a book (Only by the owner) |

> **🔒 Access Control:** Only **logged-in users** can perform CRUD operations on books. Users can update or delete only **their own** book entries.

---

## 📌 Data Validation
Data validation is handled using **Pydantic** models:
- **`user.py` & `book.py`** define data validation using:
  - `Field` → Enforces constraints on user input
  - `EmailStr` → Ensures valid email format

---

## 📌 Project Structure
```
📂 app
│── 📄 main.py        # FastAPI app instance & route inclusion
│── 📂 core
│   │── 📄 auth.py    # JWT authentication functions
│── 📂 database
│   │── 📄 database.py  # MongoDB connection
│── 📂 models
│   │── 📄 user.py   # User data validation
│   │── 📄 book.py   # Book data validation
│── 📂 api
│   │── 📄 auth.py   # Authentication API endpoints
│   │── 📄 book.py   # Book CRUD API endpoints
│── .env             # Secret keys & configuration
│── requirements.txt # Dependencies
```

---

## 🎯 Future Enhancements
- Add **Swagger UI** (`/docs`) and **Redoc UI** (`/redoc`)
- Implement **role-based access control** for admin & users
- Improve **error handling** for better API robustness

---

## 📝 License
This project is licensed under the MIT License.

💡 **Happy Coding! 🚀**


