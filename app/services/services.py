import requests
import json
import urllib
from fastapi import FastAPI, HTTPException
from typing import List
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

def create_data():
    """Creates the data."""
    data = {}
    data['API_key'] = 'AIzaSyDErHVOpa4XB1Iewo2mWU6Y44I7OelMWSE'
    data['addresses'] = ['3610+Hacks+Cross+Rd+Memphis+TN',  # depot
                        '1921+Elvis+Presley+Blvd+Memphis+TN',
                        '149+Union+Avenue+Memphis+TN',
                        '1034+Audubon+Drive+Memphis+TN',
                        '1532+Madison+Ave+Memphis+TN',
                        '706+Union+Ave+Memphis+TN',
                        '3641+Central+Ave+Memphis+TN',
                        '926+E+McLemore+Ave+Memphis+TN',
                        '4339+Park+Ave+Memphis+TN',
                        '600+Goodwyn+St+Memphis+TN',
                        '2000+North+Pkwy+Memphis+TN',
                        '262+Danny+Thomas+Pl+Memphis+TN',
                        '125+N+Front+St+Memphis+TN',
                        '5959+Park+Ave+Memphis+TN',
                        '814+Scott+St+Memphis+TN',
                        '1005+Tillman+St+Memphis+TN'
                        ]
    return data

def create_distance_matrix(data):
    addresses = data["addresses"]
    API_key = data["API_key"]
    max_elements = 100
    num_addresses = len(addresses)
    max_rows = max_elements // num_addresses
    q, r = divmod(num_addresses, max_rows)
    dest_addresses = addresses
    distance_matrix = []
    
    for i in range(q):
        origin_addresses = addresses[i * max_rows: (i + 1) * max_rows]
        response = send_request(origin_addresses, dest_addresses, API_key)
        distance_matrix += build_distance_matrix(response)

    if r > 0:
        origin_addresses = addresses[q * max_rows: q * max_rows + r]
        response = send_request(origin_addresses, dest_addresses, API_key)
        distance_matrix += build_distance_matrix(response)
    return distance_matrix

def send_request(origin_addresses, dest_addresses, API_key):
    def build_address_str(addresses):
        address_str = ''
        for i in range(len(addresses) - 1):
            address_str += addresses[i] + '|'
        address_str += addresses[-1]
        return address_str

    request = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial'
    origin_address_str = build_address_str(origin_addresses)
    dest_address_str = build_address_str(dest_addresses)
    request = request + '&origins=' + origin_address_str + '&destinations=' + dest_address_str + '&key=' + API_key
    jsonResult = urllib.request.urlopen(request).read()
    response = json.loads(jsonResult)
    return response

def build_distance_matrix(response):
    distance_matrix = []
    for row in response['rows']:
        row_list = [row['elements'][j]['distance']['value'] for j in range(len(row['elements']))]
        distance_matrix.append(row_list)
    return distance_matrix

def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = create_distance_matrix(create_data())
    data["demands"] = [0, 1, 1, 2, 4, 2, 4, 8, 8, 1, 2, 1, 2, 4, 4, 8]
    data["vehicle_capacities"] = [60]
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data

def distance_callback(from_index, to_index, data, manager):
    """Returns the distance between two nodes."""
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return data['distance_matrix'][from_node][to_node]

def demand_callback(from_index, data, manager):
    """Returns the demand of the node."""
    from_node = manager.IndexToNode(from_index)
    return data['demands'][from_node]

def solve_vrp():
    """Solves the CVRP and returns a structured solution."""
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Register distance and demand callbacks.
    transit_callback_index = routing.RegisterTransitCallback(lambda from_index, to_index: distance_callback(from_index, to_index, data, manager))
    demand_callback_index = routing.RegisterUnaryTransitCallback(lambda from_index: demand_callback(from_index, data, manager))

    # Set arc cost evaluator (distance).
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint.
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],
        True,  # start cumul to zero
        "Capacity"
    )

    # Set up search parameters.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    search_parameters.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    search_parameters.time_limit.FromSeconds(1)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Return the solution or raise an error.
    if solution:
        return print_solution(data, manager, routing, solution)
    else:
        raise HTTPException(status_code=500, detail="No solution found!")


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data["demands"][node_index]
            plan_output += f" {node_index} Load({route_load}) -> "
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        plan_output += f" {manager.IndexToNode(index)} Load({route_load})\n"
        plan_output += f"Distance of the route: {route_distance}m\n"
        plan_output += f"Load of the route: {route_load}\n"
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print(f"Total distance of all routes: {total_distance}m")
    print(f"Total load of all routes: {total_load}")


