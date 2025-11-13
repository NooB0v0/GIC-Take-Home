
# ☕ Full Stack Café Employee Management Application

This repository contains a full-stack web application to manage **cafés** and **employees** via a secure RESTful API.  
It is built with **production-ready patterns**, with a strong focus on **scalability**, **maintainability**, and **clean architecture**.

---

## 📚 Table of Contents

1. [Overview](#-overview)
2. [Technical Stack](#-technical-stack)
3. [Quick Start (Docker Deployment)](#-quick-start-docker-deployment)
4. [Database Schema & Constraints](#-database-schema--constraints)
5. [Core API Endpoints](#-core-api-endpoints)

---

## 📝 Overview

The application exposes a **Python/Flask** backend API and a **React + TypeScript** frontend:

- **Cafés**: Create, update, list, and delete cafés.
- **Employees**: Create, update, list, and delete employees.
- **Business Rules**:
  - An employee can only work at **one café**.
  - Cafés and employees are displayed with **sorted and filtered** lists.
  - Employee tenure is calculated based on start date.

Everything is packaged into **Docker containers** and orchestrated via **Docker Compose**.

---

## ⚙️ Technical Stack

### Backend API

| Component      | Technology / Pattern                                  | Notes                                                                 |
|----------------|--------------------------------------------------------|-----------------------------------------------------------------------|
| Language & API | **Python 3.11+**, **Flask**                           | RESTful API                                                           |
| Architecture   | **Clean Architecture**, **CQRS**                      | Application layer isolated from infrastructure                        |
| Validation     | **Pydantic**                                          | Request/response schema validation                                    |
| DI Container   | **injector** (Autofac-equivalent for Python)         | Dependency Injection for loose coupling                               |
| Mediator       | **Mediator Pattern**                                  | Controllers dispatch requests to handlers via mediator                |

### Data Access & Database

| Component       | Technology / Pattern     | Notes                                                       |
|-----------------|--------------------------|-------------------------------------------------------------|
| ORM             | **SQLAlchemy 2.0**       | Uses the **Repository Pattern**                            |
| Repository      | `ICafeRepository`, etc.  | Decouples business logic from database technology          |
| Database        | **PostgreSQL 16**        | RDBMS initialized via `Database/main.sql` seed script      |

### Frontend

| Component     | Technology                          | Notes                                                    |
|---------------|--------------------------------------|----------------------------------------------------------|
| Framework     | **React JS + TypeScript**           | Bootstrapped with **Vite**                              |
| UI Library    | **Ant Design (Antd)**               | Custom theming and styling                              |
| Data Grid     | **Ag-Grid**                         | Tabular café/employee listing                           |
| State/Data    | **TanStack Query**                  | Server state management + API calls                     |
| Utilities     | **Day.js**                          | Date & time utilities (e.g. tenure calculation)         |

---

## 🚀 Quick Start (Docker Deployment)

The entire stack is containerized and runs via **Docker Compose**, bringing up:

- `db` – PostgreSQL 16
- `api` – Python / Flask backend
- `web` – React / Vite frontend

### Prerequisites

- **Docker** and **Docker Compose v2+** installed.

### 1. Clone the Repository

```bash
git clone https://github.com/NooB0v0/GIC-Take-Home
cd GIC-Take-Home
```

### 2. Build and Deploy the Stack

The `--build` flag ensures images are built for your host architecture (e.g. ARM64 on Raspberry Pi):

```bash
docker compose up --build -d
```

### 3. Access the Application

- **Frontend UI (Browser)**  
  `http://[YOUR_IP_OR_localhost]:3000`

- **Backend API (Postman / HTTP client)**  
  `http://[YOUR_IP_OR_localhost]:5000`

> 💡 **Submission Note**  
> The final submission link is:  
> `http://gic-roger.duckdns.org:3000`
---

## 🗄️ Database Schema & Constraints

- Database is initialized from:

  ```text
  Database/main.sql
  ```

- Core tables include:
  - `cafes`
  - `employees`
  - `employee_cafe` (join / assignment table)

- **Business rule enforcement**:

  ```sql
  -- Pseudocode representation
  UNIQUE (employee_cafe.employee_id)
  ```

  This **UNIQUE constraint** ensures that **no employee can be assigned to more than one café** at any time.

---

## 🔗 Core API Endpoints (CRUD)

Below is a high-level overview of the main REST endpoints and their behaviors.

### 1. Cafés

**List Cafés**

```http
GET /cafes
```

- Returns a list of all cafés.
- **Sorted by**: highest number of employees.
- **Filters**:
  - `?location=<location>` – filter cafés by location.

**Create / Update / Delete Cafés**

```http
POST   /cafes
PUT    /cafes/{id}
DELETE /cafes/{id}
```

- Full **CRUD** support for cafés.
- `DELETE` cascades to remove associated **employee assignments** in the join table.

---

### 2. Employees

**List Employees**

```http
GET /employees
```

- Returns a list of all employees.
- **Sorted by**: highest number of days worked (tenure).
- **Filters**:
  - `?cafe=<cafe_id_or_name>` – filter employees by café.

**Create / Update / Delete Employees**

```http
POST   /employees
PUT    /employees/{id}
DELETE /employees/{id}
```

- Full **CRUD** support for employees.
- **Business Rules (POST)**:
  - Custom employee ID generation in the format:  
    `UIXXXXXXX` (e.g. `UI0000123`).
  - **Singapore phone number validation**.

---

