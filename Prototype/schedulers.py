from abc import ABC, abstractmethod
from schedule import Schedule, Decision, ShopDecision, TravelDecision
from input_data import InputData
from model1 import model1
from model2 import model2
from model3 import model3
from math import inf


class Scheduler(ABC):
    def __init__(self, input_data: InputData):
        self._input_data = input_data
        self._model_solution = None

    @abstractmethod
    def schedule(self) -> Schedule:
        pass

class BasicScheduler(Scheduler):
    """
    Greedily schedules based on shop and route order in input data.
    For each shop schedules all items not yet purchased.
    """
    def schedule(self) -> Schedule:
        scheduled_items = set()
        decisions = []
        previous_shop = "origin"
        for shop in self._input_data.shops:
            # purchase all available items at current shop
            purchase_made = False
            for item in self._input_data.items:
                if item.name in shop.available_products() and item.name not in scheduled_items:
                    scheduled_items.add(item.name)
                    decision = ShopDecision(item, shop)
                    decisions.append(decision)
                    purchase_made = True
            # if a purchase was made at this shop (not origin), add traveldecision        
            if purchase_made and shop.name != "origin":
                route = self._input_data.get_walking_route(previous_shop, shop.name)
                decisions.append(TravelDecision(route))
                previous_shop = shop.name
        # add travel back to origin
        route = self._input_data.get_walking_route(previous_shop, "origin")
        decisions.append(TravelDecision(route))
        return Schedule(self._input_data.origin, decisions)

class BestPriceScheduler(Scheduler):
    """
    Creates a schedule that has minimal cost.
    Does not take distance into account.
    """
    def schedule(self) -> Schedule:
        decisions = []
        shop_decisions = []

        # for each item find cheapest shop and add shopdecision
        for item in self._input_data.items:
            if item.name == "originsauce": continue
            cheapest_shop = None
            best_price = inf
            for shop in self._input_data.shops:
                if shop.get_price(item.name) == None:
                    continue
                if shop.get_price(item.name) < best_price:
                    cheapest_shop = shop
                    best_price = shop.get_price(item.name)
            shop_decisions.append(ShopDecision(item, cheapest_shop))

        # add traveldecisions (walking)
        sorted_shop_decisions = sorted(shop_decisions, key= lambda x: x.shop.name)
        previous_shop = "origin"
        for decision in sorted_shop_decisions:
            if previous_shop !=  decision.shop.name:
                route = self._input_data.get_walking_route(previous_shop, decision.shop.name)
                decisions.append(TravelDecision(route))
                previous_shop = decision.shop.name
            decisions.append(decision)
        route = self._input_data.get_walking_route(previous_shop, "origin")
        decisions.append(TravelDecision(route))

        return Schedule(self._input_data.origin,decisions)

class Model1Scheduler(Scheduler):
    """
    Schedules using simple_model.
    """  
    def schedule(self, kpi_cost=1, kpi_distance=1) -> Schedule:
        model = model1(self._input_data, kpi_cost, kpi_distance)
        model.round_solution = True
        msol = model.solve()

        num_items = len(self._input_data.items)
        num_shops = len(self._input_data.shops)

        #model.print_solution()

        decisions = []
        current_shop = 0 # start at origin (index 0)
        shops_visited = 0

        while shops_visited <= num_shops: # continue until back at origin (at most all shops)
            shops_visited += 1

            # add current shop items
            if current_shop != 0:
                for i in range(num_items):
                    if msol.get_value(f"x_{i}_{current_shop}") == 1:
                        decisions.append(ShopDecision(self._input_data.items[i], self._input_data.shops[current_shop]))

            # set next shop
            for next_shop in range(num_shops):
                if msol.get_value(f"e_{current_shop}_{next_shop}") == 1:
                    shop_from = self._input_data.shops[current_shop].name
                    shop_to = self._input_data.shops[next_shop].name
                    route = self._input_data.get_walking_route(shop_from, shop_to)
                    decisions.append(TravelDecision(route))
                    current_shop = next_shop
                    break
  
            # terminate loop if at origin again
            if current_shop == 0 and len(decisions) > 0:
                break

        return Schedule(self._input_data.origin, decisions)

class Model2Scheduler(Scheduler):
    """
    Schedules using model2.
    """  
    def schedule(self, kpi_cost=1, kpi_distance=1) -> Schedule:
        model = model2(self._input_data, kpi_cost, kpi_distance)
        model.round_solution = True
        msol = model.solve()

        num_items = len(self._input_data.items)
        num_shops = len(self._input_data.shops)
        num_routes = self._input_data.max_routes()

        #model.print_solution()

        decisions = []
        route_matrix = self._input_data.route_matrix(eq_num_routes=True)
        current_shop = 0 # start at origin (index 0)
        shops_visited = 0

        while shops_visited <= num_shops: # continue until back at origin (at most all shops)
            shops_visited += 1

            # add current shop items
            if current_shop != 0:
                for i in range(num_items):
                    if msol.get_value(f"x_{i}_{current_shop}") == 1:
                        decisions.append(ShopDecision(self._input_data.items[i], self._input_data.shops[current_shop]))
            
            # set next shop
            for next_shop in range(num_shops):
                if current_shop == next_shop: continue 
                for route_num in range(num_routes):
                    if msol.get_value(f"e_{current_shop}_{next_shop}_{route_num}") == 1:
                        shop_from = self._input_data.shops[current_shop].name
                        shop_to = self._input_data.shops[next_shop].name
                        route = route_matrix[shop_from, shop_to][route_num]
                        decisions.append(TravelDecision(route))
                        current_shop = next_shop
                        break
                if current_shop == next_shop: break # found a route taken
  
            # terminate loop if at origin again
            if current_shop == 0 and len(decisions) > 0:
                break

        return Schedule(self._input_data.origin, decisions)
    
class Model3Scheduler(Scheduler):
    """
    Schedules using model3.
    """  
    def schedule(self, kpi_cost=1, kpi_distance=1) -> Schedule:
        model = model3(self._input_data, kpi_cost, kpi_distance)
        model.round_solution = True
        msol = model.solve()

        num_items = len(self._input_data.items)
        num_shops = len(self._input_data.shops)
        num_routes = self._input_data.max_routes()

        decisions = []
        route_matrix = self._input_data.route_matrix(eq_num_routes=True)
        current_shop = 0 # start at origin (index 0)
        shops_visited = 0

        while shops_visited <= num_shops: # continue until back at origin (at most all shops)
            shops_visited += 1

            # add current shop items
            if current_shop != 0:
                for i in range(num_items):
                    quantity = int(msol.get_value(f"x_{i}_{current_shop}"))
                    if quantity > 0:
                        decisions.append(ShopDecision(self._input_data.items[i], self._input_data.shops[current_shop], quantity))
            
            # set next shop
            for next_shop in range(num_shops):
                if current_shop == next_shop: continue 
                for route_num in range(num_routes):
                    if msol.get_value(f"e_{current_shop}_{next_shop}_{route_num}") == 1:
                        shop_from = self._input_data.shops[current_shop].name
                        shop_to = self._input_data.shops[next_shop].name
                        route = route_matrix[shop_from, shop_to][route_num]
                        decisions.append(TravelDecision(route))
                        current_shop = next_shop
                        break
                if current_shop == next_shop: break # found a route taken
  
            # terminate loop if at origin again
            if current_shop == 0 and len(decisions) > 0:
                break

        return Schedule(self._input_data.origin, decisions)