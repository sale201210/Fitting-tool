import wx
import numpy as np
from NumPy1 import data
from ThFunction import Th
from time import sleep
import webbrowser

smooth = 3 # default value of smoothing method
RboxSelection2 = "Signal 1" # default name of signal to display
integral_value = 0


#===================================================================================================
# HelpWin class is not used in Fitting_tool v.1.0
class HelpWin(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Simple tutorial how to use Fitting tool", size = (600,500))
        self.help_panel = HelpPanel(self)
        self.Show()
# HelpPanel class is not used in Fitting_tool v.1.0
class HelpPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        #-------------------------------------------
        self.sizerVer = wx.BoxSizer(wx.HORIZONTAL)
        #-------------------------------------------
        self.sizerHor = wx.BoxSizer(wx.VERTICAL)
        self.Text_0 = wx.StaticText(self, wx.ID_ANY, "Please read the help file:")
        font_Text_0 = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.Text_0.SetFont(font_Text_0)
        webbrowser.open_new(r'Fitting Tool v.1.0 Help.pdf')
        #open("Fitting Tool v.1.0 Help.pdf")
        self.sizerHor.Add(self.Text_0, 0, wx.ALL, 6)

        #-----------------------------------------------
        self.sizerVer.Add(self.sizerHor, 0, wx.TOP)
        self.SetSizerAndFit(self.sizerVer)

class MainWin(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title = "Fitting tool v.1.0", pos=(-1,-1))
        self.makeMenuBar()
        self.CreateStatusBar(number=1, style=wx.STB_DEFAULT_STYLE, id=0, name="StatusBarNameStr")
        self.SetStatusText('Please start with opening/importing data file')
        self.leftPanel = LeftPanel(self)
        self.rightPanel = Rightpanel(self)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.leftPanel, 1, wx.EXPAND|wx.ALL, 1)
        self.sizer.Add(self.rightPanel, 2, wx.EXPAND|wx.ALL, 1)
        self.SetSizerAndFit(self.sizer)
        self.theory2 = Th()
        self.parent = parent

    def makeMenuBar(self):

        file_menu = wx.Menu()
        globalfunk_menu = wx.Menu()
        import_item_InFile = file_menu.Append(-1, item="&Import.. \tCtrl-I", helpString="Import data file - 4 columns: x, y1, y2, y3 where format of x is (dd.mm.yyyy hh:mm:ss) ")
        open_item_InFile = file_menu.Append(-1, item="&Open.. \tCtrl-O", helpString="Open ascii file in following format: "
                                                                                    "2 columns: x, y (delimiter=' '). Numbers are with '.' as decimal point")
        file_menu.AppendSeparator()
        SaveAs_item_InFile = file_menu.Append(wx.ID_SAVEAS)
        glob_fun_static = globalfunk_menu.Append(1, "Global Static Graph", "Global Static superposition Graph")
        glob_fun_dynamic = globalfunk_menu.Append(2, "Global fitting", "Global Dynamic superposition Graph")

        exitItem = file_menu.Append(wx.ID_EXIT)

        help_menu = wx.Menu()
        howtouse_inHelp_Item = help_menu.Append(3, "Open help file", "Step by step instruction how to use this programm")
        about_inHelp_Item = help_menu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(file_menu, "&File")
        menuBar.Append(globalfunk_menu, "&Fitting")
        menuBar.Append(help_menu, "&Help")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnImport, import_item_InFile)
        self.Bind(wx.EVT_MENU, self.OnOpen, open_item_InFile)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, SaveAs_item_InFile)
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.On_howtouse, howtouse_inHelp_Item)
        self.Bind(wx.EVT_MENU, self.OnAbout, about_inHelp_Item)
        self.Bind(wx.EVT_MENU, self.On_static_Graph, glob_fun_static)
        self.Bind(wx.EVT_MENU, self.On_dynamic_Graph, glob_fun_dynamic)

    def OnExit(self, event):
        self.Close(True)

    def On_howtouse(self, event):

        #help_frame = HelpWin(parent=wx.GetTopLevelParent(self))
        webbrowser.open_new(r'Fitting Tool v.1.0 Help.pdf')

    def OnAbout(self, event):
        wx.MessageBox("This program helps to do fitting of complex experimental data with up to four different elemental functions. \nHope you enjoy it. \nAll contacts via sale201210@gmail.com", "About", wx.OK | wx.ICON_INFORMATION)


    def OnSaveAs(self, event):

        with wx.FileDialog(self, "Save cvs file", wildcard="Cvs files (*.cvs)|*.cvs", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as f:
            if f.ShowModal() == wx.ID_CANCEL:
                return
            path = f.GetPath()
            file = f.GetFilename()
            try:
                data.save_exp(path, data.data_exp)
                self.SetStatusText("The modified data has been saved successfully as %s." %file)
            except IOError:
                wx.LogError("Can't save current data in file '%s'." % path)

    def OnImport(self, event):
        with wx.FileDialog(self, "Open csv file", wildcard="4 columns ascii file (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST ) as f:
            if f.ShowModal() == wx.ID_CANCEL:
                return
            path = f.GetPath()
            file = f.GetFilename()
            try:
                data.importdata(path)
                wx.MessageBox("The data file {} has been loaded successfully, it contains {} datapoint (d.p).".format(file, data.filesize))
                self.SetStatusText("Now you can plot experimental signals and proceed with its fitting by some elemental functions")
                self.leftPanel.Text1_L.SetLabel("Data length is {} points".format(data.filesize))
                self.leftPanel.Text2_2_L.SetLabel("Tmax = %.2f min" %data.data_exp[0][data.filesize-1])
                self.leftPanel.Int_max_L.SetValue("{}".format(data.filesize))
                self.SetTitle("Fitting tool v.1.0. Imported file: {} ".format(path))
                self.leftPanel.Rbox2_L.Enable()
            except IOError:
                wx.LogError("Can't open file " )
            except IndexError:
                self.SetStatusText("Experimental data format error ")

    def On_static_Graph(self, event):
        try:
            left_exp_And_th_limit = int(self.leftPanel.t_l)
            # for the sake of convenience make new variable here equal to left user defined limit for experimental signal data time array
            right_exp_And_th_limit = int(self.leftPanel.t_r)
            # the same for right the limit
            self.global_funk_y = np.zeros(data.data_exp[0].size, dtype='f2')
            # create and fill with zero of global_funk_y array. global_funk_y array is a summ of all elementary functions

            for self.obj in self.rightPanel.right_middle.RightMiddleX_object_list:

                self.list_current_param = [float(line[-1].GetValue()) for line in self.obj.RighMiddleX_Ext.TC_obj_list ] # read current parameters for each function
                #self.th_function2 = self.theory2.function_select(self.obj.RighMiddleX_Ext.current, data.data_exp[0], self.list_current_param)
                self.th_function2 = self.theory2.function_select(self.obj.RighMiddleX_Ext.current, data.data_exp[0], self.list_current_param)
                #choose elemental function based on its name taken from self.obj.RighMiddleX_Ext.current
                self.global_funk_y = self.global_funk_y + self.th_function2[1] # global function is sum of all elementary function


            if RboxSelection2 == "Signal 1":
                data.plot2gr(data.data_exp[0], data.smooth(data.data_exp[0], data.data_exp[1], smooth),
                             self.th_function2[0], self.global_funk_y,
                             left_exp_And_th_limit, right_exp_And_th_limit, title="Fitting of Signal 1")
            elif RboxSelection2 == "Signal 2":
                data.plot2gr(data.data_exp[0], data.smooth(data.data_exp[0], data.data_exp[2], smooth),
                             self.th_function2[0], self.global_funk_y,
                             left_exp_And_th_limit, right_exp_And_th_limit, title="Fitting of  Signal 2")
            elif RboxSelection2 == "Signal 3":
                data.plot2gr(data.data_exp[0], data.smooth(data.data_exp[0], data.data_exp[3], smooth),
                             self.th_function2[0], self.global_funk_y,
                             left_exp_And_th_limit, right_exp_And_th_limit, title="Fitting of Signal 3")
            else:
                pass
        except AttributeError:
            for jj in range(0,3):
                self.SetStatusText("")
                sleep(0.6)
                self.SetStatusText("Please start with opening/importing data file")
                sleep(0.6)

    def On_dynamic_Graph(self, event):
        try:
            #------------------------------------ Some usefull in further variables
            left_exp_And_th_limit = int(self.leftPanel.t_l)
            # for the sake of convenience make new variable here equal to left user defined limit for experimental signal data time array
            right_exp_And_th_limit = int(self.leftPanel.t_r)
            # the same for right the limit
            self.all_param_all_funk_list = [] # to store list of all parameters for every elementary function
            self.global_funk_y2 = np.zeros(data.data_exp[0].size, dtype='f2') # create and fill with zero of global_funk_y array. global_funk_y array is a summ of all elementary functions
            self.temp_list2 = []
            #----------------------------------------------
            for self.obj in self.rightPanel.right_middle.RightMiddleX_object_list: #iterate on earlier created b=RighmiddleX object list (which helps to ges assess to every elementary function
                self.temp_list2.append(self.obj.RighMiddleX_Ext.sum) # add self.obj.RighMiddleX_Ext.sum = 0 if no any errors found
            #-----------------------------------------------
            if sum(self.temp_list2) == 0: # equivalent to absence of error in the expression:  min < def < max numbers, since self.temp_list2 = [0,0,..0] if no error is found for every function

                self.list_of_f_name = []
                for self.obj in self.rightPanel.right_middle.RightMiddleX_object_list: #iterate through earlier created b=RighmiddleX object list (which helps to ges assess to every elementary function

                    self.list_name_param = [_.GetLabel() for _ in self.obj.RighMiddleX_Ext.TX_list]
                    self.list_min_param = [float(line[0].GetValue()) for line in self.obj.RighMiddleX_Ext.TC_obj_list]
                    self.list_max_param = [float(line[1].GetValue()) for line in self.obj.RighMiddleX_Ext.TC_obj_list]
                    self.list_current_param = [float(line[-1].GetValue()) for line in self.obj.RighMiddleX_Ext.TC_obj_list]

                    #self.th_function3 = self.theory2.function_select(self.obj.RighMiddleX_Ext.current, data.data_exp[0], self.list_current_param)
                    self.th_function3 = self.theory2.function_select(self.obj.RighMiddleX_Ext.current, data.data_exp[0], self.list_current_param)

                    all_param = list(zip(self.list_name_param, self.list_min_param, self.list_max_param, self.list_current_param)) # for current function zip all its parameters
                    # example of format: [('Xc', 0.01, 10.0, 2.0), ('A ', 0.05, 40.0, 20.0), ('W1', 0.05, 1.0, 0.4), ('W2', 0.05, 1.0, 0.4), ('W3', 0.05, 1.0, 0.4)]

                    self.all_param_all_funk_list.append(all_param) # make list of parameters for all elementary functions with
                    self.list_of_f_name.append(self.obj.RighMiddleX_Ext.current)
                    self.global_funk_y2 = self.global_funk_y2 + self.th_function3[1] # global function is sum of all elementary function

                if RboxSelection2 == "Signal 1":
                    self.optimized_global_parameters = data.dynamic_gr(data.data_exp[0], data.smooth(data.data_exp[0], data.data_exp[1], smooth),
                                    self.th_function3[0], self.global_funk_y2,
                                    self.all_param_all_funk_list, left_exp_And_th_limit, right_exp_And_th_limit, self.list_of_f_name, title="Fitting of Signal 1")
                elif RboxSelection2 == "Signal 2":
                    self.optimized_global_parameters = data.dynamic_gr(data.data_exp[0], data.smooth(data.data_exp[0], data.data_exp[2], smooth),
                                    self.th_function3[0], self.global_funk_y2,
                                    self.all_param_all_funk_list, left_exp_And_th_limit, right_exp_And_th_limit, self.list_of_f_name, title="Fitting of Signal 2")
                elif RboxSelection2 == "Signal 3":
                    self.optimized_global_parameters = data.dynamic_gr(data.data_exp[0], data.smooth(data.data_exp[0], data.data_exp[3], smooth),
                                    self.th_function3[0], self.global_funk_y2,
                                    self.all_param_all_funk_list, left_exp_And_th_limit, right_exp_And_th_limit, self.list_of_f_name, title="Fitting of Signal 3")
                else:
                    pass

                # ---- update current (default) values of parameters of all functions with optimized by user values
                for n in range(0, len(self.list_of_f_name)): # iterate through all functions
                    for i in range(0, len(self.list_current_param)): # iterate through all default parameters
                        self.rightPanel.right_middle.RightMiddleX_object_list[n].RighMiddleX_Ext.TC_obj_list[i][-1].SetValue(str(round(self.optimized_global_parameters[n][i], 3)))
            else:
                pass
        except AttributeError:
            for jj in range(0,3):
                self.SetStatusText("")
                sleep(0.6)
                self.SetStatusText("Please start with opening/importing data file")
                sleep(0.6)

    def OnOpen(self, event):
        with wx.FileDialog(self, "Open ascii file", wildcard="ascii file (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST ) as f:
            if f.ShowModal() == wx.ID_CANCEL:
                return
            path = f.GetPath()
            file = f.GetFilename()
            try:
                data.opendata(path)
                wx.MessageBox("The data file {} has been loaded successfully, it contains {} datapoint (d.p).".format(file, data.filesize))
                self.SetStatusText("Now you can plot experimental signals and proceed with its fitting by some elemental functions")
                self.leftPanel.Text1_L.SetLabel("Data length is {} points".format(data.filesize))
                self.leftPanel.Text2_2_L.SetLabel("Tmax = %.2f min" %data.data_exp[0][data.filesize-1])
                self.leftPanel.Int_max_L.SetValue("{}".format(data.filesize))
                self.SetTitle("Fitting tool v.1.0. Opened file: {} ".format(path))
                #if data.data_exp.shape[0] == 2:
                #    self.leftPanel.Rbox2_L.Disable()

            except IOError:
                wx.LogError("Can't open file " )
            except IndexError:
                self.SetStatusText("Experimental data format error ")

#===================================================================================================

class LeftPanel(wx.Panel):

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        """ 
        Start of description of the gadgets on the left side of the panel
        """
        Topsizer_L = wx.BoxSizer(wx.VERTICAL)

    #------------------------------------------------
        self.Text0_L = wx.StaticText(self, wx.ID_ANY, "Original data, derivative and integral calculation")
        font0_L = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.Text0_L.SetFont(font0_L)

        Text0_L_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Text0_L_sizer.Add(self.Text0_L, 0, wx.ALL, 6)
    #------------------------------------------------
        self.Text1_L = wx.StaticText(self, wx.ID_ANY, "Data length is {} points".format(0))

        Text1_L_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Text1_L_sizer.Add(self.Text1_L, 0, wx.ALL, 5)
    #------------------------------------------------
        self.Text2_1_L = wx.StaticText(self, wx.ID_ANY, "Tmin = 0 min")
        self.Text2_2_L = wx.StaticText(self, wx.ID_ANY, "Tmax =   min")

        Text2_L_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Text2_L_sizer.Add(self.Text2_1_L, 0, wx.ALL, 5)
        Text2_L_sizer.Add(self.Text2_2_L, 0, wx.ALL, 5)
    #------------------------------------------------
        smoothings= ["None", "#1", "#2", "#3"] # names of smoothing methods
        self.Rbox1_L = wx.RadioBox(self, label = "Select smoothing method, if necessary", majorDimension = 1, choices = smoothings[::-1], style = wx.RA_SPECIFY_ROWS | wx.CENTER)
        self.Bind(wx.EVT_RADIOBOX, self.OnRBox1_L, self.Rbox1_L)                                        # It is convenient to present smoothingg methods in a reverse order

        Rbox1_L_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Rbox1_L_sizer.Add(self.Rbox1_L, 0, wx.ALL, 5)
    #------------------------------------------------
        signals = ["Signal 1", "Signal 2", "Signal 3"] # names of signals
        self.Rbox2_L = wx.RadioBox(self, label = "Select Signal to show", majorDimension = 3, choices = signals, style = wx.RA_SPECIFY_ROWS | wx.CENTER)
        self.Bind(wx.EVT_RADIOBOX, self.OnRBox2_L, self.Rbox2_L)
        self.Rbox2_L.Disable()
        Rbox2_L_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Rbox2_L_sizer.Add(self.Rbox2_L, 0, wx.ALL, 5)
    #------------------------------------------------
        self.button_plot_L = wx.Button(self, label = "Show experimental Signal ") #make a button to show experimental signal as is
        self.Bind(wx.EVT_BUTTON, self.OnButton_plot, self.button_plot_L)

        Button_plot_L_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Button_plot_L_sizer.Add(self.button_plot_L, 0, wx.ALL, 5)
    #------------------------------------------------
        self.Emptyline1 = wx.StaticText(self, label = "") # Small trick for adjusting height of the window
    #------------------------------------------------
        self.Text3_Integral_title_L = wx.StaticText(self, label = "Enter left and right X limits (in points) for further proceeding", style = wx.ALIGN_CENTER)

        Text3_L_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Text3_L_sizer.Add(self.Text3_Integral_title_L, 0, wx.ALL, 5)
    #------------------------------------------------
        self.Int_min_L = wx.TextCtrl(self, value = "0", style = wx.TE_PROCESS_ENTER) # Textcontrol box for left limit
        self.Bind(wx.EVT_TEXT, self.OnInt_time_l, self.Int_min_L)

        self.Int_max_L = wx.TextCtrl(self, value = " " , style = wx.TE_PROCESS_ENTER) # Textcontrol box for right limit
        self.Bind(wx.EVT_TEXT, self.OnInt_time_r, self.Int_max_L)

        Int_min_mix_L_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Int_min_mix_L_sizer.Add(self.Int_min_L, 0, wx.ALL, 5)
        Int_min_mix_L_sizer.Add(self.Int_max_L, 0, wx.ALL, 5)
    #------------------------------------------------
        self.Time_l_L = wx.StaticText(self, label = "0, min", style = wx.ALIGN_LEFT) # display time corresponding to the left limit
        #self.gap_l_L = wx.StaticText(self, label = "       ", style = wx.ALIGN_LEFT)
        self.Time_r_L = wx.StaticText(self, label = "0, min", style = wx.ALIGN_RIGHT) # display time corresponding to the right limit

        Time_l_r_L_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Time_l_r_L_sizer.Add(self.Time_l_L, 0, wx.RIGHT, 25)
        Time_l_r_L_sizer.Add(self.Time_r_L, 0, wx.LEFT, 25)
    #------------------------------------------------

        self.Emptyline2 = wx.StaticText(self, label = "") # Small trick for adjusting height of the window
    #------------------------------------------------
        self.button_intergal_L = wx.Button(self, label = "Find integral") # Create intergal button
        self.Bind(wx.EVT_BUTTON, self.OnButton_int_L, self.button_intergal_L)

        Button_Itegral_L_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Button_Itegral_L_sizer.Add(self.button_intergal_L, 0, wx.ALL, 5)
    #------------------------------------------------
        self.Intergal_text_L = wx.StaticText(self, label = "Integral of {} = {}".format(RboxSelection2, integral_value ), style = wx.ALIGN_CENTER)
        # display value of integral of the selected experimental signal within left and right limits
        Text4_Intergal_text_L_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Text4_Intergal_text_L_sizer.Add(self.Intergal_text_L, 0, wx.ALL, 5)

    #------------------------------------------------
      # Adding all individual sizers for each gadget to Topsizer_L
        Topsizer_L.Add(Text0_L_sizer, 0, wx.CENTER)
        Topsizer_L.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        Topsizer_L.Add(Text1_L_sizer, 0, wx.CENTER)
        Topsizer_L.Add(Text2_L_sizer, 0, wx.CENTER)
        Topsizer_L.Add(Rbox1_L_sizer, 0, wx.CENTER)
        Topsizer_L.Add(Rbox2_L_sizer, 0, wx.CENTER)
        Topsizer_L.Add(Button_plot_L_sizer, 0, wx.CENTER)
        Topsizer_L.Add(self.Emptyline1, 0, wx.ALL, 7)
        Topsizer_L.Add(Text3_L_sizer, 0, wx.CENTER)
        Topsizer_L.Add(Int_min_mix_L_sizer, 0, wx.CENTER)
        Topsizer_L.Add(Time_l_r_L_sizer, 0, wx.CENTER)
        Topsizer_L.Add(self.Emptyline2, 0, wx.ALL, 7)
        Topsizer_L.Add(Text4_Intergal_text_L_sizer, 0, wx.CENTER)
        Topsizer_L.Add(Button_Itegral_L_sizer, 0, wx.CENTER)


        """ 
        End of description of the gadgets on the left side of the panel
        """

        self.SetSizerAndFit(Topsizer_L)

    """List of methods used in the LeftPanel"""
    def OnInt_time_l(self, event): # setting the left intergation limit
        self.t_r = self.Int_max_L.GetValue() #read value of maximum user defined index within data.data_exp[0] array
        self.t_l = self.Int_min_L.GetValue() #read value of minimum user defined index within data.data_exp[0] array
        try:
            if not self.t_r: # check if t_r has not been entered by user yet
                if int(self.t_l) < data.filesize and int(self.t_l) > 0: # left limit has to be above zero and lower than size of signal data array, if so
                    time_l = round(data.data_exp[0][int(self.t_l)-1],2) # calculate time in minutes
                    self.Time_l_L.SetLabel(str(time_l) +" " + "min") # update the corresponding label
                else:
                    pass
            else: # when t_r has been entered by user already
                if int(self.t_l) < int(self.t_r) and int(self.t_l) > 0: # t_l has to be less then t_r
                    time_l = round(data.data_exp[0][int(self.t_l)-1],2)
                    self.Time_l_L.SetLabel(str(time_l) +" " + "min")
                else:
                    pass
        except ValueError:
            pass
        except AttributeError:
            for jj in range(0,3):
                self.GetParent().SetStatusText("")
                sleep(0.6)
                self.GetParent().SetStatusText("Please start with opening/importing data file")
                sleep(0.6)

    def OnInt_time_r(self, event): # similar comments
        self.t_r = self.Int_max_L.GetValue() #read value of maximum user defined index within data.data_exp[0] array
        self.t_l = self.Int_min_L.GetValue() #read value of minimum user defined index within data.data_exp[0] array
        try:
            if not self.t_l:
                if int(self.t_r) <= data.filesize and int(self.t_r) > 0:
                    time_r = round(data.data_exp[0][int(self.t_r)-1],2)
                    self.Time_r_L.SetLabel(str(time_r) + " "+ "min")
                else:
                    pass
            else:
                if int(self.t_r) <= data.filesize and int(self.t_r) > int(self.t_l): # t_l has to be less then t_r
                    time_r = round(data.data_exp[0][int(self.t_r)-1],2)
                    self.Time_r_L.SetLabel(str(time_r) +" "+ "min")
                else:
                    pass
        except ValueError:
            pass
        except AttributeError:
            for jj in range(0,3):
                self.GetParent().SetStatusText("")
                sleep(0.6)
                self.GetParent().SetStatusText("Please start with opening/importing data file")
                sleep(0.6)

    def OnRBox1_L(self, event): # selection of the smoothing method (used to plot graps and calculate differentials
        RboxSelection1 = self.Rbox1_L.GetStringSelection()

        if RboxSelection1 == "#1":
            sm = 1
        elif RboxSelection1 == "#2":
            sm = 2
        elif RboxSelection1 == "#3":
            sm = 3
        else:
            sm = 0
        global smooth
        smooth = sm

    def OnRBox2_L(self, event): # selection of type of signal: signal1, signal2, signal3, diff_signal1, diff_signal2, diff_signal3
        global RboxSelection2
        RboxSelection2 = self.Rbox2_L.GetStringSelection()
        self.Intergal_text_L.SetLabel("Integral of {} = {}".format(RboxSelection2, integral_value))

    def OnButton_int_L(self, event): # integration of various signals
        try:
            if RboxSelection2 == "Signal 1":
                integral_value = data.intergSignal(data.data_exp[0],data.data_exp[1], int(self.Int_min_L.GetValue()), int(self.Int_max_L.GetValue()))
                self.Intergal_text_L.SetLabel("Integral of {} = {}".format(RboxSelection2, integral_value))
            elif RboxSelection2 == "Signal 2":
                integral_value = data.intergSignal(data.data_exp[0],data.data_exp[2], int(self.Int_min_L.GetValue()), int(self.Int_max_L.GetValue()))
                self.Intergal_text_L.SetLabel("Integral of {} = {}".format(RboxSelection2, integral_value))
            elif RboxSelection2 == "Signal 3":
                integral_value = data.intergSignal(data.data_exp[0],data.data_exp[3], int(self.Int_min_L.GetValue()), int(self.Int_max_L.GetValue()))
                self.Intergal_text_L.SetLabel("Integral of {} = {}".format(RboxSelection2, integral_value))
            else:
                pass
        except AttributeError:
            for jj in range(0,3):
                self.GetParent().SetStatusText("")
                sleep(0.6)
                self.GetParent().SetStatusText("Please start with opening/importing data file")
                sleep(0.6)

    def OnButton_plot(self, event): # Plotting graphs of the selected signals with chosen smoothing option as "smooth"

        try:
            if RboxSelection2 == "Signal 1":
                data.plot1gr_deriv(data.data_exp[0], data.smooth(data.data_exp[0], data.data_exp[1], smooth), int(self.Int_min_L.GetValue()), int(self.Int_max_L.GetValue()), title="Signal 1")
            elif RboxSelection2 == "Signal 2":
                data.plot1gr_deriv(data.data_exp[0], data.smooth(data.data_exp[0], data.data_exp[2], smooth), int(self.Int_min_L.GetValue()), int(self.Int_max_L.GetValue()), title="Signal 2")
                #data.plot1gr(data.data_exp[0], data.smooth(data.data_exp[0], data.data_exp[2], smooth), x1_label="Time, min", y1_label="Signal 2, a.u.", title="CO release")
            elif RboxSelection2 == "Signal 3":
                data.plot1gr_deriv(data.data_exp[0], data.smooth(data.data_exp[0], data.data_exp[3], smooth), int(self.Int_min_L.GetValue()), int(self.Int_max_L.GetValue()), title="Signal 3")
                #data.plot1gr(data.data_exp[0], data.smooth(data.data_exp[0], data.data_exp[3], smooth), x1_label="Time, min", y1_label="Signal 3, a.u.", title="Signal 3 vs time dependency")
            else:
                pass
        except AttributeError:
            for jj in range(0,3):
                self.GetParent().SetStatusText("")
                sleep(0.6)
                self.GetParent().SetStatusText("Please start with opening/importing data file")
                sleep(0.6)

#===================================================================================================

class Rightpanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.right_middle = RightMiddle(self)
        self.right_top = Righttop(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.right_top, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.right_middle, 0, wx.ALL | wx.EXPAND, 5)
        self.SetSizerAndFit(self.sizer)

#===================================================================================================

class Righttop(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        Topsizer_R = wx.BoxSizer(wx.VERTICAL)

        #---------------------------------------------------
        self.Text1_R = wx.StaticText(self, wx.ID_ANY, label = "Fitting part", style = wx.CENTER)
        font0_R = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.Text1_R.SetFont(font0_R)

        Text1_R_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        Text1_R_Sizer.Add(self.Text1_R, 0, wx.ALL, 5)
        #---------------------------------------------------
        self.Text2_R = wx.StaticText(self, label = "Select number of elementary functions", style = wx.CENTER)

        Text2_R_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Text2_R_sizer.Add(self.Text2_R, 0, wx.ALL, 5)
        #---------------------------------------------------
        self.Nfunction = wx.ComboBox(self, choices=["1", "2", "3", "4"], size=(100, -1))
        self.Nfunction.Bind(wx.EVT_COMBOBOX, self.GetParent().right_middle.Change)

        self.Reset_button = wx.Button(self, label = "Reset", size=(100, 30))
        self.Bind(wx.EVT_BUTTON, self.OnReset_button, self.Reset_button)
        self.Reset_button.Disable()
        Nfunction_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Nfunction_sizer.Add(self.Nfunction, 0, wx.ALL, 5)
        Nfunction_sizer.Add(self.Reset_button, 0, wx.ALL, 5)
        #---------------------------------------------------

        Topsizer_R.Add(Text1_R_Sizer, 0, wx.CENTER)
        Topsizer_R.Add(wx.StaticLine(self), 0, wx.EXPAND, 5)
        Topsizer_R.Add(Text2_R_sizer, 0, wx.CENTER, 5)
        Topsizer_R.Add(Nfunction_sizer, 0, wx.CENTER, 5)

        self.SetSizerAndFit(Topsizer_R)
        self.GetParent().Fit()

    def OnReset_button(self, event):

            for obj in self.GetParent().right_middle.RightMiddleX_object_list:
                if obj:
                    obj.Destroy()
            self.Nfunction.Enable()


#===================================================================================================

class RightMiddle(wx.Panel):
    userchoices = [" "] # create list to store choices of user
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizerAndFit(self.sizer)

    def Change(self, e):
        self.n_funk = int(e.GetString()) #current choice of user
        self.RightMiddleX_object_list = []
        self.userchoices.append(self.n_funk) # add it the list of choices
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.GetParent().right_top.Nfunction.Disable() # disable 1st combox, so that the user can't modify the number of elemental functions selected
        self.GetParent().right_top.Reset_button.Enable()
        for a in range(self.n_funk): # create new objects
            self.b = RightMiddleX(self) # create new object of RightMiddleX class
            self.sizer.Add(self.b, 0, wx.EXPAND|wx.ALL, 5)
            self.SetSizerAndFit(self.sizer)
            self.RightMiddleX_object_list.append(self.b) # make list of n_funk number of RightMiddleX panel objects

#===================================================================================================

class RightMiddleX(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        Topsizer_RBX = wx.BoxSizer(wx.VERTICAL)
        #-------------------------------------
        self.text1 = wx.StaticText(self, label = " Select  type  of  function  ", style = wx.CENTER)
        text1_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text1_sizer.Add(self.text1, 0, wx.CENTER, 5)
        #-------------------------------------
        self.theory2 = Th()
        #self.Elem_Funk = wx.ComboBox(self, choices=self.theory2.all_function_name_list)
        self.Elem_Funk = wx.ComboBox(self, choices=self.theory2.all_function_name_list)
        elem_Funk_sizer = wx.BoxSizer(wx.HORIZONTAL)
        elem_Funk_sizer.Add(self.Elem_Funk, 0, wx.CENTER, 0)
        #-------------------------------------
        self.RighMiddleX_Ext = RighMiddleX_Extclass(self)
        self.Elem_Funk.Bind(wx.EVT_COMBOBOX, self.RighMiddleX_Ext.F_Option)

        RighMiddleX_Ext_sizer = wx.BoxSizer(wx.HORIZONTAL)
        RighMiddleX_Ext_sizer.Add(self.RighMiddleX_Ext, 0, wx.CENTER, 0)
        #-------------------------------------

        Topsizer_RBX.Add(text1_sizer, 0, wx.ALL | wx.EXPAND |wx.CENTER,5)
        Topsizer_RBX.Add(elem_Funk_sizer, 0, wx.ALL | wx.CENTER,5)
        Topsizer_RBX.Add(RighMiddleX_Ext_sizer, 0, wx.ALL | wx.CENTER, 5 )
        self.SetSizerAndFit(Topsizer_RBX)

        #self.GetGrandParent().Fit()
        #self.Fit()

#===================================================================================================
class RighMiddleX_Extclass(wx.Panel):
    userchoices = [" "] # create list to store choices of user
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.list_current_param = []
        self.list_current_param_fl = []
        self.current = ''
        self.temp_list = [] # contains 0 if min < current < max or 1 in any opposite case
        self.sum = sum(self.temp_list)
        self.sizer0 = wx.BoxSizer(wx.VERTICAL)

        self.text1 = wx.StaticText(self, label = "", style = wx.CENTER) # This empty line is needed to reserve space in the panel
        self.text2 = wx.StaticText(self, label = "", style = wx.CENTER) # This empty line is needed to reserve space in the panel
        self.text3 = wx.StaticText(self, label = "", style = wx.CENTER) # This empty line is needed to reserve space in the panel
        self.sizer0.Add(self.text1, 1, wx.ALL, 60)
        self.sizer0.Add(self.text2, 1, wx.ALL, 60)
        self.sizer0.Add(self.text3, 1, wx.ALL, 60)

        self.SetSizerAndFit(self.sizer0)
        #self.GetParent().Fit()

    def F_Option(self, event):
        try:
            self.current = event.GetString() #current choice of the user
            self.userchoices.append(self.current) # add it to the list of choices
            self.theory2 = Th() # make object from TH class

            if self.current == "DbSigmoid":
                self.funk_comb_param = self.theory2.DS_comb
                self.list_current_param = self.theory2.DS_list_def_param
                self.fun_param_name = self.theory2.DS_param_name

            elif self.current == "Sinus":
                self.funk_comb_param = self.theory2.SN_comb
                self.list_current_param = self.theory2.SN_list_def_param
                self.fun_param_name = self.theory2.SN_param_name

            elif self.current == "Gauss":
                self.funk_comb_param = self.theory2.GS_comb
                self.list_current_param = self.theory2.GS_list_def_param
                self.fun_param_name = self.theory2.GS_param_name

            elif self.current == "EXP":
                self.funk_comb_param = self.theory2.EXP_comb
                self.list_current_param = self.theory2.EXP_list_def_param
                self.fun_param_name = self.theory2.EXP_param_name

            elif self.current == "Lorenz":
                self.funk_comb_param = self.theory2.LOR_comb
                self.list_current_param = self.theory2.LOR_list_def_param
                self.fun_param_name = self.theory2.LOR_param_name

            elif self.current == "Sigmoid":
                self.funk_comb_param = self.theory2.SIG_comb
                self.list_current_param = self.theory2.SIG_list_def_param
                self.fun_param_name = self.theory2.SIG_param_name
#-------------------New function ----------------------------
#           elif self.current == "New_name":
#               self.funk_comb_param = self.theory2.NF_comb
#               self.list_current_param = self.theory2.NF_list_def_param
#               self.fun_param_name = self.theory2.NF_param_name
#-------------------New function ----------------------------

            self.sizer1 = wx.BoxSizer(wx.VERTICAL)

            self.TC_obj_list = [] # list of all TC objects (TextControl)
            self.param_text0 = wx.StaticText(self, label = "   ", style = wx.CENTER)
            self.param_text1 = wx.StaticText(self, label = "Min", style = wx.CENTER)
            self.param_text2 = wx.StaticText(self, label = "Max", style = wx.CENTER)
            self.param_text3 = wx.StaticText(self, label = "Def", style = wx.CENTER)

            self.minmaxdef_sizer = wx.BoxSizer(wx.HORIZONTAL)

            self.minmaxdef_sizer.Add(self.param_text0, 0, wx.LEFT|wx.RIGHT, 10)
            self.minmaxdef_sizer.Add(self.param_text1, 0, wx.LEFT|wx.RIGHT, 10)
            self.minmaxdef_sizer.Add(self.param_text2, 0, wx.LEFT|wx.RIGHT, 10)
            self.minmaxdef_sizer.Add(self.param_text3, 0, wx.LEFT|wx.RIGHT, 10)

            self.sizer1.Add(self.minmaxdef_sizer, 0, wx.ALL, 5)
            #--------------------------------------
            self.sizer1.Add(wx.StaticLine(self), 0, wx.EXPAND, 5)
            #--------------------------------------
            self.TX_list = [] # list of name of parameters
            #  for line in self.theory2.DS_comb:
            for line in self.funk_comb_param:

                self.sizerline = wx.BoxSizer(wx.HORIZONTAL)
                self.param_text_ = wx.StaticText(self, label = line[0], style = wx.CENTER) # displays name of a parameter
                self.TX_list.append(self.param_text_) # it has format of [param_text_, param_text_, param_text_,... ] = ['Xc', 'A' , 'W1', 'W2', 'W3']
                self.sizerline.Add(self.param_text_)
                #-----------------------------------
                self.TC_list = [] # list of values of min, max, def
                for val in line[1]:
                    self.param_TC_ = wx.TextCtrl(self, value = str(val), size = (37,-1), style = wx.CENTER)
                    self.Bind(wx.EVT_TEXT, self.OnTypeText, self.param_TC_)
                    self.TC_list.append(self.param_TC_) # it has format of [self.param_TC_, self.param_TC_, self.param_TC_] = [min, max, def]
                    self.sizerline.Add(self.param_TC_, 0, wx.LEFT|wx.RIGHT, 6)

                self.TC_obj_list.append(self.TC_list) # format [[min, max, def], [min, max, def], [min, max, def],...] it is needed to read new min, max, dev values
                self.sizer1.Add(self.sizerline, 0, wx.ALL, 5)

            # these left and right limits will be used to zoom all (static and dynamic) graphs of experimental and theoretical functions in further.
            # This is needed to let user focus on the most informative part of the curve, if necessary
            #------------------------------------------------------------------
            self.sizer_button_DG = wx.BoxSizer(wx.HORIZONTAL)
            self.button_Dynamic = wx.Button(self, label = "Local fitting") # define plot dynamic graph button
            self.Bind(wx.EVT_BUTTON, self.OnButton_dynamic, self.button_Dynamic)
            self.sizer_button_DG.Add(self.button_Dynamic, 0, wx.ALL, 5)
            self.sizer1.Add(self.sizer_button_DG, 0, wx.CENTER, 0)

            #------------------------------------------------------------------
            self.sizer_ST_INT = wx.BoxSizer(wx.HORIZONTAL)
            self.Int_text = wx.StaticText(self, label = "Integral = ", style = wx.ALIGN_CENTER)
            self.sizer_ST_INT.Add(self.Int_text, 0, wx.ALL, 5)
            self.sizer1.Add(self.sizer_ST_INT, 0, wx.CENTER, 0)
            #------------------------------------------------------------------
            self.sizer_button_Int = wx.BoxSizer(wx.HORIZONTAL)
            self.button_integral = wx.Button(self, label = "Find integral") # define intergal button
            self.Bind(wx.EVT_BUTTON, self.OnFind_integral, self.button_integral)
            self.sizer_button_Int.Add(self.button_integral, 0, wx.ALL, 5)
            self.sizer1.Add(self.sizer_button_Int, 0, wx.CENTER, 0)
            #------------------------------------------------------------------
            self.sizer_button_SV = wx.BoxSizer(wx.HORIZONTAL)
            self.button_save_th_date = wx.Button(self, label = "Save data") # saves calculated data
            self.Bind(wx.EVT_BUTTON, self.OnSave_data, self.button_save_th_date)
            self.sizer_button_SV.Add(self.button_save_th_date, 0, wx.ALL, 5)
            self.sizer1.Add(self.sizer_button_SV, 0, wx.CENTER, 0)
            #------------------------------------------------------------------
            # disable combobox, so no any changes are allowed here
            self.GetParent().Elem_Funk.Disable()
            #------------------------------------------------------------------
            self.SetSizerAndFit(self.sizer1)
            self.GetParent().Fit()
        except AttributeError:
            for jj in range(0,3):
                self.GetGrandParent().GetGrandParent().SetStatusText("")
                sleep(0.6)
                self.GetGrandParent().GetGrandParent().SetStatusText("Please start with opening/importing data file")
                sleep(0.6)

    #------------------------------------------------
    def OnTypeText(self, event):
        try:
                self.list_min_param = [float(line[0].GetValue()) for line in self.TC_obj_list ] # list list of minimum values of parameters
                self.list_current_param = [float(line[-1].GetValue()) for line in self.TC_obj_list ] # read list of current = default parameters
                self.list_max_param = [float(line[1].GetValue()) for line in self.TC_obj_list ] # read list of maxnumum values of parameters

                comb_list = list(zip(self.list_min_param, self.list_current_param, self.list_max_param))
                #  comb_list = [(min, def, max), (min, def, max), (min, def, max), (min, def, max), (min, def, max)]
                self.temp_list = [] # each time when min, current and max parameters (of each elementary function) are modified, the old self.temp_list has be emptied
                for three_param in comb_list:
                    index_ = comb_list.index(three_param)
                    if three_param[1] > three_param[2] or three_param[1] < three_param[0]:
                        self.TC_obj_list[index_][-1].SetBackgroundColour("red") # highlight def textcontrol filled with red color, if max < def  or def < min
                        self.temp_list.append(1)
                    else:
                        self.temp_list.append(0)
                        if self.TC_obj_list[index_][-1].GetBackgroundColour() == "red":
                            self.TC_obj_list[index_][-1].SetBackgroundColour("white")
                self.sum = sum(self.temp_list)

        except ValueError:
            pass
#------------------------------------------------
    def OnSave_data(self, event):
        try:
            self.list_current_param = [float(line[-1].GetValue()) for line in self.TC_obj_list ]
            self.th_function = self.theory2.function_select(self.current, data.data_exp[0], self.list_current_param)

            with wx.FileDialog(self, "Save cvs file", wildcard="Cvs files (*.cvs)|*.cvs", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as f:
                if f.ShowModal() == wx.ID_CANCEL:
                    return
                path = f.GetPath()
                file = f.GetFilename()
                try:
                    data.save_exp(path, self.th_function)
                    self.GetGrandParent().GetGrandParent().SetStatusText("The {} dataset has been saved successfully as {}".format(self.current, file))

                except IOError:
                    wx.LogError("Can't save current data in file '%s'." % path)
        except AttributeError:
            for jj in range(0,3):
                self.GetGrandParent().GetGrandParent().SetStatusText("")
                sleep(0.6)
                self.GetGrandParent().GetGrandParent().SetStatusText("Please start with opening/importing data file")
                sleep(0.6)


#------------------------------------------------
    def OnFind_integral(self, event):
        try:
            self.list_current_param = [float(line[-1].GetValue()) for line in self.TC_obj_list ]
            self.left_exp_And_th_limit = int(self.GetGrandParent().GetGrandParent().leftPanel.t_l) # define new variable for left time limit
            self.right_exp_And_th_limit = int(self.GetGrandParent().GetGrandParent().leftPanel.t_r)
            #------------ update th_function with new (optimal) parameters

            self.th_function = self.theory2.function_select(self.current, data.data_exp[0], self.list_current_param)

            #------------ calculate and show integral
            self.found_integral = data.intergSignal(self.th_function[0], self.th_function[1], self.left_exp_And_th_limit, self.right_exp_And_th_limit)
            self.Int_text.SetLabel("Integral = {}".format(self.found_integral))
        except AttributeError:
            for jj in range(0,3):
                self.GetGrandParent().GetGrandParent().SetStatusText("")
                sleep(0.6)
                self.GetGrandParent().GetGrandParent().SetStatusText("Please start with opening/importing data file")
                sleep(0.6)
#------------------------------------------------
    def OnButton_dynamic(self, event):
        try:
            self.list_name_param = [_.GetLabel() for _ in self.TX_list ]
            self.list_min_param = [float(line[0].GetValue()) for line in self.TC_obj_list ]
            self.list_max_param = [float(line[1].GetValue()) for line in self.TC_obj_list ]
            self.list_current_param = [float(line[-1].GetValue()) for line in self.TC_obj_list ]
            self.th_function = self.theory2.function_select(self.current, data.data_exp[0], self.list_current_param)

            if self.sum == 0:

                self.left_exp_And_th_limit = int(self.GetGrandParent().GetGrandParent().leftPanel.t_l) # for the sake of convenience make new variable here equal to left user defined limit for experimental signal data time array
                self.right_exp_And_th_limit = int(self.GetGrandParent().GetGrandParent().leftPanel.t_r) # the same for the right limit

                if RboxSelection2 == "Signal 1":
                    self.optimized_current_values = data.dynamic_plot2gr_deriv(data.data_exp[0], data.smooth(data.data_exp[0], data.data_exp[1], smooth),
                                           self.th_function[0], self.th_function[1],
                                           self.fun_param_name, self.list_min_param, self.list_max_param, self.list_current_param,
                                           self.left_exp_And_th_limit, self.right_exp_And_th_limit, self.current, 'Signal 1')
                elif RboxSelection2 == "Signal 2":
                    self.optimized_current_values = data.dynamic_plot2gr_deriv(data.data_exp[0], data.smooth(data.data_exp[0], data.data_exp[2], smooth),
                                           self.th_function[0], self.th_function[1],
                                           self.fun_param_name, self.list_min_param, self.list_max_param, self.list_current_param,
                                           self.left_exp_And_th_limit, self.right_exp_And_th_limit, self.current, 'Signal 2')
                elif RboxSelection2 == "Signal 3":
                    self.optimized_current_values = data.dynamic_plot2gr_deriv(data.data_exp[0], data.smooth(data.data_exp[0], data.data_exp[3], smooth),
                                                   self.th_function[0], self.th_function[1],
                                                   self.fun_param_name, self.list_min_param, self.list_max_param, self.list_current_param,
                                                   self.left_exp_And_th_limit, self.right_exp_And_th_limit, self.current, 'Signal 3')
                else:
                    pass

                # ------ update optimized parameters in the Textcontrol boxes
                for i in range(0, len(self.TC_obj_list)):
                    self.TC_obj_list[i][-1].SetValue(str(self.optimized_current_values[i]))

            else:
                pass

        except AttributeError:
            for jj in range(0,3):
                self.GetGrandParent().GetGrandParent().SetStatusText("")
                sleep(0.6)
                self.GetGrandParent().GetGrandParent().SetStatusText("Please start with opening/importing data file")
                sleep(0.6)

#===================================================================================================

if __name__ == '__main__':

    app = wx.App()
    main_win = MainWin(parent=None)
    main_win.Show()
    app.MainLoop()
