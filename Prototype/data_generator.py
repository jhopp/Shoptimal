import pandas as pd
import random as rnd
from math import sqrt

# defaults
PRICE_RANGE = (0.1, 20.0)
STOCK_RANGE = (1, 50)
LOC_RANGE = (0, 100)
NUM_ITEMS = 12
NUM_PRODUCTS = max(150, NUM_ITEMS) # at least as many products as items
MAX_ITEM_QUANT = 10
NUM_ROUTES = 10 # additional routes to be generated (aside from walking)
TRAVEL_COST_RANGE = (1, 8)

class DataGenerator:
    def __init__(self, shop_names_file: str, product_names_file:str, **params) -> None:
        self.shop_names = open('input/' + shop_names_file).read().split('\n') # add close
        self.product_names= open('input/' + product_names_file).read().split('\n') # add close
        self._price_range = params.get('price_range', PRICE_RANGE)
        self._stock_range = params.get('stock_range', STOCK_RANGE)
        self._loc_range = params.get('loc_range', LOC_RANGE)
        self.num_products = params.get('num_products', NUM_PRODUCTS)
        self.num_items = params.get('num_items', NUM_ITEMS)
        self._max_item_quant = params.get('max_item_quant', MAX_ITEM_QUANT)
        self._num_routes = params.get('num_routes', NUM_ROUTES)
        self._travel_cost_range = params.get('travel_cost_range', TRAVEL_COST_RANGE)

    def set_num_products(self, num_products):
        self.num_products = num_products

    def generate_product_data(self, items, all_items_available=False):
        """
        Generates and returns a DataFrame of product data.
        Format: (shop_name, product_name, price, stock)
        """
        shops = self.shop_names.copy()
        shops.remove("origin")
        product_data = []

        if all_items_available:
            # first ensure all items can be purchased somewhere
            for item in items:
                if item == "originsauce": continue
                shop = rnd.choice(shops)
                price = round(rnd.uniform(self._price_range[0], self._price_range[1]), 2)
                quantity = rnd.randrange(self._stock_range[0], self._stock_range[1])
                product_data.append((shop, item, price, quantity))

        # generate rest of products
        n = self.num_products - (self.num_items if all_items_available else 0)
        for _ in range(n):
            shop = rnd.choice(shops)
            item = rnd.choice(self.product_names)
            price = round(rnd.uniform(self._price_range[0], self._price_range[1]), 2)
            quantity = rnd.randrange(self._stock_range[0], self._stock_range[1])
            product_data.append((shop, item, price, quantity))
        
        product_data.append(("origin", "originsauce", 0.01, 1)) # add unique product to force origin visit
        return pd.DataFrame(product_data)
    
    def generate_shop_data(self):
        """
        Generates and returns a DataFrame of shop data.
        Format: (shop_name, (location_x, location_y))
        """
        shop_data = []
        for name in self.shop_names:
            x = round(rnd.uniform(self._loc_range[0], self._loc_range[1]), 4)
            y = round(rnd.uniform(self._loc_range[0], self._loc_range[1]), 4)
            shop_data.append((name, x, y))
        return pd.DataFrame(shop_data)
    
    def generate_route_data(self, shop_data):
        """
        Generates and returns a DataFrame of route data.
        Requires shop data to have been generated.
        Format: (shop_from_name, shop_to_name, time, cost)
        """
        route_data = []
        shops = shop_data.to_numpy()

        # generate routes by walking
        for shop_from in shops:
            for shop_to in shops:
                distance = round(sqrt(pow(shop_from[1] - shop_to[1], 2) + pow(shop_from[2] - shop_to[2], 2)),2)
                route_data.append((shop_from[0], shop_to[0], distance, 0))

        # generate additional routes
        for _ in range(self._num_routes):
            shop_from = rnd.choice(shops)
            shop_to = rnd.choice(shops)
            while shop_from[0] == shop_to[0]: # only generate route to other shop
                shop_to = rnd.choice(shops)

            distance = sqrt(pow(shop_from[1] - shop_to[1], 2) + pow(shop_from[2] - shop_to[2], 2))
            cost = round(rnd.uniform(self._travel_cost_range[0], self._travel_cost_range[1]),2)
            time = round(distance / cost, 2) # time decreased based on cost
            route_data.append((shop_from[0], shop_to[0], time, cost))
        
        return pd.DataFrame(route_data)

    def generate_item_data(self):
        """
        Generates and returns a Dataframe of item data.
        Format: (product_name, quantity)
        """
        items = rnd.sample(self.product_names, k=self.num_items)
        item_data = [(name, rnd.randint(1, self._max_item_quant)) for name in items]
        item_data.append(("originsauce", 1)) # add unique item to force origin visit
        return pd.DataFrame(item_data)

    def to_csv(self, all_items_available):
        """
        Generates data for products, shops, and items, and writes the data to csv files.
        """
        item_data = self.generate_item_data()
        item_data.to_csv("input/item_data.csv", header=False, index=False)
        product_data = self.generate_product_data(item_data.iloc[:,0], all_items_available)
        product_data.to_csv("input/product_data.csv", header=False, index=False)
        shop_data = self.generate_shop_data()
        shop_data.to_csv("input/shop_data.csv", header=False, index=False)
        route_data = self.generate_route_data(shop_data)
        route_data.to_csv("input/route_data.csv", header=False, index=False)
