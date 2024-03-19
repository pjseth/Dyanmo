from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value
import random

# Sample data (replace with your actual data)
num_people = 5
num_modes = 3
num_nodes = 4

# Adjusted Capacity and Availability to make the problem feasible
Capacity = {0: 8, 1: 10, 2: 15}
Availability = {0: 1, 1: 1, 2: 1}

# Sample data with adjusted Capacity and Availability
Time = {(i, m, a, b): i * 10 + m * 5 + a * 3 + b * 2 for i in range(num_people) for m in range(num_modes) for a in range(num_nodes) for b in range(num_nodes)}
Demand = {i: 1 for i in range(num_people)}
TrafficCongestion = {(m, a, b): random.uniform(1.0, 2.0) for m in range(num_modes) for a in range(num_nodes) for b in range(num_nodes)}

# Create the LP problem
model = LpProblem(name="EvacuationProblem", sense=LpMinimize)

# Decision variables
x = {(i, j): LpVariable(name=f"x_{i}_{j}", cat="Binary") for i in range(num_people) for j in range(num_modes)}

# Objective function with traffic simulation
print(x)
for i in range(num_people):
    for j in range(num_modes):
        for a in range(num_modes):
            for b in range(num_modes):
                model += lpSum((Time[i, j, a, b] * TrafficCongestion[j, a, b]) * x[i, j]), "TotalEvacuationTime"

# Capacity constraints
for j in range(num_modes):
    model += lpSum(Demand[i] * x[i, j] for i in range(num_people)) <= Capacity[j], f"CapacityConstraint_{j}"

# Availability constraints
for j in range(num_modes):
    model += lpSum(Demand[i] * x[i, j] for i in range(num_people)) <= Availability[j], f"AvailabilityConstraint_{j}"

# Assignment constraints
for i in range(num_people):
    model += lpSum(x[i, j] for j in range(num_modes)) == 1, f"AssignmentConstraint_{i}"

# Mode availability constraints
for i in range(num_people):
    for j in range(num_modes):
        if Availability[j] == 0:
            model += x[i, j] == 0, f"ModeAvailabilityConstraint_{i}_{j}"

# Solve the problem
model.solve()

# Display the results
print("Status:", value(model.status))
print("Total Evacuation Time:", value(model.objective))
print("Assignment:")
for i in range(num_people):
    for j in range(num_modes):
        if value(x[i, j]) == 1:
            print(f"Person {i} uses Mode {j}")