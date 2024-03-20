import random
import json
import pandas as pd
import subprocess
import os
from Data import data_locations 
from datetime import datetime, timedelta




def find_lat_lon(input):
    coordTranslate = data_locations.get_coord_dict()
    
    return coordTranslate[input]
def lat_lon_to_name(value):
    dictionary = data_locations.get_coord_dict()

    for key,val in dictionary.items():
        if val == value:
            #print(f"KEY: {key} VAL: {val} VALUE: {val} ")
            return key
    print(f"VALUE NOT FOUND: {value}")
    return None
    
def generate_random_number(x, y):
    return random.randint(x, y)

def make_shipment(amount,id,pickup,p_desc,delivery,d_desc,tw,return_route,tw2):
    service = 60
    if tw != []:        
        if return_route == 0 and tw2==[]:
            shipment ={
                "amount":amount,
                "pickup":{
                    "id": id,
                    "description": p_desc,
                    "location": pickup,
                    "service": service
                },
                "delivery":{
                    "id": id,
                    "description": d_desc,
                    "location": delivery,
                    "time_windows": tw
                }
            }
        elif return_route == 0 and tw2!=[]:
            shipment ={
                "amount":amount,
                "pickup":{
                    "id": id,
                    "description": p_desc,
                    "location": pickup,
                    "time_windows": tw2,
                    "service": service
                },
                "delivery":{
                    "id": id,
                    "description": d_desc,
                    "location": delivery,
                    "time_windows": tw
                }
            }
        elif return_route == 1 or return_route == 2:
            shipment ={
                "amount":amount,
                "pickup":{
                    "id": id,
                    "description": p_desc,
                    "location": pickup,
                    "time_windows": tw
                },
                "delivery":{
                    "id": id,
                    "description": d_desc,
                    "location": delivery,
                    "service": service
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


def make_vehicle(id,per_hour,per_km,start,end,capacity,tw,profile):
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
                "profile":profile,
                "costs":{
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
            "profile":profile,
            "costs":{
                "per_hour": per_hour,
                "per_km": per_km            
            },
            "start":start,            
            "capacity": capacity,
        }
        if tw != []:
             vehicle ={
            "id":id,
            "profile":profile,
            "costs":{
                "per_hour": per_hour,
                "per_km": per_km            
            },
            "start":start,
            "capacity": capacity,
            "time_window": tw
        }
    return vehicle


def make_json(vehicles,filename,timeH,timeM,retrun_start,prev_end_time,return_route,engine,iteration,year):
    data = {
        "vehicles":[],
        "shipments":[]
    }
    #"Data/{engine}_{iteration}_{filename}.txt"
    names_list,amount_list = read_file(filename,engine,iteration,year)
    

    
    for i,name in enumerate(names_list):
        #print(i,name,amount_list[i])
        if name != '':
            amount= amount_list[i]
            id = i
            tw2= []
            if return_route == 1 or return_route == 2:
                pickup = find_lat_lon("Framnäs Badet")
                pickup.reverse()
                p_desc = "Framnäs Badet"
                delivery = find_lat_lon(name)
                delivery.reverse()
                d_desc = name
                if return_route == 1:
                    tw=[[timeH*3600 + timeM*60 , timeH*3600 + (timeM+2)*60]]
                elif return_route == 2:
                    tw=[[timeH*3600 + timeM*60 + 3600*2, timeH*3600 + timeM*60 + 3600*3]]
                else:
                    tw = []                    
            
            else:
                pickup = find_lat_lon(name)
                pickup.reverse()
                p_desc = name
                delivery = find_lat_lon("Framnäs Badet")
                delivery.reverse()
                d_desc = "Framnäs Badet"
                tw = [[timeH * 3600 + timeM * 60, timeH*3600 + (timeM + 2) * 60]]
                if prev_end_time !=0:
                    tw2 = [[prev_end_time, timeH * 3600 + (timeM-5) * 60]]
            shipment = make_shipment(amount,id,pickup,p_desc,delivery,d_desc,tw,return_route,tw2)
            data['shipments'].append(shipment)
    
    num_of_vehicles = vehicles
    #print("\n \n \n")
    #print(engine)
    #print("\n \n \n")
    if engine == "ORS":
        profile = "driving-car"
        #print(profile)
    elif engine == "VALHALLA":
        profile = "auto"
        #print(profile)
    elif engine == "OSRM":
        profile = "car"   
        #print(profile)     
    else:
        profile = "car"
        #print("Else")
    for i in range(1,num_of_vehicles+1):
        id = i
        per_hour = 0 
        per_km = 1
        tw = []
        if retrun_start != "":
            #print(f"START LOCATION IS {retrun_start} ")
            start = find_lat_lon(retrun_start)
            start.reverse()
            end = []
            if return_route == 1:
                tw = [timeH * 3600 + timeM * 60, (timeH + 1)*3600 + (timeM + 30)* 60]
            elif return_route == 2:
                tw = [prev_end_time, prev_end_time + 3600*4]
            elif return_route == 0 and prev_end_time != 0:
                tw = [prev_end_time, timeH * 3600 + (timeM + 10) * 60]
           #print(start)  
        elif retrun_start == "" or None:
            start = []     
            end = find_lat_lon("Framnäs Badet")
            end.reverse()
        capacity = [55,24,24,24,24,35]
        vehicle = make_vehicle(id,per_hour,per_km,start,end,capacity,tw,profile)
        data['vehicles'].append(vehicle)

    #print(data)
      #  Data/{iteration}/{engine}/Data/{filename}.txt
    #"Data/{iteration}/{engine}/Input/{filename}"
    with open(f"Data/{year}/{iteration}/{engine}/Input/{filename}.json",'w', encoding="utf-8") as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False))
    return filename



def read_file(filename,engine,iteration,year):
    try:
        with open(f"Data/{year}/{iteration}/{engine}/Data/{filename}.txt", 'r') as f:
            df = pd.read_csv(f, sep=",", names=['BusStop','Skill','BusRoute'],encoding='utf-8')
            #print(df)
    except FileNotFoundError:
        print(f"READ FILE: File not found. Data/{year}/{iteration}/{engine}/Data/{filename}.txt")
    except Exception as e:
        print("READ FILE: An error occurred:", e)
    data = df.groupby(['BusStop','Skill']).size()
    #print(data)
    prev_name =""
    amount = [0,0,0,0,0,0]
    ready_amount = []
    all_names = []
    for row, value in data.items():
        #print(f"*** ROW: {row} LEVEL: {row[1]} VALUE: {value} ***")
        if row[0] == prev_name or prev_name == "":
            amount[int(row[1])] = value
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
            amount[int(row[1])] = value
            #amount.insert(row[1],value)
            all_names.append(prev_name)
            #print(amount)
        prev_name = row[0]
        #print(f"Bus Stop: {row[0]} Skill: {row[1]} Count: {value} Amount: {amount}")
        #print(find_lat_lon(str(row[0])))
    #print(sum(amount))
    total = sum(amount)
    amount[0] = total
    #amount.insert(0, total)    
    ready_amount.append(amount)
    all_names.append(prev_name)
    #print(ready_amount)
    #print(all_names)
    return(all_names,ready_amount)


def read_cost_output(json_routes):
    cost_array = []
    if 'routes' in json_routes: 
        for item in json_routes['routes']:
                cost = item['cost']
                cost_array.append(cost)
                #print(item['cost'])
        #print(cost_array)
    else:
        print("Key 'routes' not found") 
    return cost_array

def best_cost(costMethod,cost_array):
    if cost_array != []:       
        if costMethod=="min":                    
                best_cost_value = min(cost_array) 
                index = cost_array.index(best_cost_value) 
                #print(f"New Best Cost: {best_cost_value} and Index is: {index}")
        elif costMethod=="max":
                best_cost_value = max(cost_array)  
                index = cost_array.index(best_cost_value) 
                #print(f"New Best Cost: {best_cost_value} and Index is: {index}")
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


def remove_shipment_from_file(shipments_to_remove,in_filename,engine,iteration,year):
    #print(f"DEBUG: TIMEWINDOW {in_filename} to create next data file. SHHIPMENT TO REMOVE: {shipments_to_remove}")
    try:
        with open(f"Data/{year}/{iteration}/{engine}/Data/{in_filename}.txt", 'r') as f:
            df = pd.read_csv(f, sep=",", names=['BusStop','Skill','BusRoute'],encoding='utf-8')
            df2 = pd.DataFrame(columns=df.columns)
            df2.to_csv(f'Data/{year}/{iteration}/{engine}/Data/return_{in_filename}.txt', sep=',',header=0, index=False, encoding='utf-8')
            for item in shipments_to_remove:
                df2 = df[df['BusStop'] == item]
                df2.to_csv(f'Data/{year}/{iteration}/{engine}/Data/return_{in_filename}.txt',mode='a', sep=',',header=0, index=False, encoding='utf-8')

            for item in shipments_to_remove:
                df = df[df['BusStop'] != item]
                #print(f"REMOVE SHIPMENT {item}")
            #print(df)       
    except FileNotFoundError:
        print("Remove Shipment: File not found.")
    except Exception as e:
        print("*** Remove Shipment: An error occurred:", e)
     
    
    """   
    suffix = int(tw[2:])  # Extract the numerical part after "tw"
    if 1 <= suffix < 8:
         tw = "tw" + str(suffix + 1)

    else:
        # Handle the case when suffix is out of range
        print("Suffix out of range.")

    """
    suffix_str=""
    for char in reversed(in_filename):
        if char.isdigit():
            suffix_str = char + suffix_str
        else:
            break
    suffix = int(suffix_str)
    suffix += 1
    in_filename = in_filename[:-len(suffix_str)] + str(suffix)

    try:
     
       df.to_csv(f'Data/{year}/{iteration}/{engine}/Data/{in_filename}.txt', sep=',',header=0, index=False, encoding='utf-8')
    
    except FileNotFoundError:
        print("Remove Shipment: File not found.")
    except Exception as e:
        print("Remove Shipment: An error occurred:", e)

def save_routes_and_remove(in_filename,costMethod,tw,engine,iteration,year):
    filename = f"Data/{year}/{iteration}/{engine}/Output/output_" + in_filename + ".json"
    json_file = read_json_file(filename)
    cost_array = read_cost_output(json_file)
    best_cost_value_1,index = best_cost(costMethod,cost_array)
    #print(f"Best Cost Value: {best_cost_value_1} With Index: {index}")
    if 'routes' in json_file:
        routes = json_file['routes']
    tw1_start_loc = ""
    tw1_duration = 0
    end_loc = ""
    timestamp = 0
    shipments_to_remove = []
    if best_cost_value_1 != -1 or index != -1:
            
        with open(f"Data/{year}/{iteration}/{engine}/Routes/routes_{in_filename}.json",'w', encoding="utf-8") as tw1_file:
            tw1_file.write(json.dumps(routes[index], indent=2, ensure_ascii=False))
        tw1 = routes[index]
        steps = tw1.get('steps', [])
        
        for item in steps:
            timestamp = item['arrival']
            if 'description' in item:
                desc = item['description']
                if shipments_to_remove == []:
                    tw1_start_loc = desc
                if desc != "Framnäs Badet":
                    shipments_to_remove.append(desc)
                    #print(f"Description: {desc}")
                    #print(f"Arrival: {str(timedelta(seconds=timestamp))}")
            else:
                print("Description not found for this step.")
        tw1_duration = tw1['duration']
        #print(shipments_to_remove)
        #print(tw1_start_loc)
        end_loc = shipments_to_remove[-1]
        #print(f"End Location: {end_loc}")
        #print(f"Last Arrival: {str(timedelta(seconds=timestamp))}")
        #print(tw1_duration)
    if tw != 1: 
        remove_shipment_from_file(shipments_to_remove,in_filename,engine,iteration,year)
        shipments_to_remove.clear()
    return best_cost_value_1,tw1_start_loc,tw1_duration, end_loc,timestamp

def run_vroom(inputfile,engine,iteration,year):
    #print(f"Sending new request to VROOM...{inputfile}")
    location = f"Data/{year}/{iteration}/{engine}/Input/"+ inputfile + ".json"
    result = f"Data/{year}/{iteration}/{engine}/Output/output_" + inputfile + ".json"
    #, '|', '\'.\''
    if engine == "OSRM":
        subprocess.run(['sudo', '../vroom/bin/vroom', '-i', location, '-o', result], capture_output=True)
    elif engine == "ORS":
        subprocess.run(['sudo', '../vroom/bin/vroom', '-i', location, '-o', result, '-r', 'ors', '-p', 'driving-car:8080', '-a', 'driving-car:0.0.0.0/ors/v2' ], capture_output=True)
    elif engine == "VALHALLA":
        subprocess.run(['sudo', '../vroom/bin/vroom', '-i', location, '-o', result, '-r', 'valhalla', '-p', 'auto:8002', '-a', 'auto:0.0.0.0'], capture_output=True)
    #print("VROOM Done!")


def bfs_vroom(costMethod,engine,filename,iteration,year):
    #print("Hello World!")
    start_time = datetime.now()
    str(costMethod).lower()
    #Chose cost method, Keeping Max cost or Keeping Min cost or Keep Max cost for TW1 and TW2
    mix = 0
    if costMethod == "min":
        print("CostMethod min")        
    elif costMethod == "max":
        print("CostMethod max")
    elif costMethod == "mix":
        print("CostMethod mix")
        mix = 1
        #costMethod = "max"
    else:
        print("No costMethod found, exit")
        exit()
    
    data = filename
    engine = str(engine).upper()
    if mix == 1:
        costMethod = "max"

    #make_json(VEHICLES,DATASET,TIME_H,TIME_M,START_LOC,DELIVERY/RETURN) 0 = DELIVERY 1 = RETURN
    #Generate 8 routes for TW1 open start
    tw1_start_time = 6*3600 + 45*60 # EARLIEST A SHIPMENT-PICKUP CAN BE PICKED UP
    tw1_filename = make_json(8, data + 'tw1',7,45,"",tw1_start_time,0,engine,iteration,year) # input for vroom
    #method to run vroom to get output.json
    run_vroom(tw1_filename,engine,iteration,year)
    best_cost_value_1,tw1_start_loc,tw1_duration, tw1_end_loc, tw1_end_time = save_routes_and_remove(tw1_filename,costMethod,0,engine,iteration,year)
    #print(f"BEST COST OF ROUTE ONE: {best_cost_value_1} TW1 START: {tw1_start_loc} TW1 DURATION: {tw1_duration}")
     
    
    #Generate 7 routes for TW2 open start
    # OR use second best route of TW1
    tw2_start_time = 7*3600 + 45*60
    tw2_filename = make_json(7,data + 'tw2',8,45,"Framnäs Badet",tw2_start_time,0,engine,iteration,year)
    #method to run vroom to get output.json
    run_vroom(tw2_filename,engine,iteration,year)
    best_cost_value_2,tw2_start_loc,tw2_duration, tw2_end_loc, tw2_end_time = save_routes_and_remove(tw2_filename,costMethod,0,engine,iteration,year)
    #print(f"BEST COST OF ROUTE TWO: {best_cost_value_2} TW2 START: {tw2_start_loc} TW2 DURATION: {tw2_duration}")
    
    
    #Generate 6 routes for TW3 but V.start is now Badet.
    #OR use start location to third best route of TW1.
    tw3_start_time = 8*3600 + 45*60
    tw3_filename = make_json(6,data + 'tw3',9,45,"Framnäs Badet",tw3_start_time,0,engine,iteration,year)
    #method to run vroom to get output.json
    run_vroom(tw3_filename,engine,iteration,year)
    best_cost_value_3,tw3_start_loc,tw3_duration, tw3_end_loc, tw3_end_time = save_routes_and_remove(tw3_filename,costMethod,0,engine,iteration,year)
    #print(f"BEST COST OF ROUTE THREE: {best_cost_value_3} TW3 START: {tw3_start_loc} TW3 DURATION: {tw3_duration}")

   
    
    #Generate return of TW1 (V.TW2.Arrive) (Revers route of TW1)    
    tw1_r_filename = make_json(1,'return_' + data + 'tw1',9,15,"Framnäs Badet",0,1,engine,iteration,year)
    run_vroom(tw1_r_filename,engine,iteration,year)
    best_cost_value_tw1_r,tw1_r_start_loc,tw1_r_duration, tw1_r_end_loc, tw1_r_end_time = save_routes_and_remove(tw1_r_filename,costMethod,1,engine,iteration,year)
    #print(f"**** #### {best_cost_value_tw1_r,tw1_r_start_loc,tw1_r_duration} ")
   
   
   
    if mix == 1:
        costMethod = "min"



    #Generate 5 routes for TW4 but V.start is now end of return of TW1
    #OR Use foruth best route from TW1 with start of end of TW1
    tw4_filename = make_json(5, data + 'tw4',10,45,tw1_r_end_loc,tw1_r_end_time,0,engine,iteration,year)
    #method to run vroom to get output.json
    run_vroom(tw4_filename,engine,iteration,year)
    best_cost_value_4,tw4_start_loc,tw4_duration, tw4_end_loc, tw4_end_time = save_routes_and_remove(tw4_filename,costMethod,0,engine,iteration,year)
    
    #print(f"BEST COST OF ROUTE FOUR: {best_cost_value_4} TW4 START: {tw4_start_loc} TW4 DURATION: {tw4_duration}")
    ##Generate return of TW2 (V.TW3.Arrive)
    tw2_r_filename = make_json(1,'return_' + data + 'tw2',10,15,"Framnäs Badet",0,1,engine,iteration,year)
    run_vroom(tw2_r_filename,engine,iteration,year)
    best_cost_value_tw2_r,tw2_r_start_loc,tw2_r_duration, tw2_r_end_loc, tw2_r_end_time = save_routes_and_remove(tw2_r_filename,costMethod,1,engine,iteration,year)
    
    #Generate 4 routes for TW5 but V.start is now end of return of TW2
    tw5_filename = make_json(4,data + 'tw5',11,45,tw2_r_end_loc,tw2_r_end_time,0,engine,iteration,year)
    run_vroom(tw5_filename,engine,iteration,year)
    best_cost_value_5,tw5_start_loc,tw5_duration, tw5_end_loc, tw5_end_time = save_routes_and_remove(tw5_filename,costMethod,0,engine,iteration,year)
    #print(f"BEST COST OF ROUTE FIVE: {best_cost_value_5} TW5 START: {tw5_start_loc} TW4 DURATION: {tw5_duration}")
    
    #OR Use fifth best route from TW1 with start of end of TW2
    #Generate return of TW3 (V.TW4.Arrive)
    tw3_r_filename = make_json(1,'return_' + data + 'tw3',11,15,"Framnäs Badet",0,1,engine,iteration,year)
    run_vroom(tw3_r_filename,engine,iteration,year)
    best_cost_value_tw3_r,tw3_r_start_loc,tw3_r_duration, tw3_r_end_loc, tw3_r_end_time = save_routes_and_remove(tw3_r_filename,costMethod,1,engine,iteration,year)
    
    #Generate 3 routes for TW6 V.start is now end of return of TW3
    #OR Use sixth best route from TW1 with start of end of TW3
    tw6_filename = make_json(3,data + 'tw6',12,45,tw3_r_end_loc,tw3_r_end_time,0,engine,iteration,year)
    run_vroom(tw6_filename,engine,iteration,year)
    best_cost_value_6,tw6_start_loc,tw6_duration, tw6_end_loc, tw6_end_time = save_routes_and_remove(tw6_filename,costMethod,0,engine,iteration,year)
    #print(f"BEST COST OF ROUTE SIX: {best_cost_value_6} TW6 START: {tw6_start_loc} TW4 DURATION: {tw6_duration}")
    
    #Generate return of TW4 (V.TW5.Arrive)
    tw4_r_filename = make_json(1,'return_' + data + 'tw4',12,15,"Framnäs Badet",0,1,engine,iteration,year)
    run_vroom(tw4_r_filename,engine,iteration,year)
    best_cost_value_tw4_r,tw4_r_start_loc,tw4_r_duration, tw4_r_end_loc, tw4_r_end_time = save_routes_and_remove(tw4_r_filename,costMethod,1,engine,iteration,year)
    
    #Generate 2 routes for TW7 V.start is now end of return of TW4
    #OR Use seventh best route from TW1 with start of end of TW4
    
    tw7_filename = make_json(2,data + 'tw7',13,45,tw4_r_end_loc,tw4_r_end_time,0,engine,iteration,year)
    run_vroom(tw7_filename,engine,iteration,year)
    best_cost_value_7,tw7_start_loc,tw7_duration, tw7_end_loc, tw7_end_time = save_routes_and_remove(tw7_filename,costMethod,0,engine,iteration,year)
    #print(f"BEST COST OF ROUTE SEVEN: {best_cost_value_7} TW7 START: {tw7_start_loc} TW7 DURATION: {tw7_duration} TW4 RETURN END TIME: {tw4_r_end_time}")
    #Generate return of TW5 (V.TW6.Arrive)
    
    tw5_r_filename = make_json(1,'return_' + data + 'tw5',13,15,"Framnäs Badet",0,1,engine,iteration,year)
    run_vroom(tw5_r_filename,engine,iteration,year)
    best_cost_value_tw5_r,tw5_r_start_loc,tw5_r_duration, tw5_r_end_loc, tw5_r_end_time = save_routes_and_remove(tw5_r_filename,costMethod,1,engine,iteration,year)

    #Generate 1 routes for TW8 V.start is now end of return of TW5
    #OR Use eight best route from TW1 with start of end of TW5
    
    #print("TIME WINDOW 8 START")
    tw8_filename = make_json(1,data + 'tw8',14,45,tw5_r_end_loc,tw5_r_end_time,0,engine,iteration,year)
    run_vroom(tw8_filename,engine,iteration,year)
    best_cost_value_8,tw8_start_loc,tw8_duration, tw8_end_loc, tw8_end_time = save_routes_and_remove(tw8_filename,costMethod,0,engine,iteration,year)
    #print(f"BEST COST OF ROUTE EIGHT: {best_cost_value_8} TW8 START: {tw8_start_loc} TW8 DURATION: {tw8_duration}")

    #Generate return of TW6 (V.TW7.Arrival)
    #print("RETURN TW6")
    tw6_r_filename = make_json(1,'return_' + data + 'tw6',14,15,"Framnäs Badet",0,1,engine,iteration,year) 
    run_vroom(tw6_r_filename,engine,iteration,year)
    best_cost_value_tw6_r,tw6_r_start_loc,tw6_r_duration, tw6_r_end_loc, tw6_r_end_time = save_routes_and_remove(tw6_r_filename,costMethod,1,engine,iteration,year)
    
    #Generate return of TW7 (V.TW8.Arrival)
    #print("RETURN TW7")
    tw7_r_filename = make_json(1,'return_' + data + 'tw7',15,15,"Framnäs Badet",0,1,engine,iteration,year)
    run_vroom(tw7_r_filename,engine,iteration,year)
    best_cost_value_tw7_r,tw7_r_start_loc,tw7_r_duration, tw7_r_end_loc, tw7_r_end_time = save_routes_and_remove(tw7_r_filename,costMethod,1,engine,iteration,year)
    
    #Generate return of TW8 but start is now end of return of TW6
    #make sure to calc route from end of tw6_return to Badet to reach 16.15
    tw8_r_filename = make_json(1,'return_' + data + 'tw8',14,15,tw6_r_end_loc,tw6_r_end_time,2,engine,iteration,year) 
    run_vroom(tw8_r_filename,engine,iteration,year)
    best_cost_value_tw8_r,tw8_r_start_loc,tw8_r_duration, tw8_r_end_loc, tw8_r_end_time = save_routes_and_remove(tw8_r_filename,costMethod,1,engine,iteration,year)

    #make_json(1,'data2023tw8_return',(14,15 + tw6_duration),tw6_start_loc,0)    
    
    #Merge all routes
        
    #Total of 16 input files and 16 output files + one input and output for mergedfile
    end_time = datetime.now()
    total = end_time - start_time
    print(f"\n\n\n*!*!*!*!*!*! TOTAL TIME: {total}*!*!*!*!*!*!  \n\n\n\n")
    return total



def calculate_total(engine,iteration,year,period):
    folder_path = f"Data/{year}/{iteration}/{engine}/Routes/"
    total_cost = 0
    for filename in os.listdir(folder_path):
        if filename.endswith(".json") and f"p{period}" in filename:
            file_path = os.path.join(folder_path, filename)
            print(file_path)
            # Open the JSON file and load the data
            with open(file_path, 'r', encoding="utf-8") as f:
               json_data = json.load(f)
            # Access the 'cost' key and add it to the total cost
            print(f"Filename: {filename} Cost: {json_data.get('cost', 0)}")
            total_cost += json_data.get('cost', 0)
    #print(f"Total cost: {total_cost}")
    return total_cost
#Request route - (return if have delivered or pickup if have returned)
#Run vroom on dataset with current position of vehicle that requested
#Output chosen node based on cost_method
#Remove from dataset and add to return dataset



def read_route(file_path,wf):
    try:
        path = ""
        with open(file_path, 'r', encoding="utf-8") as f:
            json_data = json.load(f)
            prev_name = "0000"
            path = "START: "
            # Access the 'cost' key and add it to the total cost
            for item in json_data.get('steps', 0):      
                loc = item['location'] 
                loc.reverse()            
                arrival = item['arrival']
                td = timedelta(seconds=arrival)
                #print(f"Type: {item['type']} Location: {item['location']} Name: {lat_lon_to_name(loc)}")
                if lat_lon_to_name(loc) == None:
                    print(f"*** VALUE NOT FOUND FOR: {item['description']} ***",file=wf)
                else:                     
                    name = str(lat_lon_to_name(loc))
                   
                    if prev_name != name:
                        if path == "START: ":
                            path += name + " @ " + str(td)
                        else:
                            path += " --> " + name + " @ " + str(td)   
                        prev_name = name                
            print(path,file=wf)
    except FileNotFoundError:
        print(f"READ FILE: File not found. {file_path}",file=wf)
    except Exception as e:
        print("READ FILE: An error occurred:", e,file=wf)
    
def dispaly_all_routes(filename,engine,iteration,year,total_cost,time_taken):
    
    
    with open(f"Data/{year}/{iteration}/{engine}/Final_route_{filename}.txt", 'w',encoding="utf-8") as f:
        #745 tw1
        #VEHICLE 1 PATH
        path = f"Data/{year}/{iteration}/{engine}/Routes/routes_"
        return_path = f"Data/{year}/{iteration}/{engine}/Routes/routes_return_"
        #print(f"TOTAL COST: {total_cost} \n",file=f)
        #print(f"TOTAL TIME TAKEN: {time_taken} \n",file=f)
        print(f"TOTAL_COST,TIME_TAKEN,ALL_DELIVERED",file=f)
        with open(f"Data/{year}/{iteration}/{engine}/Data/{filename}tw9.txt", 'r') as f2:
                df = pd.read_csv(f2, sep=",", names=['BusStop','Skill','BusRoute'],encoding='utf-8')
                #print(df)
                if df.empty:
                    print(f"{total_cost},{time_taken},YES",file=f)
                    print("\n",file=f)
                   # print("ALL SHIPMENTS DELIVERED \n",file=f)
                else:
                    print(f"{total_cost},{time_taken},NO",file=f)
                    #print("SOME SHIPMENTS ARE UNDELIVERED",file=f)
                    print(df)
                    print("\n",file=f)
        print("VEHICLE 1 Path",file=f)
        print("TIME WINDOW 1 TRANSPORT TO LOCATION",file=f)
        read_route(path + filename + "tw1.json",f)
        #845 tw2 (skulle kunna vara VEHICLE 2)
        print("TIME WINDOW 2 TRANSPORT TO LOCATION",file=f)
        read_route(path + filename + "tw2.json",f)
        #945 tw3
        print("TIME WINDOW 3 TRANSPORT TO LOCATION",file=f)
        read_route(path + filename + "tw3.json",f)
        #1015 r_tw2
        print("TIME WINDOW 2 RETURN PATH",file=f)
        read_route(return_path + filename + "tw2.json",f)
        #1145 tw5
        print("TIME WINDOW 5 TRANSPORT TO LOCATION",file=f)
        read_route(path + filename + "tw5.json",f)
        #1215 r_tw4
        print("TIME WINDOW 4 RETURN PATH",file=f)
        read_route(return_path + filename + "tw4.json",f)
        #1345 tw7
        print("TIME WINDOW 7 TRANSPORT TO LOCATION",file=f)
        read_route(path + filename + "tw7.json",f)
        #1415 r_tw6
        print("TIME WINDOW 6 RETURN PATH",file=f)
        read_route(return_path + filename + "tw6.json",f)
        #1615 r_tw8
        print("TIME WINDOW 8 RETURN PATH",file=f)
        read_route(return_path + filename + "tw8.json",f)
        print("",file=f)
        
        
        #VEHICLE 2 PATH
        print("VEHICLE 2 Path",file=f)
        #915 r_tw1
        print("TIME WINDOW 1 RETURN PATH",file=f)
        read_route(return_path + filename + "tw1.json",f)
        #1045 tw4
        print("TIME WINDOW 4 TRANSPORT TO LOCATION",file=f)
        read_route(path + filename + "tw4.json",f)
        #1115 r_tw3 
        print("TIME WINDOW 3 RETURN PATH",file=f)
        read_route(return_path + filename + "tw3.json",f)
        #1245 tw6
        print("TIME WINDOW 6 TRANSPORT TO LOCATION",file=f)
        read_route(path + filename + "tw6.json",f)
        #1315 r_tw5
        print("TIME WINDOW 5 RETURN PATH",file=f)
        read_route(return_path + filename + "tw5.json",f)
        #1445 tw8
        print("TIME WINDOW 8 TRANSPORT TO LOCATION",file=f)
        read_route(return_path + filename + "tw8.json",f)
        #1515 r_tw7
        print("TIME WINDOW 7 RETURN PATH",file=f)
        read_route(return_path + filename + "tw7.json",f)
        print("ALL ROUTES",file=f)
        
def result_to_csv(max_year,periods,test_runs):
    df = pd.DataFrame(columns=['TOTAL_COST','TIME_TAKEN','ALL_DELIVERED','FILENAME'])
    df.to_csv(f'total_results.txt', sep=',', encoding='utf-8',index=False)
    
    for x in range(13,max_year+1):
        year = x
        engine_list = ['ORS','OSRM','VALHALLA']
        for a in range(1,periods+1):
            filename = f"data20{year}_p{a}"
            for engine in engine_list:
                for iteration in range(1,test_runs+1):
                    with open(f"Data/{year}/{iteration}/{engine}/Final_route_{filename}.txt", 'r',encoding="utf-8") as f:
                        df = pd.read_csv(f, sep=",", names=['TOTAL_COST,TIME_TAKEN,ALL_DELIVERED'],encoding='utf-8',nrows=1,header=0)
                        df['FILENAME'] = f"20{year}/{iteration}/{engine}/{filename}"
                        #print("DF START")
                        #print(df)
                        #print("DF END")
                        df.to_csv(f'total_results.txt',mode='a', sep=',',header=0, encoding='utf-8')

test_runs = 30
periods = 2
max_years = 23
experiment_time_start = datetime.now()
for x in range(13,max_years+1):
    year = x
    for a in range(1,periods+1):
        filename = f"data20{year}_p{a}"
        for iteration in range(1,test_runs+1):
            print(filename)
            print(iteration)

            engine = "osrm"
            engine = str(engine).upper()
            time_taken = bfs_vroom("mix", engine,filename,iteration,year)
            total_cost = calculate_total(engine,iteration,year,a)
            dispaly_all_routes(filename,engine,iteration,year,total_cost,time_taken)

            
            engine = "valhalla"
            engine = str(engine).upper()
            time_taken = bfs_vroom("mix", engine,filename,iteration,year)
            total_cost = calculate_total(engine,iteration,year,a)
            dispaly_all_routes(filename,engine,iteration,year,total_cost,time_taken)

            
            engine = "ors"
            engine = str(engine).upper()
            time_taken = bfs_vroom("mix", engine,filename,iteration,year)
            total_cost = calculate_total(engine,iteration,year,a)
            dispaly_all_routes(filename,engine,iteration,year,total_cost,time_taken)
experiment_time_end = datetime.now()
total_time = experiment_time_end - experiment_time_start
print(f"\n\n\n*!*!*!*!*!*! TOTAL EXPERIMENT TIME: {total_time}*!*!*!*!*!*!  \n\n\n\n")
print()

result_to_csv(max_years,periods,test_runs)