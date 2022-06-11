CREATE TABLE customer (
    username VARCHAR(20) PRIMARY KEY,
    name VARCHAR(40) NOT NULL,
    password VARCHAR(30) NOT NULL
);
CREATE TABLE merchant (
    username VARCHAR(20) PRIMARY KEY,
    name VARCHAR(40) NOT NULL,
    password VARCHAR(30) NOT NULL
);
CREATE TABLE admin (
    username VARCHAR(20) PRIMARY KEY,
    name VARCHAR(40) NOT NULL,
    password VARCHAR(30) NOT NULL
);
/* insert into admin values ('admin', 'admin', 'admin'); */
CREATE TABLE shop (
    ID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    mer_uname VARCHAR(40) NOT NULL,
    name VARCHAR(40) NOT NULL UNIQUE,
    openTime TIME NOT NULL,
    closeTime TIME NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(40),
    rate TINYINT UNSIGNED,
    FOREIGN KEY (mer_uname) REFERENCES merchant(username)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
CREATE TABLE address (
    shop_id INT UNSIGNED PRIMARY KEY,
    city VARCHAR(40) NOT NULL,
    district VARCHAR(40) NOT NULL,
    road VARCHAR(40) NOT NULL,
    lane VARCHAR(40),
    alley VARCHAR(40),
    no VARCHAR(40) NOT NULL,
    floor TINYINT,
    FOREIGN KEY (shop_id) REFERENCES shop(ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
CREATE TABLE favorite (
    cus_name VARCHAR(20),
    shop_id INT UNSIGNED,
    PRIMARY KEY (cus_name, shop_id),
    FOREIGN KEY (cus_name) REFERENCES customer(username)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (shop_id) REFERENCES shop(ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
CREATE TABLE orders (
    ID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    cus_uname VARCHAR(20) NOT NULL,
    state VARCHAR(10) NOT NULL,
    total INT UNSIGNED NOT NULL,
    orderTime DATETIME,
    finishTime DATETIME,
    rate TINYINT UNSIGNED,
    FOREIGN KEY (cus_uname) REFERENCES customer(username)
        ON UPDATE CASCADE
);
CREATE TABLE item (
    ID INT UNSIGNED,
    shop_id INT UNSIGNED,
    name VARCHAR(40) NOT NULL,
    picture BLOB,
    price INT UNSIGNED NOT NULL,
    PRIMARY KEY(ID, shop_id),
    FOREIGN KEY (shop_id) REFERENCES shop(ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
CREATE TABLE contain (
    order_id INT UNSIGNED,
    item_id INT UNSIGNED,
    shop_id INT UNSIGNED,
    number TINYINT UNSIGNED,
    PRIMARY KEY(order_id, item_id, shop_id),
    FOREIGN KEY (order_id) REFERENCES orders(ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (item_id, shop_id) REFERENCES item(ID, shop_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);