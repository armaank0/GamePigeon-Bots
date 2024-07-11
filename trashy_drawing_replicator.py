import serial
import time
from pynput.keyboard import Key, Listener
import os

# Check that the port name matches
s = serial.Serial(port='/dev/cu.usbmodemHIDGD1', baudrate=115200, timeout=0.1)

char = ['up', 'ri', 'do', 'le']
x_move = [0, 1, 0, -1]
y_move = [-1, 0, 1, 0]
counter = 1.2
last_press = ''
drawings = os.listdir("drawings")

def on_press(key):
    global counter
    global last_press
    string = '{0}'.format(key)
    if last_press == string[4:6]:
        counter += 1.2
    else:
        counter = 1.2
    last_press = string[4:6]
    if string[0:3] == 'Key' and string[4:6] in char:
        s.write(bytes('m,' + str(round(x_move[char.index(string[4:6])] * counter)) + '/' + str(round(y_move[char.index(string[4:6])] * counter)) + '\n', 'utf-8'))
        os.system('cls' if os.name == 'nt' else 'clear')

def on_release(key):
    global last_press
    last_press = ''
    string = '{0}'.format(key)
    if len(string) == 3 and str(string[1]) == '/':
        os.system('cls' if os.name == 'nt' else 'clear')
        art = input("Enter the drawing filename (without .txt): ")
        art_x = []
        art_y = []
        slash = art.index('/')
        if art[slash + 1:] in drawings:
            with open(f"{art[slash + 1:]}.txt", "r") as file:
                length = file.readline()
                length = int(length[:-1])
                for i in range(length):
                    nextline = file.readline()
                    x_end = nextline.index('/')
                    art_x.append(int(nextline[:x_end]))
                    art_y.append(int(nextline[x_end + 1:-1]))
            s.write(bytes('l\n', 'utf-8'))
            for i in range(1, length):
                s.write(bytes('m,' + str(int(art_x[i] - art_x[i - 1])) + '/' + str(int(art_y[i] - art_y[i - 1])) + '\n', 'utf-8'))
                time.sleep(0.03)
            s.write(bytes('n\n', 'utf-8'))
        else:
            print("Drawing not found.")

if __name__ == "__main__":
    print("Use arrow keys to position the mouse, then press '/' to begin drawing.")
    s.write(bytes('n\n', 'utf-8'))
    listener = Listener(on_press=on_press,on_release=on_release)
    listener.start()
    listener.join()