import serial
import time
#import matplotlib.pyplot as plt
import serial.tools.list_ports
outputR=open('C:/temp/pytestR.txt','a')
outputI=open('C:/temp/pytestI.txt','a')
out=[]
x=[]
y1=[]
y2=[]

outR=[]
outI=[]

ports = serial.tools.list_ports.comports()

for p in ports:
    print(p)
    print('my port')

com_port = input("Enter the COM port to use:   \n")

ser = serial.Serial(com_port, 115200, timeout=2)
ser.flushInput()
ser.flushOutput()
repeat = 1
try:
  while repeat == 1:
    user_input = float(input("Enter electrode spacing (meters):  \n"))
    print(str(user_input))
    outputR.write("Spacing: "+str(user_input) + "\n")
    outputI.write("Spacing: "+str(user_input) + "\n")
    response=""
    print( "Waiting for trigger response")
#    start = "S"
#    print "Send Start"
#    ser.write(start)
#    print "wait for response"
#==============================================================================
#     while response.find('START') == -1:
#         response = ser.readline()
#         print response
#         time.sleep(1)
#==============================================================================
    cR=0
    cI=0
  
    while response.find('START') == -1:        #print "2"
        raw_data = ser.readline()
        response = raw_data.decode()
        print( response)
        time.sleep(1)
    
        finish = 0
        c = 0  
        
    for loop in range(0,12,1):
        

    #    time.sleep(5)
        out=[]
        c=0
        finish=0
        print(loop)
        while finish != 1:
            raw_data=ser.readline()
            a = raw_data.decode()
            print( a)
            if a.find('DONER') == -1:
                out.append(a)
                c += 1
            else:
                finish = 1
    #        time.sleep(1)

        outR.extend(out)
        out=[]
        c=0
        finish=0
        while finish != 1:
            raw_data=ser.readline()
            a = raw_data.decode()
            print( a)
            if a.find('DONEI') == -1:
                out.append(a)
                c += 1
            else:
                finish = 1
    #        time.sleep(1)
        outI.extend(out)
        #for i in range(0,1500,1):
        #  print i
        #  a=ser.readline()
        #  out.append(ser.readline())
    out=[]
    print('end of loop')
    c=0
    finish=0
    while finish != 1:
        raw_data=ser.readline()
        a = raw_data.decode()
        print( a)
        if a.find('DONE') == -1:
            out.append(a)
            c += 1
        else:
            finish = 1
    outR.extend(out)
    outI.extend(out)
    print('done final extend')
    for j in outR:
        outputR.write(j)
        time.sleep(0.01)
        print(j)
        
    for j in outI:
        outputI.write(j)
        time.sleep(0.01)
        print(j)
    user_input = input("Continue (Y/n)")
    if (user_input == "Y") or (user_input == "y"):
        repeat = 1
    else:
        repeat = 0
#==============================================================================
#       a=out[j].split(';')
#       if len(a)==6:
#
#           #print a
#           k=long(a[0])
#           ch0=float(a[1])
#           ch1=float(a[2])
#           ch2=float(a[3])
#           ch3=float(a[4])
#           x.append(k)
#           y1.append(ch1)
#           y2.append(ch2)
#           print j, k, ch0,ch1,ch2,ch3
#          # print j,k
#==============================================================================
except:
    print( 'exception')
finally:
    outputR.close()
    outputI.close()
#==============================================================================
#      a=out[c-2].split(';')
#      TotalTimeMicro=long(a[1])
#      print out[c-2]
#      print out[c-1]
#      recordLength=len(y1)
#      for k in range(0,recordLength,1):
#          x[k]=x[k]*TotalTimeMicro/(recordLength*1000)
#      plt.plot(x,y1)
#      plt.plot(x,y2)
#      plt.show()
#==============================================================================
    ser.close()