# 🏛️ Civic Engagement Platform

## 📘 Project Overview
This project is a civic engagement platform designed to help users interact with political content, track bills, follow political figures, and comment on legislation. It integrates a mix of **MVC** and **N-tier layered architecture** to ensure scalability, maintainability, and clear separation of concerns.

---

## 🧱 Software Architecture
<img width="564" height="978" alt="image" src="https://github.com/user-attachments/assets/e3812d80-f48d-490c-81b1-e7c4eb54b228" />


### 📊 Architectural Diagram

> ⚠️ **Diagram Edits Needed:**
> - Add arrows between layers:
>   - From each Controller to its corresponding Service
>   - From each Service to the Database
> - Add View components next to each Controller (e.g., `BillView`, `UserView`)
> - Add Repository classes in the Data Access Layer (e.g., `BillRepository`, `UserRepository`)
> - Rename “SupaBase/Firebase?” to “Database Layer” and list both as options
> - Add a legend or color key to distinguish Controllers, Services, Models, and Repositories

---

### 🧠 Architecture Explanation

This application uses a hybrid of **Model-View-Controller (MVC)** and **Layered Architecture**, organized into three layers:

#### 1. Presentation Layer
- **Controllers:**
  - `BillController`
  - `PoliticalFigureController`
  - `UserController`
  - `PoliticalNewsFeedController`
  - `CommentController`
- **Views:**
  - `BillView`
  - `UserView`
  - `NewsFeedView`
  - `CommentView`
- **Role:** Handles HTTP requests, user interactions, and delegates logic to the service layer.

#### 2. Service Layer
- **Models/Services:**
  - `Bill`
  - `User`
  - `PoliticalFigure`
  - `BAPublishes`
  - `PoliticalNewsFeed`
  - `CommentOnBill`
- **Role:** Contains business logic and domain models. Services validate input, enforce rules, and coordinate data flow between controllers and repositories.

#### 3. Data Access Layer
- **Repositories:**
  - `BillRepository`
  - `UserRepository`
  - `CommentRepository`
- **Database:**
  - Supabase or Firebase
- **Role:** Manages data persistence and retrieval. Abstracts database operations from the service layer.

---

### 🔄 Component Communication

- `BillController` → calls `Bill` service → which queries `BillRepository` → which interacts with Supabase.
- `UserController` → interacts with `User` service → which reads/writes user data via `UserRepository` → stored in Firebase.
- `PoliticalNewsFeedController` → uses `PoliticalNewsFeed` service → which aggregates news from the database.
- `CommentController` → calls `CommentOnBill` service → which stores comments via `CommentRepository`.

---

## 🧩 Technology Stack

| Layer             | Technologies                     |
|------------------|----------------------------------|
| Presentation      | React, HTML/CSS, JavaScript      |
| Service           | Node.js, Express, TypeScript     |
| Data Access       | Supabase, Firebase               |

---

## 🚀 Setup Instructions

```bash
# Clone the repo
git clone https://github.com/yourusername/civic-engagement-platform.git

# Install dependencies
npm install

# Run the app
npm start
