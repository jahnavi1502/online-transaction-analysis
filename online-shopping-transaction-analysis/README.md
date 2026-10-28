# Online Shopping Transaction Analysis System

Intermediate Python + MySQL project for analyzing individual online-store transactions.

## Folder structure
```text
online-shopping-transaction-analysis/
├── app.py                 # Flask routes and order/product workflows
├── analytics.py           # Pandas aggregation, NumPy statistics, Matplotlib charts
├── config.py              # Environment-based configuration
├── db.py                  # MySQL connection helpers
├── schema.sql             # Database and tables
├── seed.py                # Optional sample data (resets project tables!)
├── requirements.txt
├── .env.example
├── .gitignore
├── templates/             # Flask HTML pages
└── static/                # CSS and generated charts/CSV
```

## Run it (Windows)
1. Install Python 3.10+ and MySQL 8+.
2. Open MySQL Workbench, open `schema.sql`, and execute it. Or run `mysql -u root -p < schema.sql`.
3. Open terminal in this project folder:
   ```powershell
   py -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   Copy-Item .env.example .env
   ```
4. Edit `.env` and set your real MySQL password. Never upload `.env` to Git.
5. Optional demo data:
   ```powershell
   python seed.py
   ```
   WARNING: `seed.py` clears the project tables before inserting demo rows. Use only in a local development database.
6. Start the web app:
   ```powershell
   python app.py
   ```
7. Visit http://127.0.0.1:5000.

macOS/Linux: use `python3 -m venv .venv`, `source .venv/bin/activate`, and `cp .env.example .env`.

## Features
- Product catalogue and order creation with up to three item lines per order.
- Order totals calculated from `quantity * order_items.unit_price`.
- Dashboard for total/completed orders, completed sales, average transaction value and completed units sold.
- Reports for status/payment distribution, monthly order volume, product units sold, and CSV export.

## Metric rules
- Item price is snapshotted when an order is created, so later catalogue price changes do not rewrite past transactions.
- Cancelled and refunded orders remain in order counts and status/payment charts.
- Completed sales, average transaction value, and product units sold include only `Completed` orders.
- Refunded orders are excluded from completed sales; partial refunds are not modeled.
- Payment chart counts orders, not revenue.
- This is transaction-level analysis; it intentionally does not implement customer segmentation or an executive KPI dashboard.

## GitHub push
Create a new empty GitHub repository. Then run:
```bash
git init
git add .
git status
git commit -m "Initial online shopping transaction analysis system"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/online-shopping-transaction-analysis.git
git push -u origin main
```
Replace `YOUR-USERNAME`. If `origin` already exists, use:
`git remote set-url origin https://github.com/YOUR-USERNAME/online-shopping-transaction-analysis.git`

Check `.env` is ignored before pushing: `git check-ignore .env`.
