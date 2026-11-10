# Configuration file for subscription system
# Customize your subscription plans here

# Company Settings
COMPANY_NAME = "Automated Fake Review Detection"
COMPANY_EMAIL = "support@fakereviewnow.com"
WEBSITE_URL = "https://fakereviewnow.com"

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
        'badge': 'TRIAL',
        'recommended': False
    },
    '1_week': {
        'name': '1-Week Starter',
        'duration_days': 7,
        'price': 29.00,
        'features': [
            'Analyze up to 200 reviews',
            'Standard fake review detection',
            'Download detailed reports',
            'Email support'
        ],
        'badge': None,
        'recommended': False
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
        'badge': 'POPULAR',
        'recommended': True
    },
    '3_month': {
        'name': '3-Month Professional',
        'duration_days': 90,
        'price': 129.00,
        'features': [
            'Unlimited review analysis',
            'Advanced AI-powered detection',
            'Detailed fraud analytics',
            'Priority support 24/7',
            'Custom reports & insights',
            'Competitor analysis tool',
            'API access for integrations',
            'Team management (up to 5 users)'
        ],
        'badge': None,
        'recommended': False
    },
    '1_year': {
        'name': '1-Year Enterprise',
        'duration_days': 365,
        'price': 199.99,
        'features': [
            'Unlimited review analysis',
            'Advanced AI-powered detection',
            'Detailed fraud analytics',
            'Priority support 24/7',
            'Custom reports & insights',
            'Competitor analysis tool',
            'API access for integrations',
            'Team management (unlimited users)',
            'White-label solution',
            'Custom integrations'
        ],
        'badge': 'ENTERPRISE',
        'recommended': False
    }
}

# Feature Descriptions
FEATURES_DESCRIPTION = {
    'Analyze up to 50 reviews': 'Perfect for small businesses to test the service',
    'Analyze up to 200 reviews': 'Good for medium-sized businesses',
    'Unlimited review analysis': 'For large-scale operations',
    'Basic fake review detection': 'Pattern-based detection',
    'Standard fake review detection': 'Includes sentiment analysis',
    'Advanced AI-powered detection': 'Machine learning-based detection with 99% accuracy',
    'Download detection report': 'PDF format reports',
    'Download detailed reports': 'Detailed PDF and CSV reports',
    'Custom reports & insights': 'Tailored analytics for your business',
    'Email support': 'Response time: 24-48 hours',
    'Priority email & chat support': 'Response time: 2-4 hours',
    'Priority support 24/7': 'Dedicated account manager',
    'Competitor analysis tool': 'Analyze competitor reviews',
    'API access for integrations': 'RESTful API with full documentation',
    'Team management': 'Invite team members',
    'White-label solution': 'Customize branding',
    'Custom integrations': 'Integration with your systems'
}

# Currency Settings
CURRENCY_SYMBOL = 'P'
CURRENCY_CODE = 'PHP'

# Email Settings
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'noreply@fakereviewnow.com'
SENDER_PASSWORD = 'your_password_here'  # Use environment variable in production!

# UI Settings
THEME_COLOR = '#007bff'
SECONDARY_COLOR = '#6c757d'
SUCCESS_COLOR = '#28a745'
DANGER_COLOR = '#dc3545'

# Security Settings
SESSION_TIMEOUT = 3600  # 1 hour in seconds
PASSWORD_MIN_LENGTH = 8
MAX_LOGIN_ATTEMPTS = 5
LOGIN_ATTEMPT_TIMEOUT = 900  # 15 minutes in seconds

# Feature Flags
ENABLE_TRIAL = True
ENABLE_AUTO_RENEWAL = True
ENABLE_TEAM_MANAGEMENT = True
ENABLE_API = True
ENABLE_WHITE_LABEL = True
ENABLE_PREPROCESSING = True

# Preprocessing Configuration
PREPROCESSING_SETTINGS = {
    'remove_stopwords': True,
    'remove_numbers': True,
    'remove_urls': True,
    'lowercase': True
}

# Money-back Guarantee
GUARANTEE_DAYS = 7

# FAQ Items
FAQ_ITEMS = [
    {
        'question': 'Can I upgrade from 3-day to 1-month plan?',
        'answer': 'Yes! You can upgrade anytime from your dashboard. You\'ll only pay the difference.'
    },
    {
        'question': 'Is there a money-back guarantee?',
        'answer': f'Absolutely! We offer a {GUARANTEE_DAYS}-day money-back guarantee if you\'re not satisfied.'
    },
    {
        'question': 'Can I cancel my subscription anytime?',
        'answer': 'Yes, cancel anytime from your account settings without any hidden charges.'
    },
    {
        'question': 'Do you offer enterprise plans?',
        'answer': 'Yes! Contact our sales team for custom enterprise pricing and features.'
    },
    {
        'question': 'How accurate is the fake review detection?',
        'answer': 'Our advanced AI system has a 99% detection accuracy rate based on thousands of reviews.'
    },
    {
        'question': 'Is my data secure?',
        'answer': 'Yes, your data is encrypted and protected with enterprise-grade security (256-bit SSL).'
    }
]

# Support Channels
SUPPORT_EMAIL = 'support@fakereviewnow.com'
SUPPORT_PHONE = '+1-800-REVIEWS-1'
SUPPORT_HOURS = 'Monday - Friday, 9 AM - 6 PM EST'

# Social Links
SOCIAL_LINKS = {
    'twitter': 'https://twitter.com/fakereviewnow',
    'facebook': 'https://facebook.com/fakereviewnow',
    'linkedin': 'https://linkedin.com/company/fakereviewnow',
    'instagram': 'https://instagram.com/fakereviewnow'
}

# Analytics
ENABLE_ANALYTICS = True
ANALYTICS_ID = 'UA-XXXXXXXXX-X'  # Google Analytics ID

# API Rate Limiting
RATE_LIMIT_REQUESTS = 1000
RATE_LIMIT_PERIOD = 3600  # 1 hour

# Default Dashboard Stats
DEFAULT_STATS = {
    'reviews_analyzed': 0,
    'fake_detected': 0,
    'detection_rate': 0,
    'api_calls': 0
}
