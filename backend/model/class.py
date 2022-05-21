import datetime

class User:
    def __init__(self, username : str, password : str, email : str, first_name : str, last_name : str,
                 is_admin=False : bool):
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
    def __init__(self, username : str, password: str, email: str, first_name: str, last_name: str):  # primary key is username
        super().__init__(username, password, email, first_name, last_name)
        self.favorite_restaurants = []
        self.orders = []


class Owner(User):
    def __init__(self, username : str, password: str, email: str, first_name: str, last_name: str):  # primary key is username
        super().__init__(username, password, email, first_name, last_name)
        self.restaurant = None



class Order:
    def __init__(self, id : int, restaurant: str, items: str, total_price: str, date : datetime.date):  # primary key is id + restaurant
        self.id = id
        self.restaurant = restaurant
        self.items = items
        self.total_price = total_price
        self.date = date
        self.order_status = "pending"
        self.rate = None




class Restaurant:
    def __init__(self, id : int, name : str, address : str, phone_numbers : str, description : str, menu : Menu, open_time : datetime.time, close_time : datetime.time):  # primary key is id
        self.name = name
        self.adress= adress 
        self.phone_numbers = phone_numbers
        self.description = description
        self.menu = menu
        self.orders = []
        self.rating = None
        self.number_of_ratings = 0
        self.open_time = open_time
        self.close_time = close_time

    def __str__(self):
        return f"{self.name} {self.address} {self.description} {self.menu}"

    def __repr__(self):
        return f"{self.name} {self.adress} {self.description} {self.menu}"


class Item:
    def __init__(self, id : int, name : str, price : int, description : str, restaurant_id : int):  # primary key is id + restaurant
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
    def __init__(self, restaurant_id , dishes : Item[]):  # primary key is restaurant
        self.id = id
        self.restaurant = restaurant
        self.dishes = dishes

    def __str__(self):
        return f"{self.restaurant} {self.dishes}"

    def __repr__(self):
        return f"{self.restaurant} {self.dishes}"


class Address:
    def __init__(self, city : str,distinct : str, road : str, lane : str, alley : str, no : str, floor : str):
        self.city = city
        self.distinct = distinct
        self.road = road
        self.lane = lane
        self.alley = alley
        self.no = no
        self.floor = floor
    
    def __str__(self):
        return f"{self.city} {self.distinct} {self.road} {self.lane} {self.alley} {self.no} {self.floor}"

    def __repr__(self):
        return f"{self.city} {self.distinct} {self.road} {self.lane} {self.alley} {self.no} {self.floor}"

    def update(self, new_adress)