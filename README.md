# 💰 Personal Finance Manager – Raspberry Pi Web App

A lightweight, web-based personal finance management tool built with **Python (Flask)** and hosted on a **Raspberry Pi**. This application helps individuals easily track income, expenses, and generate financial reports, all from a clean and intuitive interface.

## 🧩 Features

### ✅ Transaction Management
- Add, edit, and delete transactions (income/expense)
- Attach notes, categories, and dates to transactions
- Real-time balance updates based on transaction history

### 📂 Categorization
- Dynamic category selection based on transaction type
- Support for custom user-defined categories

### 📜 Transaction History
- Chronological listing of all transactions
- Filtering options for easier browsing

### 💹 Financial Summary
- Auto-calculated balance
- PDF report generation of transaction logs and summaries

### 📄 Report Generation
- Downloadable PDF reports
- Detailed summaries for specific time periods

---

## 🛠️ Tech Stack

| Layer       | Technologies                   |
|-------------|--------------------------------|
| Backend     | Python, Flask                  |
| Database    | SQLite                         |
| Frontend    | HTML, CSS, JavaScript          |
| PDF Export  | FPDF                           |

---

## 📁 Database Schema

The app uses a simple SQLite database with a single `transactions` table:

- `id` – Unique transaction ID
- `type` – 'Income' or 'Expense'
- `category` – User-defined category
- `amount` – Monetary value
- `note` – Optional description
- `date` – Transaction date

---

## 🚀 Deployment

This project runs on a local server using a **Raspberry Pi**. However, it can be easily deployed to cloud platforms like **Heroku**, **AWS**, or **Render** for broader accessibility.

To run locally:
```bash
git clone https://github.com/your-username/personal-finance-manager.git
cd personal-finance-manager
pip install -r requirements.txt
python app.py
