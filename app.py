from flask import Flask, render_template, request, redirect, url_for, flash
from config import DATABASE_URL  # Import the Supabase URL
import psycopg2
import psycopg2.extras # Needed to get dictionary-like results

app = Flask(__name__)
app.secret_key = 'your_secret_key' # Keep your secret key

# Helper function to execute queries and fetch results from PostgreSQL
def query_db(query, args=(), one=False):
    """
    Connects to the PostgreSQL database, executes a query, and returns the results.
    """
    try:
        # Connect to the database using the URL from config
        conn = psycopg2.connect(DATABASE_URL)
        # Create a cursor that returns rows as dictionaries (like 'dictionary=True')
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cursor.execute(query, args)
        
        # For SELECT queries, fetch results. For INSERT/UPDATE/DELETE, this will be None.
        results = cursor.fetchall()
        
        # Commit the transaction to make changes permanent
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return (results[0] if results else None) if one else results
    except (Exception, psycopg2.Error) as err:
        # Flash a more generic but helpful error message
        flash(f"Database error: {err}")
        print(f"Database error: {err}") # Also print to console for debugging
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
        # Basic validation to prevent empty queries
        if raw_query:
            try:
                results = query_db(raw_query)
                if results is None:
                    # This could mean an error occurred and was flashed by query_db
                    pass
                elif not results:
                    # Query ran successfully but returned no rows
                    flash("Query executed successfully, but returned no results.")
            except Exception as e:
                flash(f"Error executing query: {e}")
        else:
            flash("Please enter a SQL query.")
    return render_template('query.html', results=results)

# Players Route with Filtering and Sorting
@app.route('/player', methods=['GET'])
def players():
    filter_position = request.args.get('filterPosition')
    sort_by = request.args.get('sortBy', 'marketvalue')
    order = request.args.get('order', 'asc')
    
    # Basic validation for sort_by and order to prevent SQL injection
    allowed_sort_columns = ['player_name', 'position', 'marketvalue', 'nationality'] # Add your player columns
    allowed_order = ['asc', 'desc']
    if sort_by not in allowed_sort_columns or order.lower() not in allowed_order:
        flash("Invalid sorting parameter.")
        return redirect(url_for('players'))

    query = "SELECT * FROM player"
    filters = []
    args = []

    if filter_position:
        filters.append("position = %s")
        args.append(filter_position)
    
    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += f" ORDER BY {sort_by} {order}"

    players = query_db(query, tuple(args))
    return render_template('players.html', players=players)

# Coaches Route with Filtering and Sorting
@app.route('/coach', methods=['GET'])
def coaches():
    sort_by = request.args.get('sortBy', 'experience')
    order = request.args.get('order', 'asc')

    allowed_sort_columns = ['coach_name', 'experience', 'nationality'] # Add your coach columns
    allowed_order = ['asc', 'desc']
    if sort_by not in allowed_sort_columns or order.lower() not in allowed_order:
        flash("Invalid sorting parameter.")
        return redirect(url_for('coaches'))
    
    query = f"SELECT * FROM coach ORDER BY {sort_by} {order}"
    coaches = query_db(query)
    return render_template('coaches.html', coaches=coaches)

# Countries Route with Sorting
@app.route('/country', methods=['GET'])
def countries():
    sort_by = request.args.get('sortBy', 'ranking')
    order = request.args.get('order', 'asc')

    allowed_sort_columns = ['country_name', 'ranking'] # Add your country columns
    allowed_order = ['asc', 'desc']
    if sort_by not in allowed_sort_columns or order.lower() not in allowed_order:
        flash("Invalid sorting parameter.")
        return redirect(url_for('countries'))

    query = f"SELECT * FROM country ORDER BY {sort_by} {order}"
    countries = query_db(query)
    return render_template('countries.html', countries=countries)

# Clubs Route with Sorting
@app.route('/club', methods=['GET'])
def clubs():
    sort_by = request.args.get('sortBy', 'year_of_establishment')
    order = request.args.get('order', 'asc')

    allowed_sort_columns = ['club_name', 'year_of_establishment'] # Add your club columns
    allowed_order = ['asc', 'desc']
    if sort_by not in allowed_sort_columns or order.lower() not in allowed_order:
        flash("Invalid sorting parameter.")
        return redirect(url_for('clubs'))
    
    query = f"SELECT * FROM club ORDER BY {sort_by} {order}"
    clubs = query_db(query)
    return render_template('clubs.html', clubs=clubs)

# Stadiums Route with Sorting
@app.route('/stadium', methods=['GET'])
def stadiums():
    sort_by = request.args.get('sortBy', 'capacity')
    order = request.args.get('order', 'asc')

    allowed_sort_columns = ['stadium_name', 'capacity', 'location'] # Add your stadium columns
    allowed_order = ['asc', 'desc']
    if sort_by not in allowed_sort_columns or order.lower() not in allowed_order:
        flash("Invalid sorting parameter.")
        return redirect(url_for('stadiums'))

    query = f"SELECT * FROM country_stadiums ORDER BY {sort_by} {order}"
    stadiums = query_db(query)
    return render_template('stadiums.html', stadiums=stadiums)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
