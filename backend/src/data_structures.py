# data_structures.py

class Vehicle:
    def __init__(self, vehicle_id, vehicle_type, capacity, location):
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.capacity = capacity
        self.location = location

class EvacuationPoint:
    def __init__(self, point_id, capacity, location):
        self.point_id = point_id
        self.capacity = capacity
        self.location = location

class Route:
    def __init__(self, start, end, intermediate_points=[]):
        self.start = start
        self.end = end
        self.intermediate_points = intermediate_points
