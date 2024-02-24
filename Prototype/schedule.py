from item import Item
from shop import Shop


class ShopDecision:
    def __init__(self, item: Item, shop: Shop) -> None:
        self.item = item
        self.shop = shop
        self.quantity = 1 # pass this as argument when item quantities are implemented

    def __repr__(self) -> str:
        return f"{self.shop.name}: {self.item.name}"

class Schedule:
    def __init__(self, origin: tuple[float, float], shop_decisions: list[ShopDecision]) -> None:
        self.origin = origin
        self.shop_decisions = shop_decisions

    def to_itemset(self) -> set[str]:
        """
        Returns set of names of items purchased.
        """
        return set([decision.item.name for decision in self.shop_decisions])
    
    def to_itemdict(self) -> dict[str, int]:
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
        total_cost = 0
        for decision in self.shop_decisions:
            total_cost += decision.shop.price_by_product[decision.item.name] # multiply by quantity once implemented
        return total_cost

    @property
    def total_distance(self) -> float:
        """

        Returns
        -------
        float : Schedule's distance traveled in distance units
        """
        distance = 0
        previous_shop = self.shop_decisions[0].shop
        distance += previous_shop.euclidian_distance(self.origin)
        for decision in self.shop_decisions:
            distance += previous_shop.euclidian_distance(decision.shop)
            previous_shop = decision.shop
        distance += previous_shop.euclidian_distance(self.origin)
        return distance

    def __repr__(self) -> str:
        return f"{self.shop_decisions}"