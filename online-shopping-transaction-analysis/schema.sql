CREATE DATABASE IF NOT EXISTS shopping_analysis CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE shopping_analysis;
CREATE TABLE IF NOT EXISTS products (
 product_id INT AUTO_INCREMENT PRIMARY KEY, product_name VARCHAR(150) NOT NULL,
 category VARCHAR(100) NOT NULL, unit_price DECIMAL(10,2) NOT NULL CHECK(unit_price>=0)
);
CREATE TABLE IF NOT EXISTS orders (
 order_id INT AUTO_INCREMENT PRIMARY KEY, order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 payment_method ENUM('UPI','Card','Cash on Delivery','Net Banking','Wallet') NOT NULL,
 order_status ENUM('Pending','Processing','Completed','Cancelled','Refunded') NOT NULL DEFAULT 'Pending'
);
CREATE TABLE IF NOT EXISTS order_items (
 item_id INT AUTO_INCREMENT PRIMARY KEY, order_id INT NOT NULL, product_id INT NOT NULL,
 quantity INT NOT NULL CHECK(quantity>0), unit_price DECIMAL(10,2) NOT NULL CHECK(unit_price>=0),
 FOREIGN KEY(order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
 FOREIGN KEY(product_id) REFERENCES products(product_id)
);
CREATE INDEX idx_orders_date ON orders(order_date);
