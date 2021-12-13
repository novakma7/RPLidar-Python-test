import serial
import time
import struct



def RPlidar_Get_info():
    #GET_INFO 0x50
    values = bytearray([0xA5, 0x50])
    ser.write(values)
    
    time.sleep(0.05) #wait for 0.05 second
    
    Rx_buffer = []
    
    while ser.in_waiting:
        data_in = ser.read()
        #print (data_in)
        for x in data_in:
            Rx_buffer.append(x) 
            #print("0x%X,"%(x), end = '') #print without line break
    
    #decode answer
    #print(Rx_buffer)
    print("RPlidar model: 0x%X,"%(Rx_buffer[7]))
    print("RPlidar firmware minor: 0x%X,"%(Rx_buffer[8]))            
    print("RPlidar firmware major: 0x%X,"%(Rx_buffer[9]))
    print("RPlidar HW: 0x%X,"%(Rx_buffer[10]))
    rplidar_serial_num = Rx_buffer[11:27]
    print("RPlidar Serial number: ")
    print ('[{}]'.format(', '.join(hex(x) for x in rplidar_serial_num)))
    

def RPlidar_Get_health():
    #GET_HEALTH 0x52
    values = bytearray([0xA5, 0x52])
    ser.write(values)
    
    time.sleep(0.05) #wait for 0.05 second
    
    Rx_buffer = []
    
    while ser.in_waiting:
        data_in = ser.read()
        #print (data_in)
        for x in data_in:
            Rx_buffer.append(x) 
            #print("0x%X,"%(x), end = '') #print without line break
    
    #decode answer
    #print(Rx_buffer)
    if Rx_buffer[7] == 0:
        print("RPlidar status GOOD")
    if Rx_buffer[7] == 1:
        print("RPlidar status WARNING")
    if Rx_buffer[7] == 2:
        print("RPlidar status ERROR")
                        
    error_code = Rx_buffer[9] *256 + Rx_buffer[8]
    print("RPlidar error code: 0x%X,"%(error_code))            
        
def RPlidar_reset():
    #RESET 0x40
    values = bytearray([0xA5, 0x40])
    ser.write(values)
    #does not return any answer
    print("RPlidar reset") 


def RPlidar_stop():
    #STOP 0x25
    values = bytearray([0xA5, 0x25])
    ser.write(values)
    #does not return any answer
    print("RPlidar stop") 
    
    #set motor pwm to 0
    values = bytearray([0xA5, 0xF0, 0x02, 0x00, 0x00, 0x57])
    #values = bytearray([0xA5, 0x25])
    ser.write(values)

    #set DTR to stop motor spinning
    ser.setDTR(True)
    
    


def RPlidar_SET_MOTOR_PWM(pwm):
    
    #DTR has to be low to make the motor spin
    ser.setDTR(False)
    
    #A5 F0 02 94 02 C1
    values = bytearray([0xA5, 0xF0, 0x02, 0x94, 0x02, 0xC1])
    #values.append(0x7f)
    
    #pwm = 660
    #payload = struct.pack("<H", pwm)
    
    ser.write(values)
    #does not return any answer
    print("RPlidar SET_MOTOR_PWM") 


def RPlidar_Force_scan():
    #FORCE SCAN 0x21
    values = bytearray([0xA5, 0x21])
    ser.write(values)
    #response packet is 7 bytes long and is
    # 0xA5,0x5A,0x5,0x0,0x0,0x40,0x81
    print("RPlidar FORCE SCAN") 
    
    data_in = ser.read(7)
    #print (data_in)
    for x in data_in:
        print("0x%X,"%(x), end = '') #print without line break

    print("")


#main program

ser = serial.Serial('com17', 115200,serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=1.0 )

RPlidar_Get_info()
RPlidar_Get_health()
#RPlidar_reset()
#RPlidar_stop()

#time.sleep(2)

RPlidar_SET_MOTOR_PWM(660)

time.sleep(5)
RPlidar_stop()


""""
#start receiving lidar data even when the lidar is not spinning

start_time = time.time()

RPlidar_Force_scan()
time.sleep(0.1) #wait for 0.05 second

Rx_buffer = [] #empty variable
#acquire data from serial line
while True:
    #sample data for 1 seconds
    if ( time.time() > (start_time + 1) ):
        #break while 
        break
    
    while ser.in_waiting:
        data_in = ser.read()
        #print (data_in)
        for x in data_in:
            Rx_buffer.append(x) 
            print("0x%X,"%(x), end = '') #print without line break

        if ( time.time() > (start_time + 1) ):
            #break while 
            break
        
#process data
#data is organized in groups of 5 bytes
# quality, angle [6:0], angle [14:7], distance [7:0], distance[15:8]

quality =  Rx_buffer[0] >> 2;
angle =  Rx_buffer[2] + (Rx_buffer[1] >> 1);
distance =  Rx_buffer[4] + Rx_buffer[3];

print("")
print("quality: %d,"%(quality))
print("angle: %d,"%(angle))
print("distance: %d,"%(distance))

print("END")

"""