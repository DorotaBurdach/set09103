import os
from flask import Flask, request, render_template, url_for,g, redirect, session, flash, abort
from functools import wraps
from werkzeug.utils import secure_filename
import sqlite3
from flask import Markup
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads/')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = "xyz123456789"
#-------------------------------------ERROR----------------


#page not found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#server problem
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

#access denied
@app.errorhandler(401)
def internal_server_error(e):
    return render_template('401.html'), 401

#--------------------------------------PAGES without login----------------


@app.route('/', methods=('GET', 'POST'))
def root():
    msg = None
    connection = sqlite3.connect("books.db")
    connection.row_factory = sqlite3.Row
    paths6 = connection.cursor().execute("SELECT * FROM books").fetchall()

    if request.method == 'POST':
      try:
        name = request.form['name']
        email = request.form['email']
        title = request.form['title']
        message = request.form['message']

        if (name and email and title and message):
           con = sqlite3.connect("books.db")
           cur = con.cursor()
           cur.execute("INSERT INTO mail (name,email,title, message) VALUES (?,?,?,?)",(name,email,title,message) )

           con.commit()
           msg = "Thank you. Your email has been sent successfully."

        else:
           msg = "Please fill up all fields"

      except:
           msg="Sorry. Something went wrong. Please try again later."

    return render_template("index.html", paths6 = paths6, msg=msg)


	
#-----------------------------------------ADMIN PANEL-------------------



@app.route("/admin")
def admin():
  if session.get('logged_in'):
    sql2 = ('SELECT * FROM books')
    connection = sqlite3.connect("books.db")
    connection.row_factory = sqlite3.Row
    all_paths = connection.cursor().execute(sql2).fetchall()

    return render_template('admin.html', all_paths = all_paths)
  else:
    abort(401)


@app.route('/login', methods=('GET', 'POST'))
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials. Please try again'
        else:
            session['logged_in'] = True
            flash('You were just logged in!')
            return redirect(url_for('admin'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
  if session.get('logged_in'):
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('login'))
  else:
    abort(401)



#---------------------------------BOOKS ADMIN
#list of books
@app.route('/list_books')
def list():
    sql = ('SELECT * FROM new')
    connection = sqlite3.connect("books.db")
    connection.row_factory = sqlite3.Row
    list_books = connection.cursor().execute(sql).fetchall()

    return render_template('list.html', list_books=list_books)
    connection.close()

	
@app.route('/up_new', methods=['GET', 'POST'])
def upload_file_new():
  if session.get('logged_in'):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file_new',
                                    filename=filename))
    return render_template("upload_new.html")
  else:
    abort(401)

from flask import send_from_directory

@app.route('/uploads_new/<filename>', methods=('GET', 'POST'))
def uploaded_file_new(filename):
  if session.get('logged_in'):
    msg = None
    if request.method == 'POST':
      try:
        title = request.form['title']
        author = request.form['author']
        desc = request.form['desc']

        if (title and author and desc):
           con = sqlite3.connect("books.db")
           cur = con.cursor()
           cur.execute("INSERT INTO new (title,author,desc,img ) VALUES (?,?,?,?)",(title,author,desc, filename) )

           con.commit()
           msg = "Record successfully added"
           message = Markup("<a href='/preview'>Preview</a>")
           flash(message)

        else:
           msg = "fill up everything man"

      except:
           msg="something went wrong"



    return render_template('suc_new.html', msg=msg)
   
  else:
    abort(401)
#----------------------------------PATHS ADMIN
#list of paths
@app.route('/list2')
def list2():

    sql5 = ('SELECT * FROM books')
    connection = sqlite3.connect("books.db")
    connection.row_factory = sqlite3.Row
    list3 = connection.cursor().execute(sql5).fetchall()

    return render_template('list.html', list3=list3)
    connection.close()


#insert path
@app.route('/insert', methods=('GET', 'POST'))
def insert():
  if session.get('logged_in'):
    msg = None
    if request.method == 'POST':
      try:
        p_name = request.form['p_name']
        p_surname = request.form['p_surname']
        p_desc = request.form['p_desc']

        if (p_name and p_surname and p_desc):
           con = sqlite3.connect("books.db")
           cur = con.cursor()
           cur.execute("INSERT INTO books (p_name,p_surname,p_desc) VALUES (?,?,?)",(p_name,p_surname,p_desc) )

           con.commit()
           msg = "Record successfully added"

        else:
           msg = "fill up everything man"

      except:
           msg="something went wrong"


    return render_template('insert.html', msg=msg)
  else:
    abort(401)

#update path
@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id):
  if session.get('logged_in'):
    msg = None
    print id
    sql2 = ('SELECT * FROM books WHERE id = ?')
    connection = sqlite3.connect("books.db")
    connection.row_factory = sqlite3.Row
    path = connection.cursor().execute(sql2,[id]).fetchall()
    print path
    if request.method == 'POST':
          con = sqlite3.connect("books.db")
          cur = con.cursor()
          query = ("UPDATE books SET p_name = ?,p_surname = ?, p_desc = ? WHERE id=?")
          print id
          cur.execute(query,(request.form['p_name'],request.form['p_surname'],request.form['p_desc'],id))
          con.commit()
          msg = "Record update"
    return render_template('edit.html',id=id, path=path, msg=msg)	
  else:
    abort(401)

@app.route('/delete/<int:id>',methods=['GET', 'POST'])
def delete(id):
   con = sqlite3.connect("books.db")
   cur = con.cursor()
   cur.execute('DELETE FROM books WHERE id=?',[id])
   con.commit()
   msg = "Deleted"

   return redirect(url_for('list'))
#-----------------------------------GUEST PANEL---------------------------


@app.route("/guest")
def guest():
  if session.get('session_guest'):

    return render_template('guest.html')
  else:
    flash('You need to login first')
    return redirect(url_for('login_guest'))



@app.route('/login_guest', methods=('GET', 'POST'))
def login_guest():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'guest' or request.form['password'] != 'guest':
            error = 'Invalid credentials. Please try again'
        else:
            session['session_guest'] = True
            flash('You were just logged in!')
            return redirect(url_for('guest'))
    return render_template('login_guest.html', error=error)

@app.route('/logout_guest')
def logout_guest():
  if session.get('session_guest'):

    session.pop('session_guest', None)
    flash('You were just logged out!')
    return redirect(url_for('login_guest'))
  else:
    abort(401)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/up', methods=['GET', 'POST'])
def upload_file():
  if session.get('session_guest'):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template("upload.html")
  else:
    abort(401)

from flask import send_from_directory

@app.route('/uploads/<filename>', methods=('GET', 'POST'))
def uploaded_file(filename):
  if session.get('session_guest'):
    msg = None
    if request.method == 'POST':
      try:
        p_name = request.form['p_name']
        p_surname = request.form['p_surname']
        p_desc = request.form['p_desc']

        if (p_name and p_surname and p_desc):
           con = sqlite3.connect("books.db")
           cur = con.cursor()
           cur.execute("INSERT INTO books (p_name,p_surname,p_desc, path_desc ) VALUES (?,?,?,?)",(p_name,p_surname,p_desc, filename) )

           con.commit()
           msg = "Record successfully added"
           message = Markup("<a href='/preview'>Preview</a>")
           flash(message)

        else:
           msg = "fill up everything man"

      except:
           msg="something went wrong"



    return render_template('suc.html', msg=msg)
   
  else:
    abort(401)

@app.route('/preview')
def preview():
  if session.get('session_guest'):
   sql2 = ('SELECT * FROM books ORDER BY id DESC LIMIT 1')
   connection = sqlite3.connect("books.db")
   connection.row_factory = sqlite3.Row
   last = connection.cursor().execute(sql2).fetchall()

   return render_template('preview.html', last = last)
  else:
    abort(401)

if __name__ == "__main__":
 app.run( host ='0.0.0.0', debug = True )

 #code from the stackoverflow to remove loading erors
 app.run(threaded=True)

