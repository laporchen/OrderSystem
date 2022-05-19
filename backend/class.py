

class User:
    def __init__(self, username, password, email, first_name, last_name,
                 is_admin=False):
        self.username = username
        self.__password = password
        self.__email = email
        self.__first_name = first_name
        self.__last_name = last_name
        self.is_admin = is_admin

    def __str__(self):
        return f"{self.username} {self.__email} {self.__first_name} {self.__last_name}"

    def __repr__(self):
        return f"{self.username} {self.__email} {self.__first_name} {self.__last_name}"

    def check_password(self, password):
        return self.__password == password


class Customer(User):
    def __init__(self, username, password, email, first_name, last_name):  # primary key is username
        super().__init__(username, password, email, first_name, last_name)
        self.favorite_restaurants = []
        self.orders = []


class Order:
    def __init__(self, id, restaurant, items, total_price, date):  # primary key is id + restaurant
        self.id = id
        self.restaurant = restaurant
        self.items = items
        self.total_price = total_price
        self.date = date
        self.order_status = "pending"
        self.rate = None


class Restaurant:
    def __init__(self, id, name, location, phone_numbers, description, menu):  # primary key is id
        self.name = name
        self.location = location
        self.phone_numbers = phone_numbers
        self.description = description
        self.menu = menu
        self.orders = []
        self.rating = None
        self.number_of_ratings = 0

    def __str__(self):
        return f"{self.name} {self.location} {self.description} {self.menu}"

    def __repr__(self):
        return f"{self.name} {self.location} {self.description} {self.menu}"


class Dish:
    def __init__(self, id, name, price, description, restaurant):  # primary key is id + restaurant
        self.name = name
        self.id = id
        self.price = price
        self.description = description
        self.restaurant = restaurant

    def __str__(self):
        return f"{self.name} {self.price} {self.description}"

    def __repr__(self):
        return f"{self.name} {self.price} {self.description}"


class Menu:
    def __init__(self, restaurant, dishes):  # primary key is restaurant
        self.id = id
        self.restaurant = restaurant
        self.dishes = dishes

    def __str__(self):
        return f"{self.restaurant} {self.dishes}"

    def __repr__(self):
        return f"{self.restaurant} {self.dishes}"
