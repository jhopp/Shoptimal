from docplex.mp.model import Model
from constants import M

def model1(input_data, kpi_cost, kpi_distance):
     """
     DOcplex model for scheduling shopping tour.
     -----
     Requires all items to be purchasable at some shop.
     Does not include item quantities.
     Distance between shops is fixed.
     Shops are always open.
     """
     shops = input_data.shops
     items = input_data.items
     shop_dist = input_data.shop_distances()

     model1 = Model(name = "model1")

     num_shops = len(shops)
     num_items = len(items)
     s_labels = range(num_shops) # shop labels
     i_labels = range(num_items) # item labels
     

     # decision variable: x_ij = 1 if item i is purchased at shop j and 0 otherwise
     x = model1.binary_var_matrix(num_items, num_shops, name = "x")

     # binary variable: s_j = 1 if shop j is visited and 0 otherwise
     s = model1.binary_var_list(num_shops, name = "s")

     # binary variable: e_jk = 1 if shop k is visited directly after shop j and 0 otherwise
     e = model1.binary_var_matrix(num_shops, num_shops, name = "e")

     # shop visit order
     u = model1.integer_var_list(keys=s_labels, ub = num_shops - 1, name = "u")

     # product prices: p_ij is the price of product i at shop j, or M if not valid
     p = [[(s.price_by_product[i.name] if i.name in s.available_products() else M) 
          for s in shops] 
          for i in items]
        
     # distances: d_kj is the distance from shop k to shop j
     d = [[shop_dist[(k.name, j.name)] for k in shops] for j in shops]

     # objective function: minimize cost
     obj_func = sum( kpi_cost * sum(p[i][j] * x[i,j] for i in i_labels) + kpi_distance * sum(d[k][j] * e[k,j] for k in s_labels) for j in s_labels)
     model1.set_objective(sense = 'min', expr = obj_func)
        
     # every item is purchased
     model1.add_constraints((sum(x[i,j] for j in s_labels) >= 1 for i in i_labels))

     # no purchase costs M or more (only valid purchases)
     model1.add_constraints(sum(x[i,j] * p[i][j] for j in s_labels) <= M - 1 for i in i_labels)

     # each used shop is visited
     model1.add_constraints((sum(x[i,j] for i in i_labels) <= 1000 * s[j] for j in s_labels))

     # each visited shop is traveled to
     model1.add_constraints(sum(e[k,j] for k in s_labels if k != j) >= s[j] for j in s_labels)

     # each traveled from shop is visited
     model1.add_constraints(sum(e[k,j] for j in s_labels if j != k) <= s[k] for k in s_labels)

     # enforce proper tour
     model1.add_constraints(u[k] - u[j] + 1 <= (num_shops - 2) * (1 - e[k,j]) for k in s_labels  if k > 0 for j in s_labels)

     return model1
        