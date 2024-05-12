from docplex.mp.model import Model
from route import Route
from constants import M

def model2(input_data, kpi_cost, kpi_distance):
     """
     DOcplex model for scheduling shopping tour.
     -----
     Requires all items to be purchasable at some shop.
     Does not include item quantities.
     Different routes can be taken between two shops.
     Shops are always open.
     """
     shops = input_data.shops
     items = input_data.items
     route_times = input_data.route_times(eq_num_routes=True)
     route_costs = input_data.route_costs(eq_num_routes=True)

     model2 = Model(name = "model2")

     num_shops = len(shops)
     num_items = len(items)
     num_routes = input_data.max_routes()
     s_labels = range(num_shops) # shop labels
     i_labels = range(num_items) # item labels
     r_labels = range(num_routes) # route labels     

     # decision variable: x_ij = 1 if item i is purchased at shop j and 0 otherwise
     x = model2.binary_var_matrix(num_items, num_shops, name = "x")

     # binary variable: s_j = 1 if shop j is visited and 0 otherwise
     s = model2.binary_var_list(num_shops, name = "s")

     # binary variable: e_jkr = 1 if shop k is visited directly after shop j using route r and 0 otherwise
     e = model2.binary_var_cube(num_shops, num_shops, num_routes, name = "e")

     # shop visit order
     u = model2.integer_var_list(keys=s_labels, ub = num_shops - 1, name = "u")

     # product prices: p_ij is the price of product i at shop j, or M if not valid
     p = [[(s.price_by_product[i.name] if i.name in s.available_products() else M) 
          for s in shops] 
          for i in items]
     
     # route duration: d_kjr is the time from shop k to shop j using route r
     d = [[[route_times[(k.name, j.name)][r] for r in r_labels] for j in shops] for k in shops]

     # route cost: c_kjr is the cost of traveling from shop k to shop j using route r
     c = [[[route_costs[(k.name, j.name)][r] for r in r_labels] for j in shops] for k in shops]

     # objective function: minimize cost
     obj_func = sum( kpi_cost * sum(p[i][j] * x[i,j] for i in i_labels) + sum((kpi_distance * d[k][j][r] + kpi_cost * c[k][j][r]) * e[k,j,r] for r in r_labels for k in s_labels) for j in s_labels)
     model2.set_objective(sense = 'min', expr = obj_func)
        
     # every item is purchased
     model2.add_constraints((sum(x[i,j] for j in s_labels) >= 1 for i in i_labels))

     # no purchase costs M or more (only valid purchases)
     model2.add_constraints(sum(x[i,j] * p[i][j] for j in s_labels) <= M - 1 for i in i_labels)

     # each used shop is visited
     model2.add_constraints((sum(x[i,j] for i in i_labels) <= 1000 * s[j] for j in s_labels))

     # each visited shop is traveled to
     model2.add_constraints(sum(e[k,j,r] for r in r_labels for k in s_labels if k != j) >= s[j] for j in s_labels)

     # each traveled from shop is visited
     model2.add_constraints(sum(e[k,j,r] for r in r_labels for j in s_labels if j != k) <= s[k] for k in s_labels)

     # enforce proper tour
     model2.add_constraints(u[k] - u[j] + 1 <= (num_shops - 2) * (1 - e[k,j,r]) for r in r_labels for k in s_labels if k > 0 for j in s_labels)

     return model2
