# API Documentation

## Base URL
```
http://localhost:5000
```

## Authentication
All endpoints (except registration and login) require an active session. Use the login endpoint to obtain a session.

---

## Endpoints

### 1. User Registration
**POST** `/register`

Register a new user account.

**Request Body:**
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123"
}
```

**Response (Success):**
```json
{
    "success": true,
    "message": "Account created successfully"
}
```

**Response (Error):**
```json
{
    "success": false,
    "message": "Email already registered"
}
```

**Status Codes:**
- 200: Account created
- 400: Invalid data

---

### 2. User Login
**POST** `/login`

Authenticate user and create session.

**Request Body:**
```json
{
    "email": "john@example.com",
    "password": "securepassword123"
}
```

**Response (Success):**
```json
{
    "success": true,
    "message": "Login successful",
    "user": "john@example.com"
}
```

**Response (Error):**
```json
{
    "success": false,
    "message": "Invalid password"
}
```

**Status Codes:**
- 200: Login successful
- 401: Invalid credentials

---

### 3. User Logout
**GET** `/logout`

Logout user and clear session.

**Response:**
```json
{
    "success": true,
    "message": "Logged out successfully"
}
```

**Status Codes:**
- 200: Logout successful

---

### 4. Create Subscription
**POST** `/checkout`

Create a new subscription for logged-in user.

**Request Body:**
```json
{
    "plan_type": "1_month",
    "fullName": "John Doe",
    "email": "john@example.com",
    "autoRenew": true
}
```

**Valid Plan Types:**
- `3_day` - 3-Day Trial ($2.99)
- `1_month` - 1-Month Premium ($29.99)

**Response (Success):**
```json
{
    "success": true,
    "message": "Subscription created successfully",
    "subscription_id": "SUB_john@example.com_1676432156.789",
    "start_date": "March 16, 2025",
    "end_date": "April 15, 2025",
    "days_remaining": 30
}
```

**Response (Error):**
```json
{
    "success": false,
    "message": "Invalid plan type"
}
```

**Status Codes:**
- 200: Subscription created
- 401: Not authenticated
- 400: Invalid plan type

---

### 5. Get Subscription Status
**GET** `/subscription-status`

Get current subscription status for logged-in user.

**Response (Active Subscription):**
```json
{
    "success": true,
    "subscription": {
        "email": "john@example.com",
        "plan_type": "1_month",
        "plan_name": "1-Month Premium",
        "start_date": "2025-03-16T10:30:00",
        "end_date": "2025-04-15T10:30:00",
        "status": "active",
        "price": 29.99,
        "transaction_id": "TXN_SUB_john@example.com_1676432156.789"
    },
    "days_remaining": 28,
    "is_active": true
}
```

**Response (No Subscription):**
```json
{
    "success": true,
    "subscription": null,
    "message": "No active subscription"
}
```

**Status Codes:**
- 200: Status retrieved
- 401: Not authenticated

---

### 6. Cancel Subscription
**POST** `/cancel-subscription`

Cancel current subscription for logged-in user.

**Response (Success):**
```json
{
    "success": true,
    "message": "Subscription cancelled successfully"
}
```

**Response (Error):**
```json
{
    "success": false,
    "message": "No active subscription to cancel"
}
```

**Status Codes:**
- 200: Subscription cancelled
- 401: Not authenticated
- 404: No subscription found

---

### 7. Get All Subscription Plans
**GET** `/api/plans`

Get list of all available subscription plans.

**Response:**
```json
[
    {
        "id": "3_day",
        "name": "3-Day Trial",
        "duration_days": 3,
        "price": 2.99,
        "features": [
            "Analyze up to 50 reviews",
            "Basic fake review detection",
            "Download detection report",
            "Email support"
        ],
        "badge": "TRIAL"
    },
    {
        "id": "1_month",
        "name": "1-Month Premium",
        "duration_days": 30,
        "price": 29.99,
        "features": [
            "Unlimited review analysis",
            "Advanced AI-powered detection",
            "Detailed fraud analytics",
            "Priority email & chat support",
            "Custom reports & insights",
            "Competitor analysis tool"
        ],
        "badge": "POPULAR"
    }
]
```

**Status Codes:**
- 200: Plans retrieved

---

### 8. Landing Page
**GET** `/`

Get landing page with subscription plans.

**Returns:** HTML landing page

---

### 9. User Dashboard
**GET** `/dashboard`

Get user dashboard. Requires active session.

**Returns:** HTML dashboard with subscription info

---

## Error Responses

### 401 Unauthorized
```json
{
    "success": false,
    "message": "Not authenticated"
}
```

### 400 Bad Request
```json
{
    "success": false,
    "message": "Invalid input"
}
```

### 404 Not Found
```json
{
    "success": false,
    "message": "Resource not found"
}
```

### 500 Server Error
```json
{
    "success": false,
    "message": "Internal server error"
}
```

---

## Rate Limiting

Currently not implemented. Recommended limits:
- Registration: 5 per IP per hour
- Login: 10 per IP per hour
- API calls: 1000 per user per hour

---

## Session Management

### Session Timeout
Default: 3600 seconds (1 hour)

### Session Storage
In-memory (use Redis in production)

### Session Cookie
- Name: `session`
- HttpOnly: true (in production)
- Secure: true (in production)
- SameSite: Lax

---

## Data Models

### User Object
```python
{
    'name': str,
    'password': str,  # Hashed in production
    'created_at': ISO 8601 timestamp,
    'subscription': str or None  # Subscription ID
}
```

### Subscription Object
```python
{
    'email': str,
    'plan_type': str,
    'plan_name': str,
    'start_date': ISO 8601 timestamp,
    'end_date': ISO 8601 timestamp,
    'status': 'active' or 'cancelled',
    'price': float,
    'transaction_id': str
}
```

---

## Code Examples

### Python Requests
```python
import requests

BASE_URL = "http://localhost:5000"

# Register
response = requests.post(
    f"{BASE_URL}/register",
    json={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123"
    }
)

# Login
session = requests.Session()
response = session.post(
    f"{BASE_URL}/login",
    json={
        "email": "john@example.com",
        "password": "password123"
    }
)

# Get subscription status
response = session.get(f"{BASE_URL}/subscription-status")
print(response.json())

# Create subscription
response = session.post(
    f"{BASE_URL}/checkout",
    json={
        "plan_type": "1_month",
        "fullName": "John Doe",
        "email": "john@example.com",
        "autoRenew": True
    }
)
print(response.json())
```

### JavaScript Fetch
```javascript
const BASE_URL = "http://localhost:5000";

// Register
async function register(name, email, password) {
    const response = await fetch(`${BASE_URL}/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({name, email, password})
    });
    return await response.json();
}

// Login
async function login(email, password) {
    const response = await fetch(`${BASE_URL}/login`, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({email, password})
    });
    return await response.json();
}

// Get subscription status
async function getSubscriptionStatus() {
    const response = await fetch(
        `${BASE_URL}/subscription-status`,
        {credentials: 'include'}
    );
    return await response.json();
}

// Create subscription
async function createSubscription(plan_type, fullName, email) {
    const response = await fetch(`${BASE_URL}/checkout`, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            plan_type,
            fullName,
            email,
            autoRenew: true
        })
    });
    return await response.json();
}
```

### cURL
```bash
# Register
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }'

# Login
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'

# Get subscription status
curl -X GET http://localhost:5000/subscription-status \
  -b cookies.txt

# Get all plans
curl -X GET http://localhost:5000/api/plans
```

---

## Webhooks (Future)

For production, implement webhooks for:
- Subscription created
- Subscription cancelled
- Subscription renewed
- Payment failed
- Payment successful

---

## Testing

### Test with Postman

1. Create Postman collection
2. Add all endpoints
3. Set up environment variables
4. Create test scripts

Example test:
```javascript
pm.test("Status code is 200", function() {
    pm.response.to.have.status(200);
});

pm.test("Response has success field", function() {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('success');
});
```

---

## Version

Current API Version: 1.0
Last Updated: February 16, 2026

---

## Support

For API issues or questions, contact: api@fakereviewnow.com
