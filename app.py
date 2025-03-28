# A program to generate a superhero name

# ----------------
# Imports
# ----------------
from flask import Flask, g, render_template, url_for, request, redirect
import sqlite3


# ----------------
# Constants
# ----------------
DATABASE = 'movies.db'

# ----------------
# Globals
# ----------------
app = Flask(__name__)

# ----------------
# Subprograms
# ----------------

# Connect to the database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Close the database connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# home route
@app.route('/')
def index():
        
    cur = get_db().cursor()
    sql = "SELECT * FROM movies;"
    cur.execute(sql)
    results = cur.fetchall()

    return render_template("index.html", movies=results)
    
# movies listing route
@app.route('/movies', methods=['GET', 'POST'])
def movie_listing():
        
    if request.method == 'POST':
        
        cur = get_db().cursor()
        search = request.form['search']      
        director_id = request.form['directors']      
        optional_director = ""
        if director_id:
            optional_director = "AND director_id = " + director_id
        sql = f'''
            SELECT * FROM movies 
            WHERE title LIKE '%' || ? || '%'
            {optional_director}
        '''
        cur.execute(sql, (search,))
        results = cur.fetchall()

    else:
        # Get all movies
        cur = get_db().cursor()
        sql = "SELECT * FROM movies;"
        cur.execute(sql)
        results = cur.fetchall()


    # Get all directors
    cur = get_db().cursor()
    sql = "SELECT * FROM directors ORDER BY name;"
    cur.execute(sql)
    directors = cur.fetchall()

    return render_template("movies.html", movies=results, directors=directors)



# add route
@app.route('/add', methods=['GET', 'POST'])
def add():

    # if request.method == 'GET':
    #     return render_template("add.html")    
    if request.method == 'POST':
        
        cur = get_db().cursor()
        new_title = request.form['title']
        new_release_date = request.form['release_date']
        new_nominations = request.form['nominations']
        new_director_id = request.form['director_id']

        sql = '''
            INSERT INTO movies (title, release_date, nominations, director_id)
            VALUES (?, ?, ?, ?);
        '''
        cur.execute(sql,(new_title, new_release_date, new_nominations, new_director_id))
        get_db().commit()  

    return redirect("/movies")




# ----------------
# Main program
# ----------------
if __name__ == '__main__':
    app.run(port=5555, debug=True)

