from tkinter import *
from tkinter.ttk import *
from matplotlib import pyplot as plt
import sys
from ParamsParse import *
import tkinter.ttk
import matplotlib.pyplot as plt
import glob #used for searching current directory for multiple data files

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
        #self.accept = [0]*len(all_lines)
        if (self.window == 0) or (self.chA == 0) or (self.chB == 0):
            self.deactivated = 1
        else:
            self.deactivated = 0

    def generate_mask(self, lineset):
        if self.deactivated:
            # the mask is unused, and disabled.
            #self.accept.clear()
            self.accept = [1]*len(lineset)
        else:
            #self.accept.clear()
            self.accept = [0]*len(lineset)
            for line in range(len(lineset)):
                timeA = lineset[line][self.chA-1]
                timeB = lineset[line][self.chB-1]
                if (timeA < 0) or (timeB < 0):
                    #chA or chB values are not valid (e.g. if ch value is -666). Move on to next
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
    def update(self):
        if (self.window == 0) or (self.chA == 0) or (self.chB == 0):
            self.deactivated = 1
        else:
            self.deactivated = 0



class Operations:
    def __init__(self, Mask12_OP, Mask23_OP, inttype, intbins):
        self.Mask12_OP = Mask12_OP
        self.Mask23_OP = Mask23_OP
        self.inttype = inttype
        self.intbins = intbins

def run():
    # where masks are generated and finally combined together.

    if ops.inttype:
        print("integrating by time")
        # integration by time
        mask1.generate_mask(all_lines)
        mask2.generate_mask(all_lines)
        mask3.generate_mask(all_lines)
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

        with open("ParseOutput.txt", 'w') as output:
            for entry in by_times_array:
                output.write(str(entry)+'\n')

        plt.plot(by_times_array)

        plt.show()




        return


    else:
        print("integrating by files")

        files = glob.glob("data_test*")
        print(files)

        firstfile = datafile1.split('_')
        basename = '_'.join(firstfile[0:-1]) + '_'

        #sort files based on the value of their numbered suffix (e.g. ****_1.txt)
        sortedfiles = sorted(files, key=lambda name:int(name[len(basename):-4]))
        by_files_array = [0]*len(files)

        print("scanning ", len(sortedfiles), " files.")

        for i in range(len(sortedfiles)):
            by_files_array[i] = Generate(sortedfiles[i])

        print(by_files_array)

        with open("ParseOutput.txt", 'w') as output:
            for entry in by_files_array:
                output.write(str(entry)+'\n')

        plt.plot(by_files_array)
        plt.show()
        return


def Generate(filename):

    all_lines = []
    with open(filename, 'r') as fobj:

        lineset = [[int(num) for num in line.split()] for line in fobj]

    print("length of file: ", len(lineset))
    totalt = 0
    for t in range(4):
        totaltt = lineset[len(lineset)-1][t]-lineset[0][t]
        if totaltt > totalt:
            totalt = totaltt

    #can I reload something the object references that was originally a global array?


    #the mask objects should still have all the coincidence parameters.
    #Just need to re-generate masks and sum the final mask for this file

    print("scanning file: ", filename)
    mask1.generate_mask(lineset)
    mask2.generate_mask(lineset)
    mask3.generate_mask(lineset)
    if ops.Mask12_OP or mask1.deactivated or mask1.deactivated:
        # do AND operation when specified op is AND, or when one of the masks is deactivated.
        finalmask = [mask1.accept[i] and mask2.accept[i] for i in range(len(mask1.accept))]
        #print("ANDing 1 and 2")
    elif ops.Mask12_OP == 0:
        finalmask = [mask1.accept[i] or mask2.accept[i] for i in range(len(mask1.accept))]
        #print("ORing 1 and 2")

    if ops.Mask23_OP or mask3.deactivated:
        finalmask = [finalmask[i] and mask3.accept[i] for i in range(len(mask1.accept))]
        #print("ANDing 12 and 3")
    elif ops.Mask23_OP == 0:
        finalmask = [finalmask[i] or mask3.accept[i] for i in range(len(mask1.accept))]
        #print("ORing 12 and 3")

    return sum(finalmask)


def GUIinit():
    #this is where you declare and fill the Mask1, Mask2, Mask3 and ops objects.
    bins_val = timebins.get()
    if bins_val != '': ops.intbins = int(bins_val)

    if bins_val == '' and ops.inttype == 1:
        style = Style()
        style.configure("BW.TLabel", foreground="red")
        timebinslabel = Label(root, text="    Integration Bins", style = "BW.TLabel")
        return
    #thingy = Mask1ChAVal.get()
    #print("this is Mask 1 ChA Val", thingy)

    #mask1 = Mask(int(Mask1ChAVal.get()),int(Mask1ChBVal.get()),int(Mask1WindowVal.get()),int(Mask1offsetVal.get()))       #channelA, channelB, window, offset):
    #mask2 = Mask(int(Mask2ChAVal.get()),int(Mask2ChBVal.get()),int(Mask2WindowVal.get()),int(Mask2offsetVal.get()))
    #mask3 = Mask(int(Mask3ChAVal.get()),int(Mask3ChBVal.get()),int(Mask3WindowVal.get()),int(Mask3offsetVal.get()))
    if (Mask1ChAVal.get() != ''): mask1.chA = int(Mask1ChAVal.get())
    if (Mask1ChBVal.get() != ''): mask1.chB = int(Mask1ChBVal.get())
    if (Mask1WindowVal.get() != ''): mask1.window = int(Mask1WindowVal.get())
    if (Mask1offsetVal.get() != ''): mask1.offset = int(Mask1offsetVal.get())


    if (Mask2ChAVal.get() != ''): mask2.chA = int(Mask2ChAVal.get())
    if (Mask2ChBVal.get() != ''): mask2.chB = int(Mask2ChBVal.get())
    if (Mask2WindowVal.get() != ''): mask2.window = int(Mask2WindowVal.get())
    if (Mask2offsetVal.get() != ''): mask2.offset = int(Mask2offsetVal.get())

    if (Mask3ChAVal.get() != ''): mask3.chA = int(Mask3ChAVal.get())
    if (Mask3ChBVal.get() != ''): mask3.chB = int(Mask3ChBVal.get())
    if (Mask3WindowVal.get() != ''): mask3.window = int(Mask3WindowVal.get())
    if (Mask3offsetVal.get() != ''): mask3.offset = int(Mask3offsetVal.get())


    mask1.update()
    mask2.update()
    mask3.update()

    print("mask1 deactivated is: ", mask1.deactivated)
    print("mask2 deactivated is: ", mask2.deactivated)
    print("mask3 deactivated is: ", mask3.deactivated)


    if (OP12Val.get() == 'AND') or (OP12Val.get() == '    '):
        ops.Mask12_OP = 1
    elif OP12Val.get() == ' OR ':
        ops.Mask23_OP = 0
    else:
        print("Mask 1-2 Operation Error")
        return

    if (OP23Val.get() == 'AND') or (OP23Val.get() == '    '):  #if unspecified, operation default is AND
        ops.Mask23_OP = 1
    elif OP23Val.get() == ' OR ':
        ops.Mask23_OP = 0
    else:
        print("Mask 2-3 Operation Error")
        return

    run() #all objects have parameters loaded, continue with calculation.

    return




#GUI specific functions
def click1():
    if checkstat1.get():
        #by time selected

        ops.inttype = 1
        check2.config(state=DISABLED)
        timebins.config(state=NORMAL)
        timebinslabel.config(state=NORMAL)
        #print(type(checkstat1.get()))
    else:
        check2.config(state=NORMAL)
        ops.inttype = 0


def click2():
    if checkstat2.get():
        #by files selected
        ops.inttype = 0
        timebins.config(state=DISABLED)
        timebinslabel.config(state=DISABLED)
        check1.config(state=DISABLED)
    else:
        check1.config(state=NORMAL)
        ops.inttype = 1



#print(sys.argv[1])
if len(sys.argv) > 2:
    if sys.argv[2] == 'g':
        #optional g tag (after datafile paramter) runs GUI
        root = Tk()
        checkstat1 = BooleanVar(root)
        checkstat2 = BooleanVar(root)


        ops = Operations(0, 0, 0, 0) #( Mask12_OP, Mask23_OP, inttype, intbins):

        #default mask values initialize them to deactivated
        mask1 = Mask(-1,-1,0,0)
        mask2 = Mask(-1,-1,0,0)
        mask3 = Mask(-1,-1,0,0)

        timebinslabel = Label(root, text="    Integration Bins", style = "BW.TLabel")

        x = 2
        y = x + 1
        z = y + 1
        a = z + 3


        OPTIONS = ['    ', "AND", " OR "]

        timeinfo = [str(int(totalt/1000000000)), 'ms']
        sep = ' '
        timelabel = Label(root, text='total time of file:').grid(row = 0, column = 0)
        timelabelval = Label(root, text=sep.join(timeinfo)).grid(row = 0, column = 1)

        space3 = Label(root, text=" ").grid(row = 1, column = 0)

        root.title('QuTAG DataParse')
        Mask1Label = Label(root, text="Mask1:   ")
        Mask1Label.grid(row = x, column = 0)
        Mask1ChA = Label(root, text="    Channel A:")
        Mask1ChA.grid(row = x, column = 1)
        Mask1ChAVal = Entry(root)
        Mask1ChAVal.grid(row = x, column = 2)
        Mask1offset = Label(root, text="    Offset (ps):")
        Mask1offset.grid(row = x, column = 3)
        Mask1offsetVal = Entry(root)
        Mask1offsetVal.grid(row = x, column = 4)
        Mask1ChB = Label(root, text="    Channel B:")
        Mask1ChB.grid(row = x, column = 5)
        Mask1ChBVal = Entry(root)
        Mask1ChBVal.grid(row = x, column = 6)
        Mask1Window = Label(root, text="    Window (ps)")
        Mask1Window.grid(row = x, column = 7)
        Mask1WindowVal = Entry(root)
        Mask1WindowVal.grid(row = x, column = 8)
        OP12Label = Label(root, text="      1-2 OP:")
        OP12Label.grid(row = x, column = 9)
        OP12Val = StringVar(root)
        OP12Val.set(OPTIONS[0]) # default value
        OP12 = OptionMenu(root, OP12Val, *OPTIONS)
        OP12.grid(row = x, column = 10)


        Mask2Label = Label(root, text="Mask2:   ")
        Mask2Label.grid(row = y, column = 0)
        Mask2ChA = Label(root, text="    Channel A:")
        Mask2ChA.grid(row = y, column = 1)
        Mask2ChAVal = Entry(root)
        Mask2ChAVal.grid(row = y, column = 2)
        Mask2offset = Label(root, text="    Offset (ps):")
        Mask2offset.grid(row = y, column = 3)
        Mask2offsetVal = Entry(root)
        Mask2offsetVal.grid(row = y, column = 4)
        Mask2ChB = Label(root, text="    Channel B:")
        Mask2ChB.grid(row = y, column = 5)
        Mask2ChBVal = Entry(root)
        Mask2ChBVal.grid(row = y, column = 6)
        Mask2Window = Label(root, text="    Window (ps)")
        Mask2Window.grid(row = y, column = 7)
        Mask2WindowVal = Entry(root)
        Mask2WindowVal.grid(row = y, column = 8)
        OP12Label = Label(root, text="      2-3 OP:")
        OP12Label.grid(row = y, column = 9)
        OP23Val = StringVar(root)
        OP23Val.set(OPTIONS[0]) # default value
        OP23 = OptionMenu(root, OP23Val, *OPTIONS)
        OP23.grid(row = y, column = 10)

        Mask3Label = Label(root, text="Mask3:   ")
        Mask3Label.grid(row = z, column = 0)
        Mask3ChA = Label(root, text="    Channel A:")
        Mask3ChA.grid(row = z, column = 1)
        Mask3ChAVal = Entry(root)
        Mask3ChAVal.grid(row = z, column = 2)
        Mask3offset = Label(root, text="    Offset (ps):")
        Mask3offset.grid(row = z, column = 3)
        Mask3offsetVal = Entry(root)
        Mask3offsetVal.grid(row = z, column = 4)
        Mask3ChB = Label(root, text="    Channel B:")
        Mask3ChB.grid(row = z, column = 5)
        Mask3ChBVal = Entry(root)
        Mask3ChBVal.grid(row = z, column = 6)
        Mask3Window = Label(root, text="    Window (ps)")
        Mask3Window.grid(row = z, column = 7)
        Mask3WindowVal = Entry(root)
        Mask3WindowVal.grid(row = z, column = 8)




        space = Label(root, text=" ").grid(row = z + 1, column = 0)
        space2 = Label(root, text=" ").grid(row = z + 2, column = 1)


        check1 = Checkbutton(text="by time", variable = checkstat1, command=click1)
        check1.grid(row = a, column = 0)

        check2 = Checkbutton(text="by files", variable = checkstat2, command=click2)
        check2.grid(row = a, column = 1)


        timebinslabel.grid(row = a, column = 7)
        timebins = Entry(root)
        timebins.grid(row = a, column = 8)

        OKbutton = Button(root,text="OK", command=GUIinit)
        OKbutton.grid(row = a+1, columnspan = 11,sticky = "nsew")

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
