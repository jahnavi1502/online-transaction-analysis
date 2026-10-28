import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from db import fetch_all
os.makedirs("static/generated", exist_ok=True)

def order_frame():
    rows=fetch_all("""
      SELECT o.order_id,o.order_date,o.payment_method,o.order_status,
             COALESCE(SUM(i.quantity*i.unit_price),0) order_total,
             COALESCE(SUM(i.quantity),0) units
      FROM orders o LEFT JOIN order_items i ON i.order_id=o.order_id
      GROUP BY o.order_id,o.order_date,o.payment_method,o.order_status
      ORDER BY o.order_date
    """)
    df=pd.DataFrame(rows)
    if not df.empty:
        df["order_date"]=pd.to_datetime(df["order_date"])
        df["order_total"]=pd.to_numeric(df["order_total"])
        df["units"]=pd.to_numeric(df["units"]).fillna(0)
    return df

def metrics():
    df=order_frame()
    if df.empty: return dict(total=0,completed=0,sales=0,average=0,units=0)
    done=df[df.order_status=="Completed"]
    values=done.order_total.to_numpy(dtype=float)
    return dict(total=len(df),completed=len(done),sales=float(done.order_total.sum()),
      average=float(np.mean(values)) if len(values) else 0,units=int(done.units.sum()))

def chart(title, labels, values, filename):
    plt.figure(figsize=(8,4))
    if labels: plt.bar(labels,values); plt.xticks(rotation=30,ha="right")
    else: plt.text(.5,.5,"No data yet",ha="center"); plt.xticks([]); plt.yticks([])
    plt.title(title); plt.tight_layout(); plt.savefig("static/generated/"+filename); plt.close()

def reports():
    df=order_frame()
    status={} if df.empty else df.order_status.value_counts().to_dict()
    payment={} if df.empty else df.payment_method.value_counts().to_dict()
    monthly=[] if df.empty else [{"label":str(k),"value":int(v)} for k,v in df.assign(month=df.order_date.dt.to_period("M").astype(str)).groupby("month").size().items()]
    chart("Order status distribution",list(status),list(status.values()),"status.png")
    chart("Payment method distribution",list(payment),list(payment.values()),"payment.png")
    chart("Monthly order volume",[x["label"] for x in monthly],[x["value"] for x in monthly],"monthly.png")
    products=fetch_all("""
      SELECT p.product_name,COALESCE(SUM(CASE WHEN o.order_status='Completed' THEN i.quantity ELSE 0 END),0) units
      FROM products p LEFT JOIN order_items i ON i.product_id=p.product_id
      LEFT JOIN orders o ON o.order_id=i.order_id
      GROUP BY p.product_id,p.product_name ORDER BY units DESC
    """)
    chart("Product units sold (completed orders)",[p["product_name"] for p in products[:10]],[int(p["units"]) for p in products[:10]],"products.png")
    return status,payment,monthly,products
