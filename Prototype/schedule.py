from item import Item
from shop import Shop
from route import Route


class ShopDecision:
    def __init__(self, item: Item, shop: Shop) -> None:
        self.item = item
        self.shop = shop
        self.quantity = 1 # pass this as argument when item quantities are implemented

    def __repr__(self) -> str:
        return f"{self.shop.name}: {self.item.name}"
    
class TravelDecision:
    def __init__(self, route: Route) -> None:
        self.route = route

    def __repr__(self) -> str:
        return f"{self.route.shop_from}: {self.route.shop_to}"

class Schedule:
    def __init__(self, origin: tuple[float, float], shop_decisions: list[ShopDecision], travel_decisions: list[TravelDecision]=[]) -> None:
        self.origin = origin
        self.shop_decisions = shop_decisions
        self.travel_decisions = travel_decisions

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
        return sum([decision.shop.price_by_product[decision.item.name] for decision in self.shop_decisions])

    @property
    def duration(self) -> float:
        """
        Returns
        -------
        float : Schedule's travel duration in time units
        """
        return sum([decision.route.time for decision in self.travel_decisions])

    def __repr__(self) -> str:
        return f"{self.shop_decisions}"