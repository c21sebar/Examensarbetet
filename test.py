import itertools
import random
import json

global_best_cost = {'cost': 0, 'version': 0, "counter": 0}

def generate_random_number(x, y):
    return random.randint(x, y)

def calculate_cost(permutation,counter):
    # This function should calculate the cost of a given permutation
    # You need to implement this function according to your specific cost calculation logic
    # For demonstration, let's assume the cost is the sum of elements
    # Example usage:
    y = counter + permutation[0]
    x = permutation[0] - 1
    random_number = generate_random_number(x, y)
   # print("")
   # print("Random number between", x, "and", y, ":", random_number)
    total = random_number
   # print(total)
    return total

def permutations_dfs(elements, visited=None, current_permutation=None, counter=None, previous_cost=None, best_cost=None):
    if visited is None:
        visited = set()
    if current_permutation is None:
        current_permutation = []
    if counter is None:
        counter = [0]
    if previous_cost is None:
        previous_cost = [0]
    if best_cost is None:
        best_cost = {'cost': 9999, 'version': 9999}
        best_cost['cost'] = 0
        best_cost['version']= 1


    if len(current_permutation) == len(elements):
        counter[0] += 1
        current_cost = calculate_cost(current_permutation,counter[0])
       # print(f"{counter[0]}: {current_permutation}, Cost: {current_cost}, Previous Cost: {previous_cost[0]}")
        previous_cost[0] = current_cost
        if current_cost > best_cost['cost']:
            best_cost['cost'] = current_cost 
            best_cost['version'] = counter[0]
            global_best_cost['cost'] = current_cost 
            global_best_cost['version'] = counter[0] 
            global_best_cost['counter'] = counter    
               
           # print(f"Best Cost: {best_cost['cost']}, Best permutation: {best_cost['version']} ")
        return

    for element in elements:
        if element not in visited:
            visited.add(element)
            current_permutation.append(element)
            permutations_dfs(elements, visited, current_permutation, counter, previous_cost, best_cost)
            visited.remove(element)
            current_permutation.pop()
   # print(f"Final --  Best Cost: {best_cost['cost']}, Best permutation: {best_cost['version']} ")
# Create a list of elements
elements = list(range(8, 0, -1))  # Reverse order
# Traverse the permutations using DFS
permutations_dfs(elements)

print(f"Elements: {elements}")
print(f"Final --  Best Cost: {global_best_cost['cost']}, Best permutation: {global_best_cost['version']} Counter: {global_best_cost['counter']}")

def dfs_vroom():
    best_cost = {'cost': 999999, 'version': 0}
    numbers = 9
    count = 0
    for a in range(1,numbers):
        #inital 8 routes for V1 7.45
        count += 1
        for b in range(1,numbers - 1):
            #Each route create route for V2 8.45 and return of 7.45 at 9.15
            count += 1
            for c in range(1,numbers - 2):
                #Each route create route for V1 9.45 and return of 8.45 at 10.15
                count += 1
                for d in range(1,numbers - 3):
                    #Each route create route for V2 10.45 and return of 9.45 at 11.15
                    count += 1
                    for e in range(1,numbers - 4):
                        #Each route create route for V1 11.45 and return of 10.45 at 12.15
                        count += 1
                        for f in range(1,numbers - 5):
                            #Each route create route for V2 12.45 and return of 11.45 at 13.15
                            count += 1
                            for g in range(1,numbers - 6):
                                #Each route create route for V1 13.45 and return of 12.45 at 14.15
                                count += 1
                                for h in range(1,numbers - 7):
                                    #Each route create route for V2 14.45 and return of 13.45 at 15.15  
                                    count += 1
                                    #Create route for V1 return of 14.45 at 16.15
                                    count += 1
                                    #Merge all routes for final route:
                                    
                                    random_number = generate_random_number(1, 100000)
                                    cost = random_number
                                    if cost < best_cost['cost']:
                                        #Compare with cheapest route and save route if cheaper cost                            
                                        #count += 1
                                        #count += 1 
                                        best_cost['cost']=cost
                                        best_cost['version']=count
                                        print(f"New best route found, Cost: {cost}, version {count}")                                   
                                    #print(f"a: {a} b: {b} c: {c} d: {d} e: {e} f: {f} g: {g} h: {h} count: {count}")
    print(f"End of loop {count}")
dfs_vroom()

def best_cost(costMethod,cost_array):       
    if costMethod=="min":                    
            best_cost_value = min(cost_array)  
            print(f"New Best Cost: {best_cost_value}")
    elif costMethod=="max":
            best_cost_value = max(cost_array)  
            print(f"New Best Cost: {best_cost_value}")
    return best_cost_value

def bfs_vroom(costMethod):
    print("Hello World!")
    #Chose cost method, Keeping Max cost or Keeping Min cost or Keep Max cost for TW1 and TW2
    if costMethod == "min":
        print("CostMethod min")        
    elif costMethod == "max":
        print("CostMethod max")
    elif costMethod == "mix":
        print("CostMethod mix")
    else:
        print("No costMethod found, exit")
        exit()
    
    best_cost_value_1 = None
    best_cost_value_2 = None
    best_cost_value_3 = None
    best_cost_value_4 = None
    best_cost_value_5 = None
    best_cost_value_6 = None
    best_cost_value_7 = None
    best_cost_value_8 = None
    cost_array = [1,4,3,2,6]
    #Generate 8 routes for TW1 open start
    for i in range(1,9):
        
        #Read cost from each json outout and save 'best' as per costMethod
        best_cost_value_1 = best_cost(costMethod,cost_array)
    #Generate 7 routes for TW2 open start
    for i in range(1,8):
        
        #Read cost from each json outout and save 'best' as per costMethod
        best_cost_value_2 = best_cost(costMethod,cost_array)

    #Generate 6 routes for TW3 but V.start is now Badet.
    for i in range(1,7):
        
        #Read cost from each json outout and save 'best' as per costMethod
        best_cost_value_3 = best_cost(costMethod,cost_array)
    #Generate return of TW1 (V.TW2.Arrive)
    reversed_num = int(str(best_cost_value_1)[::-1])
    print(f"Reversed of bcv_1: {reversed_num}")
    
    #Generate 5 routes for TW4 but V.start is now end of return of TW1
    print(f"Last of bcv_1: {(best_cost_value_1 % 10)}")
    for i in range(1,6):
        
        #Read cost from each json outout and save 'best' as per costMethod
        best_cost_value_4 = best_cost(costMethod,cost_array)

    #Generate return of TW2 (V.TW3.Arrive)
    #Generate 4 routes for TW5 but V.start is now end of return of TW2

    #Generate return of TW3 (V.TW4.Arrive)
    #Generate 3 routes for TW6 V.start is now end of return of TW3
    
    #Generate return of TW4 (V.TW5.Arrive)
    #Generate 2 routes for TW7 V.start is now end of return of TW4

    #Generate return of TW5 (V.TW6.Arrive)
    #Generate 1 routes for TW8 V.start is now end of return of TW5
    #Generate return of TW6 (V.TW7.Arrival)
   
    #Generate return of TW7 (V.TW8.Arrival)
    #Generate return of TW8 but start is now end of return of TW6
    
    #Merge all routes
        
    #Total of 16 input files and 16 output files + one input and output for mergedfile
bfs_vroom("max")

def make_shipment(amount,id,pickup,p_desc,delivery,d_desc):
    shipment ={
        "amount":amount,
        "pickup":{
            "id": id,
            "description": p_desc,
            "location": pickup
        },
        "delivery":{
            "id": id,
            "description": d_desc,
            "location": delivery
        }
    }
    return shipment
def make_vehicle(id,per_hour,per_km,start,end,capacity):
    if id == None:
        id = generate_random_number(1000,10000)
    if per_hour == None and per_km== None:
        per_hour = 3600
    if end == None:
        end = []
    if capacity == None:
        capacity = [0,0,0,0,0,0,0]
    if start == None:        
        vehicle ={
                "id":id,
                "cost":{
                    "per_hour": per_hour,
                    "per_km": per_km            
                },                
                "end":end,
                "capacity": capacity
        }
    else:
        vehicle ={
            "id":id,
            "cost":{
                "per_hour": per_hour,
                "per_km": per_km            
            },
            "start":start,
            "end":end,
            "capacity": capacity
        }
    return vehicle
def make_json():
    data = {
        "vehicles":[],
        "shipments":[]
    }
    amount= [20, 5, 5, 5, 5, 0, 0]
    id =1
    pickup = []
    p_desc = ""
    delivery = []
    d_desc = ""
    shipment = make_shipment(amount,id,pickup,p_desc,delivery,d_desc)
    data['shipments'].append(shipment)
    
    amount= [15, 5, 5, 5, 0, 0, 0]
    id =2
    pickup = []
    p_desc = "Mellby"
    delivery = []
    d_desc = "Framnäs Badet"
    shipment = make_shipment(amount,id,pickup,p_desc,delivery,d_desc)
    data['shipments'].append(shipment)

    id = 1
    per_hour = 3600 
    per_km = 0
    start = []
    end = []
    capacity = [50,15,15,15,15,30,15]
    vehicle = make_vehicle(id,per_hour,per_km,start,end,capacity)
    data['vehicles'].append(vehicle)

    id = None
    per_hour = 3600 
    per_km = 0
    start = None
    end = None
    capacity = None
    vehicle = make_vehicle(id,per_hour,per_km,start,end,capacity)
    data['vehicles'].append(vehicle)

    print(data)
    with open("test.json",'w', encoding="utf-8") as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False))
make_json()