# Political App - Architecture Documentation

## System Overview

This document provides a visual representation of the Political App architecture using Mermaid diagrams.

## Architecture Diagram

```mermaid
graph TB
    subgraph "Client Layer"
        Browser[Web Browser]
    end

    subgraph "Frontend - Flask Application"
        Flask[Flask App<br/>app.py]
        Templates[Templates<br/>HTML Pages]
        Static[Static Assets<br/>CSS/JS]
        
        Templates --> Login[login.html]
        Templates --> Index[index.html]
        Templates --> Map[map.html]
        Templates --> Quiz[quiz.html]
        Templates --> Publishes[publishes.html]
        Templates --> Admin[admin.html]
        
        Static --> CSS[styles.css]
        Static --> MapJS[map.js]
        Static --> AdminJS[admin.js]
        Static --> PublishJS[publishes.js]
    end

    subgraph "Backend - Java Services"
        JavaBackend[Java Backend<br/>Port 8080]
        
        subgraph "Controllers"
            BillCtrl[BillController]
            UserCtrl[UserController]
            CommentCtrl[CommentController]
            PoliticalFigCtrl[PoliticalFigureController]
            NewsCtrl[PoliticalNewsFeedController]
            PublishCtrl[BAPublishesController]
            SettingsCtrl[SettingsController]
        end
        
        subgraph "Services"
            AuthService[AuthenticationService]
            LoginService[LoginService]
            SignupService[SignupService]
        end
        
        subgraph "Models"
            Bill[Bill Model]
            User[User Model]
            Comment[CommentOnBill]
            PoliticalFig[Political_Figure]
            NewsFeed[PoliticalNewsFeed]
            Publish[BAPublishes]
            Settings[Settings Model]
        end
    end

    subgraph "Data Layer"
        Database[(Database)]
        UsersJSON[users.json]
        CommentsJSON[comments.json]
        PublishesJSON[publishes.json]
        BillsTXT[billsList.txt]
        DBController[DatabaseController.java]
    end

    Browser -->|HTTP Requests| Flask
    Flask -->|Render| Templates
    Flask -->|Serve| Static
    Flask -->|API Proxy| JavaBackend
    Flask -->|Read/Write| Database
    
    JavaBackend --> Controllers
    Controllers --> Services
    Controllers --> Models
    JavaBackend -->|Persist| Database
    
    Database --> UsersJSON
    Database --> CommentsJSON
    Database --> PublishesJSON
    Database --> BillsTXT
    Database --> DBController
    
    style Flask fill:#667eea,color:#fff
    style JavaBackend fill:#764ba2,color:#fff
    style Database fill:#28a745,color:#fff
```

## Data Flow Diagram

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant Flask
    participant Session
    participant Database
    participant JavaBackend

    User->>Browser: Access Political App
    Browser->>Flask: GET /
    Flask->>Session: Check user session
    Flask->>Database: Load bills, comments
    Flask->>Browser: Render index.html
    Browser->>User: Display home page

    User->>Browser: Login
    Browser->>Flask: POST /login
    Flask->>Database: Validate credentials
    Database-->>Flask: User data
    Flask->>Session: Create session
    Flask->>Browser: Login success
    Browser->>User: Redirect to home

    User->>Browser: View Bills
    Browser->>Flask: GET /api/bills
    Flask->>Database: Read billsList.txt
    Database-->>Flask: Bill data
    Flask->>Browser: JSON response
    Browser->>User: Display bills

    User->>Browser: Add Comment
    Browser->>Flask: POST /api/bills/:id/comments
    Flask->>Session: Get user info
    Flask->>Database: Save to comments.json
    Database-->>Flask: Success
    Flask->>Browser: Comment saved
    Browser->>User: Update UI
```

## Component Architecture

```mermaid
graph LR
    subgraph "Frontend Pages"
        A[Home Page] --> B[Bills Feed]
        A --> C[Interactive Map]
        A --> D[Civics Quiz]
        A --> E[Publishes]
        A --> F[Admin Panel]
        A --> G[Login/Signup]
    end

    subgraph "Core Features"
        B --> H[Bill Search]
        B --> I[Comments System]
        C --> J[Leaflet Maps]
        C --> K[State Data]
        D --> L[Quiz Engine]
        D --> M[Score Tracking]
        E --> N[Articles/Blogs]
        F --> O[User Management]
        F --> P[Content Creation]
    end

    subgraph "Authentication"
        G --> Q[User Signup]
        G --> R[User Login]
        G --> S[Admin Login]
        Q --> T[Session Management]
        R --> T
        S --> T
    end
```

## Database Schema

```mermaid
erDiagram
    USERS {
        string username PK
        string password
        boolean is_admin
    }
    
    BILLS {
        string id PK
        string title
        string description
        string category
    }
    
    COMMENTS {
        string bill_id FK
        string user
        string text
        datetime timestamp
    }
    
    PUBLISHES {
        int id PK
        string title
        string content
        string type
        datetime timestamp
    }
    
    SETTINGS {
        string user_id FK
        json preferences
    }
    
    USERS ||--o{ COMMENTS : creates
    BILLS ||--o{ COMMENTS : has
    USERS ||--o{ PUBLISHES : creates
    USERS ||--o| SETTINGS : has
```

## API Routes Flow

```mermaid
graph TD
    Start[Client Request] --> Route{Route Type}
    
    Route -->|GET /| Home[Home Page]
    Route -->|GET /login| LoginPage[Login Page]
    Route -->|POST /login| LoginAuth[Authenticate User]
    Route -->|POST /signup| SignupUser[Create New User]
    Route -->|GET /logout| Logout[Clear Session]
    
    Route -->|GET /map| MapPage[Interactive Map]
    Route -->|GET /quiz| QuizPage[Civics Quiz]
    Route -->|GET /publishes| PublishPage[Publishes Feed]
    Route -->|GET /admin| AdminPage[Admin Console]
    
    Route -->|GET /api/bills| GetBills[Fetch Bills]
    Route -->|POST /api/bills| CreateBill[Create Bill - Admin]
    Route -->|GET /api/bills/:id/comments| GetComments[Fetch Comments]
    Route -->|POST /api/bills/:id/comments| AddComment[Add Comment]
    
    Route -->|GET /api/publishes| GetPublishes[Fetch Publishes]
    Route -->|POST /api/publishes| CreatePublish[Create Publish - Admin]
    
    LoginAuth --> Session[Update Session]
    SignupUser --> SaveDB[Save to users.json]
    GetBills --> ReadDB[Read billsList.txt]
    CreateBill --> WriteDB[Write to billsList.txt]
    GetComments --> ReadComments[Read comments.json]
    AddComment --> WriteComments[Write comments.json]
    
    style LoginAuth fill:#667eea,color:#fff
    style CreateBill fill:#dc3545,color:#fff
    style CreatePublish fill:#dc3545,color:#fff
    style AdminPage fill:#ffc107,color:#333
```

## Technology Stack

```mermaid
mindmap
  root((Political App))
    Frontend
      Flask Framework
      Jinja2 Templates
      Bootstrap 5
      Leaflet.js Maps
      Custom CSS/JS
    Backend
      Python Flask
      Java Services
      REST API
    Data Storage
      JSON Files
      Text Files
      Session Storage
    Authentication
      Session Based
      Admin Roles
      User Management
    Features
      Bill Tracking
      Comments System
      Interactive Maps
      Civics Quiz
      News/Publishes
      Admin Panel
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Development Environment"
        DevContainer[Dev Container<br/>Ubuntu 24.04]
        FlaskDev[Flask Dev Server<br/>Port 5000]
        JavaDev[Java Backend<br/>Port 8080]
    end
    
    subgraph "File System"
        Frontend[frontend/src/]
        Backend[backend/]
        Database[database/]
        Static[static/]
        Templates[templates/]
    end
    
    subgraph "Runtime"
        Python[Python 3.12]
        Node[Node.js]
        Java[Java Runtime]
    end
    
    DevContainer --> FlaskDev
    DevContainer --> JavaDev
    FlaskDev --> Frontend
    FlaskDev --> Static
    FlaskDev --> Templates
    JavaDev --> Backend
    
    FlaskDev -.->|Reads/Writes| Database
    JavaDev -.->|Reads/Writes| Database
    
    Python --> FlaskDev
    Java --> JavaDev
    Node -.->|Build Tools| Frontend
    
    style DevContainer fill:#667eea,color:#fff
    style Database fill:#28a745,color:#fff
```

## User Journey Map

```mermaid
journey
    title User Experience Flow
    section First Visit
      Access Website: 5: User
      View Home Page: 5: User
      Browse Bills: 4: User
      Try to Comment: 2: User
    section Authentication
      Click Login: 5: User
      Enter Credentials: 4: User
      Login Success: 5: User
    section Engagement
      Browse Bills: 5: User
      Add Comments: 5: User
      Take Quiz: 4: User
      View Map: 4: User
      Read Publishes: 4: User
    section Admin Flow
      Admin Login: 5: Admin
      Access Admin Panel: 5: Admin
      Create Bills: 5: Admin
      Create Publishes: 5: Admin
      Manage Content: 5: Admin
```

## Security Flow

```mermaid
graph TD
    Request[Incoming Request] --> CheckSession{Session Valid?}
    
    CheckSession -->|No| Public{Public Route?}
    CheckSession -->|Yes| ValidateUser[Validate User Data]
    
    Public -->|Yes| Allow[Allow Access]
    Public -->|No| Redirect[Redirect to Login]
    
    ValidateUser --> CheckAdmin{Admin Required?}
    
    CheckAdmin -->|No| Allow
    CheckAdmin -->|Yes| IsAdmin{Is Admin User?}
    
    IsAdmin -->|Yes| Allow
    IsAdmin -->|No| Deny[403 Forbidden]
    
    Allow --> ProcessRequest[Process Request]
    ProcessRequest --> UpdateSession[Update Session]
    UpdateSession --> Response[Send Response]
    
    style Deny fill:#dc3545,color:#fff
    style Allow fill:#28a745,color:#fff
    style Redirect fill:#ffc107,color:#333
```

---

## File Structure

```
Political_App/
├── frontend/
│   └── src/
│       ├── app.py                 # Main Flask application
│       ├── static/
│       │   ├── css/
│       │   │   └── styles.css     # Global styles
│       │   └── js/
│       │       ├── map.js         # Interactive map logic
│       │       ├── admin.js       # Admin panel logic
│       │       └── publishes.js   # Publishes page logic
│       └── templates/
│           ├── base.html          # Base template
│           ├── index.html         # Home page
│           ├── login.html         # Login/Signup page
│           ├── map.html           # Interactive map
│           ├── quiz.html          # Civics quiz
│           ├── publishes.html     # Articles/Blogs
│           ├── admin.html         # Admin console
│           └── settings.html      # User settings
├── backend/
│   ├── controller/                # Java controllers
│   ├── login/                     # Authentication services
│   └── models/                    # Data models
├── database/
│   ├── users.json                 # User accounts
│   ├── comments.json              # Bill comments
│   ├── publishes.json             # Articles/Blogs
│   └── billsList.txt              # Bill data
└── docs/
    └── SRS.md                     # Requirements doc
```

## Key Features Summary

1. **User Authentication**
   - Signup/Login with session management
   - Admin role-based access control
   - Persistent sessions (7 days)

2. **Bill Management**
   - Browse and search bills
   - Comment system with user attribution
   - Category filtering

3. **Interactive Map**
   - Leaflet.js integration
   - State capitals, major cities, congressional districts
   - Multiple map styles (street, satellite, terrain)

4. **Civics Quiz**
   - 10 questions with instant feedback
   - Detailed explanations
   - Score tracking and badges

5. **Publishes System**
   - Articles and blogs
   - Search and filter functionality
   - Admin content creation

6. **Admin Panel**
   - Create bills and publishes
   - Manage content
   - View all published items
