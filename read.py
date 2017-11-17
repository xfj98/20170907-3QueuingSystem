def reading(ser):
    import serial
    import time


    
    buffer = b''
    startFlag = False
    
    count = 0
    while True:
        num = ser.inWaiting()

        if num > 0:
            
            time1 = time.time()
            buffer = buffer + ser.read(num)
            #ser.reset_input_buffer()
            startFlag = True
            
       
        while startFlag == True:
            num = ser.inWaiting()
            
            if num > 0: 
                time1 = time.time()
                buffer = buffer + ser.read(num)
                #ser.reset_input_buffer()
            #del num
            time2 = time.time()
               
            if (time2 - time1) > 0.02:
                startFlage = False
                break
        count = count + 1   
        del num

        if buffer != b'':
            break
            
        if buffer == b'\r\n':
            break
        else:
            if count > 10:
                return buffer
            #buffer == b''
            
            
            
            
    #ser.close()
    return buffer

def sending(ser,data):
    #import serial
    #ser = serial.Serial('com1',57600)

    send = ser.write(data)

    #ser.close()
