import random
import json
import pandas as pd

def find_lat_lon(input):
    coordTranslate ={
        
    }
    return coordTranslate[input]

def generate_random_number(x, y):
    return random.randint(x, y)

def make_shipment(amount,id,pickup,p_desc,delivery,d_desc,tw):
    if tw != []:        
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
                "location": delivery,
                "time_windows": tw
            }
        }
    else:
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
                "location": delivery,                
            }
        } 




    return shipment


def make_vehicle(id,per_hour,per_km,start,end,capacity,tw):
   #print(f"PRINTING MAKE VEHICLE {id,per_hour,per_km,start,end,capacity}")
    if id == None:
        id = generate_random_number(1000,10000)
    if per_hour == None and per_km== None:
        per_hour = 3600
        per_km = 0
    if end == None or "":
        end = []
    if capacity == None:
        capacity = [0,0,0,0,0,0]
    if len(start)==0:  
        #print("START LOCATION OPEN")      
        vehicle ={
                "id":id,
                "cost":{
                    "per_hour": per_hour,
                    "per_km": per_km            
                },                                
                "capacity": capacity,
                "end": end
            }
    elif len(start) != 0:
        #print("START LOCATION HAS VALUE")  
        vehicle ={
            "id":id,
            "cost":{
                "per_hour": per_hour,
                "per_km": per_km            
            },
            "start":start,
            "end": end,
            "capacity": capacity,
        }
        if tw != []:
             vehicle ={
            "id":id,
            "cost":{
                "per_hour": per_hour,
                "per_km": per_km            
            },
            "start":start,
            "end": end,
            "capacity": capacity,
            "time_windows": tw
        }
    return vehicle


def make_json(vehicles,filename,timeH,timeM,retrun_start,return_route):
    data = {
        "vehicles":[],
        "shipments":[]
    }
    names_list,amount_list = read_file(filename)

    

    
    for i,name in enumerate(names_list):
        #print(i,name,amount_list[i])
        amount= amount_list[i]
        id = i
        if return_route == 1:
            pickup = find_lat_lon("Framnäs Badet")
            pickup.reverse()
            p_desc = "Framnäs Badet"
            delivery = find_lat_lon(name)
            delivery.reverse()
            d_desc = name
            tw = []
        else:
            pickup = find_lat_lon(name)
            pickup.reverse()
            p_desc = name
            delivery = find_lat_lon("Framnäs Badet")
            delivery.reverse()
            d_desc = "Framnäs Badet"
            tw = [[timeH * 3600 + timeM * 60, timeH*3600 + (timeM + 10) * 60]]
        shipment = make_shipment(amount,id,pickup,p_desc,delivery,d_desc,tw)
        data['shipments'].append(shipment)
    
    num_of_vehicles = vehicles
    for i in range(1,num_of_vehicles+1):
        id = i
        per_hour = 3600 
        per_km = 0
        tw = []
        if retrun_start != "" or None:
            #print(f"START LOCATION IS {retrun_start} ")
            start = find_lat_lon(retrun_start)
            start.reverse()
            if return_route == 1:
                tw = [[timeH * 3600 + timeM * 60, (timeH + 1)*3600 + (timeM + 30)* 60]]
           #print(start)  
        elif retrun_start == "" or None:
            start = []     
        end = find_lat_lon("Framnäs Badet")
        end.reverse()
        capacity = [50,15,15,15,15,30]
        vehicle = make_vehicle(id,per_hour,per_km,start,end,capacity,tw)
        data['vehicles'].append(vehicle)

    #print(data)
    with open(f"Input/{filename}.json",'w', encoding="utf-8") as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False))




def read_file(filename):
    try:
        with open(f"Data/{filename}.txt", 'r') as f:
            df = pd.read_csv(f, sep=",", names=['BusStop','Skill','BusRoute'])
            #print(df)
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred:", e)
    data = df.groupby(['BusStop','Skill']).size()
    #print(data)
    prev_name =""
    amount = [0,0,0,0,0,0]
    ready_amount = []
    all_names = []
    for row, value in data.items():
        #print(f"*** ROW: {row} LEVEL: {row[1]} VALUE: {value} ***")
        if row[0] == prev_name or prev_name == "":
            amount[row[1]] = value
            #amount.insert(row[1],value)
            #print(amount)
        else:
            #print(sum(amount))
            total = sum(amount)
            amount[0] = total
            #amount.insert(0, total)
            #print(amount)
            ready_amount.append(amount)

            amount= [0,0,0,0,0,0]
            amount[row[1]] = value
            #amount.insert(row[1],value)
            all_names.append(prev_name)
           # print(amount)
        prev_name = row[0]
        #print(f"Bus Stop: {row[0]} Skill: {row[1]} Count: {value} Amount: {amount}")
        #print(find_lat_lon(str(row[0])))
    #print(sum(amount))
    total = sum(amount)
    amount[0] = total
    #amount.insert(0, total)    
    ready_amount.append(amount)
    all_names.append(prev_name)
    print(ready_amount)
    print(all_names)
    return(all_names,ready_amount)


def read_cost_output(json_routes):
    cost_array = []
    for item in json_routes['routes']:
            cost = item['cost']
            cost_array.append(cost)
            #print(item['cost'])
    print(cost_array)
    return cost_array

def best_cost(costMethod,cost_array):
    if cost_array != []:       
        if costMethod=="min":                    
                best_cost_value = min(cost_array) 
                index = cost_array.index(best_cost_value) 
                print(f"New Best Cost: {best_cost_value} and Index is: {index}")
        elif costMethod=="max":
                best_cost_value = max(cost_array)  
                index = cost_array.index(best_cost_value) 
                print(f"New Best Cost: {best_cost_value} and Index is: {index}")
    else:
        best_cost_value = -1
        index = -1
    return best_cost_value,index

def read_json_file(filename):
    try:
        with open(filename, 'r', encoding="utf-8") as f:
            json_file = json.load(f)                       
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred:", e)
    return json_file


def remove_shipment_from_file(shipments_to_remove,tw):
    try:
        with open(f"Data/Data2023{tw}.txt", 'r') as f:
            df = pd.read_csv(f, sep=",", names=['BusStop','Skill','BusRoute'])
            #print(df)
            df2 = pd.DataFrame(columns=df.columns)
            df2.to_csv(f'Data/data2023{tw}_return.txt', sep=',',header=0, index=False, encoding='ANSI')
            for item in shipments_to_remove:
                df2 = df[df['BusStop'] == item]
                df2.to_csv(f'Data/data2023{tw}_return.txt',mode='a', sep=',',header=0, index=False, encoding='ANSI')

            for item in shipments_to_remove:
                df = df[df['BusStop'] != item]
                print(f"REMOVE SHIPMENT {item}")
            #print(df)       
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("***An error occurred:", e)
 
    suffix = int(tw[2:])  # Extract the numerical part after "tw"
    if 1 <= suffix < 8:
         tw = "tw" + str(suffix + 1)
    else:
        # Handle the case when suffix is out of range
        print("Suffix out of range.")
   
    try:
       df.to_csv(f'Data/data2023{tw}.txt', sep=',',header=0, index=False, encoding='ANSI')
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("###An error occurred:", e)

def save_routes_and_remove(filename,costMethod,tw):
    json_file = read_json_file(filename)
    cost_array = read_cost_output(json_file)
    best_cost_value_1,index = best_cost(costMethod,cost_array)
    print(f"Best Cost Value: {best_cost_value_1} With Index: {index}")
    routes = json_file['routes']
    tw1_start_loc = ""
    tw1_duration = 0
    if best_cost_value_1 != -1 or index != -1:
            
        with open(f"Routes/routes_{tw}.json",'w', encoding="utf-8") as tw1_file:
            tw1_file.write(json.dumps(routes[index], indent=2, ensure_ascii=False))
        tw1 = routes[index]
        steps = tw1.get('steps', [])
        shipments_to_remove = []
        for item in steps:
            if 'description' in item:
                desc = item['description']
                if shipments_to_remove == []:
                    tw1_start_loc = desc
                if desc != "Framnäs Badet":
                    shipments_to_remove.append(desc)
                #print(f"Description: {desc}")
                else:
                    print("Description not found for this step.")
        tw1_duration = tw1['duration']
        print(shipments_to_remove)
        print(tw1_start_loc)
        print(tw1_duration)
        
        remove_shipment_from_file(shipments_to_remove,tw)
        shipments_to_remove.clear()
    return best_cost_value_1,tw1_start_loc,tw1_duration



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
    tw1_start_loc = ""
    tw1_duration = 0
    best_cost_value_2 = None
    tw2_start_loc = ""
    tw2_duration = 0
    best_cost_value_3 = None
    best_cost_value_4 = None
    best_cost_value_5 = None
    best_cost_value_6 = None
    best_cost_value_7 = None
    best_cost_value_8 = None
    

    #TODO ADD TIME WINDOW OF VEHICLES!
    #make_json(VEHICLES,DATASET,TIME_H,TIME_M,START_LOC,DELIVERY/RETURN) 0 = DELIVERY 1 = RETURN
    #Generate 8 routes for TW1 open start
    make_json(8,'data2023tw1',7,40,"",0) # input for vroom
    #method to run vroom to get output.json
    best_cost_value_1,tw1_start_loc,tw1_duration = save_routes_and_remove("Output/output.json",costMethod,"tw1")
    print(f"BEST COST OF ROUTE ONE: {best_cost_value_1} TW1 START: {tw1_start_loc} TW1 DURATION: {tw1_duration}")
     

    #Generate 7 routes for TW2 open start
    # OR use second best route of TW1
    
    make_json(7,'data2023tw2',8,40,"",0)
    #method to run vroom to get output.json
    best_cost_value_2,tw2_start_loc,tw2_duration = save_routes_and_remove("Output/output2.json",costMethod,"tw2")
    print(f"BEST COST OF ROUTE TWO: {best_cost_value_2} TW2 START: {tw2_start_loc} TW2 DURATION: {tw2_duration}")
    
    #Generate 6 routes for TW3 but V.start is now Badet.
    #OR use start location to third best route of TW1.

    make_json(6,'data2023tw3',9,40,"Framnäs Badet",0)
    #method to run vroom to get output.json
    best_cost_value_3,tw3_start_loc,tw3_duration = save_routes_and_remove("Output/output3.json",costMethod,"tw3")
    print(f"BEST COST OF ROUTE THREE: {best_cost_value_3} TW3 START: {tw3_start_loc} TW3 DURATION: {tw3_duration}")

    #Generate return of TW1 (V.TW2.Arrive) (Revers route of TW1)    
    make_json(1,'data2023tw1_return',9,15,"Framnäs Badet",1)
    #Generate 5 routes for TW4 but V.start is now end of return of TW1
    #OR Use foruth best route from TW1 with start of end of TW1
    make_json(5,'data2023tw4',10,40,tw1_start_loc,0)
    ##method to run vroom to get output.json
    best_cost_value_4,tw4_start_loc,tw4_duration = save_routes_and_remove("Output/output4.json",costMethod,"tw4")
    print(f"BEST COST OF ROUTE FOUR: {best_cost_value_4} TW4 START: {tw4_start_loc} TW4 DURATION: {tw4_duration}")
    ##Generate return of TW2 (V.TW3.Arrive)

    #Generate 4 routes for TW5 but V.start is now end of return of TW2
    make_json(4,'data2023tw5',11,40,tw2_start_loc,0)
    best_cost_value_5,tw5_start_loc,tw5_duration = save_routes_and_remove("Output/output5.json",costMethod,"tw5")
    print(f"BEST COST OF ROUTE FIVE: {best_cost_value_5} TW5 START: {tw5_start_loc} TW4 DURATION: {tw5_duration}")
    #OR Use fifth best route from TW1 with start of end of TW2
    #Generate return of TW3 (V.TW4.Arrive)
    
    
    #Generate 3 routes for TW6 V.start is now end of return of TW3
    #OR Use sixth best route from TW1 with start of end of TW3
    make_json(3,'data2023tw6',12,40,tw3_start_loc,0)
    best_cost_value_6,tw6_start_loc,tw6_duration = save_routes_and_remove("Output/output6.json",costMethod,"tw6")
    print(f"BEST COST OF ROUTE SIX: {best_cost_value_6} TW6 START: {tw6_start_loc} TW4 DURATION: {tw6_duration}")
    #Generate return of TW4 (V.TW5.Arrive)
    
    
    #Generate 2 routes for TW7 V.start is now end of return of TW4
    #OR Use seventh best route from TW1 with start of end of TW4
    #Generate return of TW5 (V.TW6.Arrive)
    make_json(2,'data2023tw7',13,40,tw4_start_loc,0)
    best_cost_value_7,tw7_start_loc,tw7_duration = save_routes_and_remove("Output/output7.json",costMethod,"tw7")
    print(f"BEST COST OF ROUTE SEVEN: {best_cost_value_7} TW7 START: {tw7_start_loc} TW7 DURATION: {tw7_duration}")


    #Generate 1 routes for TW8 V.start is now end of return of TW5
    #OR Use eight best route from TW1 with start of end of TW5
    make_json(1,'data2023tw8',14,40,tw5_start_loc,0)
    best_cost_value_8,tw8_start_loc,tw8_duration = save_routes_and_remove("Output/output8.json",costMethod,"tw8")
    print(f"BEST COST OF ROUTE EIGHT: {best_cost_value_8} TW8 START: {tw8_start_loc} TW8 DURATION: {tw8_duration}")

    #Generate return of TW6 (V.TW7.Arrival)  
    #Generate return of TW7 (V.TW8.Arrival)
    #Generate return of TW8 but start is now end of return of TW6
    
    #Merge all routes
        
    #Total of 16 input files and 16 output files + one input and output for mergedfile

bfs_vroom("max")


    