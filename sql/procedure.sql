-- ALL PROCEDURES HAVE BEEN TESTED.

DELIMITER //

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
        VALUES (0, mer_uname, name, openTime, closeTime, phone, email, 3);
        SELECT MAX(ID) INTO shopID 
        FROM shop;
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
CREATE PROCEDURE deleteItem (
    IN shop_id INT,
    IN item_id INT
)
    BEGIN
        DELETE FROM item
        WHERE item.shop_id = shop_id AND item.ID = item_id;
    END //
CREATE PROCEDURE updateItem (
    IN shop_id INT,
    IN item_id INT,
    IN name VARCHAR(40),
    IN price INT
)
    BEGIN
        UPDATE item
        SET item.name = name, item.price = price
        WHERE item.shop_id = shop_id AND item.ID = item_id;
    END //
CREATE PROCEDURE updateFav (
    IN cus_uname VARCHAR(20),
    IN shop_id INT
)
    BEGIN
        IF EXISTS(
            SELECT cus_uname
            FROM favorite
            WHERE cus_uname = favorite.cus_uname AND shop_id = favorite.shop_id
        ) THEN
            DELETE FROM favorite
            WHERE cus_uname = favorite.cus_uname AND shop_id = favorite.shop_id;
        ELSE
            INSERT INTO favorite
            VALUES(cus_uname, shop_id);
        END IF;
    END //
CREATE PROCEDURE getOrderIdAsCart (
    IN cus_uname VARCHAR(20),
    IN shop_id INT,
    IN total INT
)
    BEGIN
        DECLARE order_id INT DEFAULT 0;
        SELECT ID INTO order_id
        FROM orders, contain
        WHERE ID = contain.order_id AND orders.cus_uname = cus_uname
            AND shop_id = contain.shop_id AND orders.state = "INCART";
        IF order_id = 0 THEN
            BEGIN
                INSERT INTO orders
                VALUES (0, cus_uname, "INCART", total, NULL, NULL, 0);
                SELECT MAX(ID) INTO order_id
                FROM orders
                WHERE cus_uname = orders.cus_uname;
            END;
        END IF;
        SELECT order_id;
    END //
CREATE PROCEDURE updateContainItem (
    IN order_id INT,
    IN shop_id INT,
    IN item_id INT,
    In number TINYINT
)
    BEGIN
        IF EXISTS(
            SELECT order_id
            FROM contain
            WHERE order_id = contain.order_id AND shop_id = contain.shop_id
                AND item_id = contain.item_id
        ) THEN
            IF number = 0 THEN
                DELETE FROM contain
                WHERE order_id = contain.order_id AND shop_id = contain.shop_id
                    AND item_id = contain.item_id;
            ELSE
                UPDATE contain
                SET contain.number = number
                WHERE order_id = contain.order_id AND shop_id = contain.shop_id
                    AND item_id = contain.item_id;
            END IF;
        ELSE
            IF number <> 0 THEN
            INSERT INTO contain
            VALUES (order_id, shop_id, item_id, number);
            END IF;
        END IF;
    END //
CREATE PROCEDURE placeOrder (IN order_id INT)
    BEGIN
        UPDATE orders
        SET state = "PENDING", orderTime = NOW()
        WHERE order_id = orders.ID;
    END //
CREATE PROCEDURE receiveOrder (IN order_id INT)
    BEGIN
        UPDATE orders
        SET state = "PREPARING"
        WHERE order_id = orders.ID;
    END //
CREATE PROCEDURE cancelOrder (IN order_id INT)
    BEGIN
        UPDATE orders
        SET state = "CANCELLED", finishTime = NOW()
        WHERE order_id = orders.ID;
    END //
CREATE PROCEDURE completeOrder (IN order_id INT)
    BEGIN
        UPDATE orders
        SET state = "COMPLETED", finishTime = NOW()
        WHERE order_id = orders.ID;
    END //
CREATE PROCEDURE rateOrder (IN order_id INT, IN rate TINYINT)
    BEGIN
        UPDATE orders
        SET orders.rate = rate
        WHERE order_id = orders.ID;
    END //
CREATE FUNCTION checkUsernameAvail (uname VARCHAR(20))
RETURNS BOOL
READS SQL DATA
    BEGIN
        DECLARE ret BOOL DEFAULT TRUE;
        SELECT NOT EXISTS(
            SELECT username
            FROM customer
            WHERE username = uname
            UNION
            SELECT username
            FROM merchant
            WHERE username = uname
            UNION 
            SELECT username
            FROM admin
            WHERE username = uname
        ) INTO ret;
        RETURN ret;
    END //
CREATE FUNCTION isMerchant (uname VARCHAR(20))
RETURNS BOOL
READS SQL DATA
    BEGIN
        DECLARE ret BOOL DEFAULT TRUE;
        SELECT EXISTS (
            SELECT username
            FROM merchant
            WHERE username = uname
        ) INTO ret;
        RETURN ret;
    END //
CREATE PROCEDURE getUser (IN uname VARCHAR(20))
    BEGIN
        SELECT *
        FROM customer
        WHERE uname = username
        UNION
        SELECT *
        FROM merchant
        WHERE uname = username;
    END //
CREATE PROCEDURE getShopByUname (IN mer_name VARCHAR(20))
    BEGIN
        SELECT *
        FROM shop
        WHERE mer_uname = shop.mer_name;
    END //
CREATE PROCEDURE getShopByID (IN ID INT)
    BEGIN
        SELECT *
        FROM shop
        WHERE shop.ID = ID;
    END //

CREATE PROCEDURE getUserCart (IN shop_id INT, IN cus_uname VARCHAR(20))
    BEGIN
        SELECT orders.ID, itemTmp.name,itemTmp.ID,
        itemTmp.price, contain.number, orders.total
        FROM orders, contain, (
            SELECT ID, name, price
            FROM item 
        ) AS itemTmp
        WHERE orders.state = "INCART" AND orders.cus_uname = cus_uname
            AND contain.shop_id = shop_id AND orders.ID = contain.order_id  
            AND contain.item_id = itemTmp.ID;
    END //
CREATE PROCEDURE getAllUserCart (IN cus_uname VARCHAR(20))
    BEGIN
        SELECT orders.ID, shopTmp.name,
        itemTmp.name, itemTmp.price, contain.number, orders.total
        FROM orders, contain, (
            SELECT ID, name
            FROM shop
        ) AS shopTmp, (
            SELECT ID, name, price
            FROM item
        ) AS itemTmp
        WHERE orders.state = "INCART" AND orders.cus_uname = cus_uname
            AND orders.ID = contain.order_id AND contain.shop_id = shopTmp.ID
            AND contain.item_id = itemTmp.ID;
    END //
CREATE PROCEDURE updatePwd(IN uname VARCHAR(20), IN pwd VARCHAR(30))
    BEGIN
        UPDATE customer
        SET password = pwd
        WHERE username = uname;
        UPDATE merchant
        SET password = pwd
        WHERE username = uname;
    END //
CREATE PROCEDURE getShopPendingOrders (IN shop_id INT)
    BEGIN
        SELECT orders.ID, orders.cus_uname, itemTmp.name,
        itemTmp.price, contain.number, orders.total
        FROM orders, contain, (
            SELECT ID, name, price
            FROM item
        ) AS itemTmp
        WHERE orders.state = "PENDING" AND contain.shop_id = shop_id
            AND orders.ID = contain.order_id AND contain.item_id = itemTmp.ID;
    END //
CREATE PROCEDURE getShopPreparingOrders (IN shop_id INT)
    BEGIN
        SELECT orders.ID, orders.cus_uname, itemTmp.name,
        itemTmp.price, contain.number, orders.total
        FROM orders, contain, (
            SELECT ID, name, price
            FROM item
        ) AS itemTmp
        WHERE orders.state = "PREPARING" AND contain.shop_id = shop_id
            AND orders.ID = contain.order_id AND contain.item_id = itemTmp.ID;
    END //
CREATE PROCEDURE getShopCompleteOrders (IN shop_id INT)
    BEGIN
        SELECT orders.ID, orders.cus_uname, itemTmp.name,
        itemTmp.price, contain.number, orders.total
        FROM orders, contain, (
            SELECT ID, name, price
            FROM item
        ) AS itemTmp
        WHERE orders.state = "COMPLETED" AND contain.shop_id = shop_id
            AND orders.ID = contain.order_id AND contain.item_id = itemTmp.ID;
    END //
CREATE PROCEDURE getUserOrders (IN cus_uname INT)
    BEGIN
        SELECT orders.ID, shopTmp.name,
        itemTmp.name, itemTmp.price, contain.number, orders.total
        FROM orders, contain, (
            SELECT ID, name
            FROM shop
        ) AS shopTmp, (
            SELECT ID, name, price
            FROM item
        ) AS itemTmp
        WHERE orders.state <> "INCART" AND orders.cus_uname = cus_uname
            AND orders.ID = contain.order_id AND contain.shop_id = shopTmp.ID
            AND contain.item_id = itemTmp.ID;
    END //
CREATE PROCEDURE updateShopInfo ( 
    IN shop_id INT,
    IN name VARCHAR(40),
    IN openTime TIME,
    IN closeTime TIME,
    IN phone VARCHAR(20),
    IN email VARCHAR(40)
)
    BEGIN
        UPDATE shop
        SET shop.name = name, shop.openTime = openTime,
        shop.closeTime = closeTime, shop.phone = phone,
        shop.email = email
        WHERE shop.ID = shop_id;
    END //
CREATE PROCEDURE updateShopAddress (
    IN shop_id INT,
    IN city VARCHAR(40),
    IN district VARCHAR(40),
    IN road VARCHAR(40),
    IN lane VARCHAR(40),
    IN alley VARCHAR(40),
    IN no VARCHAR(40),
    IN floor TINYINT
)
    BEGIN
        UPDATE address
        SET address.city = city, address.district = district,
        address.road = road, address.lane = lane,
        address.alley = alley, address.no = no, address.floor = floor
        WHERE address.shop_id = shop_id;
    END //
CREATE PROCEDURE getShopByFilter (
    IN cus_uname VARCHAR(20),
    IN fav BOOL,
    IN name VARCHAR(40),
    IN lowerBound INT,
    In upperBound INT,
    IN rate TINYINT
)
    BEGIN
        CREATE TEMPORARY TABLE ret (
            fav BOOL DEFAULT FALSE,
            shop_name VARCHAR(40) PRIMARY KEY,
            lowerBound INT UNSIGNED,
            upperBound INT UNSIGNED,
            rate TINYINT UNSIGNED
        );
        INSERT INTO ret(shop_name, lowerBound, upperBound, rate)
        SELECT shop.name, MIN(item.price), MAX(item.price), shop.rate
        FROM shop, item
        WHERE shop.ID = item.shop_id
            AND (shop.name LIKE CONCAT("%", name, "%") OR item.name LIKE CONCAT("%", name, "%"))
            AND shop.rate >= rate
        GROUP BY shop.name
        HAVING MIN(item.price) >= lowerBound AND MAX(item.price) <= upperBound;
        UPDATE ret
        SET fav = TRUE
        WHERE ret.shop_name IN (
            SELECT shop.name
            FROM shop, favorite
            WHERE favorite.cus_uname = cus_uname AND shop.ID = favorite.shop_id
        );
        IF fav THEN
            SELECT *
            FROM ret
            WHERE ret.fav;
        ELSE
            SELECT *
            FROM ret;
        END IF;
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
CREATE TRIGGER delEmptyCart AFTER DELETE ON contain
    FOR EACH ROW
    BEGIN
        IF NOT EXISTS (
            SELECT order_id
            FROM contain
            WHERE order_id = OLD.order_id
        ) THEN
            DELETE FROM orders
            WHERE ID = OLD.order_id;
        END IF;
    END //

DELIMITER ;