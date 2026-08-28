# Autonomous CPAGrip AI Affiliate Agent ($0 Tech Stack)

An automated AI agent system that finds the highest EPC offers on CPAGrip for US traffic, crafts psychological marketing angles using Google Gemini, generates anti-ban pre-lander links, and sends ready-to-use content to your Telegram bot.

---

## 📁 Project Structure

```
cpagrip-ai-agent/
├── .github/
│   └── workflows/
│       └── agent_cron.yml      # 24/7 Free cloud automation via GitHub Actions
├── bridge_page/
│   └── index.html              # Free pre-lander page to host on GitHub Pages / Cloudflare
├── modules/
│   ├── offer_engine.py         # CPAGrip API scraper & EPC scoring algorithm
│   ├── content_engine.py       # Gemini Flash prompt orchestration
│   ├── bridge_generator.py     # Clean bridge URL encoder
│   └── notifier.py             # Telegram push notifications
├── main.py                     # Master execution pipeline
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── README.md                   # Documentation & Setup Guide
```

---

## 🚀 Quick Start (Local Run)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Credentials
Copy `.env.example` to `.env` and fill in your free keys:
```bash
cp .env.example .env
```

### 3. Run the Agent
```bash
python main.py
```

---

## 🌐 Deploying the Free Bridge Page (Pre-Lander)

To avoid getting banned by social media platforms:

1. Create a free GitHub repository (e.g. `rewards-hub`).
2. Upload the `bridge_page/index.html` file into it.
3. Go to **Settings** → **Pages** in GitHub → Select `main` branch → Click **Save**.
4. Your free bridge link is: `https://<your-github-username>.github.io/rewards-hub/`.

---

## ☁️ Running 24/7 for Free on GitHub Actions

1. Push this entire repository to your personal private GitHub account.
2. In your repo, go to **Settings** → **Secrets and variables** → **Actions**.
3. Add these 6 repository secrets:
   - `GEMINI_API_KEY`: *(From [Google AI Studio](https://aistudio.google.com/))*
   - `CPAGRIP_USER_ID`: *(From CPAGrip Offer Tools)*
   - `CPAGRIP_KEY`: *(From CPAGrip Offer Tools)*
   - `TELEGRAM_BOT_TOKEN`: *(From Telegram @BotFather)*
   - `TELEGRAM_CHAT_ID`: *(From Telegram @userinfobot)*
   - `BRIDGE_BASE_URL`: *(Your GitHub Pages URL)*
4. The workflow in `.github/workflows/agent_cron.yml` will automatically run every 6 hours and ping your Telegram app with hot US offers and ready-to-post responses.
