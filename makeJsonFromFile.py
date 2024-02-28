import random
import json
import pandas as pd

def find_lat_lon(input):

    coordTranslate ={
        
    }
    return coordTranslate[input]

def generate_random_number(x, y):
    return random.randint(x, y)

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
    
    id = 1
    per_hour = 3600 
    per_km = 0
    start = []
    end = []
    capacity = [50,15,15,15,15,30,15]
    vehicle = make_vehicle(id,per_hour,per_km,start,end,capacity)
    data['vehicles'].append(vehicle)

    print(data)
    with open("test.json",'w', encoding="utf-8") as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False))
#make_json()
def read_file():
    try:
        with open("Data2023.txt", 'r') as f:
            df = pd.read_csv(f, sep=",", names=['BusStop','Skill','BusRoute'])
            print(df)
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred:", e)
    data = df.groupby(['BusStop','Skill']).size()
    print(data)
    for row, value in data.items():
        print(f"Bus Stop: {row[0]} Skill: {row[1]} Count: {value}")
        #print(find_lat_lon(str(row[0])))
read_file()



    