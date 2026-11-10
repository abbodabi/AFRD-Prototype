# ==================== IMPORTS ====================
from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from services.scraper import ReviewScraper
from services.preprocessing import TextPreprocessor
from services.hf_detector import FakeReviewDetector

# Import auth module
from auth import SubscriptionManager, UsageTracker

# ==================== APP CONFIGURATION ====================
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# ==================== MAIN ROUTES ====================

@app.route('/', methods=['GET'])
def index():
    """Main dashboard - shows the detection form"""
    user_email = session.get('user_email')
    
    if user_email:
        # Get user info for display
        usage_info = UsageTracker.get_usage_status(user_email)
        subscription_status = SubscriptionManager.get_subscription_status(user_email)
        return render_template(
            'index.html', 
            user=user_email,
            usage_info=usage_info,
            subscription_status=subscription_status
        )
    
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Main detection endpoint - checks usage limits before processing
    """
    user_email = session.get('user_email')
    
    # Check usage allowance
    usage_check = UsageTracker.check_usage_allowed(user_email)
    
    if not usage_check['allowed']:
        # Handle different denial scenarios
        if usage_check.get('requires_login'):
            return redirect(url_for('login', redirect='/'))
        
        # Free limit reached - redirect to subscribe
        return render_template(
            'index.html',
            error=usage_check['message'],
            show_subscribe=True,
            user=user_email
        )
    
    # Proceed with detection
    product_url = request.form['url']

    try:
        scraper = ReviewScraper(product_url)
        reviews = scraper.scrape_reviews(max_reviews=5)
    except ValueError as e:
        return render_template("index.html", error=str(e), user=user_email)

    detector = FakeReviewDetector()

    analyzed_reviews = []
    fake_count = 0

    for r in reviews:
        pre = TextPreprocessor(r["content"])
        clean_text = pre.preprocess()

        result = detector.predict(clean_text)

        top = result[0][0]
        label = top["label"]
        confidence = round(top["score"] * 100, 2)

        prediction = "Fake" if label.lower() == "fake" else "Real"

        if prediction == "Fake":
            fake_count += 1

        analyzed_reviews.append({
            "content": r["content"],
            "prediction": prediction,
            "confidence": confidence,
            "source": r.get("source", "")
        })

    fake_percentage = round((fake_count / len(analyzed_reviews)) * 100, 2)
    
    # Record usage after successful detection
    if user_email:
        UsageTracker.record_usage(user_email)

    return render_template(
        "result.html",
        reviews=analyzed_reviews,
        fake_percentage=fake_percentage,
        user=user_email
    )

# ==================== AUTH ROUTES ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        data = request.get_json()
        result = SubscriptionManager.authenticate_user(
            data.get('email'),
            data.get('password')
        )
        if result['success']:
            session['user_email'] = data['email']
        return jsonify(result)
    
    redirect_url = request.args.get('redirect', '/dashboard')
    return render_template('login.html', redirect_url=redirect_url)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register page"""
    if request.method == 'POST':
        data = request.get_json()
        result = SubscriptionManager.create_user(
            data.get('email'),
            data.get('password'),
            data.get('name')
        )
        return jsonify(result)
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.pop('user_email', None)
    return redirect(url_for('index'))

# ==================== SUBSCRIPTION ROUTES ====================

@app.route('/dashboard')
def dashboard():
    """Dashboard page - requires login"""
    if 'user_email' not in session:
        return render_template('login.html', redirect_url='/dashboard')
    
    user_email = session['user_email']
    status = SubscriptionManager.get_subscription_status(user_email)
    usage = UsageTracker.get_usage_status(user_email)
    from auth.subscription_manager import SUBSCRIPTION_PLANS
    
    return render_template(
        'dashboard.html',
        user=user_email,
        subscription_status=status,
        usage_info=usage,
        plans=SUBSCRIPTION_PLANS
    )

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Checkout page"""
    from auth.subscription_manager import SUBSCRIPTION_PLANS
    
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
    
    user = session.get('user_email')
    return render_template('checkout.html', plans=SUBSCRIPTION_PLANS, user=user)

@app.route('/subscribe')
def subscribe():
    """Subscription plans page"""
    from auth.subscription_manager import SUBSCRIPTION_PLANS
    user_email = session.get('user_email')
    return render_template('subscribe.html', plans=SUBSCRIPTION_PLANS, user=user_email)

# ==================== API ENDPOINTS ====================

@app.route('/api/subscription-status', methods=['GET'])
def api_subscription_status():
    """API endpoint to check subscription status"""
    if 'user_email' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    status = SubscriptionManager.get_subscription_status(session['user_email'])
    return jsonify(status)

@app.route('/api/cancel-subscription', methods=['POST'])
def api_cancel_subscription():
    """Cancel current subscription"""
    if 'user_email' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    result = SubscriptionManager.cancel_subscription(session['user_email'])
    return jsonify(result)

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html', error='Page not found'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('index.html', error='Internal server error'), 500

# ==================== MAIN ENTRY POINT ====================

if __name__ == '__main__':
    # Use PORT from environment (for deployment) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
