from flask import Flask, request, render_template, url_for,g, redirect, session, flash

import sqlite3

app = Flask(__name__)

@app.route('/')
def root():
    connection = sqlite3.connect("mydatabase.db")
    connection.row_factory = sqlite3.Row

    rows = connection.cursor().execute("SELECT * FROM seasons").fetchall()
    
    return render_template("index.html", rows=rows)



#templates for errors 404, 500
	
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



	

@app.route('/trees')
@app.route('/trees/<name>')
def trees(name):
	sql = ('SELECT * FROM trees WHERE page_name = ?')
	connection = sqlite3.connect("mydatabase.db")
	connection.row_factory = sqlite3.Row     		
	trees = connection.cursor().execute(sql,[name]).fetchall()
    
	sql2 = ('SELECT * FROM seasons')
	connection = sqlite3.connect("mydatabase.db")
	connection.row_factory = sqlite3.Row     		
	all = connection.cursor().execute(sql2).fetchall()
    
	return render_template('trees.html',  name=name, all=all, trees=trees)  
	connection.close()
    
@app.route('/season')
@app.route('/season/<name>')
def season(name):
	sql = ('SELECT * FROM seasons WHERE page_name = ?')
	connection = sqlite3.connect("mydatabase.db")
	connection.row_factory = sqlite3.Row     		
	rows = connection.cursor().execute(sql,[name]).fetchall()
    
	sql2 = ('SELECT * FROM trees WHERE season = ?')
	connection = sqlite3.connect("mydatabase.db")
	connection.row_factory = sqlite3.Row     		
	trees = connection.cursor().execute(sql2,[name]).fetchall()
   	all = connection.cursor().execute("SELECT * FROM seasons").fetchall()
    
	return render_template('season.html', rows = rows, name=name, all=all, trees=trees)  
    
	
	
@app.route('/page')
def in0():
	return render_template('in0.html')  
	
@app.route("/page/celts")
def in1():
	sql2 = ('SELECT * FROM seasons')
	connection = sqlite3.connect("mydatabase.db")
	connection.row_factory = sqlite3.Row     		
	mmm = connection.cursor().execute(sql2).fetchall()
	connection.close()
	return render_template('in1.html',  mmm=mmm)
    
	
	
@app.route("/page/sacred")
def in2():
	sql2 = ('SELECT * FROM seasons')
	connection = sqlite3.connect("mydatabase.db")
	connection.row_factory = sqlite3.Row     		
	mmm = connection.cursor().execute(sql2).fetchall()
	
	sql1 = ('SELECT * FROM trees')
	connection = sqlite3.connect("mydatabase.db")
	connection.row_factory = sqlite3.Row     		
	tree_list = connection.cursor().execute(sql1).fetchall()
	
	
	return render_template('in2.html',  mmm=mmm, tree_list=tree_list)
	connection.close()
	


if __name__ == "__main__":
 app.run( host ='0.0.0.0', debug = False )
 
 #code from the stackoverflow to remove loading erors
 app.run(threaded=True)

