from flask import Flask, render_template, request, jsonify, session
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
app.secret_key = 'fake_review_detection_secret_key'

# Subscription Plans Configuration
SUBSCRIPTION_PLANS = {
    '3_day': {
        'name': '3-Day Trial',
        'duration_days': 3,
        'price': 0.00,
        'features': [
            'Analyze up to 50 reviews',
            'Basic fake review detection',
            'Download detection report',
            'Email support'
        ],
        'badge': 'TRIAL'
    },
    '1_month': {
        'name': '1-Month Premium',
        'duration_days': 30,
        'price': 99.00,
        'features': [
            'Unlimited review analysis',
            'Advanced AI-powered detection',
            'Detailed fraud analytics',
            'Priority email & chat support',
            'Custom reports & insights',
            'Competitor analysis tool'
        ],
        'badge': 'POPULAR'
    }
}

# In-memory storage for subscriptions (use database in production)
subscriptions_db = {}
users_db = {}


class SubscriptionManager:
    """Manages subscription lifecycle and user accounts"""
    
    @staticmethod
    def create_user(email, password, name):
        """Create a new user account"""
        if email in users_db:
            return {'success': False, 'message': 'Email already registered'}
        
        users_db[email] = {
            'name': name,
            'password': password,  # In production: hash this!
            'created_at': datetime.now().isoformat(),
            'subscription': None
        }
        return {'success': True, 'message': 'Account created successfully'}
    
    @staticmethod
    def authenticate_user(email, password):
        """Authenticate user login"""
        if email not in users_db:
            return {'success': False, 'message': 'User not found'}
        
        if users_db[email]['password'] != password:
            return {'success': False, 'message': 'Invalid password'}
        
        return {'success': True, 'message': 'Login successful', 'user': email}
    
    @staticmethod
    def create_subscription(email, plan_type):
        """Create a new subscription for a user"""
        if plan_type not in SUBSCRIPTION_PLANS:
            return {'success': False, 'message': 'Invalid plan type'}
        
        if email not in users_db:
            return {'success': False, 'message': 'User not found'}
        
        plan = SUBSCRIPTION_PLANS[plan_type]
        start_date = datetime.now()
        end_date = start_date + timedelta(days=plan['duration_days'])
        
        subscription_id = f"SUB_{email}_{datetime.now().timestamp()}"
        subscriptions_db[subscription_id] = {
            'email': email,
            'plan_type': plan_type,
            'plan_name': plan['name'],
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'status': 'active',
            'price': plan['price'],
            'transaction_id': f"TXN_{subscription_id}"
        }
        
        users_db[email]['subscription'] = subscription_id
        
        return {
            'success': True,
            'message': 'Subscription created successfully',
            'subscription_id': subscription_id,
            'start_date': start_date.strftime('%B %d, %Y'),
            'end_date': end_date.strftime('%B %d, %Y'),
            'days_remaining': plan['duration_days']
        }
    
    @staticmethod
    def get_subscription_status(email):
        """Get current subscription status for a user"""
        if email not in users_db:
            return {'success': False, 'message': 'User not found'}
        
        subscription_id = users_db[email]['subscription']
        if not subscription_id or subscription_id not in subscriptions_db:
            return {'success': True, 'subscription': None, 'message': 'No active subscription'}
        
        sub = subscriptions_db[subscription_id]
        end_date = datetime.fromisoformat(sub['end_date'])
        days_remaining = (end_date - datetime.now()).days
        
        return {
            'success': True,
            'subscription': sub,
            'days_remaining': max(0, days_remaining),
            'is_active': days_remaining > 0
        }
    
    @staticmethod
    def cancel_subscription(email):
        """Cancel user's subscription"""
        if email not in users_db:
            return {'success': False, 'message': 'User not found'}
        
        subscription_id = users_db[email]['subscription']
        if subscription_id and subscription_id in subscriptions_db:
            subscriptions_db[subscription_id]['status'] = 'cancelled'
            users_db[email]['subscription'] = None
            return {'success': True, 'message': 'Subscription cancelled successfully'}
        
        return {'success': False, 'message': 'No active subscription to cancel'}


# Flask Routes

@app.route('/')
def index():
    """Landing page with subscription plans"""
    return render_template('index.html', plans=SUBSCRIPTION_PLANS)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if request.method == 'POST':
        data = request.get_json()
        result = SubscriptionManager.create_user(
            data['email'],
            data['password'],
            data['name']
        )
        return jsonify(result)
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if request.method == 'POST':
        data = request.get_json()
        result = SubscriptionManager.authenticate_user(
            data['email'],
            data['password']
        )
        if result['success']:
            session['user_email'] = data['email']
        return jsonify(result)
    return render_template('login.html')


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Checkout and subscription selection"""
    if request.method == 'POST':
        if 'user_email' not in session:
            return jsonify({'success': False, 'message': 'Please login first'}), 401
        
        data = request.get_json()
        plan_type = data.get('plan_type')
        payment_method = data.get('payment_method', 'card')
        # for now we simply acknowledge the method; real integration would differ
        result = SubscriptionManager.create_subscription(
            session['user_email'],
            plan_type
        )
        if result['success']:
            result['payment_method'] = payment_method
            if payment_method == 'qr':
                result['message'] = 'QR payment selected. Please check your email for payment instructions.'
        return jsonify(result)
    
    if 'user_email' in session:
        return render_template('checkout.html', plans=SUBSCRIPTION_PLANS, user=session['user_email'])
    return render_template('checkout.html', plans=SUBSCRIPTION_PLANS)


@app.route('/dashboard')
def dashboard():
    """User dashboard with subscription info"""
    if 'user_email' not in session:
        return render_template('dashboard.html', user=None)
    
    status = SubscriptionManager.get_subscription_status(session['user_email'])
    return render_template('dashboard.html', user=session['user_email'], subscription_status=status)


@app.route('/subscription-status', methods=['GET'])
def subscription_status():
    """API endpoint to check subscription status"""
    if 'user_email' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    status = SubscriptionManager.get_subscription_status(session['user_email'])
    return jsonify(status)


@app.route('/cancel-subscription', methods=['POST'])
def cancel_subscription():
    """Cancel current subscription"""
    if 'user_email' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    result = SubscriptionManager.cancel_subscription(session['user_email'])
    return jsonify(result)


@app.route('/logout')
def logout():
    """Logout user"""
    session.pop('user_email', None)
    return jsonify({'success': True, 'message': 'Logged out successfully'})


@app.route('/api/plans')
def get_plans():
    """API endpoint to get all subscription plans"""
    plans_with_details = []
    for plan_id, plan_info in SUBSCRIPTION_PLANS.items():
        plans_with_details.append({
            'id': plan_id,
            **plan_info
        })
    return jsonify(plans_with_details)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
