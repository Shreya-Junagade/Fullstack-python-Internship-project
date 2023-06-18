from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    con = sql.connect("db_web.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from users")
    data = cur.fetchall()
    return render_template("index.html", datas=data)


@app.route("/add_user", methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        uname = request.form['uname']
        contact = request.form['contact']
        con = sql.connect("db_web.db")
        cur = con.cursor()
        cur.execute("insert into users(UNAME,CONTACT) values (?,?)", (uname, contact))
        con.commit()
        flash('User Added', 'success')
        return redirect(url_for("index"))
    return render_template("add_user.html")


@app.route("/edit_user/<string:uid>", methods=['POST', 'GET'])
def edit_user(uid):
    if request.method == 'POST':
        uname = request.form['uname']
        contact = request.form['contact']
        con = sql.connect("db_web.db")
        cur = con.cursor()
        cur.execute("update users set UNAME=?,CONTACT=? where UID=?", (uname, contact, uid))
        con.commit()
        flash('User Updated', 'success')
        return redirect(url_for("index"))
    con = sql.connect("db_web.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from users where UID=?", (uid,))
    data = cur.fetchone()
    return render_template("edit_user.html", datas=data)


@app.route("/delete_user/<string:uid>", methods=['GET'])
def delete_user(uid):
    con = sql.connect("db_web.db")
    cur = con.cursor()
    cur.execute("delete from users where UID=?", (uid,))
    con.commit()
    flash('User Deleted', 'warning')
    return redirect(url_for("index"))
# Define the search route
@app.route("/search_user/<string:uid>", methods=['GET', 'POST'])

def search_user(uid):
    if request.method == 'POST':
        search_term = request.form['search_term']
        con = sql.connect("db_web.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select * from users where UNAME like ?", ('%' + search_term + '%',))
        data = cur.fetchall()
        return render_template("search.html", datas=data, search_term=search_term)
    return render_template("search.html")




if __name__ == '__main__':
    app.secret_key = 'admin123'
    app.run(debug=True)