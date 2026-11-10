# Deployment & Setup Guide

## Local Development Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- A web browser

### Installation Steps

1. **Navigate to project directory**
```bash
cd AFRD-SUBSCRIPTION
```

2. **Create virtual environment**
```bash
python -m venv venv
```

3. **Activate virtual environment**

Windows (PowerShell):
```powershell
.\venv\Scripts\Activate.ps1
```

Windows (Command Prompt):
```cmd
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Run the application**
```bash
python subscription.py
```

6. **Access the application**
Open your browser and go to: `http://localhost:5000`

---

## Production Deployment

### Option 1: Deploy to Heroku

1. **Install Heroku CLI**
```bash
# https://devcenter.heroku.com/articles/heroku-cli
```

2. **Create Procfile**
```
web: gunicorn subscription:app
```

3. **Update requirements.txt**
```bash
pip install gunicorn
pip freeze > requirements.txt
```

4. **Create Heroku app**
```bash
heroku create your-app-name
```

5. **Deploy**
```bash
git push heroku main
```

### Option 2: Deploy to AWS

1. **Using Elastic Beanstalk**
```bash
eb init
eb create
eb deploy
```

2. **Using EC2**
- Launch EC2 instance
- Install Python and dependencies
- Configure security groups
- Set up Nginx as reverse proxy

### Option 3: Deploy to DigitalOcean

1. **Create Droplet**
- Choose Ubuntu 20.04 LTS
- Connect via SSH

2. **Install dependencies**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

3. **Clone project**
```bash
git clone your-repo-url
```

4. **Setup and run**
```bash
cd AFRD-SUBSCRIPTION
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. **Configure Nginx**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Production Considerations

### 1. Environment Variables
Create `.env` file:
```env
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost/dbname
STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key
```

### 2. Database Setup

**PostgreSQL Example:**
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database
createdb fake_review_db

# Install Python PostgreSQL driver
pip install psycopg2-binary
```

### 3. SSL/HTTPS Setup

**Using Let's Encrypt with Certbot:**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d your-domain.com
```

### 4. Security Headers
Add to Flask app:
```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

### 5. Database Backup
```bash
# Backup PostgreSQL database
pg_dump fake_review_db > backup.sql

# Restore
psql fake_review_db < backup.sql
```

### 6. Monitoring and Logging

**Using Gunicorn with systemd:**
```ini
[Unit]
Description=Fake Review Detection Service
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/AFRD-SUBSCRIPTION
ExecStart=/path/to/venv/bin/gunicorn --workers 4 subscription:app

[Install]
WantedBy=multi-user.target
```

---

## Scaling Considerations

### Database Optimization
- Use connection pooling
- Index frequently queried columns
- Archive old data

### Caching
```bash
pip install redis Flask-Caching
```

### Load Balancing
- Use Nginx or HAProxy
- Run multiple Gunicorn workers
- Use CDN for static assets

### Monitoring Tools
- Sentry (error tracking)
- Datadog (performance monitoring)
- New Relic (APM)

---

## Integration with Payment Processors

### Stripe Integration
```python
import stripe

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': 2999,  # $29.99
                    'product_data': {
                        'name': '1-Month Premium',
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('subscription_success', _external=True),
            cancel_url=url_for('subscription_cancel', _external=True),
        )
    except Exception as e:
        return str(e)
    
    return redirect(checkout_session.url, code=303)
```

### PayPal Integration
```python
from paypalrestsdk import Api
import paypalrestsdk

paypalrestsdk.configure(
    mode='sandbox',  # or 'live'
    client_id='your-client-id',
    client_secret='your-client-secret'
)
```

---

## Troubleshooting

### Issue: ModuleNotFoundError
**Solution**: Ensure virtual environment is activated
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

### Issue: Port 5000 already in use
**Solution**: Change port in `subscription.py`
```python
app.run(debug=True, port=5001)
```

### Issue: Database connection error
**Solution**: Check DATABASE_URL and ensure database is running
```bash
psql -U postgres -d fake_review_db -c "SELECT 1;"
```

### Issue: Static files not loading
**Solution**: Ensure static folder exists and rebuild
```bash
python -c "from flask import Flask; Flask(__name__).static_folder"
```

---

## Performance Optimization

### 1. Enable Caching
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})
```

### 2. Compress Responses
```bash
pip install flask-compress
```

### 3. Database Query Optimization
- Use ORM efficiently
- Avoid N+1 queries
- Implement pagination

### 4. CDN for Static Assets
- Upload CSS/JS to CloudFront
- Configure caching headers

---

## Monitoring Checklist

- [ ] Server uptime monitoring
- [ ] Database connection health
- [ ] Error tracking (Sentry)
- [ ] Performance metrics (DataDog)
- [ ] Security scanning
- [ ] SSL certificate expiration
- [ ] Backup verification
- [ ] Log rotation

---

## Maintenance

### Regular Tasks
- Update dependencies: `pip install --upgrade -r requirements.txt`
- Monitor disk space
- Review error logs
- Check security vulnerabilities
- Update SSL certificates

### Monthly
- Database optimization
- Performance review
- Security audit
- Backup verification

### Quarterly
- Dependency updates
- Infrastructure review
- Cost optimization
- Disaster recovery drill

---

For support, contact: support@fakereviewnow.com
