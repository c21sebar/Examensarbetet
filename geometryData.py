import json
import os






    
def make_geo(engine,iteration,year,period):




    folder_path = f"Data/{year}/{iteration}/{engine}/Routes/"
    total_cost = 0
    amount = [0,0,0,0,0,0]
    service = 0
    duration = 0
    waiting_time = 0
    distance = 0
    routes =[]
    count =0
    for filename in os.listdir(folder_path):
        if filename.endswith(".json") and f"p{period}" in filename:
            count +=1
            file_path = os.path.join(folder_path, filename)
            print(file_path)
            # Open the JSON file and load the data
            with open(file_path, 'r', encoding="utf-8") as f:
               json_data = json.load(f)
            # Access the 'cost' key and add it to the total cost
            #print(f"Filename: {filename} Cost: {json_data.get('cost', 0)}")
            total_cost += json_data.get('cost', 0)
            service += json_data.get('service',0)
            duration += json_data.get('duration',0)
            waiting_time += json_data.get('waiting_time',0)
            distance += json_data.get('distance',0)
            add_amount = json_data.get('amount',0)
            amount = [amount + add_amount for amount, add_amount in zip(amount, add_amount)]
            #json_data['vehicle'] = count
            routes.append(json_data)
    

    vehicles = []
    folder_path = f"Data/{year}/{iteration}/{engine}/Input/"
    for filename in os.listdir(folder_path):
        if filename.endswith(".json") and f"p{period}" in filename:
            count +=1
            file_path = os.path.join(folder_path, filename)
            print(file_path)
            # Open the JSON file and load the data
            with open(file_path, 'r', encoding="utf-8") as f:
               json_data = json.load(f)
            vehicles += json_data.get('vehicles')
            #vehicles.append(v)
    jobs = []
    folder_path = f"Data/{year}/{iteration}/{engine}/Input/"
     
    '''
    for filename in os.listdir(folder_path):
        if filename.endswith(".json") and f"p{period}" in filename:
            count +=1
            file_path = os.path.join(folder_path, filename)
            print(file_path)
            # Open the JSON file and load the data
            with open(file_path, 'r', encoding="utf-8") as f:
               json_data = json.load(f)
            v = json_data.get('jobs')
            jobs.append(v)
    '''
    
    shipments = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json") and f"p{period}" in filename and "return" in filename:
            count +=1
            file_path = os.path.join(folder_path, filename)
            print(file_path)
            # Open the JSON file and load the data
            with open(file_path, 'r', encoding="utf-8") as f:
               json_data = json.load(f)
            shipments += json_data.get('shipments')
            #shipments += v
    for filename in os.listdir(folder_path):
        if filename.endswith(".json") and f"p{period}" in filename and not "return" in filename and "tw1" in filename:
            count +=1
            file_path = os.path.join(folder_path, filename)
            print(file_path)
            # Open the JSON file and load the data
            with open(file_path, 'r', encoding="utf-8") as f:
               json_data = json.load(f)
            shipments += json_data.get('shipments')
           # shipments.append(v)
    
    unassigned = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json") and f"p{period}" in filename and not "return" in filename and "tw8" in filename:
            count +=1
            file_path = os.path.join(folder_path, filename)
            print(file_path)
            # Open the JSON file and load the data
            with open(file_path, 'r', encoding="utf-8") as f:
               json_data = json.load(f)
            try:
                unassigned += json_data.get('unassigned')
                #unassigned.append(v)
            except Exception as e:
                print("All shipment delivered", e)
                   
    summary = {
        "cost": total_cost,
        "unassigned": unassigned,
        "amount": amount,
        "service": service,
        "duration": duration,
        "waiting_time": waiting_time,
        "distance": distance
    }
    
    solution = {    
        "code": 0,
        "summary":summary,
        "unassigned":unassigned,
        "routes": routes
    }
    total = {
        "vehicles":vehicles,
        "jobs":jobs,
        "shipments":shipments,
        "solution": solution
    }
    #print(f"Total cost: {total_cost}")
    
    with open(f"Data/{year}/{iteration}/{engine}/map_total_route_p{period}.json",'w', encoding="utf-8") as f:
        f.write(json.dumps(total, indent=2, ensure_ascii=False))


test_runs = 30
periods = 2
max_years = 23
for x in range(13,max_years+1):
    year = x
    for a in range(1,periods+1):
        filename = f"data20{year}_p{a}"
        for iteration in range(1,test_runs+1):
            
            engine = "osrm"
            engine = str(engine).upper()
            make_geo(engine,iteration,year,a)

            engine = "valhalla"
            engine = str(engine).upper()
            make_geo(engine,iteration,year,a)

            engine = "ors"
            engine = str(engine).upper()
            make_geo(engine,iteration,year,a)