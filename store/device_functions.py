import serial.tools.list_ports
from django.http import HttpResponse
import serial
import time


def check_finger_return_id(send_char):
    print("Check fingerprint")

    currentPort = None

    ports = list(serial.tools.list_ports.comports())
    # print("port port is", ports[0])
    for p in ports:
        print(p.description)
        if "CP210x" in p.description:
            currentPort = p
            break

    if currentPort == None:
        print("No device found")
        # TODO:Create a small page with device not found
        # return HttpResponse("No device found")
        return -2
    print("port is", currentPort.device)
    try:
        arduino = serial.Serial(port=currentPort.device,
                                baudrate=9600, timeout=.1)
    except:
        return -3
        # return HttpResponse("Device busy")  # Device busy message

    while(True):
        if(arduino.read().decode('utf-8') == '.'):
            break

    arduino.write(bytes(send_char, 'utf-8'))
    arduino.reset_input_buffer()

    waiting_counter = 0

    while(not arduino.in_waiting):
        print("waiting...")
        waiting_counter = waiting_counter+1
        time.sleep(0.5)
        if(waiting_counter > 30):
            return -4

    fingid = arduino.readline().decode('utf-8')
    print('The detected ID is ', fingid)
    arduino.write(bytes('x', 'utf-8'))

    return int(fingid)


def enroll_finger_with_id(fingId):
    currentPort = None

    ports = list(serial.tools.list_ports.comports())
    # print("port port is", ports[0])
    for p in ports:
        print(p.description)
        if "CP210x" in p.description:
            currentPort = p
            break

    if currentPort == None:
        print("No device found")
        # TODO:Create a small page with device not found
        # return HttpResponse("No device found")
        return -2
    print("port is", currentPort.device)
    try:
        arduino = serial.Serial(port=currentPort.device,
                                baudrate=9600, timeout=.1)
    except:
        return -3
        # return HttpResponse("Device busy")  # Device busy message

    while(True):
        if(arduino.read().decode('utf-8') == '.'):
            break

    arduino.write(bytes('e', 'utf-8'))
    arduino.reset_input_buffer()
    time.sleep(0.5)
    arduino.write(bytes(fingId, 'utf-8'))
    return 0
