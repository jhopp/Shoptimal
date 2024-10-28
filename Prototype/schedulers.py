from abc import ABC, abstractmethod
from schedule import Schedule, ShopDecision, TravelDecision
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

class ModelScheduler(Scheduler):
    """
    Base scheduler class for schedulers using a DOcplex model.
    """
    def model_schedule(self, model) -> Schedule:
        msol = model.solve()

        decisions = []
        current_shop = 0 # start at origin (index 0)

        for _ in range(len(self._input_data.shops)): # continue until back at origin (at most all shops)
            # add current shop items
            if current_shop != 0:
                purchases = self.get_shop_decisions(msol, current_shop)
                decisions.extend(purchases)
            
            # set next shop
            travel = self.get_travel_decision(msol, current_shop)
            decisions.append(travel)
            current_shop = self._input_data.get_shop_index(travel.route.shop_to)
  
            # terminate loop if at origin again
            if current_shop == 0 and len(decisions) > 0:
                return Schedule(self._input_data.origin, decisions)

        raise RuntimeError("Traversed all shops without returning to origin.")

    def get_travel_decision(self, solution, shop_from):
        """
        Returns the TravelDecision originating at shop_from in the solution.
        """
        num_shops = len(self._input_data.shops)
        num_routes = self._input_data.max_routes()
        route_matrix = self._input_data.route_matrix(eq_num_routes=True)
        for shop_to in range(num_shops):
            for route_num in range(num_routes):
                if solution.get_value(f"e_{shop_from}_{shop_to}_{route_num}") == 1:
                    shop_from_name = self._input_data.shops[shop_from].name
                    shop_to_name = self._input_data.shops[shop_to].name
                    route = route_matrix[shop_from_name, shop_to_name][route_num]
                    return TravelDecision(route)
        raise LookupError(f"Unable to find TravelDecision originating at {shop_from} in the solution.")
    
    def get_shop_decisions(self, solution, shop):
        """
        Returns a list of ShopDecisions made at a given shop in the solution.
        """
        num_items = len(self._input_data.items)
        shop_decisions = []
        for i in range(0, num_items):
            quantity = int(solution.get_value(f"x_{i}_{shop}"))
            if quantity > 0:
                shop_decisions.append(ShopDecision(self._input_data.items[i], self._input_data.shops[shop], quantity))
        return shop_decisions

class Model1Scheduler(ModelScheduler):
    """
    Schedules using model1.
    """ 
    def schedule(self, kpi_cost=1, kpi_distance=1) -> Schedule:
        model = model1(self._input_data, kpi_cost, kpi_distance)
        model.round_solution = True
        return self.model_schedule(model)

    def get_travel_decision(self, solution, shop_from):
        """
        Returns the TravelDecision originating at shop_from in the solution.
        """
        num_shops = len(self._input_data.shops)
        for shop_to in range(num_shops):
            if solution.get_value(f"e_{shop_from}_{shop_to}") == 1:
                shop_from_name = self._input_data.shops[shop_from].name
                shop_to_name = self._input_data.shops[shop_to].name
                route = self._input_data.get_walking_route(shop_from_name, shop_to_name)
                return TravelDecision(route)
        raise LookupError(f"Unable to find TravelDecision originating at {shop_from} in the solution.")

class Model2Scheduler(ModelScheduler):
    """
    Schedules using model2.
    """  
    def schedule(self, kpi_cost=1, kpi_distance=1) -> Schedule:
        model = model2(self._input_data, kpi_cost, kpi_distance)
        model.round_solution = True
        return self.model_schedule(model)
        
    
class Model3Scheduler(ModelScheduler):
    """
    Schedules using model3.
    """  
    def schedule(self, kpi_cost=1, kpi_distance=1) -> Schedule:
        model = model3(self._input_data, kpi_cost, kpi_distance)
        model.round_solution = True
        return self.model_schedule(model)