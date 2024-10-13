from docplex.mp.model import Model
from constants import M

def model3(input_data, kpi_cost, kpi_distance):
     """
     DOcplex model for scheduling shopping tour.
     -----
     Requires all items to be purchasable at some shop.
     Different routes can be taken between two shops.
     Shop product stock is taken into account.
     Shops are always open.
     """
     shops = input_data.shops
     items = input_data.items
     route_times = input_data.route_times(eq_num_routes=True)
     route_costs = input_data.route_costs(eq_num_routes=True)

     model3 = Model(name = "model3")

     num_shops = len(shops)
     num_items = len(items)
     num_routes = input_data.max_routes()
     s_labels = range(num_shops) # shop labels
     i_labels = range(num_items) # item labels
     r_labels = range(num_routes) # route labels     

     # decision variable: x_ij is the amount of item i is purchased at shop j
     x = model3.integer_var_matrix(num_items, num_shops, lb = 0, name = "x")

     # binary variable: s_j = 1 if shop j is visited and 0 otherwise
     s = model3.binary_var_list(num_shops, name = "s")

     # decision variable: e_jkr = 1 if shop k is visited directly after shop j using route r and 0 otherwise
     e = model3.binary_var_cube(num_shops, num_shops, num_routes, name = "e")

     # shop visit order
     u = model3.integer_var_list(keys=s_labels, ub = num_shops - 1, name = "u")

     # product prices: p_ij is the price of product i at shop j, or M if not valid
     p = [[(s.price_by_product[i.name] if i.name in s.available_products() else M) 
          for s in shops] 
          for i in items]
     
     # product stock: z_ij is the stock of product i at shop j, or 0 if not valid
     z = [[(s.stock_by_product[i.name] if i.name in s.available_products() else 0) 
          for s in shops] 
          for i in items]
     
     # item quantities: q_i is the amount of item i we would like to purchase
     q = [item.quantity for item in items]
     
     # route duration: d_kjr is the time from shop k to shop j using route r
     d = [[[route_times[(k.name, j.name)][r] for r in r_labels] for j in shops] for k in shops]

     # route cost: c_kjr is the cost of traveling from shop k to shop j using route r
     c = [[[route_costs[(k.name, j.name)][r] for r in r_labels] for j in shops] for k in shops]

     # objective function: minimize cost
     obj_purchase_cost = sum(p[i][j]    * x[i,j]   for i in i_labels for j in s_labels)
     obj_travel_cost   = sum(c[k][j][r] * e[k,j,r] for r in r_labels for k in s_labels for j in s_labels)
     obj_travel_time   = sum(d[k][j][r] * e[k,j,r] for r in r_labels for k in s_labels for j in s_labels)
     obj_func = kpi_cost * (obj_purchase_cost + obj_travel_cost) + kpi_distance * obj_travel_time
     model3.set_objective(sense = 'min', expr = obj_func)
        
     # every item is purchased
     model3.add_constraints(sum(x[i,j] for j in s_labels) >= q[i] for i in i_labels)

     # no purchase costs M or more (only valid purchases)
     model3.add_constraints(sum(x[i,j] * p[i][j] for j in s_labels) <= M - 1 for i in i_labels)

     # no purchase exceeds stock and only if shop is visited
     model3.add_constraints(x[i,j] <= z[i][j] * s[j] for i in i_labels for j in s_labels)

     # each visited shop is traveled to
     model3.add_constraints(sum(e[k,j,r] for r in r_labels for k in s_labels if k != j) >= s[j] for j in s_labels)

     # each traveled from shop is visited
     model3.add_constraints(sum(e[k,j,r] for r in r_labels for j in s_labels if j != k) <= s[k] for k in s_labels)

     # enforce proper tour
     model3.add_constraints(u[k] - u[j] + 1 <= (num_shops - 2) * (1 - e[k,j,r]) for r in r_labels for k in s_labels if k > 0 for j in s_labels)

     return model3
