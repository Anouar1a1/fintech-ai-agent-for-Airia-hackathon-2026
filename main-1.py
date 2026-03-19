from flask import Flask, request, jsonify
import requests
import json
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# ==========================================
# 🔑 CONFIGURATION & CREDENTIALS
# ==========================================
TEAMS_WEBHOOK_URL = "YOUR_TEAMS_WEBHOOK_URL_HERE"
SLACK_WEBHOOK_URL = "YOUR_SLACK_WEBHOOK_URL_HERE"

EMAIL_SENDER = "your_email@gmail.com"
EMAIL_APP_PASSWORD = "your_16_letter_app_password"

# ==========================================
# 🛡️ THE CYBER WATCHER (NVD Scraper)
# ==========================================
def fetch_recent_vulnerabilities(company_name, hours_back):
    print(f"🔍 Scanning NVD for '{company_name}' (Last {hours_back}h)...")
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    
    now = datetime.utcnow()
    past_date = now - timedelta(hours=hours_back)
    date_format = "%Y-%m-%dT%H:%M:%S.000"
    
    params = {
        "keywordSearch": company_name,
        "pubStartDate": past_date.strftime(date_format),
        "pubEndDate": now.strftime(date_format),
        "resultsPerPage": 3 
    }
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status() 
        data = response.json()
        vulnerabilities = data.get("vulnerabilities", [])
        
        if not vulnerabilities:
            return False
        return True # Found something!
    except Exception as e:
        print(f"⚠️ NVD Scan Error: {e}")
        return False

# ==========================================
# 🔀 THE TRANSLATOR (Company to Ticker)
# ==========================================
def get_stock_ticker(company_name):
    url = "https://query2.finance.yahoo.com/v1/finance/search"
    params = {"q": company_name, "quotesCount": 1, "newsCount": 0}
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        quotes = response.json().get('quotes', [])
        
        if not quotes:
            return None
        return quotes[0].get('symbol')
    except Exception:
        return None

# ==========================================
# 📈 THE FINANCIAL REALITY (Market Data)
# ==========================================
def get_live_market_data(ticker_symbol):
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker_symbol}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json().get("chart", {}).get("result", [])
        
        if not result:
            return None
            
        meta = result[0].get("meta", {})
        current_price = meta.get("regularMarketPrice")
        previous_close = meta.get("previousClose")
        
        if current_price is None or previous_close is None:
            return None
            
        if previous_close == 0:
            percent_change = 0.0
        else:
            percent_change = ((current_price - previous_close) / previous_close) * 100
            
        return {"price": round(current_price, 2), "change": round(percent_change, 2)}
    except Exception:
        return None

# ==========================================
# 📣 BROADCAST FUNCTIONS
# ==========================================
def send_teams_alert(company, ticker, price, change, has_threats):
    if TEAMS_WEBHOOK_URL == "YOUR_TEAMS_WEBHOOK_URL_HERE": return
    
    color = "FF0000" if has_threats else "00FF00"
    status = "🚨 CRITICAL RISK" if has_threats else "✅ NO THREATS DETECTED"
    
    payload = {
        "@type": "MessageCard",
        "themeColor": color,
        "summary": f"FinTech Risk Alert: {company.upper()}",
        "sections": [{
            "activityTitle": f"**FinTech Risk Assessment: {company.upper()}**",
            "activitySubtitle": status,
            "facts": [
                {"name": "Ticker:", "value": ticker if ticker else "N/A"},
                {"name": "Price:", "value": f"${price}" if price else "N/A"},
                {"name": "24h Change:", "value": f"{change}%" if change is not None else "N/A"}
            ]
        }]
    }
    try: requests.post(TEAMS_WEBHOOK_URL, json=payload)
    except Exception: pass

def send_slack_alert(company, ticker, price, change, has_threats):
    if SLACK_WEBHOOK_URL == "YOUR_SLACK_WEBHOOK_URL_HERE": return
    status = "🚨 *CRITICAL RISK*" if has_threats else "✅ *SECURE*"
    message = f"🛡️ *FinTech Risk Assessment: {company.upper()}*\n> {status}\n> *Ticker:* {ticker}\n> *Change:* {change}%"
    try: requests.post(SLACK_WEBHOOK_URL, json={"text": message})
    except Exception: pass

def send_email_alert(company, ticker, price, change, has_threats, receiver_email):
    subject = f"FinTech Risk Alert: {company.upper()} Assessment"
    body = f"CYBER THREAT DETECTED FOR {company.upper()}.\n\n" if has_threats else f"Routine scan complete for {company.upper()}.\n\n"
    body += f"Ticker: {ticker}\nCurrent Price: ${price}\n24h Change: {change}%\n\nPlease review immediately."

    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"🚨 Email Error: {e}")
        return False

# ==========================================
# 🌐 FLASK API ROUTES (AIRIA TOOLS)
# ==========================================
@app.route('/scan_cyber_threats', methods=['POST'])
def scan_cyber_threats():
    data = request.json
    company_name = data.get("company_name")
    hours = data.get("hours_back", 24)
    print(f"🤖 AIRIA INCOMING REQUEST: Scanning {company_name} for threats...")
    
    has_threats = fetch_recent_vulnerabilities(company_name, hours)
    return jsonify({"company": company_name, "critical_threats_found": has_threats})

@app.route('/check_financials', methods=['POST'])
def check_financials():
    data = request.json
    company_name = data.get("company_name")
    print(f"🤖 AIRIA INCOMING REQUEST: Checking financials for {company_name}...")
    
    ticker = get_stock_ticker(company_name)
    if not ticker: return jsonify({"error": "No public ticker found."})
        
    market_data = get_live_market_data(ticker)
    if not market_data: return jsonify({"error": "Could not fetch market data."})
    
    return jsonify({
        "ticker": ticker,
        "current_price": market_data['price'],
        "percent_change_24h": market_data['change']
    })

@app.route('/send_alerts', methods=['POST'])
def send_alerts():
    data = request.json
    company_name = data.get("company_name", "Unknown")
    ticker = data.get("ticker", "N/A")
    price = data.get("price", "N/A")
    change = data.get("change", "N/A")
    has_threats = data.get("has_threats", False)
    client_email = data.get("client_email")
    
    print(f"📣 AIRIA INCOMING REQUEST: Broadcasting alerts for {company_name}...")
    
    # Always fire internal webhooks (if you set up the URLs at the top)
    send_teams_alert(company_name, ticker, price, change, has_threats)
    send_slack_alert(company_name, ticker, price, change, has_threats)
    
    if client_email:
        print(f"📧 Client provided email ({client_email}). Sending report...")
        success = send_email_alert(company_name, ticker, price, change, has_threats, receiver_email=client_email)
        if success:
            return jsonify({"status": f"Alerts triggered. Email successfully sent to {client_email}."})
        else:
            return jsonify({"status": f"Internal alerts triggered. Email to {client_email} failed."})
    else:
        return jsonify({"status": "Internal alerts triggered. No client email requested."})

if __name__ == '__main__':
    app.run(port=5000)