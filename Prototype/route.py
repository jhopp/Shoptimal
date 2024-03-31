
class Route:
    def __init__(self, shop_from: str, shop_to: str, time: float, cost: float) -> None:
        self.shop_from = shop_from
        self.shop_to = shop_to
        self.time = time
        self.cost = cost

    def __repr__(self) -> str:
        return f"{self.shop_from} -> {self.shop_to} in {self.time} for {self.cost}"