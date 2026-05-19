from flask import Flask, render_template, request, redirect, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'fitness_buddy_secret'

# --- ADD THIS LINE RIGHT HERE ---
# This forces the app to look in its exact folder location
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fitness_buddy.db')
def init_db():
    conn = sqlite3.connect(DB_PATH) # Changed this line
    cursor = conn.cursor()
    # ... rest of your code ...# This creates the table structure
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            fitness_goal TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/join', methods=['POST'])
def join_beta():
    name = request.form.get('full_name')
    email = request.form.get('email')
    goal = request.form.get('fitness_goal')

    conn = sqlite3.connect('fitness_buddy.db', timeout=20)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (full_name, email, fitness_goal) VALUES (?, ?, ?)",
            (name, email, goal)
        )
        conn.commit()
        return render_template('index.html', success=True, name=name)
    except sqlite3.IntegrityError:
        return "Database Error: This email is already registered!"
    except Exception as e:
        return f"Database Error: {e}"
    finally:
        conn.close()
        
    @app.route('/admin')
    def admin_panel():
    conn = sqlite3.connect(DB_PATH)          # <-- Indent 4 spaces
    cursor = conn.cursor()                    # <-- Indent 4 spaces
    
    # FIX: "fitness_goal" was missing...     # <-- Indent 4 spaces
    cursor.execute("SELECT id, full_name...") # <-- Indent 4 spaces
    all_users = cursor.fetchall()             # <-- Indent 4 spaces
    conn.close()                              # <-- Indent 4 spaces
    return render_template('admin.html', ...) # <-- Indent 4 spaces

@app.route('/delete/<int:user_id>')   # <-- Move completely to the left (0 spaces)
def delete_user(user_id):             # <-- Move completely to the left (0 spaces)
    conn = sqlite3.connect(DB_PATH)   # <-- Keep indented (4 spaces)
    cursor = conn.cursor()             # <-- Keep indented (4 spaces)
    
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    return redirect('/admin')

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
