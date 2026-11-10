# Quick Start Guide - Fake Review Detection Subscription

## Fast Setup (2 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python subscription.py
```

### Step 3: Open in Browser
Go to: **http://localhost:5000**

---

## Testing the System

### Test User Account
- **Email**: test@example.com
- **Password**: password123

### Test Flow
1. Click "Sign Up" → Create account
2. Click "Login" → Login with your credentials
3. Choose a subscription plan (3-Day or 1-Month)
4. Complete checkout with test payment info
5. View your subscription on the dashboard

### Test Payment Info
- **Card Number**: 4111 1111 1111 1111
- **Expiry**: 12/25
- **CVV**: 123
- **Zip Code**: 12345

---

## Key Features Demo

### 1. Landing Page
- View both subscription plans side-by-side
- Compare features and pricing
- See why our service is unique
- Read FAQs

### 2. Subscription Plans

**3-Day Trial ($2.99)**
- Great for testing
- 50 reviews analysis limit
- Basic detection features

**1-Month Premium ($29.99)**
- Full access
- Unlimited analysis
- Advanced AI features
- Priority support

### 3. User Dashboard
- View active subscription
- Track days remaining
- Monitor usage stats
- Cancel anytime
- Upgrade plan

### 4. Account Management
- Secure login/logout
- Password protected accounts
- Session management
- Personalized dashboard

---

## Project Files

| File | Purpose |
|------|---------|
| `subscription.py` | Flask app & backend logic |
| `requirements.txt` | Python dependencies |
| `templates/index.html` | Landing page |
| `templates/register.html` | Sign up page |
| `templates/login.html` | Login page |
| `templates/checkout.html` | Payment/checkout |
| `templates/dashboard.html` | User dashboard |
| `static/style.css` | Styling |

---

## Customization

### Change Subscription Plans
Edit `subscription.py` → `SUBSCRIPTION_PLANS` dictionary

### Change Pricing
Modify the `'price'` field in subscription plans

### Change Feature List
Update the `'features'` array for each plan

### Change Styling
Edit `static/style.css`

### Change Branding
Update:
- Logo in navbar
- Company name
- Colors and fonts
- Email addresses

---

## Troubleshooting

### Port Already in Use
If port 5000 is busy, modify in `subscription.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change 5000 to 5001
```

### Python Not Found
Make sure Python 3.7+ is installed:
```bash
python --version
```

### Import Errors
Reinstall dependencies:
```bash
pip uninstall -r requirements.txt
pip install -r requirements.txt
```

### Virtual Environment Issues
Delete `venv` folder and recreate:
```bash
python -m venv venv
```

---

## Next Steps

1. ✅ Install and run the application
2. ✅ Test the user flow
3. ✅ Customize pricing and features
4. ✅ Integrate with your fake review detection engine
5. ✅ Add payment processor (Stripe, PayPal)
6. ✅ Deploy to production

---

## Support

Need help? Check the README.md for detailed documentation.

Happy reviewing! 🔍
