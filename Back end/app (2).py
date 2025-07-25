from flask import Flask, render_template, request, redirect, jsonify, send_file
import sqlite3
from fpdf import FPDF

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    # Create transactions table
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 type TEXT,
                 category TEXT,
                 amount REAL,
                 note TEXT,
                 date TEXT)''')

    # Create categories table
    c.execute('''CREATE TABLE IF NOT EXISTS categories
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 type TEXT CHECK(type IN ('Income', 'Expense')),
                 name TEXT UNIQUE)''')

    conn.commit()
    conn.close()

# Function to get transactions from the database
def get_transactions():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("SELECT * FROM transactions ORDER BY date DESC")
    transactions = c.fetchall()
    conn.close()
    return transactions

# Function to calculate the balance
def calculate_balance(transactions):
    balance = 0
    for transaction in transactions:
        if transaction[1] == 'Income':
            balance += transaction[3]
        elif transaction[1] == 'Expense':
            balance -= transaction[3]
    return balance

# Route to serve categories as JSON
@app.route('/categories.json')
def get_categories():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT type, name FROM categories ORDER BY type, name")
    rows = c.fetchall()
    conn.close()

    categories = {'Income': [], 'Expense': []}
    for cat_type, name in rows:
        if name not in categories[cat_type]:  # Prevent duplicate entries in the list
            categories[cat_type].append(name)

    return jsonify(categories)


# Home route
@app.route('/')
def index():
    transactions = get_transactions()
    balance = calculate_balance(transactions)
    return render_template('index.html', transactions=transactions, balance=balance)

# Route to add a transaction
@app.route('/add', methods=['POST'])
def add():
    data = (
        request.form['type'],
        request.form['category'],
        float(request.form['amount']),
        request.form['note'],
        request.form['date']
    )
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("INSERT INTO transactions (type, category, amount, note, date) VALUES (?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()
    return redirect('/')

# Route to delete a transaction
@app.route('/delete/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Route to reset all transactions
@app.route('/reset', methods=['POST'])
def reset_transactions():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("DELETE FROM transactions")
    conn.commit()
    conn.close()
    return redirect('/')

# Route to generate and download PDF report
import os

@app.route('/download-pdf')
def download_pdf():
    transactions = get_transactions()
    balance = calculate_balance(transactions)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Use the absolute path of the installed font
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    # Verify if the font file exists
    if not os.path.exists(font_path):
        return "Error: System font not found at /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 500

    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", "", 12)

    # Title
    pdf.cell(200, 10, "Personal Finance Report", ln=True, align="C")
    pdf.ln(10)

    pdf.cell(200, 10, f"Total Balance: LKR{balance}", ln=True)
    pdf.ln(10)

    for t in transactions:
        pdf.cell(200, 10, f"[{t[5]}] {t[1]} - LKR{t[3]} ({t[2]}) : {t[4]}", ln=True)

    pdf_file_path = "transactions_report.pdf"
    pdf.output(pdf_file_path)

    try:
        return send_file(pdf_file_path, as_attachment=True)
    except Exception as e:
        return f"Error while downloading: {str(e)}", 500





if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
