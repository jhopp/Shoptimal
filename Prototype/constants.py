M = 120 * 10000 # a very large number!

# data generator defaults
PRICE_RANGE = (0.1, 20.0)
STOCK_RANGE = (1, 50)
LOC_RANGE = (0, 100)
NUM_ITEMS = 12
NUM_PRODUCTS = max(150, NUM_ITEMS) # at least as many products as items
MAX_ITEM_QUANT = 10
NUM_ROUTES = 10 # additional routes to be generated (aside from walking)
TRAVEL_COST_RANGE = (1, 8)