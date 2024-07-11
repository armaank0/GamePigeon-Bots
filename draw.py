from pynput import mouse

art_x = []
art_y = []
drawing = False
counter = 0

def on_move(x, y):
    global drawing
    global counter
    global art_x
    global art_y
    if drawing == True:
        if len(art_x) != 0:
            if x > art_x[-1] + 8 or x < art_x[-1] - 8 or y > art_y[-1] + 8 or y < art_y[-1] - 8:
                art_x.append(x)
                art_y.append(y)
        else:
            art_x.append(x)
            art_y.append(y)

def on_click(x, y, button, pressed):
    global drawing
    global art_x
    global art_y
    if pressed:
        drawing = True
    else:
        drawing = False
        filename = input("Enter a filename: ")
        with open(f"drawings/{filename}.txt", "w") as file:
            file.write(str(len(art_x)) + '\n')
            for line in range(len(art_x)):
                file.write(str(round(art_x[line])) + '/')
                file.write(str(round(art_y[line])) + '\n')
        art_x = []
        art_y = []

listener = mouse.Listener(on_click=on_click,on_move=on_move)
listener.start()
listener.join()