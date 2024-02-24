from abc import ABC, abstractmethod
from schedule import Schedule, ShopDecision
from input_data import InputData
from simple_model import simple_model


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
    
class Model1Scheduler(Scheduler):
    """
    Schedules using simple_model
    """  
    def schedule(self, kpi1, kpi2) -> Schedule:
        model = simple_model(self._input_data, kpi1, kpi2)
        #model.parameters.timelimit = 5
        msol = model.solve()

        num_items = len(self._input_data.items)
        num_shops = len(self._input_data.shops)

        model.print_solution()

        shop_decisions = []
        current_shop = 0 # start at origin (index 0)
        shops_visited = 0

        while shops_visited <= num_shops: # continue until back at origin (at most all shops)
            shops_visited += 1
            # add current shop items
            for i in range(num_items):
                if msol.get_value(f"x_{i}_{current_shop}") == 1:
                    shop_decisions.append(ShopDecision(self._input_data.items[i], self._input_data.shops[current_shop]))

            # set next shop
            for next_shop in range(num_shops):
                if next_shop == current_shop:
                    continue
                if msol.get_value(f"e_{current_shop}_{next_shop}") == 1:
                    current_shop = next_shop
                    break
  
            # terminate loop if new current shop is origin
            if current_shop == 0:
                shops_visited = num_shops # run one more iteration to add origin as final decision
            
        return Schedule(self._input_data.origin, shop_decisions)
