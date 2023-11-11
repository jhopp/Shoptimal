
class ShopDecision:
    def __init__(self, item_name: str, shop_name: str) -> None:
        self.item_name = item_name
        self.shop_name = shop_name

    def __repr__(self) -> str:
        return f"{self.shop_name}: {self.item_name}"

class Schedule:
    def __init__(self,
                 shop_decisions: list[ShopDecision]) -> None:
        self.shop_decisions = shop_decisions

    @property
    def cost(self) -> float:
        """

        Returns
        -------
        float : Schedule's cost in monetary units
        """
        return 1.0

    @property
    def total_distance(self) -> float:
        """

        Returns
        -------
        float : Schedule's distance traveled in distance units
        """
        return 1.0

    def __repr__(self) -> str:
        return f"{self.shop_decisions}"