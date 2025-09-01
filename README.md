# 📡 IPAM API

An **IP Address Management (IPAM) API** built with **FastAPI** and **PostgreSQL**.  
It allows you to manage Virtual Networks (**VNets**) and **Subnets** with full CRUD support, CIDR validation, overlap checks, and detailed network information (address, netmask, broadcast, etc.).

---

## 🚀 Technologies
- [FastAPI](https://fastapi.tiangolo.com/)  
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/)  
- [PostgreSQL](https://www.postgresql.org/)  
- [Docker & Docker Compose](https://docs.docker.com/)  
- [Alembic](https://alembic.sqlalchemy.org/) (migrations support)  

---

## 📦 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/djulianOps/ipam-api.git
cd ipam-api
```

### 2. Start services with Docker Compose
```bash
docker-compose up --build
```

This will:

Start PostgreSQL on port 5432

Start the API on port 8000

### 3. Check API health
```bash
curl http://localhost:8000/ping
```
Expected response:
```json
{"ping": "pong"}
```

---

### 📖 API Documentation

Interactive docs available at:

- Swagger UI → http://localhost:8000/docs

- ReDoc → http://localhost:8000/redoc

### 🔑 API Endpoints & Examples
#### VNets
| Method | Endpoint             | Description                  |
|--------|----------------------|------------------------------|
| GET    | `/vnets`             | List all VNets               |
| GET    | `/vnets/{id}`        | Get a VNet by ID             |
| GET    | `/vnets/search?cidr=`| Get a VNet by CIDR           |
| POST   | `/vnets`             | Create a new VNet            |
| PUT    | `/vnets/{id}`        | Update a VNet by ID          |
| DELETE | `/vnets/{id}`        | Delete a VNet by ID          |

#### Subnets
| Method | Endpoint               | Description                   |
|--------|------------------------|-------------------------------|
| GET    | `/subnets`             | List all Subnets              |
| GET    | `/subnets/{id}`        | Get a Subnet by ID            |
| GET    | `/subnets/search?cidr=`| Get a Subnet by CIDR          |
| POST   | `/subnets`             | Create a new Subnet           |
| PUT    | `/subnets/{id}`        | Update a Subnet by ID         |
| DELETE | `/subnets/{id}`        | Delete a Subnet by ID         |

---
#### VNets
#### ➕ Create VNet

cURL
```bash
curl -X POST http://localhost:8000/vnets/ \
  -H "Content-Type: application/json" \
  -d '{"name":"VNET-Prod","cidr":"10.0.0.0/16"}'
```

HTTPie
```bash
http POST :8000/vnets/ name=VNET-Prod cidr=10.0.0.0/16
```

Response:
```json
{
  "id": 1,
  "name": "VNET-Prod",
  "cidr": "10.0.0.0/16",
  "address": "10.0.0.0",
  "netmask": "255.255.0.0",
  "wildcard": "0.0.255.255",
  "network": "10.0.0.0",
  "broadcast": "10.0.255.255",
  "class_type": "A",
  "subnets": []
}
```

#### 📋 List VNets

cURL
```bash
curl http://localhost:8000/vnets/
```

HTTPie
```bash
http :8000/vnets/
```

#### 🔍 Get VNet by ID

cURL
```bash
curl http://localhost:8000/vnets/1
```

HTTPie
```bash
http :8000/vnets/1
```

#### ✏️ Update VNet

cURL
```bash
curl -X PATCH http://localhost:8000/vnets/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"VNET-Prod-Updated","cidr":"10.1.0.0/16"}'
```

HTTPie
```bash
http PATCH :8000/vnets/1 name=VNET-Prod-Updated cidr=10.1.0.0/16
```

#### ❌ Delete VNet

cURL
```bash
curl -X DELETE http://localhost:8000/vnets/1
```

HTTPie
```bash
http DELETE :8000/vnets/1
```

#### Subnets
#### ➕ Create Subnet (inside a VNet)

cURL
```bash
curl -X POST http://localhost:8000/vnets/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Subnet-Web","cidr":"10.0.1.0/24"}'
```

HTTPie
```bash
http POST :8000/vnets/1 name=Subnet-Web cidr=10.0.1.0/24
```

Response:
```json
{
  "id": 10,
  "name": "Subnet-Web",
  "cidr": "10.0.1.0/24",
  "vnet_id": 1,
  "address": "10.0.1.0",
  "netmask": "255.255.255.0",
  "wildcard": "0.0.0.255",
  "network": "10.0.1.0",
  "broadcast": "10.0.1.255",
  "class_type": "A"
}
```

#### 📋 List Subnets

cURL
```bash
curl http://localhost:8000/subnets/
```

HTTPie
```bash
http :8000/subnets/
```

#### 🔍 Get Subnet by ID

cURL
```bash
curl http://localhost:8000/subnets/10
```

HTTPie
```bash
http :8000/subnets/10
```

#### ✏️ Update Subnet

cURL
```bash
curl -X PATCH http://localhost:8000/subnets/10 \
  -H "Content-Type: application/json" \
  -d '{"name":"Subnet-DB","cidr":"10.0.2.0/24"}'
```

HTTPie
```bash
http PATCH :8000/subnets/10 name=Subnet-DB cidr=10.0.2.0/24
```

#### ❌ Delete Subnet

cURL
```bash
curl -X DELETE http://localhost:8000/subnets/10
```

HTTPie
```bash
http DELETE :8000/subnets/10
```

---

### 📝 Logs

Logs are configured in **logging.conf** and output to stdout.
They can be easily integrated into observability tools such as Datadog, Grafana Loki, or ELK Stack.

## 📌 Roadmap

- [x] VNet CRUD
- [x] Subnet CRUD
- [x] CIDR validation & overlap prevention
- [x] Structured logging
- [ ] Database migrations with Alembic
- [ ] Authentication & RBAC (future)