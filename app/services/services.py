from fastapi import FastAPI, HTTPException
from typing import List, Dict, Optional
import googlemaps
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import pandas as pd

app = FastAPI()

API_KEY = 'AIzaSyDErHVOpa4XB1Iewo2mWU6Y44I7OelMWSE'  # Replace with your actual API key
gmaps = googlemaps.Client(key=API_KEY)

# Define the depot
depot = {
    'location': (29.399013114383962, -98.52633476257324)
}

# Define the shipments
shipments = [
    {'name': 'Santa\'s Place', 'location': (29.417361, -98.437544)},
    {'name': 'Los Barrios', 'location': (29.486833, -98.508355)},
    {'name': 'Jacala', 'location': (29.468601, -98.524849)},
    {'name': 'Nogalitos', 'location': (29.394394, -98.530070)},
    {'name': 'Alamo Molino', 'location': (29.351701, -98.514740)},
    {'name': 'Jesse and Sons', 'location': (29.435115, -98.593962)},
    {'name': 'Walmart', 'location': (29.417867, -98.680534)},
    {'name': 'City Base Entertainment', 'location': (29.355400, -98.445857)},
    {'name': 'Combat Medic Training', 'location': (29.459497, -98.434057)}
]

# Define a function to build the distance matrix
def build_distance_matrix(depot, shipments, measure='distance'):
    try:
        origins = [depot['location']] + [shipment['location'] for shipment in shipments]
        destinations = origins
        dm_response = gmaps.distance_matrix(origins=origins, destinations=destinations)
        dm_rows = [row['elements'] for row in dm_response['rows']]
        distance_matrix = [[item[measure]['value'] for item in dm_row] for dm_row in dm_rows]
        return distance_matrix
    except Exception as e:
        print(f'Something went wrong building the distance matrix: {e}')
        return None

def create_data_model(distance_matrix, num_vehicles):
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = distance_matrix
    data['num_vehicles'] = num_vehicles
    data['depot'] = 0
    return data

def extract_routes(num_vehicles, manager, routing, solution):
    routes = {}
    for vehicle_id in range(num_vehicles):
        routes[vehicle_id] = []
        index = routing.Start(vehicle_id)
        while not routing.IsEnd(index):
            routes[vehicle_id].append(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
        routes[vehicle_id].append(manager.IndexToNode(index))
    return routes

def print_solution(num_vehicles, manager, routing, solution):
    max_route_distance = 0
    for vehicle_id in range(num_vehicles):
        index = routing.Start(vehicle_id)
        plan_output = f'Route for vehicle {vehicle_id}:\n'
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += f' {manager.IndexToNode(index)} -> '
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        plan_output += f'{manager.IndexToNode(index)}\n'
        plan_output += f'Cost of the route: {route_distance}\n'
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    print(f'Maximum route cost: {max_route_distance}')

def generate_solution(data, manager, routing):  
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint
    dimension_name = 'Distance'
    
    # Option 1: Comment out the distance constraint if unnecessary
    # routing.AddDimension(
    #     transit_callback_index,
    #     0,  # no slack
    #     max_travel_distance,  # vehicle maximum travel distance
    #     True,  # start cumul to zero
    #     dimension_name)
    # distance_dimension = routing.GetDimensionOrDie(dimension_name)
    # distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    
    # Use a more flexible heuristic
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.GLOBAL_CHEAPEST_ARC

    # Solve the problem
    solution = routing.SolveWithParameters(search_parameters)
    return solution


def solve_vrp_for(distance_matrix, num_vehicles):
    data = create_data_model(distance_matrix, num_vehicles)
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)
    solution = generate_solution(data, manager, routing)
    
    if solution:
        print_solution(num_vehicles, manager, routing, solution)
        routes = extract_routes(num_vehicles, manager, routing, solution)
        return routes
    else:
        print('No solution found.')
        return None

@app.get("/distance_matrix", response_model=List[List[int]])
async def get_distance_matrix():
    distance_matrix = build_distance_matrix(depot, shipments, 'distance')
    if distance_matrix is not None:
        return distance_matrix
    else:
        raise HTTPException(status_code=500, detail="Error building distance matrix")

@app.get("/vrp_solution", response_model=Optional[Dict[int, List[int]]])
async def get_vrp_solution(num_vehicles: int):
    distance_matrix = build_distance_matrix(depot, shipments, 'distance')
    if distance_matrix is not None:
        routes = solve_vrp_for(distance_matrix, num_vehicles)
        if routes is not None:
            return routes
        else:
            raise HTTPException(status_code=500, detail="No solution found for the given number of vehicles")
    else:
        raise HTTPException(status_code=500, detail="Error building distance matrix")
