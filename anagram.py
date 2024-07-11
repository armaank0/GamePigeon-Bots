import serial
import time
import json
s = serial.Serial(port='/dev/cu.usbmodemHIDGD1', baudrate=115200, timeout=0.1)

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
    s.write(bytes('c,-127/110\n', 'utf-8'))
    s.write(bytes('n\n', 'utf-8'))

    while True:
        command = input("Enter 'm' to re-position or the 6 letters with the format 'abcdef': ")
        if command == 'm':
            s.write(bytes('c,-127/110\n', 'utf-8'))
        elif len(command) == 6:
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
            print(list_all)

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
            for word in list_all:
                ind = 0
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
                    for cycle in range(abs((next_p - ind))):
                        s.write(bytes('m,' + str(abs(next_p - ind)/(next_p - ind) * 43) + '/0\n', 'utf-8'))
                        time.sleep(0.02)
                    ind = next_p
                    s.write(bytes('l\n', 'utf-8'))
                    time.sleep(0.02)
                    s.write(bytes('n\n', 'utf-8'))
                    time.sleep(0.02)
                
                for cycle in range(next_p):
                    s.write(bytes('m,-43/0\n', 'utf-8'))
                    time.sleep(0.02)
                s.write(bytes('m,0/-42\n', 'utf-8'))
                time.sleep(0.02)

                # Go click the enter
                s.write(bytes('m,0/-70\n', 'utf-8'))
                time.sleep(0.02)
                s.write(bytes('m,50/0\n', 'utf-8'))
                time.sleep(0.02)
                s.write(bytes('l\n', 'utf-8'))
                time.sleep(0.08)
                s.write(bytes('n\n', 'utf-8'))
                time.sleep(0.02)
                s.write(bytes('m,-50/0\n', 'utf-8'))
                time.sleep(0.02)
                s.write(bytes('m,0/70\n', 'utf-8'))
                time.sleep(0.02)

                s.write(bytes('m,0/42\n', 'utf-8'))
                time.sleep(0.02)
            print("Completed!")
            break