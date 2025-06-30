
# 🐾 Spy Cat Agency – Backend (FastAPI)

This is the **backend API** for the Spy Cat Agency system. It provides a RESTful interface to manage spy cats, their missions, and their targets.

---

## 🔧 Tech Stack

- FastAPI  
- SQLite  
- SQLAlchemy  
- TheCatAPI (for breed validation)  

---

## 📦 Features

### 🐱 Spy Cats

- Create, retrieve, update, and delete spy cats  
- Fields: `name`, `years_of_experience`, `breed`, `salary`  
- Breed validation via [TheCatAPI](https://thecatapi.com/)  

### 🎯 Missions & Targets

- Create missions with 1–3 targets  
- Assign missions to cats (only one per cat at a time)  
- Mark targets as complete, freeze notes on completion  
- Cannot delete assigned missions  
- Update target notes (unless complete)  

---

## 🚀 Getting Started

### 1. Clone and navigate

```bash
git clone https://github.com/gabriel-araujo-git/spy-cat-agency-backend.git
cd spy-cat-agency-backend
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the FastAPI server

```bash
uvicorn main:app --reload
```

### 5. Access the API

- Base URL: `http://localhost:8000`  
- Swagger Docs: `http://localhost:8000/docs`  
- Redoc: `http://localhost:8000/redoc`  

> ℹ️ The SQLite database (`spycat.db`) will be automatically created on first run.

---

## 📬 Postman Collection

Included in the repo: [`postman_collection.json`](./postman_collection.json)

### To use:

1. Open Postman  
2. Import the collection file  
3. Use pre-configured requests for spy cats CRUD  

---

## 📝 Notes

- Each cat can only have one active mission at a time  
- Notes become immutable once a target or mission is completed  
- Missions assigned to cats cannot be deleted  
- Breed validation is required and uses TheCatAPI  

---

## 📁 Project Structure

```
spy-cat-agency-backend/
├── app/
├── main.py
├── requirements.txt
├── postman_collection.json
├── README.md
└── .gitignore
```

---
