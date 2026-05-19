from flask import Flask, render_template, request, redirect, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'fitness_buddy_secret'

# --- NEW: This function builds the table if it's missing ---
def init_db():
    conn = sqlite3.connect('fitness_buddy.db')
    cursor = conn.cursor()
    # This creates the table structure
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            fitness_goal TEXT NOT NULL,
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

if __name__ == '__main__':
   @app.route('/admin')
   def admin_panel():
    conn = sqlite3.connect('fitness_buddy.db')
    cursor = conn.cursor()
    # 1. We ask for the ID so the delete button knows which row to hit
    cursor.execute("SELECT full_name, email, fitness_goal, created_at, id FROM users")
    all_users = cursor.fetchall()
    conn.close()
    return render_template('admin.html', users=all_users)

@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    conn = sqlite3.connect('fitness_buddy.db')
    cursor = conn.cursor()
    # 2. This finds the specific ID and deletes it
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    # 3. This sends you back to the admin page to see the updated list
    return redirect('/admin')
# Make sure this part below has NO spaces before it
if __name__ == '__main__':
    init_db()
    # This line allows the server to tell your app which 'port' to use
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    