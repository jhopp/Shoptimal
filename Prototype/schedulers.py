from abc import ABC, abstractmethod
from schedule import Schedule, ShopDecision
from input_data import InputData

class Scheduler(ABC):
    def __init__(self, input_data: InputData):
        self._input_data = input_data

    @abstractmethod
    def schedule(self) -> Schedule:
        pass

class BasicScheduler(Scheduler):
    """
    Greedily schedules based on shop order in input data.
    For each shop schedules all items not yet purchased.
    """
    def schedule(self) -> Schedule:
        scheduled_items = set()
        shop_decisions = []
        for shop in self._input_data.shops:
            for item in self._input_data.items:
                if item.name in shop.available_products() and item.name not in scheduled_items:
                    scheduled_items.add(item.name)
                    shop_decisions.append(ShopDecision(item, shop))
            if len(shop_decisions) >= len(self._input_data.items):
                break
        return Schedule(self._input_data.origin, shop_decisions)