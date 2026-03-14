from flask import Flask, jsonify, render_template, request, redirect, url_for, session

import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'flower_shop_68_1_db'
}

app.config['SECRET_KEY'] = 'asdfghjkl'


@app.route('/home', methods=['GET'])
def home():
    #return "Welcome to the home page!"
    #from flask import jsonify
    #return jsonify({"Message":"Welcome to the home page!"})
    name = "John"
    age = 30
    my_dict = {"name": "Yor", "age": "25"}
    return render_template('home.html', name=name, age=age, my_dict=my_dict)

@app.route('/create', methods=['GET'])
def create():
    return render_template('create.html')

@app.route('/store', methods=['POST'])
def store():
    if request.method == 'POST':
        flower_name = request.form['flowername']
        flower_price = float(request.form['flowerPrice'])
        flower_place = request.form['flowerPlace']
        flower_description = request.form['flowerDescription']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = "INSERT INTO flowers (flower_name, flower_price, flower_place, flower_description) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (flower_name, flower_price, flower_place, flower_description))

        conn.commit()
        cursor.close()
        conn.close()

        session['alert_status'] = 'success'
        session['alert_message'] = 'Flower created successfully!'
        return redirect(url_for('/'))
    else:
        session['alert_status'] = 'error'
        session['alert_message'] = 'Invalid request method.'
        return redirect(url_for('/'))

@app.route('/', methods=['GET'])
def index():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM flowers")
    flowers = cursor.fetchall()

    cursor.close()
    conn.close()

    if 'alert_status' in session and 'alert_message' in session:
        alert_message = {
            'status': session['alert_status'],
            'message': session['alert_message']
        }
        del session['alert_status']
        del session['alert_message']
    else:
        alert_message = {
            'status': None,
            'message': None 
        }
    return render_template('index.html', flowers=flowers, alert_message=alert_message)

@app.route('/edit/<int:flower_id>', methods=['GET'])
def edit(flower_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM flowers WHERE id = %s", (flower_id,))
    flower = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('edit.html', flower=flower)

@app.route('/update/<int:flower_id>', methods=['POST'])
def update(flower_id):
    if request.method == 'POST':
        flower_name = request.form['flowername']
        flower_price = float(request.form['flowerPrice'])
        flower_place = request.form['flowerPlace']
        flower_description = request.form['flowerDescription']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = "UPDATE flowers SET flower_name = %s, flower_price = %s, flower_place = %s, flower_description = %s WHERE id = %s"
        cursor.execute(query, (flower_name, flower_price, flower_place, flower_description, flower_id))

        conn.commit()
        cursor.close()
        conn.close()

        session['alert_status'] = 'success'
        session['alert_message'] = 'Flower updated successfully!'
        return redirect('/')
    else:
        session['alert_status'] = 'error'
        session['alert_message'] = 'Invalid request method.'
        return redirect('/')


@app.route('/delete/<int:flower_id>', methods=['GET'])
def delete(flower_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = "DELETE FROM flowers WHERE id = %s"
    cursor.execute(query, (flower_id,))

    conn.commit()
    cursor.close()
    conn.close()

    session['alert_status'] = 'success'
    session['alert_message'] = 'Flower deleted successfully!'
    return redirect('/')

if __name__ == '__main__':
    #app.run() #production
    app.run(debug=True) #development