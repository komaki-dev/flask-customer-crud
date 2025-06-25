from flask import Flask,request,render_template,redirect,url_for
import sqlite3

app = Flask(__name__)

@app.route("/" ,methods=["GET","POST"])
def index():

    con = sqlite3.connect("CRM.db")
    date_all = con.execute("SELECT * FROM customers WHERE deleted = 0").fetchall()
    con.close()

    customers = []
    for row in date_all:
        customers.append({"id":row[0],
                        "name":row[1],
                        "email":row[2],
                        "phone":row[3],
                        "note": row[4],
                        "deleted":row[5]})

    return render_template("main.html", customers=customers)

@app.route("/form", methods=["GET","POST"])
def form():
    if request.method =="POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        note = request.form["note"]

        con = sqlite3.connect("CRM.db")
        con.execute("INSERT INTO customers (name, email, phone, note) VALUES (?,?,?,?)",(name, email, phone, note))
        con.commit()
        con.close()

        return redirect(url_for('index'))
    return render_template("form.html")

@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):
    if request.method =="POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        note = request.form["note"]


        con = sqlite3.connect("CRM.db")
        c = con.cursor()
        c.execute("UPDATE customers \
                  SET name=?,\
                   email=?,\
                   phone=?,\
                   note=? WHERE id=?",(name, email, phone, note,id))
        con.commit()
        con.close()

        return redirect(url_for("index"))
    
    con = sqlite3.connect("CRM.db")
    c = con.cursor()
    row = con.execute("SELECT * FROM customers WHERE id =?",(id,)).fetchone()
    con.close()

    customer =({"id":row[0], "name":row[1], "email":row[2], "phone":row[3], "note": row[4]})

    return render_template("edit.html", customer=customer)


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    if request.method =="POST":
        con = sqlite3.connect("CRM.db")
        c = con.cursor()
        c.execute("UPDATE customers SET deleted =? WHERE id =?",(1, id))
        con.commit()
        con.close()

    return redirect(url_for('index'))

@app.route("/deleted")
def deleted():
    con = sqlite3.connect("CRM.db")
    deleted = con.execute("SELECT * FROM customers WHERE deleted = 1").fetchall()
    con.close()

    del_list =[]
    for row in deleted:
        del_list.append({"id":row[0],
                         "name":row[1],
                          "email":row[2],
                          "phone":row[3],
                          "note": row[4],
                          "deleted":row[5]})
    return render_template("deleted.html", del_list=del_list)

@app.route("/restore/<int:id>",methods=["POST"])
def restore(id):
    con = sqlite3.connect("CRM.db")
    c = con.cursor()
    c.execute("UPDATE customers SET deleted =? WHERE id =?",(0, id))
    con.commit()
    con.close()

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
