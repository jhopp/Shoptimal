from shop import Shop
from item import Item
from route import Route
import pandas as pd
from constants import M

class InputData:
    def __init__(self, origin: tuple[float, float], shops: list[Shop], items: list[Item], routes: list[Route]) -> None:
        """
        origin: (float, float)
            Start- and end location of user.
        shops: list[Shop]
            List of shops from which items can be purchased.
        items: list[Item]
            List of items to be purchased; the shopping list.
        """
        self.origin = origin
        self.shops = shops
        self.items = items # shopping list
        self.routes = routes

    def _get_origin(path: str) -> tuple[float, float]:
        return (50, 50)
    
    def _get_shops(path: str, origin: tuple[float, float]) -> list[Shop]:
        shop_data = pd.read_csv(path + 'shop_data.csv', header=None, index_col=False)
        shop_list = [Shop(name, (loc_x, loc_y), {}, {}) for name, loc_x, loc_y in shop_data.to_numpy()]
        shops = dict([(shop.name, shop) for shop in shop_list])

        shops["origin"].location = origin # update origin location

        product_data = pd.read_csv(path + 'product_data.csv', header=None, index_col=False)
        for (shop_name, product_name, price, stock) in product_data.to_numpy():
            if shop_name in shops.keys():
                shops[shop_name].price_by_product[product_name] = price
                shops[shop_name].stock_by_product[product_name] = stock
            else:
                raise Exception("Encountered unknown shop name")
        return list(shops.values())
    
    def _get_items(path: str) -> list[Item]:
        item_data = pd.read_csv(path + 'item_data.csv', header=None, index_col=False)
        items = [Item(name, quantity) for (name, quantity) in item_data.values]
        return items

    def _get_routes(path: str) -> list[Route]:
        route_data = pd.read_csv(path + 'route_data.csv', header=None, index_col=False)
        routes = [Route(shop_from, shop_to, time, cost) for (shop_from, shop_to, time, cost) in route_data.values]
        return routes

    @classmethod
    def from_csv(cls, path: str):
        origin = cls._get_origin(path)
        shops = cls._get_shops(path, origin)
        items = cls._get_items(path)
        routes = cls._get_routes(path)
        return InputData(origin, shops, items, routes)
    
    def unavailable_items(self) -> list[str]:
        """
        Returns names of items not available in any shops.
        """
        items = []
        for item in self.items:
            available_in = [item.name in shop.available_products() for shop in self.shops]
            if not any(available_in):
                items.append(item)
        return items

    def shop_distances(self) -> dict[(str, str), float]:
        """
        Returns dictionary of distances between shops: (from, to).
        """
        distances = {}
        for shop1 in self.shops:
            for shop2 in self.shops:
                if (shop1.name, shop2.name) not in distances:
                    distances[(shop1.name, shop2.name)] = round(shop1.euclidian_distance(shop2), 4)
                    distances[(shop2.name, shop1.name)] = distances[(shop1.name, shop2.name)]
        return distances
    
    def route_matrix(self,eq_num_routes: bool) -> dict[(str,str), list[Route]]:
        """
        Returns dictionary of routes: (shop_from, shop_to, route)
        If eq_num_routes is true, all pairs of shops will have an equal number of routes between them.
        """
        # add real routes to result dictionary
        routes = {}
        for route in self.routes:
            if (route.shop_from, route.shop_to) in routes:
                routes[(route.shop_from, route.shop_to)].append(route)
            else:
                routes[(route.shop_from, route.shop_to)] = [route]

        # give all pairs an equal number of routes by adding dummies
        if eq_num_routes:
            max_routes = self.max_routes() # or max([len(x) for x in routes.values()])
            dummy_route = Route("", "", M, M)
            for (shop_from, shop_to) in routes.keys():
                num_routes = len(routes[(shop_from, shop_to)])
                num_add = max_routes - num_routes
                for _ in range(num_add):
                    routes[(shop_from, shop_to)].append(dummy_route)
        return routes
    
    def route_times(self, eq_num_routes: bool) -> dict[(str,str), list[float]]:
        """
        Returns dictionary of route times: (from, to, route_num)
        If eq_num_routes is true, all pairs of shops will have an equal number of routes between them.
        """
        route_matrix = self.route_matrix(eq_num_routes)
        times = {key:[r.time for r in routes] for key,routes in route_matrix.items()}
        return times

    def route_costs(self, eq_num_routes: bool) -> dict[(str,str), list[float]]:
        """
        Returns dictionary of route costs: (from, to, route_num)
        If eq_num_routes is true, all pairs of shops will have an equal number of routes between them.
        """
        route_matrix = self.route_matrix(eq_num_routes)
        costs = {key:[r.cost for r in routes] for key,routes in route_matrix.items()}
        return costs

    def max_routes(self) -> int:
        """
        Returns the maximum number of routes across any ordered pair of shops.
        """
        num_routes = dict()
        for route in self.routes:
            if (route.shop_from, route.shop_to) in num_routes:
                num_routes[route.shop_from, route.shop_to] += 1
            else:
                num_routes[route.shop_from, route.shop_to] = 1
        return max(num_routes.values()) 

    def get_walking_route(self, shop_from: str, shop_to: str) -> Route:
        """
        Returns the route from shop_from to shop_to by walking.
        This route should always exist in the input data.
        """
        for route in self.routes:
            if route.shop_from == shop_from and route.shop_to == shop_to and route.cost == 0:
                return route
        raise LookupError(f"Could not find walking route from {shop_from} to {shop_to}.")

    def __repr__(self) -> str:
        return f"{self.shops}\n{self.items}"