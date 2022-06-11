-- DELIMITER //

--Some procedure are not test yet!

CREATE PROCEDURE insertCustomer(
    IN username VARCHAR(20),
    IN name VARCHAR(40),
    IN password VARCHAR(30)
)
    BEGIN
        INSERT INTO customer
        VALUES (username, name, password);
    END //
CREATE PROCEDURE insertMerchant(
    IN username VARCHAR(20),
    IN name VARCHAR(40),
    IN password VARCHAR(30)
)
    BEGIN
        INSERT INTO merchant
        VALUES (username, name, password);
    END //
CREATE PROCEDURE insertAdmin(
    IN username VARCHAR(20),
    IN name VARCHAR(40),
    IN password VARCHAR(30)
)
    BEGIN
        INSERT INTO admin
        VALUES (username, name, password);
    END //
CREATE PROCEDURE insertShop ( 
    IN mer_uname VARCHAR(40),
    IN name VARCHAR(40),
    IN openTime TIME,
    IN closeTime TIME,
    IN phone VARCHAR(20),
    IN email VARCHAR(40),
    IN city VARCHAR(40),
    IN district VARCHAR(40),
    IN road VARCHAR(40),
    IN lane VARCHAR(40),
    IN alley VARCHAR(40),
    IN no VARCHAR(40),
    IN floor TINYINT
)
    BEGIN
        DECLARE shopID INT DEFAULT 0;
        INSERT INTO shop
        VALUES (0, mer_uname, name, openTime, closeTime, phone, email, 0);
        SELECT ID INTO shopID
        FROM shop
        WHERE name = shop.name;
        INSERT INTO address
        VALUES (shopID, city, district, road, lane, alley, no, floor);
    END //
CREATE PROCEDURE insertItem (
    IN shop_id INT,
    IN name VARCHAR(40),
    IN pic BLOB,
    IN price INT
)
    BEGIN
        DECLARE maxID INT DEFAULT 0;
        SELECT MAX(ID) INTO maxID
        FROM item
        WHERE shop_id = item.shop_id;
        IF maxID IS NULL THEN
            SET maxID = 0;
        END IF;
        INSERT INTO item
        VALUES (maxID+1, shop_id, name, pic, price);
    END //
CREATE PROCEDURE insertFav (
    IN cus_uname VARCHAR(20),
    IN shop_id INT,
)
    BEGIN
        INSERT INTO
        VALUES (cus_uname, shop_id);
    END //
CREATE PROCEDURE insertOrder (
    IN cus_uname VARCHAR(20),
    IN total INT,
    OUT order_id INT,
)
    BEGIN
        DECLARE nowDateTime DATETIME;
        SET nowDateTime = NOW();
        INSERT INTO orders
        VALUES (0, cus_uname, "PENDING", total, nowDateTime, NULL, 0);
        SELECT ID INTO order_id
        FROM orders
        WHERE orders.cus_uname = cus_uname AND orders.orderTime = nowDateTime;
    END //
CREATE PROCEDURE setContainItem (
    IN order_id INT,
    IN item_id INT,
    IN shop_id INT,
    In number TINYINT,
)
    BEGIN
        INSERT INTO contain
        VALUES (order_id, item_id, shop_id, number);
    END //
CREATE PROCEDURE searchShop (
    IN cus_name VARCHAR(20),
    IN fav BOOL, IN name VARCHAR(40),
    IN lowerBound INT,
    In upperBound INT,
    IN rate INT
)
    BEGIN
        CREATE TEMPORARY TABLE ret (
            fav BOOL,
            shop_name VARCHAR(40) PRIMARY KEY,
            lowerBound INT UNSIGNED,
            upperBound INT UNSIGNED,
            rate TINYINT UNSIGNED
        );
        INSERT INTO ret(shop_name, lowerBound, upperBound, rate)
        SELECT name, MIN(price), MAX(price), rate
        FROM shop, 
        --TODO
    END //
CREATE TRIGGER updateAvgRate AFTER UPDATE ON orders
    FOR EACH ROW
    BEGIN
        IF NEW.rate > 0 THEN
            BEGIN
                DECLARE shopID INT DEFAULT 0;
                DECLARE avgRate INT DEFAULT 0;
                SELECT shop_id INTO shopID
                FROM contain
                WHERE NEW.ID = order_id;

                SELECT ROUND(AVG(rate)) INTO avgRate
                FROM contain, orders
                WHERE shopID = shop_id AND orders.ID = order_id AND rate > 0;

                UPDATE shop
                SET rate = avgRate
                WHERE ID = shopID;
            END;
        END IF; 
    END //

-- DELIMITER ;

--TODO
--checkUserExist