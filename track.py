from pynput import mouse
from pynput.keyboard import Key, Listener
import serial

# Check that the port name matches
s = serial.Serial(port='/dev/cu.usbmodemHIDGD1', baudrate=115200, timeout=0.1)

last_x = 0
last_y = 0

def on_move(x, y):
    global last_x
    global last_y
    s.write(bytes('m,' + str(x - last_x) + '/' + str(y - last_y) + '\n', 'utf-8'))
    last_x = x
    last_y = y

def on_click(x, y, button, pressed):
    global last_x
    global last_y
    if button == mouse.Button.left:
        if pressed:
            s.write(bytes('l\n', 'utf-8'))
        else:
            s.write(bytes('n\n', 'utf-8'))
    elif button == mouse.Button.right:
        if pressed:
            s.write(bytes('r\n', 'utf-8'))
        else:
            s.write(bytes('f\n', 'utf-8'))
    last_x = x
    last_y = y

def on_scroll(x, y, dx, dy):
    global last_x
    global last_y
    if dy < 0:
        s.write(bytes('d\n', 'utf-8'))
    else:
        s.write(bytes('u\n', 'utf-8'))
    last_x = x
    last_y = y

special = ['ct', 'al', 'cm', 'sp', 'up', 'ri', 'do', 'le', 'en', 'ba', 'ca', 'sh', 'ta']
special_code = [128, 130, 131, 32, 218, 215, 217, 216, 176, 178, 193, 129, 179]
    
def on_press(key):
    string = '{0}'.format(key)
    if string[0:3] == 'Key':
        s.write(bytes('k,' + str(special_code[special.index(string[4:6])]) + '/0\n', 'utf-8'))
    else:
        s.write(bytes('k,' + str(ord(string[1])) + '/0\n', 'utf-8'))

def on_release(key):
    string = '{0}'.format(key)
    if string[0:3] == 'Key':
        s.write(bytes('j,' + str(special_code[special.index(string[4:6])]) + '/0\n', 'utf-8'))
    else:
        s.write(bytes('j,' + str(ord(string[1])) + '/0\n', 'utf-8'))

listener1 = Listener(on_press=on_press,on_release=on_release)
listener2 = mouse.Listener(on_click=on_click,on_move=on_move,on_scroll=on_scroll)
listener1.start()
listener2.start()

if __name__ == "__main__":
    s.write(bytes('n\n', 'utf-8'))
    while True:
        listener1.join()
        listener2.join()