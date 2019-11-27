import numpy as np
from ThFunction import Th
import matplotlib.pyplot as plt
import math
from matplotlib.widgets import Slider, Button

class Work():

    def __init__(self):
        self.theory1 = Th()
        pass

    def opendata(self, path):
        self.path = path
        time, signal1 =  np.loadtxt(self.path, delimiter=' ', skiprows=1, usecols=(0,1), unpack=True)
        if time.size == signal1.size:
            self.filesize = time.size
        self.data_exp = np.around(np.array([time, signal1]), decimals=4)

    def importdata(self, path):

        #--- import is needed to proceed with data-time formate like this: 12.07.2019 11:56:04
        #---- This unussual format is manually converted to datetime64 format: 2019-04-05T17:14:51

        self.path_op = path

        time_date, signal1, signal2, signal3 = np.loadtxt(self.path_op, # read experimental csv file
            dtype={'names': ('column x', 'column y', 'column z', 'column k'),'formats': ('U22', 'f4', 'f4', 'f4')},
            delimiter=';', converters={0: lambda old: str(old)[8:12]+'-'+str(old)[5:7]+'-'+str(old)[2:4]+' '+str(old)[13:21]}, # reformating date and time
            skiprows=1, usecols=(0, 1, 2, 3), unpack=True)
            # time_date - 1st column read in U22 (text, i.e. "04.05.2019  17:14:51") format, which is reformated to fit datetime64 format, i.e. "2019-04-05T17:14:51"
            # Signal1 - 2nd column  read in f4 (float) format
            # Signal2 - 3rd column  read in f4 (float) format
            # Signal3 - 4th column  read in f4 (float) format
        if time_date.size == signal1.size == signal2.size == signal3.size:
            self.filesize = time_date.size

            time_min = np.zeros(time_date.size, dtype='f2') # form and fill in with zeros new realtime vector, whose values are of float (f2) type
            #co2max = np.amax(co2)
            signal1 = (signal1-signal1[0])
            #comax = np.amax(co)
            signal2 = (signal2-signal2[0])
            for i in range(0, time_date.size):
                # fill each value in the realtime vector
                # Length of Peak1 = 1174
                #
                # Process finished with exit code 0 as a difference between current time and time zero (at the start of the experiment)
                # realtime vector has the same length as time_date vector, has dimension of real minutes (calculated as number of seconds over 60
                time_min[i] = (int(str(np.datetime64(time_date[i],'s')-np.datetime64(time_date[0],'s')).split()[0]))/60
                # inital point is set as zero moment of time, the rest time points are calculated in minutes
            self.data_exp = np.around(np.array([time_min, signal1, signal2, signal3]), decimals=4)

    def save_exp(self, path, data):
        #data has format of np.array[[time], [signal1], [signal2], [signal3]]
        np.savetxt(path, data[0:2].T, fmt='%.4f', delimiter=' ') # here we deliberately get keep first two columns only and get rid of another two.

    def plot1gr(self, dataset_x, dataset_y, x1_label, y1_label, title):
        # Create the plot object

        _, ax = plt.subplots()

        # Plot the best fit line, set the linewidth (lw), color and
        # transparency (alpha) of the line
        ax.plot(dataset_x, dataset_y, lw = 2, color = 'tab:blue', alpha = 1)

        # Label the axes and provide a title
        #ax.set_title(title)
        plt.title = title
        ax.set_xlabel(x1_label)
        ax.set_ylabel(y1_label)
        plt.show()

    def plot2gr(self, dataset1_x, dataset1_y , dataset2_x, dataset2_y, x_min, x_max, title):
        _, ax = plt.subplots()

        # Plot the best fit line, set the linewidth (lw), color and
        # transparency (alpha) of the line
        ax.plot(dataset1_x[x_min:x_max], dataset1_y[x_min:x_max], lw=1, color='tab:blue', alpha=1)
        ax.plot(dataset2_x[x_min:x_max], dataset2_y[x_min:x_max], lw=1, color='tab:red', alpha=1)

        plt.ylabel('Signal')
        plt.xlabel("Time")
        #plt.title(title_)
        plt.title = title
        plt.show()

    def Signal_error(self, data_th_x, data_th_y): # to calculare error between data_th_y and data_exp[1]
        error_y = np.zeros(data_th_x.size, dtype='f2')
        for i in range(0, data_th_x.size):

            error_y[i] = math.sqrt( (self.data_exp[1][i]-data_th_y[i])**2 )
        return 1000*np.sum(error_y)/math.sqrt((data_th_x.size-1)*data_th_x.size)
        #print("The error between EXP and Th data is ",self.error)

    def Two_Signals_error(self, data_exp_x, data_exp_y, data_th_x, data_th_y): # Intended be to called with any two signals which have to be compared
        try:
            error_y = np.zeros(data_th_x.size, dtype='f2')
            for i in range(0, data_th_x.size):
                error_y[i] = math.sqrt( (data_exp_y[i] - data_th_y[i])**2 )
            return 1000*np.sum(error_y)/math.sqrt((data_th_x.size-1)*data_th_x.size)
        except AttributeError:
            pass

    def diff(self, data_x, data_y):

        if data_x.size != data_y.size:
            print("data_x's size is not equal to data_y's size")
        else:
            devy1 = np.zeros(data_x.size, dtype='f2')

            for i in range(0, data_x.size-1): #
                if i == 0:
                    devy1[i] = (4*data_y[i+1]-3*data_y[i]-data_y[i+2])/(2*(data_x[i+1]-data_x[i]))
                elif i == data_x.size-1:
                    devy1[i] = (3*data_y[i]-4*data_y[i-1]+data_y[i-2])/(2*(data_y[i]-data_x[i-1]))
                else:
                    devy1[i] = (data_y[i+1]-data_y[i-1])/(data_x[i+1]-data_x[i-1]) # calculate 1s derivative
            return devy1

    def smooth(self, data_x, data_y, smooth):
        if smooth == 0: #no smoothing
            return data_y

        elif smooth == 1: #2nd smoothing algorithm using "5 points method"
            #datasm_y = np.zeros(data_x.size, dtype='f2')
            datasm_y = data_y.copy()
            for i in range(2, data_x.size-2): # exclude first [0] and last [size-1] point from calculation of smoothed data_y. They will be calculated separately
                datasm_y[i] = (data_y[i-2]+data_y[i-1]+data_y[i]+data_y[i+1]+data_y[i+2])/5
            datasm_y[1] = 0.1*(4*data_y[0]+3*data_y[1]+2*datasm_y[2]+datasm_y[3])
            datasm_y[0] = (3*data_y[0]+2*datasm_y[1]+datasm_y[2]-data_y[4])/5
            datasm_y[data_x.size-2] = 0.1*(4*data_y[data_x.size-1]+3*data_y[data_x.size-2]+2*datasm_y[data_x.size-3]+datasm_y[data_x.size-4])

            #datasm_y[data_x.size-1] = 0.2*(3*data_y[data_x.size-1]+2*datasm_y[data_x.size-2]+datasm_y[data_x.size-3]+datasm_y[data_x.size-5])
            #print('length datasm_y = ', datasm_y.size)
            return datasm_y
        elif smooth == 2:
            """
             As it happens sometimes in experimental data_y sets, some its non zero values (see *) can be found several times within the set, as is seen in data_y example.
             Thus causes significant error in calculation of derivatives, so in order to prevent it, we modify some values of data_y set with help of linear approximation
            * there is nothing wrong if repeated zero values are in the experimental data_y set, is basically means absence of signal,
            these zero values have to set in the smoothed data_y set.
        
            Here are the examples of x and y data sets:
            data_x = np.array([1, 2, 3, 4, 5, 6, 7, 8,  9,  10,   11,  12, 13, 14, 15,   16,  17,   18,    19,   20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35])
            data_y = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 3, 3, 3, 3, 5,  9.1, 12.3, 12.2, 7,  8, 10, 9.1,  9.1, 9.1,  9.1,  9.1,  12, 13, 15, 24, 23, 22, 21], dtype='f2' )
                    """
            data_ysm = data_y.copy() # make copy of original data_y
            uniques, uniques_idx, counts = np.unique(data_y, return_index=True, return_counts=True)
            duplicates = data_y[uniques_idx[counts>1] ] # make a list of values from data_y set, which can be found in the set more than 1 time
            if duplicates[0] == 0:
                duplicates = np.delete(duplicates, 0) # we allow zeros (if any) to stay unchanged by removing them from the list of duplicates
                #print(duplicates)

            for i in duplicates:
                duplicate_ind = np.where(data_y == i)[0] # make list of indexes of duplicates

                x_0 = data_x[duplicate_ind[0]] # determine initial index within the data_x and data_y arrays, where duplicates start to appear
                y_0 = data_y[duplicate_ind[0]]
                if duplicate_ind[duplicate_ind.size-1] < data_x.size: # if the last value in duplicate_ind array is not last value of the data_x array (wee need one more point)
                    try:
                        x_ls = data_x[duplicate_ind[duplicate_ind.size-1]+1] # determine final + 1 index within data_x and data_y arrays, where duplicates end
                        y_ls = data_y[duplicate_ind[duplicate_ind.size-1]+1]
                    except IndexError:
                        return data_ysm
                else: #if the last value in duplicate_ind array is the last value of the data_x array
                    try:
                        x_ls = data_x[duplicate_ind[duplicate_ind.size-1]] # determine last index within data_x and data_y arrays, where duplicates end
                        y_ls = data_y[duplicate_ind[duplicate_ind.size-1]]
                    except IndexError:
                        return data_ysm
                if x_ls != x_0:
                    k = (y_ls-y_0)/(x_ls-x_0) # determination of slope "k"
                else:
                    return data_ysm # in case, the data are so "bad" (all X_ls=X_0) the original data_y will be returned
                b = y_0-k*x_0 # and intersept "b" for linear aproximation of new smoothed data_y a
                for z in range(duplicate_ind[0], duplicate_ind[duplicate_ind.size-1]+1): # at those indexes of the data_x where, duplicates were found
                    data_ysm[z]=k*data_x[z]+b # applying linear approximation for whose indexes "z"
                #    print(f"Size of smoothed data_y = {data_ysm.size}")
            return data_ysm
        elif smooth == 3:
            data_ysm = data_y.copy() # make copy of original data_y
            uniques, uniques_idx, counts = np.unique(data_y, return_index=True, return_counts=True)
            duplicates = data_y[uniques_idx[counts>1] ] # make a list of values from data_y set, which can be found in the set more than 1 time
            if duplicates[0] == 0:
                duplicates = np.delete(duplicates, 0) # we allow zeros (if any) to stay unchanged by removing them from the list of duplicates
                #print(duplicates)

            for i in duplicates:
                duplicate_ind = np.where(data_y == i)[0] # make list of indexes of duplicates

                x_0 = data_x[duplicate_ind[0]] # determine initial index within the data_x and data_y arrays, where duplicates start to appear
                y_0 = data_y[duplicate_ind[0]]
                if duplicate_ind[duplicate_ind.size-1] < data_x.size: # if the last value in duplicate_ind array is not last value of the data_x array (wee need one more point)
                    try:
                        x_ls = data_x[duplicate_ind[duplicate_ind.size-1]+1] # determine final + 1 index within data_x and data_y arrays, where duplicates end
                        y_ls = data_y[duplicate_ind[duplicate_ind.size-1]+1]
                    except IndexError:
                        return data_ysm
                else: #if the last value in duplicate_ind array is the last value of the data_x array
                    try:
                        x_ls = data_x[duplicate_ind[duplicate_ind.size-1]] # determine last index within data_x and data_y arrays, where duplicates end
                        y_ls = data_y[duplicate_ind[duplicate_ind.size-1]]
                    except IndexError:
                        return data_ysm
                if x_ls != x_0:
                    k = (y_ls-y_0)/(x_ls-x_0) # determination of slope "k"
                else:
                    return data_ysm # in case, the data are so "bad" (all X_ls=X_0) the original data_y will be returned
                b = y_0-k*x_0 # and intersept "b" for linear aproximation of new smoothed data_y a
                for z in range(duplicate_ind[0], duplicate_ind[duplicate_ind.size-1]+1): # at those indexes of the data_x where, duplicates were found
                    data_ysm[z]=k*data_x[z]+b # applying linear approximation for whose indexes "z"
                #    print(f"Size of smoothed data_y = {data_ysm.size}")
            """     Applying 1st method to the data_ysm   """
            datasm2_y = data_ysm.copy()
            for i in range(2, data_x.size-2): # exclude first [0] and last [size-1] point from calculation of smoothed data_y. They will be calculated separately
                datasm2_y[i] = (data_y[i-2]+data_y[i-1]+data_y[i]+data_y[i+1]+data_y[i+2])/5
            datasm2_y[1] = 0.1*(4*data_y[0]+3*data_y[1]+2*datasm2_y[2]+datasm2_y[3])
            datasm2_y[0] = (3*data_y[0]+2*datasm2_y[1]+datasm2_y[2]-data_y[4])/5
            datasm2_y[data_x.size-2] = 0.1*(4*data_y[data_x.size-1]+3*data_y[data_x.size-2]+2*datasm2_y[data_x.size-3]+datasm2_y[data_x.size-4])
            #datasm2_y[data_x.size-1] = 0.2*(3*data_y[data_x.size-1]+2*datasm2_y[data_x.size-2]+datasm2_y[data_x.size-3]+datasm2_y[data_x.size-5])
            return datasm2_y

    def intergSignal(self, data_x, data_y, imin:int, imax:int):
        if imin is None or imax is None or data_x is None or data_y is None or imin>=imax:
            return 0
        else:
            self.imin = imin
            self.imax = imax
            I = 0
            I2 = 0

            h = data_x[self.imin+1]-data_x[self.imin]

            for i in range(1, self.imax-self.imin-1, 2):
                I2 = I2 + data_y[i-1]+ 4*data_y[i] + data_y[i+1]
            I = round(I2*h/3,1)
            return I

    def dynamic_plot2gr_deriv(self, data_exp_x, data_exp_y, data_th_x, data_th_y, list_param, list_min_param, list_max_param, list_def_param, x_min, x_max, current_func_name, title):
        # to make graph where experimental and theoretical graphs are displayed together and user can dynamically adjust each parameter of the latter with help of sliders
        # data_exp_x and data_exp_y - experimental x and y datasets
        # data_th_x, data_th_y - Initial (with default parameters) theoretical x and y datasets
        # list_min_param - list of names of initial parameters, e.g. ["Xc", "A ", "W1", "W2", "W3"]
        # list_min_param - list of minimal values of these parameters (will be used as left margin of sliders)
        # list_max_param - list of maximal values of these parameters (will be used as right margin of sliders)
        # list_def_param - list of default values of these parameters (will be used as initial (default) value of sliders)
        plt.subplots(figsize = (9,6))
        fig1 = plt.subplot(2, 1, 1)
        l1_1, = plt.plot(data_exp_x[x_min:x_max], data_exp_y[x_min:x_max], color = 'tab:red', label = 'Experimental' ) # signal plot (e.g. experimental)
        l1_2, = plt.plot(data_th_x[x_min:x_max], data_th_y[x_min:x_max], color = 'tab:blue', label = 'Theoretical') # signal plot (e.g. theoretical)
        plt.legend(bbox_to_anchor=(0.95, 0.95), loc='upper right', borderaxespad=0.)
        anotation1 = fig1.annotate('Error = ' ,xy=(0.65, 0.7), xycoords='axes fraction',  horizontalalignment='left', verticalalignment='top', fontsize = 15, color = "red")
        plt.ylabel('Signal')
        plt.title = title


        fig2 = plt.subplot(2, 1, 2)
        l2_1, = plt.plot(data_exp_x[x_min:x_max], self.diff(data_exp_x[x_min:x_max], data_exp_y[x_min:x_max]), color = 'tab:red', label = 'Experimental') # signal derivative plot (e.g. experimental)
        l2_2, = plt.plot(data_th_x[x_min:x_max], self.diff(data_th_x[x_min:x_max], data_th_y[x_min:x_max]), color = 'tab:blue', label = 'Theoretical') # signal derivative plot (e.g. theoretical)
        plt.legend(bbox_to_anchor=(0.95, 0.95), loc='upper right', borderaxespad=0.)
        anotation2 = fig2.annotate('Error = ' ,xy=(0.65, 0.7), xycoords='axes fraction',  horizontalalignment='left', verticalalignment='top', fontsize = 15, color = "red")
        plt.xlabel('Time')
        plt.ylabel("Signal derivative")

        plt.subplots_adjust(left=0.07, bottom=0.07, top = 0.96, right = 0.60) # Set positions of fig1 and fig2

        axcolor = 'lightgoldenrodyellow'


        nn = len(list_param) # number of parameters = number of sliders
        list_axes = []
        for i in range(0, nn):
            gadget_ = plt.axes([0.67, 0.1+0.04*i, 0.25, 0.02], facecolor=axcolor) # coordinates of gadget=sliders
            list_axes.append(gadget_)

        list_sl = [] # list of sliders
        comb = zip(list_axes, list_param, list_min_param, list_max_param, list_def_param) # for making iteration easier


        for n in comb:
            sl_ = Slider(n[0], n[1], n[2], n[3], n[4]) # create sliders (gadget, name of parameter, min_value, max_value, initial=default value) for each parameter
                                                    # example s_xc_1 = Slider(ax_xc_1, 'X', 0.1, 30.0, valinit=b.xc_1)
            list_sl.append(sl_)

        def update(val): # what happens when slider is moved
            list_new_param = []
            for sl_ in list_sl: # for each slider in the list
                new_param = sl_.val # read new value from the slider as new_param variable
                list_new_param.append(new_param) # make list of new value of parameters to transfer it to data_th_y_new

            data_th_y_new = self.theory1.function_select(current_func_name, self.data_exp[0], list_new_param)[1][x_min:x_max]

            # --------------calculate and show signal's error
            signal_err = round(self.Two_Signals_error(data_exp_x[x_min:x_max], data_exp_y[x_min:x_max], data_th_x[x_min:x_max], data_th_y_new), 0)  #calculate  error between data_exp[1] and data_th_y_new
            anotation1.set_text('Error =' + str(signal_err)) # update annotation1 text

            # --------------calculate signal derivative error and show it
            data_th_y_dif_new = self.diff(data_th_x[x_min:x_max], data_th_y_new) # calculate derivative of data_th_y_new
            data_exp_derive_y = self.diff(data_exp_x[x_min:x_max], data_exp_y[x_min:x_max]) # calculate derivative of data_exp
            signal_derivative_error = round(self.Two_Signals_error(data_exp_x[x_min:x_max], data_exp_derive_y, data_th_x[x_min:x_max], data_th_y_dif_new), 0)  #calculate  error between self.data_exp_derive_y and self.data_th_y_dif_new
            anotation2.set_text('Error =' + str(signal_derivative_error)) # update annotation2 text


            # -------------update fig 1 and fi2 with new signal and signal derivative data
            l1_2.set_ydata(data_th_y_new) # update fig1 with new y - dataset
            l2_2.set_ydata(data_th_y_dif_new) # update fig2 with new y - dataset

            #fig1.canvas.draw_idle()
            #fig2.canvas.draw_idle()

        for sl_ in list_sl:
            sl_.on_changed(update) # update sliders

        button_color = 'Lavender'
        resetax = plt.axes([0.77, 0.9, 0.1, 0.04])
        button = Button(resetax, 'Reset', color=button_color, hovercolor='0.975')
        close_window = plt.axes([0.71, 0.8, 0.23, 0.04])
        button2 = Button(close_window, 'Close&Export parameters', color=button_color, hovercolor='0.975')

        def reset(event):
            for sl_ in list_sl:
                sl_.reset() # for each slider reset to its default value

        def close_window(event):
            plt.close()

        button.on_clicked(reset)
        button2.on_clicked(close_window)

        plt.show()
        return [round(i.val,3) for i in list_sl ]

    def dynamic_gr(self, data_exp_x, data_exp_y, data_th_x, data_th_y, all_param_all_funk, x_min, x_max, list_of_f_name, title):
        #
        # The function plots given experimental and theoretical datasets within x_min and x_max range.
        # With help of sliders user can do manual fine tuning of actual parameters of each selected elemental function to minimize the difference (shown as an error)
        # between theoretical and experimental curves for earlier selected signal 1, 2 or 3 and the corresponding derivative curve
        # With help of 'Close&export parameters' user can close the graph window and export self optimized parameters (for each selected function) to the main window
        #
        # data_exp_x - experimental x-dataset in np.array format
        # data_exp_y - experimental y-dataset in np.array format
        # data_th_x - Theoretical (calculated) x-dataset in np.array format
        # data_th_y - Theoretical (calculated) y-dataset in np.array format
        # Example of all_param_all_funk = [('Xc', 0.01, 10.0, 2.0), ('A ', 0.05, 40.0, 20.0), ('W1', 0.05, 1.0, 0.4), ('W2', 0.05, 1.0, 0.4), ('W3', 0.05, 1.0, 0.4), and similar for other functions..]
        # x_min - left border (in point) format - int, e.g. x_min = 0
        # y_min - right border (in point) format - int, e.g. x_max = 400
        # list_of_f_name = ['Dsigmoid','Sinus', 'Gauss', etc]
        # title = e.g. 'Signal 1'
        #
        plt.subplots(figsize = (10,6))
        fig1 = plt.subplot(2, 1, 1)
        l1_1, = plt.plot(data_exp_x[x_min:x_max], data_exp_y[x_min:x_max], color = 'tab:red', label = 'Experimental' ) # signal plot (e.g. experimental)
        l1_2, = plt.plot(data_th_x[x_min:x_max], data_th_y[x_min:x_max], color = 'tab:blue', label = 'Theoretical') # signal plot (e.g. theoretical)
        plt.legend(bbox_to_anchor=(0.95, 0.95), loc='upper right', borderaxespad=0.)
        anotation1 = fig1.annotate('Error = ' ,xy=(0.65, 0.7), xycoords='axes fraction',  horizontalalignment='left', verticalalignment='top', fontsize = 15, color = "red")
        plt.ylabel('Signal')
        plt.title = title

        fig2 = plt.subplot(2, 1, 2)
        l2_1, = plt.plot(data_exp_x[x_min:x_max], self.diff(data_exp_x[x_min:x_max], data_exp_y[x_min:x_max]), color = 'tab:red', label = 'Experimental') # signal derivative plot (e.g. experimental)
        l2_2, = plt.plot(data_th_x[x_min:x_max], self.diff(data_th_x[x_min:x_max], data_th_y[x_min:x_max]), color = 'tab:blue', label = 'Theoretical') # signal derivative plot (e.g. theoretical)
        plt.legend(bbox_to_anchor=(0.95, 0.95), loc='upper right', borderaxespad=0.)
        anotation2 = fig2.annotate('Error = ' ,xy=(0.65, 0.7), xycoords='axes fraction',  horizontalalignment='left', verticalalignment='top', fontsize = 15, color = "red")
        plt.xlabel('Time')
        plt.ylabel("Signal derivative")

        plt.subplots_adjust(left=0.07, bottom=0.1, top = 0.95, right = 0.60) # Set positions of fig1 and fig2

        #ax.margins(x=0)
        axcolor = 'lightgoldenrodyellow'

        list_of_number_of_parameters = []
        list_sl_long = []

        #--------------- extract following parameters from all_param_all_funk.
        #---------- Parameters: name, min, max, def. Example: [('Xc', 0.01, 10.0, 2.0), ('A ', 0.05, 40.0, 30.0), ('W1', 0.05, 1.0, 0.4), ('W2', 0.05, 1.0, 0.4), ('W3', 0.05, 1.0, 0.4)]
        for n in range(0, len(list_of_f_name)): # iterate through the list of used functions. Example of list_of_f_name = ['DbSigmoid', 'Sinus', 'DbSigmoid']
            # n - index of each elemental function
            funk_param_list = all_param_all_funk[n]  # calculate list of parameters for n-th function
            list_of_number_of_parameters.append(len(funk_param_list)) # make list of number of parameters for current function e.g. [5, 3, 5] for three functions like DS, SN, DS
            list_sl_short = []
            for i in range(0, len(funk_param_list)): # i - index of a parameter within one function
                # typical element of funk_param_list element is like this:
                gadget_ = plt.axes([0.67, 0.02 + 0.22*n + 0.04*i, 0.25, 0.02], facecolor=axcolor) # coordinates of all gadget=sliders, each gadget corresponds to one parameter for all elementary functions
                # ----------------create sliders------------------------
                slider_=Slider(gadget_, funk_param_list[i][0], funk_param_list[i][1], funk_param_list[i][2], funk_param_list[i][3])
                      # Slider(gadget, name_of_parameters, min_value_of_parameter, max_value_of_parameter, default_value_of_parameter
                list_sl_short.append((slider_)) # make list of all generated sliders
            list_sl_long.append(list_sl_short)
        #-----------------------------------------------------------------

        def update(val): # what happens when slider is moved
            self.global_funk_y = np.zeros(self.data_exp[0].size, dtype='f2')[x_min:x_max] # create and fill with zero of global_funk_y array. global_funk_y array is a summ of all elementary functions

            #------read new information from each slider--------------
            self.val_long_list = [] # to store current parameters for all elementaty functions.

            for n in range(0, len(list_of_number_of_parameters)): # example of list_of_number_of_parameters=[5, 4, 5] for list_of_f_name = ['DbSigmoid', 'Sinus', 'DbSigmoid']
                val_short_list = [] # to be used to store current values of parameters within one function
                for i in range(0, list_of_number_of_parameters[n]): # for n = 0, i = 0, 1, 2, 3, 4. for n=1 , i = 0, 1, 2, 3, etc
                    new_param_ = list_sl_long[n][i].val # read value from list_sl_long
                    val_short_list.append(new_param_)
                self.val_long_list.append(val_short_list) #Example =[[1.682, 26.576, 0.4, 0.4, 0.4], [4.0, 20.0, 0.4, 0.4, 0.4], [6.0, 20.0, 0.4, 0.4, 0.4]]
            #---------------------------------------------------------

            # ----------determine which elemental function was selected and calculate its y-values with current parameters from val_long_list[f_number] and global function
            for f_number in range(0, len(list_of_f_name)): # go through all functions
                data_th_y_new = self.theory1.function_select(list_of_f_name[f_number], self.data_exp[0], self.val_long_list[f_number])[1][x_min:x_max]
                # calculates new theoretical y- dataset based on new parameters from the long_list

                # --- calculate superposition of elemental function - i.e. - global function
                self.global_funk_y = self.global_funk_y + data_th_y_new # global function is sum of all elementary function

            # --------------calculate and show signal's error
            signal_err = round(self.Two_Signals_error(data_exp_x[x_min:x_max], data_exp_y[x_min:x_max], data_th_x[x_min:x_max], self.global_funk_y), 0)  #calculate  error between data_exp[1] and data_th_y_new

            anotation1.set_text('Error =' + str(signal_err)) # update annotation1 text

            # --------------calculate signal derivative error and show it
            data_th_y_dif_new = self.diff(data_th_x[x_min:x_max], self.global_funk_y) # calculate derivative of self.global_funk_y
            data_exp_derive_y = self.diff(data_exp_x[x_min:x_max], data_exp_y[x_min:x_max]) # calculate derivative of data_exp
            signal_derivative_error = round(self.Two_Signals_error(data_exp_x[x_min:x_max], data_exp_derive_y, data_th_x[x_min:x_max], data_th_y_dif_new), 0)  #calculate  error between self.data_exp_derive_y and self.data_th_y_dif_new

            anotation2.set_text('Error =' + str(signal_derivative_error)) # update annotation2 text

            # ---------------------------------------------------------------------

            l1_2.set_ydata(self.global_funk_y) # update fig1 with new y - dataset
            l2_2.set_ydata(data_th_y_dif_new) # update fig2 with new y - dataset
            #fig1.canvas.draw_idle()
            #fig2.canvas.draw_idle()

        #------- update sliders----------------
        list_sl = [slider_ for row in list_sl_long for slider_ in row] # flattening of the nested list_sl_long list
        for sl_ in list_sl:
            sl_.on_changed(update) # update sliders

        #------- reset sliders----------------
        #resetax = plt.axes([0.77, 0.95, 0.1, 0.04])
        #button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

        button_color = 'Lavender'
        close_window = plt.axes([0.71, 0.9, 0.23, 0.04])
        button2 = Button(close_window, 'Close&Export parameters', color=button_color, hovercolor='0.975')

        def close_window(event):
            plt.close()

        button2.on_clicked(close_window)
        plt.show()

        return self.val_long_list # returns new list of optimized parameters to update the ones in the main window

    def plot2gr_deriv(self, dataset1_x, dataset1_y, dataset2_x, dataset2_y, title = "Signal and its time derivative"):
        plt.subplot(2, 1, 1)
        plt.plot(dataset1_x, dataset1_y, color = 'tab:red', label = 'Experimental' ) # signal plot (e.g. experimental)
        plt.plot(dataset2_x, dataset2_y, color = 'tab:blue', label = 'Theoretical') # signal plot (e.g. theoretical)
        plt.legend(bbox_to_anchor=(0.85, 0.85), loc='upper right', borderaxespad=0.)
        plt.title = title
        plt.ylabel('Signal')

        plt.subplot(2, 1, 2)
        plt.plot(dataset1_x, self.diff(dataset1_x, dataset1_y), color = 'tab:red', label = 'Experimental') # signal derivative plot (e.g. experimental)
        plt.plot(dataset2_x, self.diff(dataset2_x, dataset2_y), color = 'tab:blue', label = 'Theoretical') # signal derivative plot (e.g. theoretical)
        plt.legend(bbox_to_anchor=(0.85, 0.85), loc='upper right', borderaxespad=0.)
        plt.xlabel('time (min)')
        plt.ylabel("Signal derivative")

        plt.show()

    def plot1gr_deriv(self, dataset1_x, dataset1_y, x_min, x_max, title = "Signal and its time derivative"):

        plt.subplot(2, 1, 1)
        plt.plot(dataset1_x[x_min:x_max], dataset1_y[x_min:x_max], color = 'tab:red', label = 'Experimental' ) # signal plot (e.g. experimental)
        plt.legend(bbox_to_anchor=(0.85, 0.85), loc='upper right', borderaxespad=0.)
        plt.title = title
        plt.ylabel('Signal')
        #-------------------------------
        plt.subplot(2, 1, 2)
        plt.plot(dataset1_x[x_min:x_max], self.diff(dataset1_x[x_min:x_max], dataset1_y[x_min:x_max]), color = 'tab:red', label = 'Experimental') # signal derivative plot (e.g. experimental)
        plt.legend(bbox_to_anchor=(0.85, 0.85), loc='upper right', borderaxespad=0.)
        plt.xlabel('time (min)')
        plt.ylabel("Signal derivative")
        plt.show()

data = Work()











