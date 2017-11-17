#!/usr/bin/env python
# -*- coding: utf-8 -*-


import serial
import time
from read import reading
from read import sending
from led import send_message

def main():
    
    
    tempLib = []
    time1 = 0
    time2 = 0
    count = 0
    ser = serial.Serial('com1',57600)
    #print(ser.portstr)
    
    while True:
        information = reading(ser)
        index = len(information)
        
        
        if len(information) != 0 and (information != 32):
            if (information[0] == 35) and (information[index-1] == 36):
                info = information.decode('gb2312')
                print(info)
                
                if info.find('name:')!= -1:
                    result1 = info.split('#')[-1].split('$')[0]
                    #将字符串中的空格删除
                    result1 = ''.join(result1.split())
                    
                    result = result1.split('name:')[1:]
                    del info
                    for j in range(0,len(result)):
                        if len(result[j]) != 0:
                            if len(result)!=0:
                                tempLib.extend(result)
                                sending(ser,b'ok')
                            
                    #print(result)
                    #print(len(result[0]))          
                        
                else:
                     sending(ser,'Fail')
    

        if time1 == 0:
            #判断信息是否更新
            if count < len(tempLib):
                resultList = list(tempLib[count])
                print(resultList)
               
                orderNum = str(count+1)
                orderList = list(orderNum)
                del orderNum
                symbol = ':'
                symbolList = list(symbol)
                del symbol
                orderList.extend(symbolList)
                orderList.extend(resultList)
                send_message(orderList)
                

                count+=1
                time1 = time.time()
            
        else:
            time2 = time.time()
           
            if (time2-time1) > 30:
                
            #判断信息是否更新
                if count < len(tempLib):
                    resultList = list(tempLib[count])
                    orderNum = str(count+1)
                    orderList = list(orderNum)
                    del orderNum
                    symbol = ':'
                    symbolList = list(symbol)
                    del symbol
                    orderList.extend(symbolList)
                    orderList.extend(resultList)
                    send_message(orderList)
                    
                    count+=1
                    time1 = time.time()
            else:
                pass

        continue
            


   
main()
print('over')
