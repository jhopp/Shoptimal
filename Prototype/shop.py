
class Shop:
    def __init__(self,
                 name: str,
                 location: (float, float),
                 price_by_product: dict[str, float],
                 stock_by_product: dict[str, int]) -> None:
        self.name = name
        self.location = location
        self.price_by_product = price_by_product
        self.stock_by_product = stock_by_product

    def __repr__(self) -> str:
        return f"{self.name}: {self.price_by_product}"