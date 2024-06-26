from math import sqrt

class Shop:
    def __init__(self,
                 name: str,
                 location: tuple[float, float],
                 price_by_product: dict[str, float],
                 stock_by_product: dict[str, int]) -> None:
        self.name = name
        self.location = location
        self.price_by_product = price_by_product
        self.stock_by_product = stock_by_product

    def get_price(self, product_name) -> float:
        """
        Returns the price of the product given, or None if not offered in shop.
        """
        if product_name in self.available_products():
            return self.price_by_product[product_name]
        return None

    def available_products(self) -> set[str]:
        products = [product_name for product_name in self.price_by_product.keys()]
        return set(products)

    def euclidian_distance(self, other) -> float:
        (x1, y1) = self.location
        (x2, y2) = other.location if type(other) == Shop else other
        return sqrt((pow(x1 - x2, 2) + pow(y1 - y2, 2)))

    def __repr__(self) -> str:
        return f"{self.name}: {self.price_by_product}"