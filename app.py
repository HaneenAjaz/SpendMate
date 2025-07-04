from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'            # Your MySQL username
app.config['MYSQL_PASSWORD'] = 'Haneen@10'            # Your MySQL password
app.config['MYSQL_DB'] = 'expense_db'        # Your DB name

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        cur.execute("INSERT INTO expenses (description, amount) VALUES (%s, %s)", (description, amount))
        mysql.connection.commit()
        return redirect('/')

    cur.execute("SELECT * FROM expenses")
    expenses = cur.fetchall()
    total = sum([expense[2] for expense in expenses])
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM expenses WHERE id = %s", (id,))
    mysql.connection.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

