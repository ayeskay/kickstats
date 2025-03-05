from flask import Flask, render_template, request, redirect, url_for, flash
from config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure MySQL connection
db_config = {
    'user': MYSQL_USER,
    'password': MYSQL_PASSWORD,
    'host': 'localhost',
    'database': MYSQL_DATABASE
}

# Helper function to execute queries and fetch results
def query_db(query, args=(), one=False):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, args)
        results = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return (results[0] if results else None) if one else results
    except mysql.connector.Error as err:
        flash(f"Database error: {err}")
        return None

# Landing Page
@app.route('/')
def index():
    return render_template('index.html')

# Query Passthrough Route
@app.route('/query', methods=['GET', 'POST'])
def query():
    results = None
    if request.method == 'POST':
        raw_query = request.form.get('query')
        try:
            results = query_db(raw_query)
        except Exception as e:
            flash(f"Error executing query: {e}")
    return render_template('query.html', results=results)

# Players Route with Filtering and Sorting
@app.route('/player', methods=['GET'])
def players():
    filter_position = request.args.get('filterPosition')
    sort_by = request.args.get('sortBy', 'marketvalue')
    order = request.args.get('order', 'asc')
    
    query = "SELECT * FROM player"
    filters = []
    args = []

    if filter_position:
        filters.append("position = %s")
        args.append(filter_position)
    
    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += f" ORDER BY {sort_by} {order}"

    players = query_db(query, args)
    return render_template('players.html', players=players)

# Coaches Route with Filtering and Sorting
@app.route('/coach', methods=['GET'])
def coaches():
    sort_by = request.args.get('sortBy', 'experience')
    order = request.args.get('order', 'asc')
    
    query = f"SELECT * FROM coach ORDER BY {sort_by} {order}"
    coaches = query_db(query)
    return render_template('coaches.html', coaches=coaches)

# Countries Route with Sorting
@app.route('/country', methods=['GET'])
def countries():
    sort_by = request.args.get('sortBy', 'ranking')
    order = request.args.get('order', 'asc')
    
    query = f"SELECT * FROM country ORDER BY {sort_by} {order}"
    countries = query_db(query)
    return render_template('countries.html', countries=countries)

# Clubs Route with Sorting
@app.route('/club', methods=['GET'])
def clubs():
    sort_by = request.args.get('sortBy', 'year_of_establishment')
    order = request.args.get('order', 'asc')
    
    query = f"SELECT * FROM club ORDER BY {sort_by} {order}"
    clubs = query_db(query)
    return render_template('clubs.html', clubs=clubs)

# Stadiums Route with Sorting
@app.route('/stadium', methods=['GET'])
def stadiums():
    sort_by = request.args.get('sortBy', 'capacity')
    order = request.args.get('order', 'asc')
    
    query = f"SELECT * FROM country_stadiums ORDER BY {sort_by} {order}"
    stadiums = query_db(query)
    return render_template('stadiums.html', stadiums=stadiums)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
