import numpy as np
import math

class Th():
    def __init__(self):
        # -------------------------------------------------
        # Define theoretical elemental function #1
        self.function1_name = "DbSigmoid"
        self.DS_param_name = ["Xc", "A ", "W1", "W2", "W3"]
        self.DS_param1_val = [0.01, 10, 2.0] # list of [min, max, def] values of parameter Xc
        self.DS_param2_val = [0.05, 40, 20] # list of [min, max, def] values of parameter A
        self.DS_param3_val = [0.05, 5.0, 0.5] # list of [min, max, def] values of parameter W1
        self.DS_param4_val = [0.05, 5.0, 0.5] # # list of [min, max, def] values of parameter W2
        self.DS_param5_val = [0.05, 5.0, 0.5] # # list of [min, max, def] values of parameter W3

        self.DS_param_number = len(self.DS_param_name)
        self.DS_all_val = [self.DS_param1_val, self.DS_param2_val, self.DS_param3_val, self.DS_param4_val, self.DS_param5_val]
        self.DS_comb = zip(self.DS_param_name, self.DS_all_val)
        self.DS_list_def_param = [n[-1] for n in self.DS_all_val]

        #----------------------------------------------------
        #Define theoretical elemental function #2 Y = A * Sin (W*X + Ph)
        self.function2_name = "Sinus"
        self.SN_param_name =["A", "W", "Ph"]
        self.SN_param1_val = [0.01, 30, 3]
        self.SN_param2_val = [0.1, 20, 1]
        self.SN_param3_val = [0, 2*math.pi, 0]

        self.SN_param_number = len(self.SN_param_name)
        self.SN_all_val = [self.SN_param1_val, self.SN_param2_val, self.SN_param3_val]
        self.SN_comb = zip(self.SN_param_name, self.SN_all_val)
        self.SN_list_def_param = [n[-1] for n in self.SN_all_val]

        #----------------------------------------------------
        #Define theoretical elemental function #3 Y = A*Exp( -(X-B)^2 / (2*C^2 )
        self.function3_name = "Gauss"
        self.GS_param_name =["A", "B", "C"]
        self.GS_param1_val = [0.01, 30, 3]
        self.GS_param2_val = [0.1, 20, 3]
        self.GS_param3_val = [0.01, 2, 1]

        self.GS_param_number = len(self.GS_param_name)
        self.GS_all_val = [self.GS_param1_val, self.GS_param2_val, self.GS_param3_val]
        self.GS_comb = zip(self.GS_param_name, self.GS_all_val)
        self.GS_list_def_param = [n[-1] for n in self.GS_all_val]

        #----------------------------------------------------
        #Define theoretical elemental function #4 - Y = A*Exp(-B*X)
        self.function4_name = "EXP"
        self.EXP_param_name =["A", "B"]
        self.EXP_param1_val = [0.01, 20, 2]
        self.EXP_param2_val = [0.01, 1, 0.5]

        self.EXP_param_number = len(self.EXP_param_name)
        self.EXP_all_val = [self.EXP_param1_val, self.EXP_param2_val]
        self.EXP_comb = zip(self.EXP_param_name, self.EXP_all_val)
        self.EXP_list_def_param = [n[-1] for n in self.EXP_all_val]
        #----------------------------------------------------
        #Define theoretical elemental function #5 - Y = [A/(2Pi)]*[1/{ (x-x0)^2 + A^2/4  }]
        self.function5_name = "Lorenz"
        self.LOR_param_name =["A", "X0"]
        self.LOR_param1_val = [0.01, 2, 0.05]
        self.LOR_param2_val = [0, 15, 12]

        self.LOR_param_number = len(self.LOR_param_name)
        self.LOR_all_val = [self.LOR_param1_val, self.LOR_param2_val]
        self.LOR_comb = zip(self.LOR_param_name, self.LOR_all_val)
        self.LOR_list_def_param = [n[-1] for n in self.LOR_all_val]
        #----------------------------------------------------
        #Define theoretical elemental function #6 - Y = [A/(1 + Exp(2*b*(x-C)))   ]
        #------------------------------------------------------------------
        self.function6_name = "Sigmoid"
        self.SIG_param_name =["A", "B", "C"]
        self.SIG_param1_val = [0.1, 5, 1]
        self.SIG_param2_val = [0.1, 5, 1.5]
        self.SIG_param3_val = [0, 15, 3]

        self.SIG_param_number = len(self.SIG_param_name)
        self.SIG_all_val = [self.SIG_param1_val, self.SIG_param2_val, self.SIG_param3_val]
        self.SIG_comb = zip(self.SIG_param_name, self.SIG_all_val)
        self.SIG_list_def_param = [n[-1] for n in self.SIG_all_val]
#-------------------New function ----------------------------
#---!!! Here is the place to define new theoretical elemental function #7 - Y = Y(X) !!!----
#       self.function7_name = "New_name"
#       self.NF_param_name =["A", "B", "C"]
#       self.NF_param1_val = [0.1, 5, 1]
#       self.NF_param2_val = [0.1, 5, 1.5]
#       self.NF_param3_val = [0, 15, 3]

#       self.NF_param_number = len(self.NF_param_name)
#       self.NF_all_val = [self.NF_param1_val, self.NF_param2_val, self.NF_param2_val] # note here the number of parameters
#       self.NF_comb = zip(self.NF_param_name, self.NF_all_val)
#       self.NF_list_def_param = [n[-1] for n in self.NF_all_val]
#-------------------New function ----------------------------

        self.all_function_name_list = [self.function1_name, self.function2_name, self.function3_name, self.function4_name, self.function5_name, self.function6_name]
#-------------------New function ----------------------------
#       self.all_function_name_list = [self.function1_name, self.function2_name, self.function3_name, self.function4_name, self.function5_name, self.function6_name, self.function7_name]
#-------------------New function ----------------------------

    # method how to calculate theoretical elemental function #1
    #RuntimeWarning
    def DbSigmoid(self, data_x, arg): # data_x - the np data array where function 1 is defined, arg - several arguments used to calculate y value of fuction 1
        self.xc, self.a, self.w1, self.w2, self.w3 = arg
        self.data_th1_y = self.a*(1-1/(1+np.exp(-(data_x-self.xc-0.5*self.w1)/self.w3)))/(1+np.exp(-(data_x-self.xc+0.5*self.w1)/self.w2))
        return np.array([data_x, self.data_th1_y])

    # method how to calculate theoretical elemental function #2
    def Sinus(self, data_x, arg):
        self.a, self.w, self.ph = arg
        self.data_th2_y = self.a*np.sin(self.w*data_x + self.ph)
        return np.array([data_x, self.data_th2_y])

    # method how to calculate theoretical elemental function #3
    def Gauss(self, data_x, arg):
        self.a, self.b, self.c = arg
        self.data_th3_y = self.a*(np.exp(-(data_x-self.b)**2/(2*self.c**2) ))
        return np.array([data_x, self.data_th3_y])

    # method how to calculate theoretical elemental function #2
    def EXP(self, data_x, arg):
        self.a, self.b = arg
        self.data_th4_y = self.a*np.exp(-self.b*data_x)
        return np.array([data_x, self.data_th4_y])
    # method how to calculate theoretical elemental function #2
    def LOR(self, data_x, arg):
        self.a, self.x0 = arg
        self.data_th5_y = (self.a/(2*math.pi))/((data_x-self.x0)**2 + 0.25*self.a**2)
        return np.array([data_x, self.data_th5_y])

    def SIG(self, data_x, arg):
        self.a, self.b, self.c = arg
        self.data_th6_y = self.a/(1+np.exp(-2*self.b*(data_x-self.c)))
        return np.array([data_x, self.data_th6_y])

#-------------------New function ----------------------------
#   def NF(self, data_x, arg):
#       self.a, self.b, self.c = arg
#       self.data_th6_y = self.a+self+b+self.c+data_x
#       return np.array([data_x, self.data_th6_y])
#-------------------New function ----------------------------

    def function_select(self, f_name, data_x, param_list):
        # depending on the f_name parameters returns certain mathematical function EXP, LOR, etc
        # f_name - is a acronym used to call function, e.g. f_name = "DbSigmoid"
        # data_x - data.data_exp[0] array
        # param_list list of current parameters of the function  param_list =[4.0, 2.5, 0.6, 0.5, 0.5] for DbSigmoid

        if f_name == "DbSigmoid":
            return self.DbSigmoid(data_x, param_list)
        elif f_name == "Sinus":
            return self.Sinus(data_x, param_list)
        elif f_name == "Gauss":
            return self.Gauss(data_x, param_list)
        elif f_name == "EXP":
            return self.EXP(data_x, param_list)
        elif f_name == "Lorenz":
            return self.LOR(data_x, param_list)
        elif f_name == "Sigmoid":
            return self.SIG(data_x, param_list)
#-------------------New function ----------------------------
#       elif f_name == "New_name":
#           return self.NF(data_x, param_list)
#-------------------New function ----------------------------
        else:
            pass

theory = Th()


