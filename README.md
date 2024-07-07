# Shoptimal
Shoptimal is an application which creates an efficient schedule of shops to visit to complete a shopping list. It takes into consideration the time required to complete the tour and the total cost of purchasing the items.

## Running the application
Running main.py starts the application. The required libraries can be found in 'requirements.txt'. The current application creates output in the console only.

## Input data
The input data is automatically generated and read as part of the application execution. Product and shop names can be modified in 'product_names.txt' and 'shop_names.txt' respectively.

## Algorithms
The following scheduling algorithms have been implemented:
#### 1. BasicScheduler
Greedy scheduler that iterates over the shops in an arbitrary order, purchasing any required items when possible. The purpose of this scheduler is to act as a benchmark for other schedulers, as it is not very efficient.
#### 2. BestPriceScheduler
Creates a schedule with the lowest possible monetary cost. For each item on the shopping list, it finds the shop where this item is cheapest and creates a decision to purchase the item at that shop accordingly. It sorts the purchase decisions so each shop is only visited once, but otherwise does not take travel time into account. The purpose of this scheduler is to serve as a lower bound of the cost any schedule can have given some input data.
#### 3. Model1Scheduler
Uses a linear programming model (DOcplex) to create a schedule, optimising for both the monetary cost and the travel time of the schedule. As this involves multi-objective optimisation, the scheduler has weight parameters to scale the importance of the cost or time. This model considers only a single costless route between any pair of shops.
#### 4. Model2Scheduler
Expands upon the previous linear programming model by allowing for multiple routes between pairs of shops with varying cost and time.

## Limitations
The schedulers do not currently take into account item/product quantities and shop opening/closing times.
