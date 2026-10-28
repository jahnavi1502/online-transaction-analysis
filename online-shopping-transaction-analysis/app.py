from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from config import Config
from db import fetch_all, get_connection, execute
from analytics import metrics, reports, order_frame
import os
app=Flask(__name__); app.config.from_object(Config)
PAYMENTS=["UPI","Card","Cash on Delivery","Net Banking","Wallet"]
STATUSES=["Pending","Processing","Completed","Cancelled","Refunded"]

@app.template_filter("money")
def money(v): return f"₹{float(v or 0):,.2f}"

@app.route("/")
def home():
    try:
        m=metrics()
        recent=fetch_all("""SELECT o.order_id,o.order_date,o.payment_method,o.order_status,
          COALESCE(SUM(i.quantity*i.unit_price),0) total FROM orders o LEFT JOIN order_items i ON i.order_id=o.order_id
          GROUP BY o.order_id,o.order_date,o.payment_method,o.order_status ORDER BY o.order_date DESC LIMIT 8""")
        return render_template("index.html",m=m,recent=recent)
    except Exception as e:
        return render_template("index.html",m=None,recent=[],error=str(e))

@app.route("/products")
def products():
    return render_template("products.html",products=fetch_all("SELECT * FROM products ORDER BY product_name"))

@app.route("/products/new",methods=["GET","POST"])
def product_new():
    if request.method=="POST":
        name=request.form.get("name","").strip(); cat=request.form.get("category","").strip()
        try:
            price=float(request.form.get("price",""))
            if not name or not cat or price<0: raise ValueError()
            execute("INSERT INTO products(product_name,category,unit_price) VALUES(%s,%s,%s)",(name,cat,price))
            flash("Product added."); return redirect(url_for("products"))
        except ValueError: flash("Enter valid product details.")
    return render_template("product_form.html")

@app.route("/orders")
def orders():
    rows=fetch_all("""SELECT o.order_id,o.order_date,o.payment_method,o.order_status,
      COALESCE(SUM(i.quantity*i.unit_price),0) total,COALESCE(SUM(i.quantity),0) units
      FROM orders o LEFT JOIN order_items i ON i.order_id=o.order_id
      GROUP BY o.order_id,o.order_date,o.payment_method,o.order_status ORDER BY o.order_date DESC""")
    return render_template("orders.html",orders=rows)

@app.route("/orders/new",methods=["GET","POST"])
def order_new():
    products=fetch_all("SELECT * FROM products ORDER BY product_name")
    if request.method=="POST":
        payment=request.form.get("payment"); status=request.form.get("status")
        try:
            lines=[]
            for pid,qty in zip(request.form.getlist("product_id"),request.form.getlist("quantity")):
                if pid and qty:
                    q=int(qty)
                    if q<1: raise ValueError()
                    p=fetch_all("SELECT product_id,unit_price FROM products WHERE product_id=%s",(int(pid),))
                    if p: lines.append((int(pid),q,float(p[0]["unit_price"])))
            if payment not in PAYMENTS or status not in STATUSES or not lines: raise ValueError()
            date=request.form.get("order_date") or datetime.now().strftime("%Y-%m-%dT%H:%M")
            dt=datetime.strptime(date,"%Y-%m-%dT%H:%M")
            conn=get_connection(); cur=conn.cursor()
            try:
                cur.execute("INSERT INTO orders(order_date,payment_method,order_status) VALUES(%s,%s,%s)",(dt,payment,status))
                oid=cur.lastrowid
                cur.executemany("INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES(%s,%s,%s,%s)",[(oid,*x) for x in lines])
                conn.commit()
            except Exception: conn.rollback(); raise
            finally: cur.close(); conn.close()
            flash(f"Order #{oid} saved."); return redirect(url_for("orders"))
        except (ValueError,TypeError): flash("Select payment/status and add product lines with positive quantities.")
    return render_template("order_form.html",products=products,payments=PAYMENTS,statuses=STATUSES,now=datetime.now().strftime("%Y-%m-%dT%H:%M"))

@app.route("/reports")
def report_page():
    status,payment,monthly,products=reports()
    return render_template("reports.html",status=status,payment=payment,monthly=monthly,products=products)

@app.route("/export/orders.csv")
def export_csv():
    df=order_frame(); path="static/order_summary.csv"; df.to_csv(path,index=False)
    return send_file(path,as_attachment=True,download_name="order_summary.csv")

if __name__=="__main__": app.run(debug=True,host="127.0.0.1",port=5000)
