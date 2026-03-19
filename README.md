# 🛡️ FinTech Risk Agent: Autonomous Threat Intelligence Pipeline

**Built for the Airia AI Agents Hackathon**
### 🔗 Live Demo
**[Test the FinTech Risk Agent on Airia Here](https://explore.airia.com/YOUR-LINK-HERE](https://community.airia.ai/import-agent/E2ZWpUsX8upZ4wQMEWHJVm0dLlNxhQi3rK5gy2lR6zt )**

> **⚠️ Judge's Note Regarding the Live Link:** > Because this agent executes real Python code to interact with APIs and send emails, the backend is currently hosted locally via a secure Ngrok tunnel. If the agent fails to respond in the Airia chat, the local tunnel may be temporarily offline. **Please refer to our 4-minute demo video** to see the full autonomous pipeline and omnichannel webhook execution in action!

## 💡 The Inspiration
In modern algorithmic trading, when a major cyber breach hits Bloomberg news, the market prices in the drop within milliseconds. Portfolio managers are always 24 hours too late. We wanted to capture the **"Golden Window"**—the critical time between a vulnerability being logged in the National Vulnerability Database (NVD) and the broader market reacting.

We built an autonomous AI agent that monitors technical vulnerability databases, cross-references the data with live financial markets, and alerts risk management teams *before* the news cycle catches on.

## ⚙️ What it does
The FinTech Risk Agent acts as an autonomous cybersecurity analyst and financial researcher. Through a natural language chat interface, users can ask the agent to assess the risk of any publicly traded company. 

Behind the scenes, the agent autonomously executes a multi-step pipeline:
1. **Cyber Threat Scanning:** Queries the NIST NVD API for any zero-day vulnerabilities or critical CVEs associated with the company in the last 24-48 hours.
2. **Financial Impact Check:** Translates the company name to a stock ticker and queries Yahoo Finance for live market pricing and 24-hour percentage changes.
3. **Omnichannel Broadcasting:** If the user provides an email address, the agent formulates a comprehensive risk report and securely dispatches it to Microsoft Teams, Slack, and the client's Email via an automated webhook pipeline.

## 🏗️ Architecture & Tech Stack
This project leverages a hybrid cloud/local architecture to keep memory footprint low while maximizing AI reasoning speed.

* **The Brain (Cloud):** Airia Agent Builder powered by **Claude 3.5 Haiku**. The LLM handles natural language processing, orchestrates tool calling, and formats the final reports.
* **The Muscles (Local API):** A lightweight **Python Flask** backend running locally.
* **The Bridge:** **Ngrok** creates a secure, temporary tunnel allowing the Airia cloud agent to trigger our local Python functions safely.
* **Integrations:** NIST NVD REST API, Yahoo Finance API, Microsoft Teams Webhooks, Slack Webhooks, and standard `smtplib` for email routing.

## 🚀 How to Run it Locally

### Prerequisites
* Python 3.x installed
* An active [Ngrok](https://ngrok.com/) account
* Webhook URLs for Slack/Teams (Optional)
* A Gmail App Password (Optional, for email alerts)

### Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/fintech-risk-agent.git](https://github.com/yourusername/fintech-risk-agent.git)
   cd fintech-risk-agent
