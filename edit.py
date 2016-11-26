from flask import Flask, request, render_template, url_for,g, redirect, session, flash
from functools import wraps

import sqlite3

app = Flask(__name__)

@app.route('/form', methods=('GET', 'POST'))
def form():
    msg = None
    if request.method == 'POST':
      try:
        one = request.form['one']
        two = request.form['two']

        if (one and two):
           con = sqlite3.connect("db.db")
           cur = con.cursor()
           cur.execute("INSERT INTO tb1 (one,two) VALUES (?,?)",(one,two) )

           con.commit()
           msg = "Record successfully added"

        else:
           msg = "fill up everything man"

      except:
           msg="something went wrong"


    return render_template('form.html', msg=msg)

if __name__ == "__main__":
 app.run( host ='0.0.0.0', debug = False )

 #code from the stackoverflow to remove loading erors
 app.run(threaded=True)

