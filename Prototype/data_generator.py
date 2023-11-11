import pandas as pd
import random as rnd

# defaults
PRICE_RANGE = (0.1, 20.0)
STOCK_RANGE = (1, 50)
LOC_RANGE = (0, 100)
NUM_PRODUCTS = 100
NUM_ITEMS = 12
MAX_ITEM_QUANT = 10

class DataGenerator:
    def __init__(self, shop_names_file: str, product_names_file:str, **params) -> None:
        self.shop_names = open(shop_names_file).read().split('\n') # add close
        self.product_names= open(product_names_file).read().split('\n') # add close
        self._PRICE_RANGE = params.get('price_range', PRICE_RANGE)
        self._STOCK_RANGE = params.get('stock_range', STOCK_RANGE)
        self._LOC_RANGE = params.get('loc_range', LOC_RANGE)
        self.num_products = params.get('num_products', NUM_PRODUCTS)
        self.num_items = params.get('num_items', NUM_ITEMS)

    def set_num_products(self, num_products):
        self.num_products = num_products

    def generate_product_data(self):
        """
        Generates and returns a DataFrame of product data.
        Format: (shop_name, product_name, price, stock)
        """
        product_data = [(
            rnd.choice(self.shop_names),
            rnd.choice(self.product_names),
            round(rnd.uniform(self._PRICE_RANGE[0], self._PRICE_RANGE[1]), 2),
            rnd.randrange(self._STOCK_RANGE[0], self._STOCK_RANGE[1]))
            for _ in range(self.num_products)
        ]
        return pd.DataFrame(product_data)
    
    def generate_shop_data(self):
        """
        Generates and returns a DataFrame of shop data.
        Format: (shop_name, (location_x, location_y))
        """
        shop_data = []
        for name in self.shop_names:
            x = round(rnd.uniform(self._LOC_RANGE[0], self._LOC_RANGE[1]), 4)
            y = round(rnd.uniform(self._LOC_RANGE[0], self._LOC_RANGE[1]), 4)
            shop_data.append((name, (x,y)))
        return pd.DataFrame(shop_data)
    
    def generate_item_data(self):
        """
        Generates and returns a Dataframe of item data.
        Format: (product_name, quantity)
        """
        items = rnd.choices(self.product_names, k=self.num_items)
        item_data = [(name, rnd.randint(1, MAX_ITEM_QUANT)) for name in items]
        return pd.DataFrame(item_data)

    def to_csv(self):
        """
        Generates data for products, shops, and items, and writes the data to csv files.
        """
        product_data = self.generate_product_data()
        product_data.to_csv("product_data.csv", header=False, index=False)
        shop_data = self.generate_shop_data()
        shop_data.to_csv("shop_data.csv", header=False, index=False)
        item_data = self.generate_item_data()
        item_data.to_csv("item_data.csv", header=False, index=False)
