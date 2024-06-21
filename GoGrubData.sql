-- create database gogrubDB;
USE gogrubDB;
CREATE TABLE customer (
    customer_id INT auto_increment PRIMARY KEY NOT NULL,
    customer_name varchar(255) NOT NULL,
    customer_phone varchar(10) NOT NULL,
    customer_address TEXT NOT NULL,
    customer_password varchar(255) NOT NULL
);
CREATE TABLE restaurant (
    restaurant_id INT auto_increment PRIMARY KEY NOT NULL,
    restaurant_name varchar(255) NOT NULL,
    restaurant_phone varchar(10) NOT NULL,
    restaurant_address TEXT NOT NULL,
    restaurant_password varchar(255) NOT NULL
);
CREATE TABLE orders (
    order_id INT auto_increment PRIMARY KEY NOT NULL,
    order_status bool NOT NULL,
    order_time datetime NOT NULL,
    mode_of_payment varchar(255) NOT NULL,
    amount INT NOT NULL,
    order_address text NOT NULL
);
CREATE TABLE food (
    food_id INT auto_increment PRIMARY KEY NOT NULL,
    food_name varchar(255) NOT NULL,
	price int NOT NULL,
    stock int NOT NULL,
    isveg bool NOT NULL
);
CREATE TABLE delivery_worker (
    worker_id INT auto_increment PRIMARY KEY NOT NULL,
    worker_name varchar(255) NOT NULL,
	worker_phone varchar(10) NOT NULL,
    worker_password varchar(255) NOT NULL,
    worker_salary int NOT NULL
);
alter table restaurant 
add column access varchar(255);

ALTER TABLE food
ADD CONSTRAINT fk_res_id
FOREIGN KEY (res_id) REFERENCES restaurant(restaurant_id);

ALTER TABLE food
ADD COLUMN res_id int;


ALTER TABLE orders
ADD COLUMN cust_id int;

ALTER TABLE orders
ADD COLUMN work_id int;

ALTER TABLE orders
ADD CONSTRAINT fk_cust_id
FOREIGN KEY (cust_id) REFERENCES customer(customer_id);

ALTER TABLE orders
ADD CONSTRAINT fk_work_id
FOREIGN KEY (work_id) REFERENCES delivery_worker(worker_id);

ALTER TABLE delivery_worker
ADD COLUMN work_address varchar(255);

ALTER TABLE delivery_worker
ADD COLUMN work_address varchar(255);

ALTER TABLE delivery_worker
drop COLUMN work_address;
Alter table delivery_worker
drop column worker_salary;
Alter table delivery_worker
add column worker_salary int;

Alter table restaurant
add column res_desc varchar(255);

alter table restaurant
drop column res_desc ;

update restaurant set restaurant_desc="we are the best burger company" where restaurant_name="burger club";

desc restaurant;

SELECT food.*, restaurant.restaurant_name AS res_name
FROM food
JOIN restaurant ON food.res_id = restaurant.restaurant_id
WHERE food.res_id = 1;

ALTER TABLE orders
ADD CONSTRAINT fk_res_id
FOREIGN KEY (res_id) REFERENCES restaurant(restaurant_id);
Use gogrubDB;
alter table orders modify column order_status varchar(255);

create table contains(
	food_id1 int,
    order_id1 int,
    quantity int
);
alter table contains
add constraint fk_order_id
foreign key (order_id1) references orders(order_id);

alter table customer add column loyalty_points int default 0;





DELIMITER //
CREATE TRIGGER award_loyalty_points
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    DECLARE points_to_award INT;

    -- Calculate points based on the order amount (e.g., 1 point per $10)
    SET points_to_award = NEW.amount DIV 10;

    -- Update the customer's loyalty points
    UPDATE customer
    SET loyalty_points = loyalty_points + points_to_award
    WHERE customer_id = NEW.cust_id;
END //

DELIMITER ;





DELIMITER //

CREATE TRIGGER update_deliveries_count_and_increment_salary
AFTER UPDATE ON orders
FOR EACH ROW
BEGIN
    -- Check if the order status is updated to 'Delivered'
    IF NEW.order_status = 'Delivered' THEN
        -- Update the deliveries count for the worker
        UPDATE delivery_worker
        SET deliveries_count = deliveries_count + 1
        WHERE worker_id = NEW.work_id;

        -- Check if the worker has completed 100 deliveries
        IF (SELECT deliveries_count FROM delivery_worker WHERE worker_id = NEW.work_id) >= 100 THEN
            -- Increment the worker's salary by 1000 and reset the deliveries count
            UPDATE delivery_worker
            SET worker_salary = worker_salary + 1000,
                deliveries_count = 0
            WHERE worker_id = NEW.work_id;
        END IF;
    END IF;
END //

DELIMITER ;


CREATE VIEW view_orders AS
SELECT o.order_id, o.order_status, o.order_time, o.mode_of_payment, o.amount, o.order_address, 
       o.cust_id, c.customer_name, o.work_id, w.worker_name, o.res_id, r.restaurant_name
FROM orders o
JOIN customer c ON o.cust_id = c.customer_id
JOIN delivery_worker w ON o.work_id = w.worker_id
JOIN restaurant r ON o.res_id = r.restaurant_id;

