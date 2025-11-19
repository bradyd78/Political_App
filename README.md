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

Presentation Layer (MVC Controllers)

This is the topmost layer and consists of the controllers and user interface code.

Components:

AppManager

UserController

BillController

PoliticalFigureController

Responsibilities:

Receives user actions (menu selections, input commands)

Translates UI requests into service-layer calls

Formats data before displaying back to the user

Does not implement business logic

Communication:

Controllers → call → Service Layer Managers
Controllers → display output → User

This is equivalent to the Presentation Layer described in the sample file where Spring Controllers handle requests and rely on Services to execute logic 

SampleReadMeFile

.

Business / Service Layer

This layer contains the core logic of the system. It mirrors the “Service” section of the sample project, which includes InfluencerService, ReviewService, and others 

SampleReadMeFile

.

Components:

UserManager

BillManager

PoliticalFigureManager

Responsibilities:

Validate inputs received from controllers

Apply political app business rules

Coordinate interactions between controllers and models

Prepare data for display or further processing

Communication:

Service Layer → reads/writes → Data Layer
Service Layer → returns results → Controller Layer

This is the same pattern as the Business Layer in the sample file, where business logic is kept separate from controllers and models.

Data / Model Layer

This layer stores the application’s domain data, similar to the Model and Repository sections of the sample file 

SampleReadMeFile

.

Components:

User

Bill

Political_Figure

(Optionally) a file/database storage handler

Responsibilities:

Represent core data structures

Store attributes of domain entities

Support serialization or persistence (future)

Provide structured data to service layer

Communication:

Models → accessed by → Managers
Models → return entity data → Managers

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
