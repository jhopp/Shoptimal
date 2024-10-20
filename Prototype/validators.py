from abc import ABC, abstractmethod
from input_data import InputData
from schedule import Schedule

class ScheduleChecker(ABC):
    def __init__(self, input_data: InputData, schedule: Schedule):
        """
        Checks that the given schedule meets some criterion.
        """
        self._input_data = input_data
        self._schedule = schedule

    @abstractmethod
    def check(self):
        pass

class AllItemsArePurchased(ScheduleChecker):
    def check(self) -> bool:
        """
        Checks that all items have been purchased.
        """
        item_set = self._schedule.to_itemset()
        for item in self._input_data.items:
            if item.name == "originsauce": continue
            if item.name not in item_set:
                return False
        return True
    
class AllPurchasesAreItems(ScheduleChecker):
    def check(self) -> bool:
        """
        Checks that are purchased items were on the list.
        """
        purchased_items = self._schedule.to_itemset()
        shopping_list = [item.name for item in self._input_data.items]
        return all([item in shopping_list for item in purchased_items]) 

class AllPurchasesAreOffered(ScheduleChecker):
    def check(self) -> bool:
        """
        Checks that all items are purchased at a shop that sells that item.
        """
        for decision in self._schedule.shop_decisions:
            if decision.item.name not in decision.shop.available_products():
                return False
        return True

class ShopsAreVisitedOnce(ScheduleChecker):
    def check(self) -> bool:
        """
        Checks that shops are only visited once.
        This means shopdecisions at some shop should be in sequence.
        Passing this check is not required for a schedule to be valid.
        """
        travel_decisions = self._schedule.travel_decisions
        shop_names = [decision.route.shop_to for decision in travel_decisions]
        return len(set(shop_names)) == len(travel_decisions)

class TravelFormsValidTour(ScheduleChecker):
    def check(self) -> bool:
        """
        Checks that the travel decisions form a valid tour.
        This means the shop_from of any travel decision is the shop_to of the previous travel decision.
        """
        previous_shop = "origin"
        for decision in self._schedule.travel_decisions:
            if decision.route.shop_from != previous_shop:
                return False
            previous_shop = decision.route.shop_to
        return previous_shop == "origin"
    
class AllPurchasesWithinStock(ScheduleChecker):
    def check(self) -> bool:
        """
        Checks that no purchase made exceeds the stock of the product at that shop.
        """
        for decision in self._schedule.shop_decisions:
            if decision.quantity > decision.shop.get_stock(decision.item.name):
                return False
        return True

class ScheduleValidator:
    def __init__(self, input_data: InputData, schedule: Schedule):
        self._input_data = input_data
        self._schedule = schedule
        self._checker_classes = [
            AllItemsArePurchased,
            AllPurchasesAreItems,
            AllPurchasesAreOffered,
            ShopsAreVisitedOnce,
            TravelFormsValidTour,
            AllPurchasesWithinStock
        ]

    def validate(self) -> None:
        for checker_cls in self._checker_classes:
            checker = checker_cls(schedule=self._schedule, input_data=self._input_data)
            is_valid = checker.check()
            print(f"{checker_cls.__name__:30s} : {'PASS' if is_valid else 'FAIL'}")