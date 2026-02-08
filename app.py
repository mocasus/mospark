from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in production
DB_NAME = 'dapur_cilok.db'

# IMPORTANT: Vercel serverless functions are read-only.
# A local SQLite file will be reset on every deployment/cold start.
# For production, use a managed database like Postgres (e.g., Supabase, Neon) or MongoDB.
# This setup works for demonstration/read-only purposes on Vercel after initial seed,
# but admin changes will be lost.

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL,
            image_url TEXT,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# Routes

@app.route('/')
def index():
    # Attempt to init DB if not exists (for Vercel first run, though read-only file system might block this if not in /tmp)
    # On Vercel, we can't easily write to the root directory.
    # We rely on the DB file being committed to the repo for read-only access.
    try:
        if not os.path.exists(DB_NAME):
             # Fallback: In a real serverless env with no persistent DB, this would fail or return empty.
             # We just return empty list to avoid crashing.
             return render_template('index.html', menu_items=[])

        conn = get_db_connection()
        menu_items = conn.execute('SELECT * FROM menu').fetchall()
        conn.close()
        return render_template('index.html', menu_items=menu_items)
    except Exception as e:
        return f"Database Error: {e}", 500

# Admin Auth (Simple)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password123'  # Simple hardcoded password

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Login Gagal!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('login'))

def is_logged_in():
    return session.get('admin_logged_in')

@app.route('/admin')
def admin_dashboard():
    if not is_logged_in():
        return redirect(url_for('login'))

    try:
        conn = get_db_connection()
        menu_items = conn.execute('SELECT * FROM menu').fetchall()
        conn.close()
        return render_template('admin_dashboard.html', menu_items=menu_items)
    except:
        return render_template('admin_dashboard.html', menu_items=[])

@app.route('/admin/add', methods=['GET', 'POST'])
def add_menu():
    if not is_logged_in():
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form['description']
            price = request.form['price']
            image_url = request.form.get('image_url', '') # Use get() to avoid KeyError
            category = request.form['category']

            conn = get_db_connection()
            conn.execute('INSERT INTO menu (name, description, price, image_url, category) VALUES (?, ?, ?, ?, ?)',
                         (name, description, price, image_url, category))
            conn.commit()
            conn.close()
            flash('Menu berhasil ditambahkan! (Catatan: Data akan hilang saat redeploy di Vercel)')
            return redirect(url_for('admin_dashboard'))
        except sqlite3.OperationalError:
             flash('Error: Database is read-only on Vercel Serverless environment.')
             return redirect(url_for('admin_dashboard'))

    return render_template('menu_form.html', action='Add')

@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
def edit_menu(id):
    if not is_logged_in():
        return redirect(url_for('login'))

    conn = get_db_connection()
    item = conn.execute('SELECT * FROM menu WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form['description']
            price = request.form['price']
            image_url = request.form.get('image_url', '')
            category = request.form['category']

            conn.execute('UPDATE menu SET name = ?, description = ?, price = ?, image_url = ?, category = ? WHERE id = ?',
                         (name, description, price, image_url, category, id))
            conn.commit()
            conn.close()
            flash('Menu berhasil diupdate!')
            return redirect(url_for('admin_dashboard'))
        except sqlite3.OperationalError:
             flash('Error: Database is read-only on Vercel Serverless environment.')
             conn.close()
             return redirect(url_for('admin_dashboard'))

    conn.close()
    return render_template('menu_form.html', action='Edit', item=item)

@app.route('/admin/delete/<int:id>')
def delete_menu(id):
    if not is_logged_in():
        return redirect(url_for('login'))
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM menu WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash('Menu berhasil dihapus!')
    except sqlite3.OperationalError:
        flash('Error: Database is read-only on Vercel Serverless environment.')

    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    # Ensure DB exists locally
    if not os.path.exists(DB_NAME):
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
