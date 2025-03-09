# A program to generate a superhero name

# ----------------
# Imports
# ----------------
from flask import Flask, g, render_template
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
    



# ----------------
# Main program
# ----------------
if __name__ == '__main__':
    app.run(port=5555, debug=True)

