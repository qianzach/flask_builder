from flask import Flask, g, render_template, request
import sqlite3


#Pages
app = Flask(__name__)

# Main Page
@app.route("/")
def main():
    """
    function used access to our base home page
    """
    return render_template("base.html")  #returns our home base page

# Page with messages
@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    """
    submit a message function inspired by Professor Chodrow's example MNIST ML model code
    """
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        try:
            return render_template('submit.html', name=request.form['name'], message=request.form['message'])
        except:
            return render_template('submit.html')

#Page with table
@app.route('/view/')
def view():
    """
    used to display messages from random_messages()
    """
    cap = 5 #use prof. chodrow's limit for # of messages
    tbl_list = random_messages(cap) # Run random_messages() to get a list of tuples of random messages
    return render_template('view.html', messages=tbl_list)

#functions
def get_message_db():
    """
    This function should handle creating the database of messages, and it does so by checking for any message in the g attribute of our app
    
    Check existence of table called 'messages' exists, and create one if non-existent
    
    Return the connection g.message_db
    """
    if 'message_db'  not in g: #check existence of message in g attribute
        g.message_db = sqlite3.connect("message_db.sqlite")
    conn = g.message_db
    cursor = conn.cursor()
    #we need to make a table messages if it doesn't already exist
    cursor.execute("CREATE TABLE IF NOT EXISTS messages (ID INTEGER NOT NULL AUTOINCREMENT, name TEXT, message TEXT, PRIMARY KEY (ID));")
    
    return g.message_db

def insert_message(request):
    """
     The goal of this function is to handle inserting a user message into the SQL database of messages.
    """
    #1. extract message and handle from request
    message = request.form["message"]
    name = request.form["name"]
    
    #Using a cursor, insert the message into the message database.
    #Remember that you’ll need to provide an ID number, the handle, and the message itself.
    #You’ll need to write a SQL command to perform the insertion.
    db = get_message_db()
    cursor = db.cursor() #access cursor
    cursor.execute("INSERT INTO messages (message, name) VALUES (?, ?)", (message, name)) #inserting row
    db.commit() #commit changes
    db.close() #close connection

def random_messages(n):
    """
    this function's purpose is to randomly return a collection of n messages from the messages db
    """

    db = get_message_db()
    cursor = db.cursor()

    randoms = cursor.execute("SELECT message, name FROM messages ORDER BY RAND()  LIMIT ?", (n)).fetchall()
    db.close()

    if len(randoms) > 0:
        return randoms
    else:
        return None


