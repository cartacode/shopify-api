# Shopify Order App

## How to set up environment
1. Install dependencies:
```bash
pip3 install -r requirements.txt
```

2. Copy sample.env.py and change name into env.py. Replace the placeholders with your Shopify store credentials.
```bash
API_KEY = '<SHOPIFY_API_KEY>'
PASSWORD = '<SHOPIFY_PASSWORD>'
SHARED_SECRET = '<SHARED_SECRET>'
SHOP_NAME = '<SHOP_NAME>'
```

## How to run app
```bash
python app.py
```