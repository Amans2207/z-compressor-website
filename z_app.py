import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

# 1. App initialization sirf EK baar honi chahiye, sabse upar
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

app.secret_key = 'z_compressor_secret_key'

def get_db():
    # Render ke liye database connection
    conn = sqlite3.connect('z_compressor.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- ROUTES ---

@app.route('/')
def home():
    return render_template('z_index.html')

@app.route('/shop')
def shop():
    category = request.args.get('category')
    conn = get_db()
    if category:
        items = conn.execute("SELECT * FROM inventory WHERE category LIKE ?", ('%'+category+'%',)).fetchall()
    else:
        items = conn.execute("SELECT * FROM inventory").fetchall()
    conn.close()
    return render_template('shop.html', items=items, category=category)

@app.route('/checkout/<int:id>')
def checkout(id):
    conn = get_db()
    item = conn.execute("SELECT * FROM inventory WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template('checkout.html', item=item)

@app.route('/payment-success')
def payment_complete():
    return render_template('success.html')

# --- ADMIN & LOGIN ROUTES ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == 'AmanStudio2026':
            session['logged_in'] = True
            return redirect(url_for('admin'))
    return '''
        <div style="text-align:center; padding:100px; font-family:sans-serif;">
            <h2>Z-Admin Login</h2>
            <form method="post">
                <input type="password" name="password" placeholder="Enter Password" style="padding:10px; width:250px;">
                <button type="submit" style="padding:10px 20px; background:#004a99; color:white; border:none; cursor:pointer;">Login</button>
            </form>
        </div>
    '''

@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = get_db()
    items = conn.execute("SELECT * FROM inventory").fetchall()
    conn.close()
    return render_template('z_admin.html', items=items)

@app.route('/admin/add', methods=['POST'])
def z_add():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    name = request.form['name']
    part_no = request.form['part_no']
    category = request.form['category']
    price = request.form['price']
    description = request.form['description']
    image = request.form.get('image', '') # Use get to avoid errors if missing
    
    conn = get_db()
    conn.execute("INSERT INTO inventory (name, part_no, category, price, description, image) VALUES (?,?,?,?,?,?)",
                 (name, part_no, category, price, description, image))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# --- SERVER START ---

if __name__ == '__main__':
    # Render dynamic port use karta hai
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)