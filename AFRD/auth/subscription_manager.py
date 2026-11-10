"""
Subscription Manager Module
Handles subscription lifecycle, user accounts, and plan management.
"""
from datetime import datetime, timedelta
import os

# ==================== CONFIGURATION ====================
# Subscription Plans Configuration (PHP - Philippine Pesos)
SUBSCRIPTION_PLANS = {
    '3_day': {
        'name': '3-Day Trial',
        'duration_days': 3,
        'price': 0,
        'features': [
            'Analyze up to 50 reviews',
            'Basic fake review detection',
            'Download detection report',
            'Email support'
        ],
        'badge': 'TRIAL',
        'recommended': False
    },
    '1_month': {
        'name': '1-Month Premium',
        'duration_days': 30,
        'price': 99,
        'features': [
            'Unlimited review analysis',
            'Advanced AI-powered detection',
            'Detailed fraud analytics',
            'Priority email & chat support',
            'Custom reports & insights',
            'Competitor analysis tool'
        ],
        'badge': 'POPULAR',
        'recommended': True
    }
}

# In-memory storage (use database in production)
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
        
        subscription_id = users_db[email].get('subscription')
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
        
        subscription_id = users_db[email].get('subscription')
        if subscription_id and subscription_id in subscriptions_db:
            subscriptions_db[subscription_id]['status'] = 'cancelled'
            users_db[email]['subscription'] = None
            return {'success': True, 'message': 'Subscription cancelled successfully'}
        
        return {'success': False, 'message': 'No active subscription to cancel'}
    
    @staticmethod
    def is_subscribed(email):
        """Check if user has active subscription"""
        status = SubscriptionManager.get_subscription_status(email)
        return status.get('is_active', False)
    
    @staticmethod
    def get_user_info(email):
        """Get user information"""
        if email not in users_db:
            return None
        user = users_db[email].copy()
        user.pop('password', None)  
        return user
