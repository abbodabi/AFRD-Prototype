"""
Usage Tracker Module
Handles free tier usage tracking (5 uses per 24 hours).
"""
from datetime import datetime, timedelta
from collections import defaultdict

# In-memory storage for usage tracking
# Structure: {email: {'count': int, 'reset_date': datetime}}
usage_db = defaultdict(lambda: {'count': 0, 'reset_date': None})

# Free tier configuration
FREE_USAGE_LIMIT = 5
FREE_USAGE_RESET_HOURS = 24


class UsageTracker:
    """Manages free tier usage tracking"""
    
    @staticmethod
    def check_usage_allowed(email):
        """
        Check if user is allowed to use the service.
        
        Returns:
            dict: {
                'allowed': bool,
                'remaining': int,
                'reset_in_hours': float,
                'message': str
            }
        """
        # If no email (not logged in), apply anonymous limit
        if not email:
            return UsageTracker._check_anonymous_usage()
        
        # Check if user has active subscription
        from .subscription_manager import SubscriptionManager
        if SubscriptionManager.is_subscribed(email):
            return {
                'allowed': True,
                'remaining': -1,  # Unlimited
                'reset_in_hours': 0,
                'message': 'Unlimited access (subscribed)',
                'is_subscribed': True
            }
        
        # Check free usage limit
        return UsageTracker._check_free_usage(email)
    
    @staticmethod
    def _check_anonymous_usage():
        """Check anonymous user usage (no login)"""
        # Use a session-based key for anonymous users
        return {
            'allowed': False,
            'remaining': 0,
            'reset_in_hours': 0,
            'message': 'Please login to use the service',
            'requires_login': True,
            'is_subscribed': False
        }
    
    @staticmethod
    def _check_free_usage(email):
        """Check free tier usage for logged-in non-subscribed user"""
        user_usage = usage_db[email]
        current_time = datetime.now()
        
        # Check if we need to reset (24-hour window)
        if user_usage['reset_date'] is None:
            # First time user, set reset date
            user_usage['reset_date'] = current_time + timedelta(hours=FREE_USAGE_RESET_HOURS)
            user_usage['count'] = 0
        
        # Check if reset time has passed
        if current_time >= user_usage['reset_date']:
            # Reset the counter
            user_usage['count'] = 0
            user_usage['reset_date'] = current_time + timedelta(hours=FREE_USAGE_RESET_HOURS)
        
        remaining = FREE_USAGE_LIMIT - user_usage['count']
        
        if remaining > 0:
            return {
                'allowed': True,
                'remaining': remaining,
                'reset_in_hours': (user_usage['reset_date'] - current_time).total_seconds() / 3600,
                'message': f'{remaining} free uses remaining today',
                'is_subscribed': False
            }
        else:
            reset_time = user_usage['reset_date']
            hours_until_reset = (reset_time - current_time).total_seconds() / 3600
            return {
                'allowed': False,
                'remaining': 0,
                'reset_in_hours': hours_until_reset,
                'message': f'Daily limit reached. Resets in {round(hours_until_reset, 1)} hours.',
                'is_subscribed': False
            }
    
    @staticmethod
    def record_usage(email):
        """Record a usage of the detection service"""
        if not email:
            return {'success': False, 'message': 'User not required'}
        
        # Skip if user is subscribed (unlimited)
        from .subscription_manager import SubscriptionManager
        if SubscriptionManager.is_subscribed(email):
            return {'success': True, 'message': 'Usage recorded (unlimited)'}
        
        # Record usage for free tier
        user_usage = usage_db[email]
        current_time = datetime.now()
        
        # Initialize if needed
        if user_usage['reset_date'] is None:
            user_usage['reset_date'] = current_time + timedelta(hours=FREE_USAGE_RESET_HOURS)
        
        # Check if we need to reset
        if current_time >= user_usage['reset_date']:
            user_usage['count'] = 0
            user_usage['reset_date'] = current_time + timedelta(hours=FREE_USAGE_RESET_HOURS)
        
        # Increment count
        user_usage['count'] += 1
        
        return {
            'success': True,
            'message': 'Usage recorded',
            'remaining': FREE_USAGE_LIMIT - user_usage['count']
        }
    
    @staticmethod
    def get_usage_status(email):
        """Get detailed usage status for a user"""
        return UsageTracker.check_usage_allowed(email)
    
    @staticmethod
    def reset_usage(email):
        """Manually reset usage (admin function)"""
        if email in usage_db:
            usage_db[email] = {'count': 0, 'reset_date': None}
        return {'success': True, 'message': 'Usage reset'}
    
    @staticmethod
    def get_reset_time(email):
        """Get the reset time for a user"""
        user_usage = usage_db[email]
        if user_usage['reset_date']:
            return user_usage['reset_date'].strftime('%Y-%m-%d %H:%M:%S')
        return None
