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

if __name__ == '__main__':
    #app.run() #production
    app.run(debug=True) #development