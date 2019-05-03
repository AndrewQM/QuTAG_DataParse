from tkinter import *
from matplotlib import pyplot as plt
import sys
from ParamsParse import *

numbers=[]
testsite_array = []


#Datafile to parse is given as parameter when running the program
datafile1 = sys.argv[1]

with open(datafile1, 'r') as fobj:

    all_lines = [[int(num) for num in line.split()] for line in fobj]

print("length of file: ", len(all_lines))
totalt = 0
for t in range(4):
    totaltt = all_lines[len(all_lines)-1][t]-all_lines[0][t]
    if totaltt > totalt:
        totalt = totaltt
print("total time of file: ", int(totalt/1000000000), "ms")




class Mask:
    def __init__(self, channelA, channelB, window, offset):
        self.chA = channelA
        self.chB = channelB
        self.window = window
        self.offset = offset
        self.accept = [0]*len(all_lines)
        if (self.window == 0) or (self.chA == 0) or (self.chB == 0):
            self.deactivated = 1
        else:
            self.deactivated = 0

    def generate_mask(self):
        if self.deactivated:
            # the mask is unused, and disabled.
            self.accept = [1]*len(all_lines)
        else:
            for line in range(len(all_lines)):
                timeA = all_lines[line][self.chA-1]
                timeB = all_lines[line][self.chB-1]
                if (timeA < 0) or (timeB < 0):
                    #no coincidence found in event. Move on to next
                    continue

                #correct for offset
                timeB = timeB - self.offset

                #accept or reject event based on window
                self.septime = abs(timeA - timeB)
                if self.septime < self.window:
                    self.accept[line] = 1
            #window = timewindow(all_lines[line][0], totalt, all_lines[0][0])
            #print("window:", window)
            #array goes from 0 to 3, channels go from 1 to 4


class Operations:
    def __init__(self, Mask12_OP, Mask23_OP, inttype, intbins):
        self.Mask12_OP = Mask12_OP
        self.Mask23_OP = Mask23_OP
        self.inttype = inttype
        self.intbins = intbins

def run():
    # this is where the magic happens
    print(mask1.chA)
    print(mask1.chB)
    print(mask1.window)
    print(mask1.offset)

    if ops.inttype:
        print("integrating by time")
        # integration by time
        mask1.generate_mask()
        mask2.generate_mask()
        mask3.generate_mask()
        if ops.Mask12_OP or mask1.deactivated or mask1.deactivated:
            # do AND operation when specified op is AND, or when one of the masks is deactivated.
            finalmask = [mask1.accept[i] and mask2.accept[i] for i in range(len(mask1.accept))]
            print("ANDing 1 and 2")
        elif ops.Mask12_OP == 0:
            finalmask = [mask1.accept[i] or mask2.accept[i] for i in range(len(mask1.accept))]
            print("ORing 1 and 2")

        if ops.Mask23_OP or mask3.deactivated:
            finalmask = [finalmask[i] and mask3.accept[i] for i in range(len(mask1.accept))]
            print("ANDing 12 and 3")
        elif ops.Mask23_OP == 0:
            finalmask = [finalmask[i] or mask3.accept[i] for i in range(len(mask1.accept))]
            print("ORing 12 and 3")

        by_times_array = [0]*ops.intbins

        currenttime = all_lines[0][0]
        prevtime = all_lines[0][0]
        j = 0

        bintime = int(totalt/ops.intbins)
        #now do the integration for each bin
        for i in range(ops.intbins):
            coincsum = 0
            while (currenttime - prevtime) < bintime:
                if j > (len(all_lines)-1):
                    print("ending and i is: ", i)
                    break
                coincsum = coincsum + finalmask[j]
                currenttime = all_lines[j][0]
                j = j+1
            by_times_array[i] = coincsum
            prevtime = currenttime
        print(finalmask[0:50])
        print()
        print()
        print(by_times_array)


    else:
        # integration by files
        # first file already loaded
        mask1.generate_mask()
        mask2.generate_mask()
        mask3.generate_mask()
        if ops.Mask12_OP or mask1.deactivated or mask1.deactivated:
            # do AND operation when specified op is AND, or when one of the masks is deactivated.
            finalmask = [mask1.accept[i] and mask2.accept[i] for i in range(len(mask1.accept))]
            print("ANDing 1 and 2")
        elif ops.Mask12_OP == 0:
            finalmask = [mask1.accept[i] or mask2.accept[i] for i in range(len(mask1.accept))]
            print("ORing 1 and 2")

        if ops.Mask23_OP or mask3.deactivated:
            finalmask = [finalmask[i] and mask3.accept[i] for i in range(len(mask1.accept))]
            print("ANDing 12 and 3")
        elif ops.Mask23_OP == 0:
            finalmask = [finalmask[i] or mask3.accept[i] for i in range(len(mask1.accept))]
            print("ORing 12 and 3")




        by_files_array = []
        by_files_array.append(sum(finalmask))

        print("not finished")
        exit()
        #now loop though the other files
        # for i in range(extrafiles):






def GUIinit():
    #this is where you declare and fill the Mask1, Mask2, Mask3 and ops objects.
    window_val = timewindow.get()

    ops.intbins = int(window_val)

    print(mask1.chA)
    print(mask1.chB)
    print(mask1.window)

    if ops.inttype:
        print("using by time")

    #mask1.generate_mask()
    print(mask1.accept[1:30])
    run()




#GUI specific functions
def click1():
    if checkstat1.get():
        #by time selected

        ops.inttype = 1
        check2.config(state=DISABLED)
        timewindow.config(state=NORMAL)
        timewindowlabel.config(state=NORMAL)
    else:
        check2.config(state=NORMAL)
        bytime = 0


def click2():
    if checkstat2.get():
        #by files selected
        ops.inttype = 0
        timewindow.config(state=DISABLED)
        timewindowlabel.config(state=DISABLED)
        check1.config(state=DISABLED)
    else:
        check1.config(state=NORMAL)
        byfiles = 0



#print(sys.argv[1])
if len(sys.argv) > 2:
    if sys.argv[2] == 'g':
        #optional g tag (after datafile paramter) runs GUI
        root = Tk()
        checkstat1 = BooleanVar(root)
        checkstat2 = BooleanVar(root)

        Mask1CHA = 1
        Mask1CHB = 2
        Mask1window = 20
        Mask1offset = 2254700

        Mask2CHA = 0
        Mask2CHB = 0
        Mask2window = 0
        Mask2offset = 0

        Mask3CHA = 0
        Mask3CHB = 0
        Mask3window = 0
        Mask3offset = 0



        mask1 = Mask(Mask1CHA,Mask1CHB,Mask1window,Mask1offset)
        mask2 = Mask(Mask2CHA,Mask2CHB,Mask2window,Mask2offset)
        mask3 = Mask(Mask3CHA,Mask3CHB,Mask3window,Mask3offset)

        ops = Operations(1, 1, 0, 0)


        check1 = Checkbutton(text="by time", variable = checkstat1, command=click1)
        check1.grid(row = 0, column = 0)

        check2 = Checkbutton(text="by files", variable = checkstat2, command=click2)
        check2.grid(row = 0, column = 1)

        timewindowlabel = Label(root, text="    Integration Bins")
        timewindowlabel.grid(row = 0, column = 2)
        timewindow = Entry(root)
        timewindow.grid(row = 0, column = 3)

        OKbutton = Button(root,text="OK", command=GUIinit)
        OKbutton.grid(row = 1, columnspan = 4,sticky = "nsew")

        root.mainloop()
else:
    #GUI not requested with g tag
    #using dataparse_params.txt file
    Params = params_parse("dataparse_params.txt")

    #load data from the params_parser object to this program's objects
    ops = Operations(Params.Mask12_OP, Params.Mask23_OP, Params.inttype, Params.intbins)
    mask1 = Mask(Params.Mask1ChA,Params.Mask1ChB,Params.Mask1window,Params.Mask1offset)
    mask2 = Mask(Params.Mask2ChA,Params.Mask2ChB,Params.Mask2window,Params.Mask2offset)
    mask3 = Mask(Params.Mask3ChA,Params.Mask3ChB,Params.Mask3window,Params.Mask3offset)
    #print("Mask1ChA is:", Params.Mask1ChB)
    run()
