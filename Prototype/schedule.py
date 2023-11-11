
class ShopDecision:
    def __init__(self, item_name: str, shop_name: str) -> None:
        self.item_name = item_name
        self.shop_name = shop_name
        self.quantity = 1 # pass this as argument when item quantities are implemented

    def __repr__(self) -> str:
        return f"{self.shop_name}: {self.item_name}"

class Schedule:
    def __init__(self, shop_decisions: list[ShopDecision]) -> None:
        self.shop_decisions = shop_decisions

    def to_itemset(self) -> set(str):
        """
        Returns set of items purchased.
        """
        return set([decision.item_name for decision in self.shop_decisions])
    
    def to_itemdict(self) -> dict(str, int):
        """
        Returns dictionary of (item_name, quantity purchased).
        """
        item_dict = dict()
        for decision in self.shop_decisions:
            if decision.item_name in item_dict.keys():
                item_dict[decision.item_name] += decision.quantity
            else:
                item_dict[decision.item_name] = decision.quantity
        return item_dict

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