
# ☕ Full Stack Café Employee Management Application


## 🚀 Quick Start: Instructions to Compile and Run

This application is fully containerized using Docker Compose. The following steps will build the necessary images, initialize the PostgreSQL database, and launch both the Python API (Backend) and React Web UI (Frontend).

The entire stack is containerized and runs via **Docker Compose**, bringing up:

- `db` – PostgreSQL 16
- `api` – Python / Flask backend
- `web` – React / Vite frontend

### Prerequisites

- **Docker**
- **Docker Compose v2+**


## Local Step and Compilation
### 1. Clone the Repository

```bash
git clone https://github.com/NooB0v0/GIC-Take-Home
cd GIC-Take-Home
```

### 2. Verify Seed Data: Ensure the database initialization script and seed data are available.

- Schema & Data: Verify that the `Database/main.sql` file contains both the `CREATE TABLE` statements and the `INSERT` seed data.

- Logos: Ensure any seed images referenced (e.g., `/logos/coffee.png`) are present in the corresponding host volume directory (`./cafe_employee_backend/public/logos`).

### 3. Handle External DNS (If Hosting): 
If running on a public IP with a DDNS service (like DuckDNS), ensure your `vite.config.ts` has the correct `allowedHosts` set to prevent the `Blocked request` error.

## 2. Running the Application Stack
The application relies on the `docker-compose.yml` file located in the project root to orchestrate three services: db, api, and web.

**Build and Run**: Execute the following command from the project root folder. The `--build` flag ensures both the Python and React code are compiled into new Docker images.

```bash
docker compose up --build -d
```

## 3. Access the Application

- **Frontend UI (Browser)**  
  `http://[YOUR_IP_OR_localhost]:3000`

- **Backend API (Postman / HTTP client)**  
  `http://[YOUR_IP_OR_localhost]:5000`

> 💡 **Submission Note**  
> The final submission link is:  
> `http://gic-roger.duckdns.org:3000`
---

## 4. Stop and Clean Up
To stop the application and clean up containers and networks:
```bash
docker compose down
```

To fully reset the database and force a new schema initialization on the next run:
```bash
docker volume rm [YOUR_PROJECT_NAME]_postgres_data
```
(Replace [YOUR_PROJECT_NAME] with your repository's root folder name as used by Docker.)




## 5. ⚠️ Troubleshooting (Client-Side Access)

If the application fails to load when accessed from the public URL, showing a  `net::ERR_BLOCKED_BY_CLIENT `error, this is a client-side security conflict and not a bug in the code or server configuration.

Issue: The browser's Ad-Blocker or Privacy Extensions (e.g., uBlock Origin, Privacy Badger) are blocking the necessary cross-port request from the frontend (`:3000`) to the backend API (`:5000`).

Resolution: Please temporarily disable all privacy/ad-blocking extensions for the application URL, or use a clean Incognito/Private browser window.