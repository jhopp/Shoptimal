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
        for item in purchased_items:
            if item not in shopping_list:
                return False
        return True      

class AllPurchasesAreValid(ScheduleChecker):
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
        visited = set()
        prev_shop = None
        for decision in self._schedule.shop_decisions:
            name = decision.shop.name
            if name == prev_shop:
                continue
            if name in visited:
                return False
            visited.add(name)
            prev_shop = name
        return True

class ScheduleValidator:
    def __init__(self, input_data: InputData, schedule: Schedule):
        self._input_data = input_data
        self._schedule = schedule
        self._checker_classes = [
            AllItemsArePurchased,
            AllPurchasesAreItems,
            AllPurchasesAreValid,
            ShopsAreVisitedOnce
        ]

    def validate(self) -> None:
        for checker_cls in self._checker_classes:
            checker = checker_cls(schedule=self._schedule, input_data=self._input_data)
            is_valid = checker.check()
            print(f"{checker_cls.__name__:30s} : {'PASS' if is_valid else 'FAIL'}")