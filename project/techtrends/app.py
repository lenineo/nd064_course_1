import sqlite3
import logging

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
from logging.handlers import RotatingFileHandler

connections = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global connections
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    connections+=1
    return connection

def decrease_connection():
    global connections
    if(connections>0):
        connections-=1

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    decrease_connection()
    app.logger.info(post['title'])
    return post

def get_post_count():
    connection = get_db_connection()
    posts = connection.execute('SELECT count(*) FROM posts as count').fetchone()
    connection.close()
    decrease_connection()
    return posts[0]

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    decrease_connection()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.info("Page is ton found : 404")
      return render_template('404.html'), 404
    else:
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info("About us page is retrieved")
    return render_template('about.html')

# Define the post creation functionality
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            decrease_connection()
            app.logger.info("A new article is created")
            return redirect(url_for('index'))

    return render_template('create.html')

# Define the About Us page
@app.route('/healthz')
def health_status():
    data = {"result" : "OK - healthy"}
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    app.logger.debug("Request /status")
    return response

@app.route("/metrics")
def metrics():

    data = {"db_connection_count": connections, "post_count": get_post_count()}
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    app.logger.debug("Request /metrics")
    return response

# start the application on port 3111
if __name__ == "__main__":

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

    log_file = 'app.log'

    logs_handler = RotatingFileHandler(filename=log_file, mode='a', maxBytes=5 * 1024 * 1024,
                                       backupCount=2, encoding=None, delay=0)
    logs_handler.setFormatter(formatter)
    logs_handler.setLevel(logging.DEBUG)

    logging.basicConfig(level=logging.DEBUG,
                        handlers=[logs_handler])

    app.run(host='0.0.0.0', port='3111')
