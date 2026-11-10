"""
Authentication and Subscription Routes
Handles login, register, logout, dashboard, checkout, and subscription management.
"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from .subscription_manager import SubscriptionManager, SUBSCRIPTION_PLANS
from .usage_tracker import UsageTracker

# Create Blueprint
auth_bp = Blueprint('auth', __name__)

# Helper to require login
def require_login(f):
    """Decorator to require login for a route"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('auth.login', redirect=request.url))
        return f(*args, **kwargs)
    return decorated_function


# ==================== AUTH ROUTES ====================

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if request.method == 'POST':
        data = request.get_json()
        result = SubscriptionManager.create_user(
            data.get('email'),
            data.get('password'),
            data.get('name')
        )
        return jsonify(result)
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if request.method == 'POST':
        data = request.get_json()
        result = SubscriptionManager.authenticate_user(
            data.get('email'),
            data.get('password')
        )
        if result['success']:
            session['user_email'] = data['email']
        return jsonify(result)
    
    # Check for redirect parameter
    redirect_url = request.args.get('redirect', '/dashboard')
    return render_template('login.html', redirect_url=redirect_url)


@auth_bp.route('/logout')
def logout():
    """Logout user"""
    session.pop('user_email', None)
    return redirect(url_for('index'))


# ==================== SUBSCRIPTION ROUTES ====================

@auth_bp.route('/dashboard')
def dashboard():
    """User dashboard with subscription info"""
    if 'user_email' not in session:
        return render_template('login.html', redirect_url='/dashboard')
    
    user_email = session['user_email']
    status = SubscriptionManager.get_subscription_status(user_email)
    usage = UsageTracker.get_usage_status(user_email)
    
    return render_template(
        'dashboard.html',
        user=user_email,
        subscription_status=status,
        usage_info=usage,
        plans=SUBSCRIPTION_PLANS
    )


@auth_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Checkout and subscription selection"""
    if request.method == 'POST':
        if 'user_email' not in session:
            return jsonify({'success': False, 'message': 'Please login first'}), 401
        
        data = request.get_json()
        plan_type = data.get('plan_type')
        
        result = SubscriptionManager.create_subscription(
            session['user_email'],
            plan_type
        )
        return jsonify(result)
    
    if 'user_email' in session:
        return render_template('checkout.html', plans=SUBSCRIPTION_PLANS, user=session['user_email'])
    return render_template('checkout.html', plans=SUBSCRIPTION_PLANS)


@auth_bp.route('/subscribe')
def subscribe_page():
    """Subscription plans landing page"""
    if 'user_email' in session:
        # Check if already subscribed
        status = SubscriptionManager.get_subscription_status(session['user_email'])
        if status.get('is_active'):
            return redirect(url_for('auth.dashboard'))
        return render_template('subscribe.html', plans=SUBSCRIPTION_PLANS, user=session['user_email'])
    return render_template('subscribe.html', plans=SUBSCRIPTION_PLANS)


# ==================== API ENDPOINTS ====================

@auth_bp.route('/api/subscription-status', methods=['GET'])
def subscription_status():
    """API endpoint to check subscription status"""
    if 'user_email' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    status = SubscriptionManager.get_subscription_status(session['user_email'])
    return jsonify(status)


@auth_bp.route('/api/usage-status', methods=['GET'])
def usage_status():
    """API endpoint to check usage status"""
    if 'user_email' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    usage = UsageTracker.get_usage_status(session['user_email'])
    return jsonify(usage)


@auth_bp.route('/api/cancel-subscription', methods=['POST'])
def cancel_subscription():
    """Cancel current subscription"""
    if 'user_email' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    result = SubscriptionManager.cancel_subscription(session['user_email'])
    return jsonify(result)


@auth_bp.route('/api/plans')
def get_plans():
    """API endpoint to get all subscription plans"""
    plans_with_details = []
    for plan_id, plan_info in SUBSCRIPTION_PLANS.items():
        plans_with_details.append({
            'id': plan_id,
            **plan_info
        })
    return jsonify(plans_with_details)
