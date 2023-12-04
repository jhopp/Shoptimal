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

    def _get_shops(path: str) -> list[Shop]:
        shop_data = pd.read_csv(path + 'shop_data.csv', header=None, index_col=False)
        shop_list = [Shop(name, (loc_x, loc_y), {}, {}) for name, loc_x, loc_y in shop_data.to_numpy()]
        shops = dict([(shop.name, shop) for shop in shop_list])

        product_data = pd.read_csv(path + 'product_data.csv')
        for (shop_name, product_name, price, stock) in product_data.to_numpy():
            if shop_name in shops.keys():
                shops[shop_name].price_by_product[product_name] = price
                shops[shop_name].stock_by_product[product_name] = stock
            else:
                raise Exception("Encountered unknown shop name")
        return list(shops.values())
    
    def _get_items(path: str) -> list[Item]:
        item_data = pd.read_csv(path + 'item_data.csv')
        items = [Item(name, quantity) for (name, quantity) in item_data.values]
        return items

    @classmethod
    def from_csv(cls, path: str):
        shops = cls._get_shops(path)
        items = cls._get_items(path)
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

    def shop_distances(self) -> dict[(str, str), float]:
        """
        Returns dictionary of distances between shops: (from, to).
        """
        distances = {}
        for shop1 in self.shops:
            for shop2 in self.shops:
                if (shop1.name, shop2.name) not in distances:
                    distances[(shop1.name, shop2.name)] = round(shop1.euclidian_distance(shop2), 4)
                    distances[(shop2.name, shop1.name)] = distances[(shop1.name, shop2.name)]
        return distances

    def __repr__(self) -> str:
        return f"{self.shops}\n{self.items}"