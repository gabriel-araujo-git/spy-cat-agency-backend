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

---

## 🚀 Getting Started

### 1. Clone and navigate

```bash
git clone https://github.com/YOUR_USERNAME/spy-cat-agency-backend.git
cd spy-cat-agency-backend
