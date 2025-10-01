# API Documentation

## Overview

In this project, we created a RESTful API server for managing mobile money transactions. Our implementation uses Python’s built-in `http.server` library to handle HTTP requests and responses, and stores transaction data in a JSON file. We designed the API to support basic authentication and CRUD operations.

---

## How We Created the Server

- We used Python’s `BaseHTTPRequestHandler` and `HTTPServer` classes to build the server.
- Before starting the server, we prompt the user for a username and password using the terminal. The password input is hidden for security using the `getpass` module.
- If the credentials are incorrect, the server prints `401 Unauthorized due to Invalid credentials` and exits.
- Once authenticated, the server listens on `localhost:8080` for incoming API requests.

---

## API Authentication

- Every API request must include HTTP Basic Authentication headers.
- The server checks for the correct username (`team2`) and password (`alu@123`) in the request headers.
- If authentication fails, the server responds with a `401 Unauthorized` status.

---

## Why We Used `curl`

We used the `curl` command-line tool to interact with our API endpoints during development and testing.  
`curl` is widely used for making HTTP requests from the terminal. It allows us to easily specify request methods (GET, POST, PUT, DELETE), add headers, send authentication credentials, and include request bodies.  
Using `curl` helped us quickly verify that our API endpoints were working as expected and made it simple to test different scenarios and error cases.

---

## API Endpoints and Examples

### 1. Get All Transactions

**Endpoint:**  
`GET /transactions`

**Request Example:**
```bash
curl -u team2:alu@123 http://localhost:8080/transactions
```
**Response Example:**
```json
[
    {
        "transaction_id": "76662021700",
        "type": "transfer",
        "amount": "2000",
        "sender": "Jane Smith (*********013)",
        "receiver": "You",
        "timestamp": "2024-05-10T16:30:51",
        "new_balance": "2000",
        "message": null,
        "financial_transaction_id": "76662021700",
        "service_center": "+250788110381",
        "fee": "0"
    }
]
```

---

### 2. Get a Single Transaction

**Endpoint:**  
`GET /transactions/{id}`

**Description:**  
We implemented this endpoint to retrieve a specific transaction by its ID.

**Request Example:**
```bash
curl -u team2:alu@123 http://localhost:8080/transactions/76662021700
```
**Response Example:**
```json
{
    "transaction_id": "76662021700",
    "type": "transfer",
    "amount": "2000",
    "sender": "Jane Smith (*********013)",
    "receiver": "You",
    "timestamp": "2024-05-10T16:30:51",
    "new_balance": "2000",
    "message": null,
    "financial_transaction_id": "76662021700",
    "service_center": "+250788110381",
    "fee": "0"
}
```

---

### 3. Add a New Transaction

**Endpoint:**  
`POST /transactions`

**Description:**  
We designed this endpoint to add a new transaction.

**Request Example:**
```bash
curl -X POST -u team2:alu@123 -H "Content-Type: application/json" -d '{
    "transaction_id": "1234567890",
    "type": "transfer",
    "amount": "5000",
    "sender": "You",
    "receiver": "John Doe",
    "timestamp": "2024-05-13T10:00:00",
    "new_balance": "15880",
    "message": null,
    "financial_transaction_id": "1234567890",
    "service_center": "+250788110381",
    "fee": "0"
}' http://localhost:8080/transactions
```

---

### 4. Update a Transaction

**Endpoint:**  
`PUT /transactions/{id}`

**Description:**  
We created this endpoint to update an existing transaction by its ID.

**Request Example:**
```bash
curl -X PUT -u team2:alu@123 -H "Content-Type: application/json" -d '{
    "transaction_id": "76662021700",
    "type": "transfer",
    "amount": "2500",
    "sender": "Jane Smith (*********013)",
    "receiver": "You",
    "timestamp": "2024-05-10T16:30:51",
    "new_balance": "2500",
    "message": null,
    "financial_transaction_id": "76662021700",
    "service_center": "+250788110381",
    "fee": "0"
}' http://localhost:8080/transactions/76662021700
```

---

### 5. Delete a Transaction

**Endpoint:**  
`DELETE /transactions/{id}`

**Description:**  
We implemented this endpoint to delete a transaction by its ID.

**Request Example:**
```bash
curl -X DELETE -u team2:alu@123 http://localhost:8080/transactions/76662021700
```

---

## Error Codes

| Error Code | Description                                 |
|------------|---------------------------------------------|
| 400        | Bad Request (e.g., invalid JSON)            |
| 401        | Unauthorized (invalid credentials)          |
| 404        | Not Found (endpoint/ID does not exist)      |

---

## Data Storage

- All transactions are stored in `data/transactions.json`.
- The server reads from and writes to this file for every CRUD operation.

---
