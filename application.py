import os, random, json

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3


from helpers import apology, login_required


def getApp():
    return app

# Configure application
app = Flask(__name__)

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000, debug=False)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
conn = sqlite3.connect('texts.db', check_same_thread=False)

cursor = conn.cursor()

'''
@app.route("/")
@login_required
def index():
    
    return render_template("main.html")

'''

@app.route("/")
@login_required
def speaking_test():
    return render_template("spech.html")

@app.route("/about")
@login_required
def about():
    return render_template("about.html")

@app.route("/profile")
@login_required
def history():
    cursor.execute("SELECT COUNT(easy_id) FROM easy WHERE easy_id in (SELECT text_id from study WHERE learned = 1 AND user_id = ?)", [session['user_id']])
    easy = cursor.fetchall()
    easy = [item for t in easy for item in t]
    

    cursor.execute("SELECT COUNT(medium_id) FROM intermediate WHERE medium_id in (SELECT text_id from study WHERE learned = 1 AND user_id = ?)", [session['user_id']])
    medium = cursor.fetchall()
    medium = [item for t in medium for item in t]
    

    cursor.execute("SELECT COUNT(hard_id) FROM advanced WHERE hard_id in (SELECT text_id from study WHERE learned = 1 AND user_id = ?)", [session['user_id']])
    hard = cursor.fetchall()
    hard = [item for t in hard for item in t]
    
    diff = [easy, medium, hard]
    
    if max(diff) == 0:
        level = "You didn't learned anything yet"
    elif max(diff) == easy:
        level = "Your level is beginner"
    elif max(diff) == medium:
        level = "Your level is intermediate"
    elif max(diff) == hard:
        level = "Your level is advanced"
        
    cursor.execute("SELECT text FROM dbt WHERE text_id in (SELECT text_id FROM study WHERE learned = 1 AND user_id = ?)",
                   [session['user_id']] )
    learned_text = cursor.fetchall()
    learned_text = [item for t in learned_text for item in t]

    return render_template("profile.html", learned=learned_text, level = level)


@app.route("/get_text/easy")
@login_required
def get_text_easy():
    # Get easy text from db
    easy_text = cursor.execute("SELECT text FROM dbt WHERE text_id in (SELECT easy_id FROM easy)")
    easy_text = [item for t in easy_text for item in t]
    # Get learned texts
    cursor.execute("SELECT text FROM dbt WHERE text_id in (SELECT DISTINCT text_id FROM study WHERE learned = 1 AND user_id = ?)",
                   [session['user_id']] ) 
    learned_text = cursor.fetchall()
    learned_text = [item for t in learned_text for item in t]
    to_learn = []
    # Find which texts from db user didnt learn
    for i in easy_text:
        if i not in learned_text:
            to_learn.append(i)
    # Return random easy text which user didnt learned yet
    choice = random.randint(0, len(to_learn) - 1)
    return jsonify(to_learn[choice])

@app.route("/get_text/medium")
@login_required
def get_text_medium():
    cursor.execute("SELECT text FROM dbt WHERE text_id in (SELECT DISTINCT text_id FROM study WHERE learned = 1 AND user_id = ?)",
                   [session['user_id']] ) 
    learned_text = cursor.fetchall()
    learned_text = [item for t in learned_text for item in t]
    to_learn = []
    medium_text = cursor.execute("SELECT text FROM dbt WHERE text_id in (SELECT medium_id FROM intermediate)") 
    medium_text = [item for t in medium_text for item in t]
    # Find which texts from db user didnt learn
    for i in medium_text:
        if i not in learned_text:
            to_learn.append(i)
    # Return random medium text which user didnt learned yet
    choice = random.randint(0, len(to_learn) - 1)
    return jsonify(to_learn[choice])

@app.route("/get_text/hard")
@login_required
def get_text_hard():
    # Get learned texts
    cursor.execute("SELECT text FROM dbt WHERE text_id in (SELECT DISTINCT text_id FROM study WHERE learned = 1 AND user_id = ?)",
                   [session['user_id']] ) 
    hard_text = cursor.execute("SELECT text FROM dbt WHERE text_id in (SELECT hard_id FROM advanced)") 
    hard_text = [item for t in hard_text for item in t]

    learned_text = cursor.fetchall()
    learned_text = [item for t in learned_text for item in t]
    to_learn = []
    # Find which texts from db user didnt learn
    for i in hard_text:
        if i not in learned_text:
            to_learn.append(i)
    # Return random hard text which user didnt learned yet
    choice = random.randint(0, len(to_learn) - 1)
    return jsonify(to_learn[choice])


@app.route("/get_text")
@login_required
def get_text():
    
    random_text = cursor.execute("SELECT text FROM dbt") 
    random_text = [item for t in random_text for item in t]
    choice = random.randint(0, len(random_text) - 1)
    return jsonify(random_text[choice])
    

@app.route("/speach_analize", methods=["GET", "POST"])
@login_required

def speach_analize():
    '''to do'''
    if request.method == "POST":
        

        user_text = request.form.get('user_text')
        
        
        given_text = request.form.get('given_text')
        '''
        given_text_wo_sign = given_text.replace('.', '')
        given_text_wo_sign = given_text.replace('?', '')
        given_text_wo_sign = given_text.replace('!', '')
        '''
        print(given_text)

        # Remove sign from user and given texts
        for ch in ['.','?','!',',','(',')']:
            if ch in given_text:
                given_text_wo_sign = given_text.replace(ch,"")
            elif ch in user_text:
                user_text = user_text.replace(ch,"")

        user_text = user_text.replace('.', '')
        user_words = user_text.lower().split()

        given_text_wo_sign = given_text_wo_sign.replace('.', '')
        given_text_wo_sign = given_text_wo_sign.replace(')', '')
        given_text_wo_sign = given_text_wo_sign.replace('(', '')
        given_text_wo_sign = given_text_wo_sign.replace("'", '')
        text_words = (given_text_wo_sign.lower()).split()

        res = {"mess":"","wrong" : [], "count" : 0} 
        
        print(given_text_wo_sign)
        print(user_text)
        print(text_words)
        print(user_words)
        
        # Check user was right or not

        congrats = "You are right"
        if given_text_wo_sign.lower() == user_text.lower():
            res['mess'] += "You are right"
            # Get id of text
            cursor.execute("SELECT text_id FROM dbt WHERE text = ?;", [given_text])
            text_id = cursor.fetchall()
            text_id = [item for t in text_id for item in t]
            print(text_id)
           
            # update table
            cursor.execute("INSERT INTO study VALUES(?, ?, ?)", (session['user_id'], int(text_id[0]), 1))
            
            conn.commit()
            return res
        else:
            # Check which words are wrong
    
            res['mess'] += "You said those wrong words"
            wrong_words = []
            for i in range(len(text_words)):
                if user_words[i] not in  text_words:
                    res['wrong'].append(user_words[i])
                    res['count'] += 1
                if i + 1 >= len(user_words):
                    break
            return res



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("You must provide username")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("You must provide password")
            return render_template("login.html")

        # Query database for username
        username=request.form.get("username")
        cursor.execute("SELECT * FROM users WHERE username = ?",
                        [username])
        rows = cursor.fetchall()
        conn.commit()
        # Ensure username exists and password is correct
        if len(rows) == 1:
            if not check_password_hash(rows[0][2], request.form.get("password")):
                flash("invalid username and/or password")
                return render_template("login.html")
                
        else:
            flash("invalid username and/or password")
            return render_template("login.html")
            
        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    if request.method == "POST":
        sql = "SELECT username FROM users"
        new_username = request.form.get("username")
        cursor.execute(sql)
        usernames = cursor.fetchall()
        usernames = [item for t in usernames for item in t]

        conn.commit()
        
        
        # Ensure provided username
        if request.form.get("username") == None:
            flash("Must provide username")
            return render_template("register.html")
            

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password")
            return render_template("register.html")

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("Passwords doesn't match")
            return render_template("register.html")

        # Ensure username is not taken
        elif new_username in usernames:
            flash("Username taken")
            return render_template("register.html")

        # Ensure password contain alphabetical character
        password = request.form.get("password")

        flag = False
        for i in password:
            if i.isalpha():
                flag = True
                break

        if not flag:
            flash("Password must contain at least one alhabetical character")
            return render_template("register.html")
        user = [request.form.get('username'), generate_password_hash((request.form.get('password')))]
        cursor.executemany("INSERT INTO users(username, hash) VALUES(?, ?)",
                    (user,))
        
        # Remember which user has logged in
        cursor.execute("SELECT * FROM users WHERE username = ?",
                        [new_username])
        new_user = cursor.fetchall()
        new_user = [item for t in new_user for item in t]
        print(new_user)
        session.clear()
        session['user_id'] = new_user[0]
        conn.commit()
        flash("Registred!")

        return  redirect('/')

    else:
        return render_template("register.html")

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Register user"""
    if request.method == "POST":
        # Get password's hash
        current_password = request.form.get("current_password")
        if current_password == None:
            flash("Invalid password")
            return render_template("Must provide current password")
            
       # rows = db.execute("SELECT hash FROM users WHERE id = :id", id=session['user_id'])
       # password_hash = rows[0]['hash']
        id = session['user_id']
        cursor.execute("SELECT hash FROM users WHERE id = ?", [id])
        hash = cursor.fetchall()
        password_hash = hash[0][0]
        conn.commit()
        # Ensure current password is correct
        if not check_password_hash(password_hash, current_password):
            flash("Invalid password")
            return render_template("change_password.html")
            

        # Ensure password was submitted
        elif not request.form.get("new_password"):
            flash("You must provide passwrod")
            return render_template("change_password.html")

        elif not request.form.get("new_password_confirmation"):
            flash("You must confirm new password")
            return render_template("change_password.html")

        # Ensure passwords match
        elif request.form.get("new_password") != request.form.get("new_password_confirmation"):
            flash("Passwords doesn't match")
            return render_template("change_password.html")

        # Ensure password contain alphabetical character
        new_password = request.form.get("new_password")

        flag = False
        for i in new_password:
            if i.isalpha():
                flag = True
                break

        if not flag:
            flash("Password must contain at least one alhabetical character")
            return render_template("register.html")

        
        # Update password
        phash = generate_password_hash(new_password)
        new_user = cursor.execute("UPDATE users SET hash = ? WHERE id = ?",
                    (phash, session['user_id']))

        session["user_id"] = new_user.fetchall()
        conn.commit()
        flash("Password has been changed!")

        return redirect("/login")

    else:
        return render_template("change_password.html")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return flash(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
