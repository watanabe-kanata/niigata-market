from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = "niigata-secret"

#商品データ
products = [
    {
        "id": 0,
        "name": "コシヒカリ",
        "price": 3980,
        "description": "新潟を代表するブランド米",
        "image": "kosihikari.jpeg",
        "category": "rice"
    },
    {
        "id": 1,
        "name": "新之助",
        "price": 4280,
        "description": "大粒で甘みのある人気品種",
        "image": "sinnosuke.jpeg",
        "category": "rice"
    },
    {
        "id": 2,
        "name": "コシイブキ",
        "price": 3580,
        "description": "毎日の食卓にピッタリ",
        "image": "kosiibuki.jpeg",
        "category": "rice"
    },
    {
        "id": 3,
        "name": "八海山",
        "price": 2800,
        "description": "新潟を代表する淡麗辛口の日本酒",
        "image": "hakkaisan.jpeg",
        "category": "sake"
    },
    {
        "id": 4,
        "name": "久保田",
        "price": 3200,
        "description": "全国的に人気の新潟銘酒",
        "image": "kubota.jpeg",
        "category": "sake"
    },
    {
        "id": 5,
        "name": "ばかうけ",
        "price": 250,
        "description": "新潟生まれの定番せんべい",
        "image": "bakauke.jpeg",
        "category": "snack"
    },
    {
        "id": 6,
        "name": "柿の種",
        "price": 300,
        "description": "新潟名物のピリ辛おつまみ 6袋詰",
        "image": "kakinotane.jpeg",
        "category": "snack"
    }


]

#トップページ
@app.route("/")
def home():

    rice_products = [p for p in products if p["category"] == "rice"]
    sake_products = [p for p in products if p["category"] == "sake"]
    snack_products = [p for p in products if p["category"] == "snack"]
    return render_template(
        "index.html",
        rice_products=rice_products,
        sake_products=sake_products,
        snack_products=snack_products
    )

#商品詳細
@app.route("/detail/<int:product_id>")
def detail(product_id):
    product = products[product_id]
    return render_template(
        "detail.html",
        product=product,
        product_id=product_id)

#カート機能
@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    quantity = int(request.form["quantity"])

    if "cart" not in session:
        session["cart"] = []

    session["cart"].append({
        "product_id": product_id,
        "quantity": quantity
    })

    session.modified = True

    return redirect("/cart")

#カート
@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])

    items = []
    total = 0

    for item in cart_items:
        product = products[item["product_id"]]
        quantity = item["quantity"]
        subtotal = product["price"] * quantity

        items.append({
            "name": product["name"],
            "price": product["price"],
            "quantity": quantity,
            "subtotal": subtotal,
            "image": product["image"]
        })

        total += subtotal

    return render_template(
        "cart.html",
        items=items,
        total=total
    )

#削除
@app.route("/remove_from_cart/<int:item_index>", methods=["POST"])
def remove_from_cart(item_index):
    if "cart" in session:
        session["cart"].pop(item_index)
        session.modified = True

    return redirect("/cart")
#購入確認
@app.route("/checkout")
def checkout():
    cart_items = session.get("cart", [])

    items = []
    total = 0

    for item in cart_items:
        product = products[item["product_id"]]
        quantity = item["quantity"]
        subtotal = product["price"] * quantity

        items.append({
            "name": product["name"],
            "quantity": quantity,
            "subtotal": subtotal,
            "image": product["image"]
        })
        total += subtotal

    return render_template(
        "checkout.html",
        items=items,
        total=total
    )

#購入完了
@app.route("/complete", methods=["POST"])
def complete():
    session.pop("cart", None)
    return render_template("complete.html")

if __name__ == "__main__":
    app.run(debug=True)