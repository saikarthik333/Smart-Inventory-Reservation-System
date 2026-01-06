# 🚀 Smart Inventory Reservation System

**Concurrency-safe | Fair | Waitlist-enabled | Analytics-ready**

A backend-first smart inventory reservation system designed for **high-traffic flash-sale scenarios**, ensuring **no overselling**, **fair access**, and **automatic recovery from abandoned carts**.

live link: https://smart-inventory-reservation-system.onrender.com/static/index.html
---

## 📌 Problem Statement

In high-demand e-commerce scenarios (flash sales, limited drops), multiple users attempt to purchase the same product simultaneously.  
This often leads to:

- Overselling
- Inventory locked by abandoned carts
- Unfair checkout experiences
- Inconsistent state under concurrency

This project solves these problems with a **deterministic, concurrency-safe backend architecture**.

---

## ✅ Key Features

### 🔒 Concurrency Safety
- SKU-level locking ensures **inventory never goes negative**
- Safe under multiple simultaneous requests

### ⏳ TTL-Based Reservations
- Inventory is reserved when checkout begins
- Reservations automatically expire (default: 5 minutes)
- Prevents cart hoarding

### ⚖️ Fairness Engine
- Tracks user behavior
- Adjusts reservation TTL dynamically
- Discourages abusive reservation patterns

### 📋 FIFO Waitlist
- When inventory runs out, users are waitlisted
- Waitlisted users are **automatically upgraded** when stock becomes available

### 📊 Inventory Health Analytics
- Real-time visibility into:
  - Available stock
  - Waitlist size
  - Demand status (`HEALTHY`, `HIGH_DEMAND`, `OUT_OF_STOCK`)

### 🤖 Optional AI Insights
- AI-generated business-friendly explanations of inventory demand
- Fully optional and **never part of the transaction path**

### 🧩 Clean Layered Architecture
- Controllers → Services → Storage
- Easy to extend (Redis, DB, external services)

---

## 🏗️ Architecture Overview

```text
Smart Inventory Reservation System/
│
├── app/
│   ├── main.py
│   │
│   ├── controllers/
│   │   ├── inventory.py
│   │   ├── checkout.py
│   │   └── analytics.py
│   │
│   ├── services/
│   │   ├── inventory_service.py
│   │   ├── reservation_service.py
│   │   ├── fairness_service.py
│   │   ├── waitlist_service.py
│   │   ├── health_service.py
│   │   └── ai_insight_service.py
│   │
│   ├── storage/
│   │   └── in_memory_store.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   └── utils/
│       └── locks.py
│
├── static/
│   └── index.html
│
├── requirements.txt
├── start.sh
├── README.md
└── .gitignore
```

---

## 🔁 Core API Workflow

### 1️⃣ Initialize Inventory
POST /inventory/init
```
{
  "sku": "SKU123",
  "quantity": 5
}
```

### 2️⃣ Reserve Inventory
POST /inventory/reserve
```
{
  "sku": "SKU123",
  "user_id": "userA",
  "quantity": 1
}
```

### 3️⃣ Confirm Checkout
POST /checkout/confirm
```
{
  "reservation_id": "uuid"
}
```

### 4️⃣ Cancel Checkout
POST /checkout/cancel
```
{
  "reservation_id": "uuid"
}
```

### 5️⃣ Inventory Health Analytics
GET /analytics/inventory/{sku}
```
{
  "sku": "SKU123",
  "available_inventory": 0,
  "waitlist_size": 3,
  "status": "HIGH_DEMAND"
}
```
---

## 🧪 Demo Flow (Recommended)

1. Initialize inventory (`quantity = 1`)
2. User A reserves → **RESERVED**
3. User B reserves → **WAITLISTED**
4. User A cancels
5. User B auto-upgraded → **RESERVED**
6. Confirm checkout
7. Check inventory health → **OUT_OF_STOCK**

---

## 🖥️ Frontend (Demo UI)

A minimal HTML frontend is included for demonstration purposes.

Access at:
/static/index.html

> The UI is intentionally simple — the innovation lies in the backend logic.

---

## 🤖 AI Insights (Optional)

- AI is used **only for analytics**
- Never affects inventory, reservations, or checkout
- System runs safely even if AI is disabled

Example:
GET /analytics/ai/inventory/{sku}

---

## 🚀 Deployment

### Platform
- Render (Free Tier)

### Start Command
bash start.sh

---

## 🛡️ Design Principles

- Deterministic state transitions
- Idempotent APIs
- Concurrency safety
- Clear separation of concerns
- Production-ready patterns

---

## 🔮 Future Enhancements

- Redis-backed storage
- Persistent database (PostgreSQL)
- Rate limiting
- Live inventory updates
- Admin dashboard

---

## 👤 Author

**Motapothula Sai Karthik**  
B.Tech CSE (2026)  


