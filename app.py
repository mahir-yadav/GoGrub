from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta, datetime
import random
from random import randint
from markupsafe import escape
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost", user="root", passwd="mahir@2004", database="gogrubDB")
app = Flask(__name__)
cursor = mydb.cursor()
app.permanent_session_lifetime = timedelta(days=3)
app.secret_key = "mahir"

admin_name = "9000000000"
admin_password = "gogrub"


@app.route("/", methods=["POST", "GET"])
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login():
    if(request.method == "GET"):
        return render_template("login.html", message=session.pop('message', ''))
    else:
        # print(request.form)
        phone_number = request.form["phn_no"]
        type = request.form["typeof"]
        password = request.form["pass"]
        q = ""
        # print(type)
        if(type == "customer"):
            q = f"SELECT * FROM customer WHERE customer_phone='{phone_number}';"
            cursor.execute(q)
            myresult = cursor.fetchall()
            if(len(myresult) == 1 and password == myresult[0][4]):
                session['logged_in'] = True
                session['user'] = myresult[0]

                return redirect(url_for("customer"))
            else:
                session['message'] = "Wrong Phone Number or Password! Try Again!"
                return redirect(url_for("login"))

        elif(type == "restaurant"):
            q = f"SELECT * FROM restaurant WHERE restaurant_phone='{phone_number}';"
            cursor.execute(q)
            myresult = cursor.fetchall()
            if(len(myresult) == 1 and password == myresult[0][4]):
                if(myresult[0][5] == 'Given'):
                    session['logged_in'] = True
                    session['user'] = myresult[0]
                    return redirect(url_for("restaurant"))
                else:
                    session['message'] = "Admin will go through your application and will notify in 1 to 2 days!!"
                    return redirect(url_for("login"))

            else:
                session['message'] = "Wrong Phone Number or Password! Try Again!"
                return redirect(url_for("login"))
        elif(type == "worker"):
            q = f"SELECT * FROM delivery_worker WHERE worker_phone='{phone_number}';"
            cursor.execute(q)
            myresult = cursor.fetchall()
            if(len(myresult) == 1 and password == myresult[0][3]):
                session['logged_in'] = True
                session['user'] = myresult[0]
                return redirect(url_for("delivery"))
            else:
                session['message'] = "Wrong Phone Number or Password! Try Again!"
                return redirect(url_for("login"))
        elif(type == "admin"):
            if(phone_number == admin_name and password == admin_password):
                session['logged_in'] = True
                return redirect(url_for("admin"))
            else:
                session['message'] = "Wrong Phone Number or Password! Try Again!"
                return redirect(url_for("login"))


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if(request.method == "GET"):
        return render_template("signup.html")
    else:
        # print(request.form)
        username = request.form["Name"]
        phone_number = request.form["phn_no"]
        type = request.form["typeof"]
        address = request.form["address"]
        password = request.form["pass"]

        if(type == "customer"):
            q = f"insert into customer(customer_name, customer_phone, customer_address, customer_password) values ('{username}', '{phone_number}','{address}','{password}');"
            cursor.execute(q)
            mydb.commit()

        if(type == "restaurant"):
            descr = request.form["description"]
            q = f"insert into restaurant(restaurant_name, restaurant_phone, restaurant_address, restaurant_password,access,restaurant_desc) values ('{username}', '{phone_number}','{address}','{password}','Not Given','{descr}');"
            cursor.execute(q)
            mydb.commit()
        if(type == "delivery_worker"):
            q = f"insert into delivery_worker(worker_name,worker_phone, work_address, worker_password) values ('{username}', '{phone_number}','{address}','{password}');"
            cursor.execute(q)
            mydb.commit()

        return redirect(url_for("login"))


@app.route("/customer", methods=["POST", "GET"])
def customer():
    if "user" in session:
        mycursor = mydb.cursor()
        mycursor.execute("select * from restaurant where access='Given';")
        myresult = mycursor.fetchall()
        mycursor.execute(
            f"select * from customer where customer_phone={session['user'][2]}")
        myresult2 = mycursor.fetchall()

        return render_template("customer.html", x=myresult, y=myresult2)
    else:
        return redirect(url_for("login"))


@app.route("/admin", methods=["POST", "GET"])
def admin():
    mycursor = mydb.cursor()
    q = f"select * from restaurant where access='Not Given';"
    mycursor.execute(q)
    myresult = mycursor.fetchall()
    return render_template("admin.html", x=myresult)


@app.route("/customer/food", methods=['POST'])
def fooditems():
    if "user" in session:
        id = request.form['itemId']
        mycursor = mydb.cursor()
        # print(id)
        mycursor.execute(
            f"SELECT food.*, restaurant.restaurant_name AS res_name FROM food JOIN restaurant ON food.res_id = restaurant.restaurant_id WHERE food.res_id = {id};")
        myresult = mycursor.fetchall()

        return render_template("customerfood.html", x=myresult)
    else:
        return redirect(url_for("login"))


@app.route("/customer/profile")
def custprof():
    if "user" in session:
        phone = session["user"][2]
        # print(phone)
        mycursor = mydb.cursor()
        mycursor.execute(
            f"Select * from Customer where customer_phone = '{phone}'")
        myresult = mycursor.fetchall()
        # print(myresult)
        return render_template("customerProfile.html", x=myresult)
    else:
        return redirect(url_for("login"))


@app.route("/customer/add_to_order", methods=['POST', 'GET'])
def add_to_order():

    # food_id = request.form.get("food_id")
    # food_name = request.form.get("food_name")
    # food_price= request.form.get("food_price")
    # res_id=request.form.get("res_id")
    # quantity = request.form.get("quantity")

    # # Adding item and quantity to the order stored in session
    # session["order"].append({"food_id": food_id, "food_name": food_name ,"food_price": food_price ,"quantity": quantity})
    # print(session['order'])
    # # Implement logic to check stock availability, etc.
    # mycursor = mydb.cursor()
    # mycursor.execute(f"SELECT food.*, restaurant.restaurant_name AS res_name FROM food JOIN restaurant ON food.res_id = restaurant.restaurant_id WHERE food.res_id = {res_id};")
    # myresult = mycursor.fetchall()
    # return render_template("customerfood.html", x = myresult) # Adjust as needed
    # # return redirect(url_for("customer"))
    if request.method == 'POST':
        food_id = escape(request.form.get("food_id"))
        food_name = escape(request.form.get("food_name"))
        food_price = escape(request.form.get("food_price"))
        res_id = escape(request.form.get("res_id"))
        quantity = escape(request.form.get("quantity"))

        mycursor = mydb.cursor()
        mycursor.execute(
            f"update food set stock=stock-'{quantity}' where food_id='{food_id}';")
        mydb.commit()
        # Initialize the order list in session if it doesn't exist
        if "order" not in session:
            session["order"] = []

        # Adding item and quantity to the order stored in session
        session["order"].append({"food_id": food_id, "food_name": food_name,
                                "food_price": food_price, "quantity": quantity, "res_id": res_id})

        # Mark the session as modified
        session.modified = True

        print(session['order'])

        # Retrieve the food items again for rendering
        mycursor.execute(
            f"SELECT food.*, restaurant.restaurant_name AS res_name FROM food JOIN restaurant ON food.res_id = restaurant.restaurant_id WHERE food.res_id = {res_id};")
        myresult = mycursor.fetchall()
        return render_template("customerfood.html", x=myresult)
    else:
        # If the method is not POST, redirect to the customer page or an appropriate page
        return redirect(url_for("customer"))


@app.route("/customer/place_order", methods=['GET', 'POST'])
def place_order():
    if "order" in session and "user" in session:
        user_id = session["user"][0]  # Assuming you store user info in session

        # Assuming you have a function to calculate the total amount
        # print(session)
        total_amount = calculate_total_amount(session["order"])
        payment_method = request.form.get("payment_method")
        # Placeholder: Insert into orders table
        order_id1 = insert_order_to_db(
            user_id, total_amount, payment_method, session['order'][0]['res_id'])

        # # Placeholder: Insert each item in session["order"] into order_items table
        # for item in session["order"]:
        #     insert_order_item_to_db(order_id, item["food_id"], item["quantity"])
        mycursor = mydb.cursor()

        for item in session['order']:
            foodid = item["food_id"]
            quan = item["quantity"]
            q = f"insert into contains(food_id1,order_id1,quantity) values('{foodid}','{order_id1}','{quan}');"
            mycursor.execute(q)
            mydb.commit()
        session.pop("order", None)  # Clear the order from session

        return render_template("placeorder.html", order_id=order_id1, amount=total_amount)
    else:
        # Handle case where there's no order in session or user is not logged in
        return redirect(url_for("login"))


def calculate_total_amount(order_items):
    # Implement calculation of total amount based on order_items
    total = 0
    for item in order_items:
        # Assume you have a function get_price_by_food_id to get the price of each item
        total += int(item["food_price"]) * int(item["quantity"])
    return total


def insert_order_to_db(user_id, total_amount, payment_method, res_id):
    # Implement insertion to your orders table and return the order ID
    order_status = "On The Way"
    order_date = datetime.now()
    mycursor = mydb.cursor()
    mycursor1 = mydb.cursor()
    mycursor1.execute(f"select worker_id from delivery_worker;")
    myresult = mycursor1.fetchall()

    worker_ids = [worker_id[0] for worker_id in myresult]

    # Select a random worker_id from the list
    random_worker_id = random.choice(worker_ids)

    mycursor.execute(
        f"insert into orders (order_status,order_time,mode_of_payment,amount,order_address,cust_id,work_id,res_id) values ('{order_status}','{order_date}','{payment_method}','{total_amount}','{session['user'][3]}','{session['user'][0]}','{random_worker_id}','{res_id}');")
    # myresult = mycursor.fetchall()
    mydb.commit()
    return mycursor.lastrowid


@app.route("/customer/orders")
def pastorders():
    if "user" in session:
        user = session["user"][0]
        mycursor = mydb.cursor()
        mycursor.execute(
            f"SELECT * from view_orders where cust_id = {user};")
        myresult = mycursor.fetchall()
        mycursor.execute(f"select * from customer where customer_id={user};")
        myres = mycursor.fetchall()

        return render_template("customerorders.html", x=myresult, y=myres)
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/restaurant", methods=["POST", "GET"])
def restaurant():
    if "user" in session:
        restaurantID = session.get("user")[0]
        q = f"SELECT * FROM Food WHERE res_id = '{restaurantID}';"
        mycursor = mydb.cursor()
        mycursor.execute(q)
        myresult = mycursor.fetchall()
        mycursor.execute(
            f"SELECT restaurant_name from restaurant WHERE restaurant_id='{restaurantID}';")
        myresult2 = mycursor.fetchall()
        myresult.append(session.get("user")[3])
        return render_template("restaurant.html", x=myresult, y=myresult2)
    else:
        return redirect(url_for("login"))


@app.route("/restaurant/orders", methods=["POST", "GET"])
def restaurant_orders():
    if "user" in session:
        restaurantID = session.get("user")[0]
        q = f"SELECT f.food_name, f.isveg, f.stock, o.order_time, o.cust_id, o.work_id,c.quantity,cust.customer_name,w.worker_name from orders o JOIN contains c on c.order_id1=o.order_id JOIN food f on c.food_id1=f.food_id JOIN customer cust on o.cust_id=cust.customer_id JOIN delivery_worker w on o.work_id=w.worker_id where o.res_id = '{restaurantID}' and o.order_status='On The Way';"
        mycursor = mydb.cursor()
        mycursor.execute(q)
        myresult = mycursor.fetchall()
        myresult.append(session.get("user")[3])
        mycursor.execute(
            f"SELECT restaurant_name from restaurant WHERE restaurant_id='{restaurantID}';")
        myresult2 = mycursor.fetchall()
        return render_template("restaurantOrders.html", x=myresult, y=myresult2)
    else:
        return redirect(url_for("login"))


@app.route("/restaurant/profile")
def restaurant_prof():
    if "user" in session:
        user = session["user"][0]
        q = f"SELECT * FROM restaurant WHERE restaurant_id = '{user}'"
        mycursor = mydb.cursor()
        mycursor.execute(q)
        myresult = mycursor.fetchall()
        return render_template("restaurantprofile.html", x=myresult)
    else:
        return redirect(url_for("login"))


@app.route("/restaurant/food", methods=['GET'])
def restaurant_food():

    return render_template("add_food.html")


@app.route("/restaurant/add_food", methods=['POST'])
def add_food():
    user = session['user'][0]

    food_name = request.form.get('foodName')
    price = request.form.get('foodPrice')
    is_veg = request.form.get('foodIsVeg')
    stock = request.form.get('foodstock')
    mycursor = mydb.cursor()
    q = f"insert into food(food_name,price,stock,isveg,res_id) values ('{food_name}','{price}','{stock}','{is_veg}','{user}');"
    mycursor.execute(q)
    mydb.commit()
    return redirect(url_for("restaurant"))


@app.route("/delivery", methods=["POST", "GET"])
def delivery():
    if "user" in session:
        user = session["user"][0]
        mycursor = mydb.cursor()
        mycursor.execute(
            f"Select o.order_id, r.restaurant_name, r.restaurant_address,c.customer_phone, c.customer_address,o.mode_of_payment, o.amount ,c.customer_name from orders o, restaurant r, customer c where c.customer_id = o.cust_id and r.restaurant_id = o.res_id and o.work_id = '{user}' and o.order_status='On The Way';")
        myresult = mycursor.fetchall()

        mycursor.execute(
            f"SELECT  worker_name FROM  delivery_worker where worker_id='{user}';")
        myresult3 = mycursor.fetchall()
        return render_template("delivery.html", x=myresult, z=myresult3)
    else:
        # print("a")
        return redirect(url_for("login"))


@app.route("/delivery/profile")
def delivery_profile():
    if "user" in session:
        user = session["user"][0]
        mycursor = mydb.cursor()
        mycursor.execute(
            f"Select * from delivery_worker where worker_id = '{user}'")
        myresult = mycursor.fetchall()
        return render_template("deliveryprofile.html", x=myresult)
    else:
        return redirect(url_for("login"))


@app.route('/mark-delivered', methods=['POST'])
def mark_delivered():
    if "user" in session:
        order_id = request.form.get('order_id')
        mycursor = mydb.cursor()
        q = f"update orders set order_status='Delivered' where order_id='{order_id}';"
        mycursor.execute(q)
        mydb.commit()
        # return render_template("delivery.html", x=myresult, z=myresult3)
        return redirect(url_for("delivery"))
    else:
        # print("a")
        return redirect(url_for("login"))


@app.route('/give-access', methods=['POST'])
def give_access():

    res_id = request.form.get('res_id')
    mycursor = mydb.cursor()
    q = f"update restaurant set access='Given' where restaurant_id='{res_id}';"
    mycursor.execute(q)
    mydb.commit()
    # return render_template("delivery.html", x=myresult, z=myresult3)
    return redirect(url_for("admin"))


@app.route('/worker_salary', methods=['GET'])
def worker_salary():
    print("aa")
    mycursor = mydb.cursor()
    q = f"select * from delivery_worker;"
    mycursor.execute(q)
    myresult = mycursor.fetchall()
    # return render_template("delivery.html", x=myresult, z=myresult3)
    return render_template("worker_salary.html", x=myresult)


@app.route('/update_salary', methods=['POST'])
def update_salary():
    # print("aa")
    worker_id = request.form.get('worker_id')
    new_salary = request.form['new_salary']
    mycursor = mydb.cursor()
    q = f"update delivery_worker set worker_salary='{new_salary}' where worker_id='{worker_id}';"
    mycursor.execute(q)
    mydb.commit()
    # return render_template("delivery.html", x=myresult, z=myresult3)
    return redirect(url_for("worker_salary"))


@app.route('/update_stock', methods=['POST'])
def update_stock():
    # print("aa")
    food_id = request.form.get('food_id')
    new_stock = request.form['new_stock']
    mycursor = mydb.cursor()
    q = f"update food set stock=stock+'{new_stock}' where food_id='{food_id}';"
    mycursor.execute(q)
    mydb.commit()
    # return render_template("delivery.html", x=myresult, z=myresult3)
    return redirect(url_for("restaurant"))


def redeem_customer_points(customer_id):
    pass


def get_customer_points(customer_id):
    mycursor = mydb.cursor()
    query = f"SELECT loyalty_points FROM customer WHERE customer_id='{customer_id}'"
    mycursor.execute(query)
    # fetchone() returns a tuple, we need the first element
    customer_points = mycursor.fetchone()[0]
    return customer_points


def redeem_customer_points(customer_id, points_to_redeem):
    mycursor = mydb.cursor()
    query = f"SELECT loyalty_points FROM customer WHERE customer_id='{customer_id}'"
    mycursor.execute(query)
    # fetchone() returns a tuple, we need the first element
    customer_points = mycursor.fetchone()[0]

    if customer_points >= points_to_redeem:
        update_query = f"UPDATE customer SET loyalty_points = loyalty_points - {points_to_redeem} WHERE customer_id='{customer_id}'"
        mycursor.execute(update_query)
        mydb.commit()
        return True
    else:
        return False


@app.route('/customer/points')
def customer_points():

    customer_id = session['user'][0]
    customer_points = get_customer_points(customer_id)
    return render_template('redeem.html', points=customer_points)


@app.route('/customer/redeem_points', methods=['GET', 'POST'])
def redeem_points():

    customer_id = session['user'][0]

    if request.method == 'POST':
        points_to_redeem = int(request.form['pointsToRedeem'])
        success = redeem_customer_points(customer_id, points_to_redeem)

        if success:
            flash(
                f"Successfully redeemed {points_to_redeem/100} Rupees!", 'success')
        else:
            flash("Sorry, you don't have enough points to redeem.", 'error')

        return redirect(url_for('customer_points'))

    # If method is GET, render the redeem.html template
    customer_points = get_customer_points(customer_id)
    return render_template('redeem.html', points=customer_points)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
