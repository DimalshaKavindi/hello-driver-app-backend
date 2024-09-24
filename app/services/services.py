import requests
import csv
import json
import urllib
import pandas as pd
from fastapi import FastAPI, HTTPException
from typing import List
from datetime import datetime
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

app = FastAPI()

def time_to_minutes(time_str):
    """Convert time string (e.g., '8:00AM') to minutes since midnight."""
    dt = datetime.strptime(time_str, '%I:%M%p')
    return (dt.hour-8) * 60 + dt.minute

def read_data_from_csv(file_path):
    df = pd.read_csv(file_path)
    addresses = df[['location_latitude', 'location_longitude']].values.tolist()
    demands = df['order_weight'].tolist()
    
    # Convert time windows to hours
    time_windows = []
    for from_time, to_time in zip(df['from'], df['to']):
        from_minute = time_to_minutes(from_time)
        to_minute = time_to_minutes(to_time)
        time_windows.append((from_minute, to_minute))
    
    return addresses, demands, time_windows


def create_data():
    file_path = r'D:\Intern\hello-driver-app-backend\app\models\orders.csv'
    addresses, demands, time_windows = read_data_from_csv(file_path)
    
    data = {}
    data['API_key'] = 'AIzaSyDErHVOpa4XB1Iewo2mWU6Y44I7OelMWSE'
    data['addresses'] = addresses
    data["demands"] = demands
    data["time_windows"] = time_windows
    data["vehicle_capacities"] = [140,50,50]
    data['num_vehicles'] = 3
    data['depot'] = 0
    
    return data


def create_matrix(data):
    addresses = data["addresses"]
    API_key = data["API_key"]
    max_elements = 100
    num_addresses = len(addresses)
    max_rows = max_elements // num_addresses
    q, r = divmod(num_addresses, max_rows)
    dest_addresses = addresses
    distance_matrix = []
    time_matrix = []
    
    for i in range(q):
        origin_addresses = addresses[i * max_rows: (i + 1) * max_rows]
        response = send_request(origin_addresses, dest_addresses, API_key)
        distance_matrix += build_distance_matrix(response)
        time_matrix += build_time_matrix(response)

    if r > 0:
        origin_addresses = addresses[q * max_rows: q * max_rows + r]
        response = send_request(origin_addresses, dest_addresses, API_key)
        distance_matrix += build_distance_matrix(response)
        time_matrix += build_time_matrix(response)
    return distance_matrix,time_matrix

def send_request(origin_addresses, dest_addresses, API_key):
    def build_address_str(addresses):
        address_str = ''
        for i in range(len(addresses)):
        # Each address should be formatted as 'lat,lng'
            lat, lng = addresses[i]
            address_str += f'{lat},{lng}'
            if i < len(addresses) - 1:
                address_str += '|'
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

def build_time_matrix(response):
    time_matrix = []
    for row in response['rows']:
        row_list = [row['elements'][j]['duration']['value'] for j in range(len(row['elements']))]
        # Convert seconds to minutes (or any unit you prefer)
        row_list = [time // 60 for time in row_list]  # Time in minutes
        time_matrix.append(row_list)
    return time_matrix

def create_data_model():
    """Stores the data for the problem, including both distance and time matrices."""
    data = {}
    data_model = create_data()
    distance_matrix, time_matrix = create_matrix(data_model)
    
    data['distance_matrix'] = distance_matrix     # In meter
    data['time_matrix'] = time_matrix             # In minutes
    data["time_windows"] = data_model["time_windows"]
    data["demands"] = data_model["demands"]
    data["vehicle_capacities"] = data_model["vehicle_capacities"]
    data["num_vehicles"] = data_model["num_vehicles"]
    data["depot"] = data_model["depot"]
    
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

def time_callback(from_index, to_index, data, manager):
        """Returns the travel time between the two nodes."""
        # Convert from routing variable Index to time matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['time_matrix'][from_node][to_node]

def solve_vrp():
    """Solves the CVRP and returns a structured solution."""
    data = create_data_model()
    #Create node index to variable index mapping
    manager = pywrapcp.RoutingIndexManager(len(data['time_matrix']), len(data['vehicle_capacities']), data['depot']) 
    routing = pywrapcp.RoutingModel(manager)

    # Time callback
    def time_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['time_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(time_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Time dimension
    time = 'Time'
    routing.AddDimension(
        transit_callback_index,
        10,  # allow waiting time
        1900,  # maximum time
        False,
        time)
    time_dimension = routing.GetDimensionOrDie(time)

    # Add time window constraints
    for location_idx, time_window in enumerate(data['time_windows']):
        if location_idx == data['depot']:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])

    depot_idx = data['depot']
    for vehicle_id in range(len(data['vehicle_capacities'])):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(
            data['time_windows'][depot_idx][0],
            data['time_windows'][depot_idx][1])

    for i in range(len(data['vehicle_capacities'])):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i)))
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.End(i)))

    # Capacity constraint
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,
        data['vehicle_capacities'],
        True,
        "Capacity")

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        print_solution(data, manager, routing, solution)
        result = {}
        for vehicle_id in range(len(data['vehicle_capacities'])):
            index = routing.Start(vehicle_id)
            vehicle_route = []
            vehicle_loads = []
            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                vehicle_route.append(node_index)
                vehicle_loads.append(data['demands'][node_index])
                index = solution.Value(routing.NextVar(index))
            vehicle_route.append(manager.IndexToNode(index))  # End node
            result[vehicle_id] = {
                'route': vehicle_route,
                'loads': vehicle_loads,
            }
        return result
    else:
        raise HTTPException(status_code=500, detail="No solution found!")


def format_solution(data, manager, routing, solution):
    """Formats the solution into a structured dictionary."""
    routes = {}
    total_distance = 0
    total_load = 0

    for vehicle_id in range(len(data['vehicle_capacities'])):
        index = routing.Start(vehicle_id)
        route = []
        route_distance = 0
        route_load = 0

        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route.append(node_index)
            route_load += data['demands'][node_index]
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)

        # Capture end point and stats for each vehicle
        routes[vehicle_id] = {
            "route": route,
            "distance": route_distance,
            "load": route_load
        }
        total_distance += route_distance
        total_load += route_load

    # Final solution data
    return {
        "routes": routes,
        "total_distance": total_distance,
        "total_load": total_load
    }

# function to print the results/solution
def print_solution(data, manager, routing, solution):
    print(f'Objective: {solution.ObjectiveValue()}')  # The objective function
    time_dimension = routing.GetDimensionOrDie('Time')
    total_time = 0
    total_distance = 0
    total_loadLB = 0
    
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_loadLB = 0
        
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            node_index = manager.IndexToNode(index)
            
            # Display node index, time, and load in one line
            plan_output += f'{node_index} Time({solution.Min(time_var)},{solution.Max(time_var)}) Load({route_loadLB}) -> '
            
            # Accumulate the route load
            route_loadLB += data['demands'][node_index]
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            
            # Accumulate distance for the current arc
            route_distance += data['distance_matrix'][manager.IndexToNode(previous_index)][manager.IndexToNode(index)]
        
        # Final stop at the depot
        time_var = time_dimension.CumulVar(index)
        node_index = manager.IndexToNode(index)
        
        # Add the final stop details (the depot) to the plan
        plan_output += f'{node_index} Time({solution.Min(time_var)},{solution.Max(time_var)}) Load({route_loadLB})\n'
        
        # Display the total time, distance, and load for the vehicle
        plan_output += f'Time of the route: {solution.Min(time_var)} min\n'
        plan_output += f'Distance of the route: {route_distance} m\n'
        plan_output += f'Load of the route: {route_loadLB}\n'
        
        # Print the result for the current vehicle
        print(plan_output)
        
        # Update totals across all vehicles
        total_distance += route_distance
        total_loadLB += route_loadLB
        total_time += solution.Min(time_var)
    
    # Print the overall totals for all vehicles
    print(f'Total time of all routes: {total_time} min')
    print(f'Total distance of all routes: {total_distance} m')
    print(f'Total load of all routes: {total_loadLB}')
