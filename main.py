import serial
import serial.tools.list_ports
import time
import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import threading
from threading import Lock
import multiprocessing
from multiprocessing import Process,Event,Queue,freeze_support

ser = serial.Serial()
receivedata=[]
drawdata=[]

serialName = []
port_list = list(serial.tools.list_ports.comports())
for i in port_list:
    serialName.append(i[0])
print(serialName)
# print(tuple(serialName))

window = tk.Tk()  # 创建窗口
window.title('林业雄的串口助手')
window.geometry('900x600')

threadLock = threading.Lock()
var = tk.IntVar()  # 一个变量

def showdata():
    global receivedata
    while True:
        '''
        n = ser.inWaiting()
        s = ser.read(n)
        '''
        s=ser.read_all()
        threadLock.acquire()
        if(s.decode()!=''):
            receivedata.append(s.decode())
        try:
            if (s.decode() != ''):
                drawdata.append(float(s.decode()[:-2]))
        except:
            print("有非数字字符")
        threadLock.release()
        #print(drawdata)
        #print(s.decode())
        t0.insert('end', s)
        time.sleep(0.1)

def senddata():
    while True:
        demo = e0.get().encode()
        ser.write(demo)
        time.sleep(0.1)

def draw():
    a.clear()
    threadLock.acquire()
    if len(receivedata)>5:
        a.plot(receivedata[-5:])
    else:
        a.plot(receivedata)
    threadLock.release()
    plt.pause(0.1)
    canvas.draw()


def startdraw():
    #time.sleep(10)
    for i in range(10):
        time.sleep(2)
        draw()
        plt.pause(3)
        time.sleep(2)

def autodraw():
    if(th2.isAlive()==False):
        th2.start()

def cleardraw():
    a.clear()
    canvas.draw()

def setPort(*args):  # 处理事件，*args表示可变参数
    ser.port = comboxlist0.get()

def setbaudrate(*args):
    ser.baudrate = int(comboxlist1.get())

def setShujv(*args):
    ser.bytesize = int(comboxlist2.get())
check={"N":serial.PARITY_NONE,"E":serial.PARITY_EVEN,"O":serial.PARITY_ODD}
def setcheck(*args):
    ser.parity = check[comboxlist3.get()]

stop={"1":serial.STOPBITS_ONE, "1.5":serial.STOPBITS_ONE_POINT_FIVE, "2":serial.STOPBITS_TWO}
def setstop(*args):
    print(stop[comboxlist4.get()])
    ser.stopbits = stop[comboxlist4.get()]

def go(*args):  # 处理事件，*args表示可变参数
    print(comboxlist.get())  # 打印选中的值


def opencom():
    if (ser.is_open == False):
        ser.open()
    print(ser.is_open)
    #s = ser.readline().decode()
    if(th0.isAlive()==False):
        #print(1)
        #print(th0)
        th0.start()

def send():
    if (ser.is_open == False):
        ser.open()
    print(ser.is_open)
    if(on_hit and th0.isAlive()==False):
        th0.start()
    if(th1.isAlive()==False):
        th1.start()

def clearreceive():
    receivedata.clear()
    t0.delete(0.0, 'end')

on_hit = False

def selection():
    global on_hit
    on_hit=var.get()

label0 = tk.Label(window, text='串口', font=10)
label0.place(y=50, x=50)
label1 = tk.Label(window, text='波特率', font=10)
label1.place(y=100, x=50)
label2 = tk.Label(window, text='数据位', font=10)
label2.place(y=150, x=50)
label3 = tk.Label(window, text='校验位', font=10)
label3.place(y=200, x=50)
label4 = tk.Label(window, text='停止位', font=10)
label4.place(y=250, x=50)

comvalue0 = tk.StringVar()  # 窗体自带的文本，新建一个值
comboxlist0 = ttk.Combobox(window, textvariable=comvalue0)  # 初始化
comboxlist0["values"] = tuple(serialName)
comboxlist0.current(0)  # 选择第一个
comboxlist0.bind("<<ComboboxSelected>>", setPort)  # 绑定事件,(下拉列表框被选中时，绑定go()函数)
comboxlist0.place(y=50, x=150)

comvalue1 = tk.StringVar()
comboxlist1 = ttk.Combobox(window, textvariable=comvalue1)  # 初始化
comboxlist1["values"] = ("1200", "2400", "4800", "9600", "14400", "19200")
comboxlist1.current(0)  # 选择第一个
comboxlist1.bind("<<ComboboxSelected>>", setbaudrate)  # 绑定事件,(下拉列表框被选中时，绑定go()函数)
comboxlist1.place(y=100, x=150)

comvalue2 = tk.StringVar()
comboxlist2 = ttk.Combobox(window, textvariable=comvalue2)  # 初始化
comboxlist2["values"] = ("8","7","6","5")
comboxlist2.current(0)  # 选择第一个
comboxlist2.bind("<<ComboboxSelected>>", setShujv)  # 绑定事件,(下拉列表框被选中时，绑定go()函数)
comboxlist2.place(y=150, x=150)

comvalue3 = tk.StringVar()
comboxlist3 = ttk.Combobox(window, textvariable=comvalue3)  # 初始化
comboxlist3["values"] = ("N","E","O")
comboxlist3.current(0)  # 选择第一个
comboxlist3.bind("<<ComboboxSelected>>", setcheck)  # 绑定事件,(下拉列表框被选中时，绑定go()函数)
comboxlist3.place(y=200, x=150)

comvalue4 = tk.StringVar()
comboxlist4 = ttk.Combobox(window, textvariable=comvalue4)  # 初始化
comboxlist4["values"] = ("1", "1.5", "2")
comboxlist4.current(0)  # 选择第一个
comboxlist4.bind("<<ComboboxSelected>>", setstop)  # 绑定事件,(下拉列表框被选中时，绑定go()函数)
comboxlist4.place(y=250, x=150)

b0 = tk.Button(window, text='打开串口', width=35, height=1, command=opencom)
b0.place(y=300, x=50)
b1 = tk.Button(window, text='清除接收', width=35, height=1, command=clearreceive)
b1.place(y=350, x=50)
e0 = tk.Entry(window, show=None, width=35)
e0.place(y=400, x=50)

c1 = tk.Checkbutton(window, text='接受数据', variable=var, onvalue=1, offvalue=0,
                    command=selection)
c1.place(y=450, x=50)
b1 = tk.Button(window, text='Send', width=20, height=1, command=send)
b1.place(y=450, x=150)

t0 = tk.Text(window, width=65, height=15)
t0.place(y=50, x=350)

b2 = tk.Button(window, text='draw', width=10, height=1, command=draw)
b2.place(y=270, x=350)
b3 = tk.Button(window, text='auto-draw', width=10, height=1, command=startdraw)
b3.place(y=320, x=350)
b3 = tk.Button(window, text='clear', width=10, height=1, command=cleardraw)
b3.place(y=370, x=350)

f = Figure(figsize=(4, 3), dpi=100)
#plt.ion()
a = f.add_subplot(111)  # 添加子图:1行1列第1个
#a.plot([1,2,3])
canvas = FigureCanvasTkAgg(f, master=window)
canvas.draw()
canvas.get_tk_widget().place(y=270, x=450)

if __name__ == '__main__':
    freeze_support()
    th0 = threading.Thread(target=showdata)
    th1 = threading.Thread(target=senddata)
    #th2 = threading.Thread(target=startdraw)
    #th2.start()
    window.mainloop()
