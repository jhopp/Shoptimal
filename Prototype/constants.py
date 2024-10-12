M = 120 * 10000 # a very large number!

# data generator defaults
PRICE_RANGE = (0.1, 20.0)
STOCK_RANGE = (1, 20)
LOC_RANGE = (0, 100)
NUM_ITEMS = 12
NUM_PRODUCTS = max(150, NUM_ITEMS) # at least as many products as items
MAX_ITEM_QUANT = 10
NUM_ROUTES = 10 # additional routes to be generated (aside from walking)
TRAVEL_COST_RANGE = (1, 8)

# ANSI codes (for pretty printing)
CEND      = '\33[0m'
CBOLD     = '\33[1m'

CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
CVIOLET = '\33[35m'
CBLUE2   = '\33[94m'
