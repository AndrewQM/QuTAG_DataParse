
class params_parse:
    def __init__(self,filename):

        with open(filename, 'r') as fobj:

            self.params = [line for line in fobj]

        self.inttype = self.params[0].split()[-1]
        if self.inttype == "bytime":
            self.inttype = 1
        else:
            self.inttype = 0

        self.intbins = int(self.params[1].split()[-1])

        self.Mask1ChA = int(self.params[5].split()[-1])
        self.Mask1ChB = int(self.params[6].split()[-1])
        self.Mask1window = int(self.params[7].split()[-1])
        self.Mask1offset = int(self.params[8].split()[-1])

        maskop = self.params[10].split()[-1]
        if maskop == "AND":
            self.Mask12_OP = 1
        if maskop == "OR":
            self.Mask12_OP = 0
        else:
            self.Mask12_OP = -1

        self.Mask2ChA = int(self.params[13].split()[-1])
        self.Mask2ChB = int(self.params[14].split()[-1])
        self.Mask2window = int(self.params[15].split()[-1])
        self.Mask2offset = int(self.params[16].split()[-1])

        maskop = self.params[18].split()[-1]
        if maskop == "AND":
            self.Mask23_OP = 1
        if maskop == "OR":
            self.Mask23_OP = 0
        else:
            self.Mask23_OP = -1

        self.Mask3ChA = int(self.params[21].split()[-1])
        self.Mask3ChB = int(self.params[22].split()[-1])
        self.Mask3window = int(self.params[23].split()[-1])
        self.Mask3offset = int(self.params[24].split()[-1])





#print("inttype is", inttype)
#print("intbins is:", intbins)
#print(Mask)
