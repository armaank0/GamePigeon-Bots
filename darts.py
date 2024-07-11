import serial
import time
s = serial.Serial(port='/dev/cu.usbmodemHIDGD1', baudrate=115200, timeout=0.1)

points = ['60', '57', '54', '51', '50', '48', 
          '45', '42', '39', '38', '36', '34', '33', '32', '30',
          '28', '27', '26', '24', '22', '21',
          '20', '19', '18', '17', '16', '15',
          '14', '13', '12', '11', '10', '9', '8',
          '7', '6', '5', '4', '3', '2', '1',
          ]

x = [0, -14, 18, 14, -1, -30,
     28, -30, 29, -17, -18, 17, -31, -49, 30,
     -44, -24, 44, -31, -50, -21,
     0, -15, 20, 15, -35, 35,
     -40, 40, -20, -40, 40, -30, -40,
     -28, 40, -10, 30, 0, 28, 10,

    ]

y = [-58, -29, -53, -29, -43, -33,
     -35, -48, -47, -7, -53, -7, -43, -30, -38,
     -50, -50, -50, -38, -43, -30,
     -65, -20, -62, -20, -32, -32,
     -50, -50, -62, -43, -36, -56, -36,
     -25, -43, -65, -56, -15, -25, -65, 
    ]

if __name__ == "__main__":
    s.write(bytes('c,8/60\n', 'utf-8'))
    s.write(bytes('n\n', 'utf-8'))

    while True:
        command = input("Enter 'm' to re-position or a point value: ")
        if command == 'm':
            s.write(bytes('c,8/60\n', 'utf-8'))
            s.write(bytes('n\n', 'utf-8'))
        elif command in points:
            s.write(bytes('l\n', 'utf-8'))
            time.sleep(0.03)
            s.write(bytes('m,' + str(x[points.index(command)]) + '/-120\n', 'utf-8'))
            time.sleep(0.03)
            s.write(bytes('m,0/' + str(y[points.index(command)]) + '\n', 'utf-8'))
            time.sleep(0.03)
            s.write(bytes('n\n', 'utf-8'))
            time.sleep(0.03)
            s.write(bytes('c,8/60\n', 'utf-8'))
        else:
            print("Command doesn't exist.")