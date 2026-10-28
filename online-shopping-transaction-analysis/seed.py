# WARNING: demo seed resets all rows in these project tables. Use only in a development database.
from datetime import datetime,timedelta
from db import get_connection
products=[("Wireless Mouse","Electronics",599),("USB-C Cable","Electronics",249),("Notebook Set","Stationery",199),("Water Bottle","Home",399),("Bluetooth Speaker","Electronics",1499)]
orders=[
 (1,"UPI","Completed",[(1,1),(2,2)]),(2,"Card","Completed",[(5,1)],
 ),(3,"Cash on Delivery","Pending",[(3,3),(4,1)]),(4,"Wallet","Cancelled",[(1,1)]),
 (5,"UPI","Refunded",[(4,1)]),(6,"Net Banking","Completed",[(2,4),(3,2)]),
 (7,"Card","Processing",[(4,2),(1,1)])]
conn=get_connection(); cur=conn.cursor()
try:
 cur.execute("SET FOREIGN_KEY_CHECKS=0"); cur.execute("TRUNCATE order_items"); cur.execute("TRUNCATE orders"); cur.execute("TRUNCATE products"); cur.execute("SET FOREIGN_KEY_CHECKS=1")
 cur.executemany("INSERT INTO products(product_name,category,unit_price) VALUES(%s,%s,%s)",products)
 for days,pay,status,lines in orders:
  cur.execute("INSERT INTO orders(order_date,payment_method,order_status) VALUES(%s,%s,%s)",(datetime.now()-timedelta(days=days*4),pay,status)); oid=cur.lastrowid
  cur.executemany("INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES(%s,%s,%s,%s)",[(oid,p,q,products[p-1][2]) for p,q in lines])
 conn.commit(); print("Demo data inserted.")
except Exception: conn.rollback(); raise
finally: cur.close(); conn.close()
