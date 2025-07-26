from flask import Flask,request,jsonify
import pandas as pd
import os
app=Flask(__name__)
data_path = os.path.join(os.path.dirname(__file__),"data")
orders=pd.read_csv(os.path.join(data_path,"orders.csv"))
products=pd.read_csv(os.path.join(data_path,"products.csv"))
inventory=pd.read_csv(os.path.join(data_path,"inventory.csv"))
@app.route("/")
def home():
    return"E-commerce Chatbot Backend is Running!"

@app.route("/top-products",methods=["GET"])
def top_products():
    top=orders["product_id"].value_counts(),head(5).index.tolist()
    top_names=products[products["product_id"].isin(top)]["product_name"].tolist()
    return jsonify({"top_5_products":top_names})
@app.route("/order-status/<order_id>",methods=["GET"])
def order_status(order_id):
    order_row=orders[orders["order_id"]==int(order_id)]
    if order_row.empty:
        return jsonify({"status":"order not found"}),404
    return jsonify(order_row.to_dict(orient="records")[0])
@app.route("/stock/<product_name>",methods=["GET"])
def product_stock(product_name):
    row=inventory[inventory["product_name"].str.lower()==product_name.lower()]
    if row.empty:
        return jsonify({"stock":"product not found"}),404
    return jsonify({"product":product_name,"stock_left":int(row["stock"].values[0])})
if __name__ == "__main__":
    app.run(debug=True)
