import serial
import time
import json
s = serial.Serial(port='/dev/cu.usbmodemHIDGD1', baudrate=115200, timeout=2)

def RemoveFromList(thelist, val):
    return [value for value in thelist if value != val]

def GetDic():
    try:
        with open("wordlist.json") as file:
            data = json.load(file)
        diclist = []
        for i in range(26):
            diclist += data[chr(i+97)]
        return diclist
    except FileNotFoundError:
        print("No Dictionary!")
        return 
    
def Word2Vect(word):
    l = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    v = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    w = word.lower()
    wl = list(w)
    for i in range(0, len(wl)):
        if wl[i] in l:
            ind = l.index(wl[i])
            v[ind] += 1
    return v

def Vect2Int(vect):
    pv = 0
    f = 0
    for i in range(0, len(vect)):
        wip = (vect[i]*(2**pv))
        f += wip
        pv += 4
    return f
    
def Ints2Dic(dic):
    d = {}
    for i in range(0, len(dic)):
        v = Word2Vect(dic[i])
        Int = Vect2Int(v)
        if Int in d:
            tat = d.get(Int)
            tat.append(dic[i])
            d[Int] = tat
        elif Int not in d:
            d[Int] = [dic[i]]
    return d
        
d = GetDic()
ind = Ints2Dic(d)

from itertools import permutations

def words(letters):
    for n in range(1, len(letters)+1):
        yield from map(''.join, permutations(letters, n))

if __name__ == "__main__":
    s.write(bytes('n\n', 'utf-8'))

    while True:
        command = input("Enter 'm6' to re-position for 6 letters, 'm7' for 7 letters, or a string of 6-7 letters in the format 'abcdef' to begin solving: ")
        if command == 'm6':
            s.write(bytes('c,-127/110\n', 'utf-8'))
        elif command == 'm7':
            s.write(bytes('c,-127/107\n', 'utf-8'))
            time.sleep(0.02)
            s.write(bytes('m,-5/0\n', 'utf-8'))
        elif len(command) == 6 or len(command) == 7:
            move_len = 0
            move_two = 0
            if len(command) == 6:
                move_len = 43
                move_two = 70
            elif len(command) == 7:
                move_len = 39
                move_two = 62

            all = set(words(command))

            list_all = []
            for word in all:
                v = Vect2Int(Word2Vect(word))
                tp = ind.get(v)
                if isinstance(tp, list):
                    for word in range(len(tp)):
                        tp[word] = tp[word].lower()
                    list_all += tp

            list_all = list(set(list_all))
            list_all = sorted(list_all, key=len)
            list_all = [item for item in list_all if len(item)>=3]
            list_all = list(reversed(list_all))
            #print(list_all)

            chars = [*command]
            multi = []
            multi_val = []
            multi_list = []
            for char in chars:
                if char not in multi:
                    letter_inst = [i for i,val in enumerate(chars) if val==char]
                    if len(letter_inst) > 1:
                        multi.append(char)
                        multi_val.append(len(letter_inst))
                        multi_list.append(letter_inst)

            p = 0
            ind = 0
            for word in list_all:
                print(word)
                for char in word:
                    letter_count = word.count(char)
                    if letter_count == 1:
                        next_p = chars.index(char)
                    else:
                        next_p = multi_list[multi.index(char)][multi_val[multi.index(char)] - 1]
                        multi_val[multi.index(char)] -= 1
                        if multi_val[multi.index(char)] == 0:
                            letter_inst = [i for i,val in enumerate(chars) if val==char]
                            multi_val[multi.index(char)] = len(letter_inst)
                    
                    
                    cycles = abs(next_p - ind)
                    for cycle in range(cycles // 2):
                        s.write(bytes('m,' + str(abs(next_p - ind)/(next_p - ind) * move_two) + '/0\n', 'utf-8'))
                        time.sleep(0.02)
                        cycles -= 2
                    for cycle in range(cycles):
                        s.write(bytes('m,' + str(abs(next_p - ind)/(next_p - ind) * move_len) + '/0\n', 'utf-8'))
                        time.sleep(0.02)
                    ind = next_p
                    time.sleep(0.02)
                    s.write(bytes('l\n', 'utf-8'))
                    time.sleep(0.02)
                    s.write(bytes('n\n', 'utf-8'))
                    time.sleep(0.02)

                if ind == 0:
                    s.write(bytes('m,' + str(move_len) + '0\n', 'utf-8'))
                    ind = 1
                    time.sleep(0.02)
                elif ind == len(command) - 1:
                    s.write(bytes('m,' + str(-move_len) + '/0\n', 'utf-8'))
                    ind -= 1
                    time.sleep(0.02)

                # Go click the enter
                s.write(bytes('m,0/-112\n', 'utf-8'))
                time.sleep(0.05)
                s.write(bytes('l\n', 'utf-8'))
                time.sleep(0.08)
                s.write(bytes('n\n', 'utf-8'))
                time.sleep(0.04)
                s.write(bytes('m,0/112\n', 'utf-8'))
                time.sleep(0.02)

            print("Completed!")
            break