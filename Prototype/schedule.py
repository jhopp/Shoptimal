from item import Item
from shop import Shop
from route import Route
from constants import CBLUE, CBLUE2, CBOLD, CGREEN, CVIOLET, CYELLOW, CEND


class ShopDecision:
    def __init__(self, item: Item, shop: Shop, quantity: int = 1) -> None:
        self.item = item
        self.shop = shop
        self.quantity = quantity

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
        purchase_cost = sum([decision.shop.price_by_product[decision.item.name] for decision in self.shop_decisions])
        travel_cost = sum([decision.route.cost for decision in self.travel_decisions])
        return purchase_cost + travel_cost

    @property
    def duration(self) -> float:
        """
        Returns
        -------
        float : Schedule's travel duration in time units
        """
        return sum([decision.route.time for decision in self.travel_decisions])
    
    def __iter__(self):
        self._iter_travel = 0
        self._iter_shop = 0
        return self

    def __next__(self):
        # stop iteration if out of decisions (last travel means no more shop)
        if self._iter_travel >= len(self.travel_decisions):
            raise StopIteration
        # return shop_decision if purchase made at current shop
        if self._iter_shop < len(self.shop_decisions):
            decision = self.shop_decisions[self._iter_shop]
            current_shop = self.travel_decisions[self._iter_travel].route.shop_from
            if decision.shop.name == current_shop:
                self._iter_shop += 1
                return decision
        # return travel_decision if purchase not made and can travel
        decision = self.travel_decisions[self._iter_travel]
        self._iter_travel += 1
        return decision

    def __str__(self) -> str:
        schedule_string = ""
        for dec in self:
            if isinstance(dec, ShopDecision):
                cost = dec.shop.price_by_product[dec.item.name]
                schedule_string += CGREEN + f"{'Purchased'}  " + CEND
                schedule_string += CBLUE + f"{dec.quantity:<2} " + CEND
                schedule_string += f"{dec.item.name:<14} "
                schedule_string += "for " + CBLUE2 + f"{cost}\n" + CEND
            if isinstance(dec, TravelDecision):
                schedule_string += CYELLOW + f"{'Traveled'} " + CEND
                schedule_string += CVIOLET + f"{dec.route.time:<6} " + CEND
                schedule_string += CBOLD + f"→ " + CEND 
                schedule_string += f"{dec.route.shop_to:<10} "        
                schedule_string += "for " + CBLUE2 + f"{dec.route.cost}\n" + CEND
        return schedule_string

    def __repr__(self) -> str:
        return f"{self.shop_decisions}"