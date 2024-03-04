import subprocess



def hello():
    print("Hello World!")
    process1 = subprocess.run(['sudo', '../vroom/bin/vroom', '-i', '../vroom/docs/test.json', '-o', 'test,json','|', '\'.\''], capture_output=True)
    print(process1.stdout.decode())
    print('Command: ' + str(process1.args))
    print('Return Code: ' + str(process1.returncode))
    print('Current Directory : ' + str(subprocess.run(['pwd'])))

def hello2(inputfile):
    print("Sending new request to VROOM...")
    print("Hello World!")
    location = "Input/"+ inputfile
    result = "Output/" + inputfile
    process1 = subprocess.run(['sudo', '../vroom/bin/vroom', '-i', location, '-o', result, '|', '\'.\''], capture_output=True)
   


hello2("data2023tw1.json")