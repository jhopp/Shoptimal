from shop import Shop
from item import Item
import pandas as pd

class InputData:
    def __init__(self, shops: list[Shop], items: list[Item]) -> None:
        """
        shops: list[Shop]
            List of shops from which items can be purchased.
        items: list[Item]
            List of items to be purchased; the shopping list.
        """
        self.shops = shops
        self.items = items # shopping list

    def get_shops(path: str) -> list[Shop]:
        shop_data = pd.read_csv(path + 'shop_data.csv', header=None, index_col=False)
        shop_list = [Shop(name, loc, {}, {}) for name, loc in shop_data.to_numpy()]
        shops = dict([(shop.name, shop) for shop in shop_list])

        product_data = pd.read_csv(path + 'product_data.csv')
        for (shop_name, product_name, price, stock) in product_data.to_numpy():
            if shop_name in shops.keys():
                shops[shop_name].price_by_product[product_name] = price
                shops[shop_name].stock_by_product[product_name] = stock
            else:
                raise Exception("Encountered unknown shop name")
        return list(shops.values())
    
    def get_items(path: str) -> list[Item]:
        item_data = pd.read_csv(path + 'item_data.csv')
        items = [Item(name, quantity) for (name, quantity) in item_data.values]
        return items

    @classmethod
    def from_csv(cls, path: str):
        shops = cls.get_shops(path)
        items = cls.get_items(path)
        return InputData(shops, items)
    
    def unavailable_items(self) -> list[str]:
        """
        Returns names of items not available in any shops.
        """
        items = []
        for item in self.items:
            available_in = [item.name in shop.available_products() for shop in self.shops]
            if not any(available_in):
                items.append(item)
        return items

    def __repr__(self) -> str:
        return f"{self.shops}\n{self.items}"