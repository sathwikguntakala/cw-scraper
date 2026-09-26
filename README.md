# CW Daily Chicken Rates Scraper 🐔

An automated web scraper that fetches daily wholesale broiler / chicken market rates across **Andhra Pradesh (AP)** and **Telangana (TS)** and synchronizes them directly into **Cloud Firestore** for the 'CW' Flutter Web & Mobile App.

---

## 📌 Features
- **Comprehensive Coverage**: Generates synchronized rates for all **26 AP districts** and all **33 TS districts**.
- **Three Standard Poultry Tiers**:
  1. 🐔 **Live Bird (Farm Gate)**
  2. 🍗 **Dressed (With Skin)**
  3. 🥩 **Skinless Chicken**
- **Automated Scheduling**: Runs daily at **6:00 AM IST** via GitHub Actions.
- **100% Free Firebase Spark Plan Friendly**: Uses ~59 document writes once per day (well within Firebase's 20,000 free writes/day).

---

## 🚀 Local Testing

1. **Install Dependencies**:
   ```bash
   pip install -r scraper/requirements.txt
   ```

2. **Run in Dry-Run Mode** (No Firebase credentials needed):
   ```bash
   python scraper/scrape_rates.py --dry-run
   ```

3. **Run with Live Firestore Write**:
   - Place your `serviceAccountKey.json` inside this directory, or:
   - Set the `FIREBASE_SERVICE_ACCOUNT` environment variable with the JSON contents.
   ```bash
   python scraper/scrape_rates.py
   ```

---

## ⚙️ GitHub Actions Automation

The workflow file [`.github/workflows/daily_scrape.yml`](../.github/workflows/daily_scrape.yml) triggers:
- **Every day at 6:00 AM IST** (`00:30 UTC`).
- **On Demand** via the **Run workflow** button under the GitHub Actions tab.
