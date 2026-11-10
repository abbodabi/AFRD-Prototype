# Fake Review Detection - Subscription System

A complete web-based subscription interface for an online fake review detection service offering flexible subscription plans.

## Features

### Subscription Plans
- **3-Day Trial Plan**: $2.99 - Perfect for testing the service
  - Analyze up to 50 reviews
  - Basic fake review detection
  - Download detection report
  - Email support

- **1-Month Premium Plan**: $29.99 - Full access
  - Unlimited review analysis
  - Advanced AI-powered detection
  - Detailed fraud analytics
  - Priority email & chat support
  - Custom reports & insights
  - Competitor analysis tool

### User Features
- User registration and authentication
- Secure subscription management
- Dashboard with subscription status
- Real-time subscription tracking
- Subscription upgrade/cancellation
- User account management
- Responsive design for all devices

## Project Structure

```
AFRD-SUBSCRIPTION/
├── subscription.py           # Flask application & backend logic
├── requirements.txt         # Python dependencies
├── templates/              # HTML templates
│   ├── index.html         # Landing page with pricing
│   ├── register.html      # User registration
│   ├── login.html         # User login
│   ├── checkout.html      # Subscription checkout
│   └── dashboard.html     # User dashboard
└── static/
    └── style.css          # Styling
```

## Installation

### 1. Clone/Download the Project
```bash
cd AFRD-SUBSCRIPTION
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**On Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

### Start the Flask Server
```bash
python subscription.py
```

The application will run at `http://localhost:5000`

## Usage

### User Flow

1. **Landing Page** (/)
   - View subscription plans and features
   - See pricing comparison
   - Access FAQs

2. **Sign Up** (/register)
   - Create a new account
   - Enter name, email, password
   - Automatic redirect to login

3. **Login** (/login)
   - Enter email and password
   - Secure session management

4. **Checkout** (/checkout)
   - Select subscription plan
   - Enter billing information
   - Process payment
   - Confirm subscription

5. **Dashboard** (/dashboard)
   - View current subscription status
   - Track days remaining
   - See usage statistics
   - Access quick actions
   - Upgrade or cancel subscription

## API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /login` - Login user
- `GET /logout` - Logout user

### Subscription Management
- `POST /checkout` - Create subscription
- `GET /subscription-status` - Get current subscription
- `POST /cancel-subscription` - Cancel subscription

### Data
- `GET /api/plans` - Get all subscription plans
- `GET /` - Landing page
- `GET /dashboard` - User dashboard

## Database (In-Memory)

This demo uses in-memory storage. For production, integrate with:
- PostgreSQL
- MongoDB
- MySQL
- Firebase

## Security Notes

⚠️ **Important**: This is a demonstration system. For production use:

1. **Hash Passwords**: Use `werkzeug.security.generate_password_hash()`
2. **Use HTTPS**: Enable SSL/TLS
3. **Add CSRF Protection**: Use Flask-WTF
4. **Database**: Replace in-memory storage with proper database
5. **Payment Processing**: Integrate with Stripe, PayPal, or similar
6. **Input Validation**: Add comprehensive input validation
7. **Rate Limiting**: Implement rate limiting
8. **Logging**: Add security logging
9. **Session Management**: Configure secure session cookies
10. **Environment Variables**: Store secrets in .env file

## Features to Enhance

- Email verification on signup
- Password reset functionality
- Payment gateway integration
- Invoice generation
- Usage analytics dashboard
- Subscription renewal reminders
- Multi-language support
- Dark mode
- Two-factor authentication
- API keys for developers
- Team management
- Billing history
- Support ticket system

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Template Engine**: Jinja2
- **Session Management**: Flask Sessions

## Support

For issues or questions, contact support@fakereviewnow.com

## License

© 2026 Fake Review Detector. All rights reserved.

## Future Enhancements

- Integration with multiple payment processors
- Advanced analytics and reporting
- API for third-party integrations
- Mobile app
- Browser extension
- Real-time notifications
- Machine learning model updates
- Enterprise features
- White-label solution
