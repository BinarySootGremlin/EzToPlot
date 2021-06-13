import os
import matplotlib.pyplot as plt
import scipy.odr as odr
import uncert_lib
import numpy as np
from string import ascii_lowercase

def perform_odr(model, parameter_count, x, y, xerr, yerr, override_start=[]):
    odr_model = odr.Model(model)
    if(0 in xerr):
        odr_data = odr.RealData(x, y, sy=yerr)
    elif(0 in yerr):
        odr_data = odr.RealData(x, y, sx=xerr)
    else:
        odr_data = odr.RealData(x, y, sx=xerr, sy=yerr)

    beta0 = []

    if(len(override_start)<=0):
        for i in range(parameter_count):
            beta0.append(1)
    else:
        beta0 = override_start

    odr_regression = odr.ODR(odr_data, odr_model, beta0=beta0, maxit=1000000000)
    output = odr_regression.run()
    return output

def get_error(value_column, plain_values,err_types,err_settings,err_columns):
    err = 0
    for err_number, err_type in enumerate(err_types):
        column_count = 0
        if(err_type == "resolution"):
            err += uncert_lib.resolution_uncert(float(plain_values[err_columns[column_count]]),err_settings[err_number])
            column_count = column_count + 1
        if(err_type == "digit"):
            err += uncert_lib.digit_uncert(plain_values[value_column],err_settings[err_number])
        if(err_type == "percentage"):
            err += uncert_lib.percent_uncert(float(plain_values[value_column]),err_settings[err_number])
        if(err_type == "plain"):
            err += float(err_settings[column_count])
            column_count = column_count + 1
    return err

class file_parser:
    def __init__(self, file, x_column, y_column, x_settings_columns, y_settings_columns, x_err_types, y_err_types, x_err_setting, y_err_setting):
        self.file = file
        self.x_column = x_column
        self.y_column = y_column
        self.x_settings_columns = x_settings_columns
        self.y_settings_columns = y_settings_columns
        self.x_err_types = x_err_types
        self.y_err_types = y_err_types
        self.x_err_setting = x_err_setting
        self.y_err_setting = y_err_setting
        self.x_data = []
        self.y_data = []
        self.x_err = []
        self.y_err = []
        self.check_cohearance()
        self.parse_file()

    def parse_file(self):
        plain_values = []
        with open(self.file) as file:
            for line in file:
                plain_values.clear()
                for index, value in enumerate(line.split(",")):
                    plain_values.append(value.rstrip())

                if len(plain_values)-1 < self.x_column:
                    raise ValueError("LINE IN FILE IS SHORTER THAN %n" % (self.x_column))
                if len(plain_values)-1 < self.y_column:
                    raise ValueError("LINE IN FILE IS SHORTER THAN %n" % (self.y_column))

                self.x_data.append(float(plain_values[self.x_column]))
                self.y_data.append(float(plain_values[self.y_column]))
                xerr = 0
                for err_number, x_err_type in enumerate(self.x_err_types):
                    column_count = 0
                    if(x_err_type == "resolution"):
                        xerr += uncert_lib.resolution_uncert(float(plain_values[self.x_settings_columns[column_count]]),self.x_err_setting[err_number])
                        column_count = column_count + 1
                    if(x_err_type == "digit"):
                        xerr += uncert_lib.digit_uncert(plain_values[self.x_column],self.x_err_setting[err_number])
                    if(x_err_type == "percentage"):
                        xerr += uncert_lib.percent_uncert(float(plain_values[self.x_column]),self.x_err_setting[err_number])
                    if(x_err_type == "plain"):
                        xerr += float(self.x_err_setting[column_count])
                        column_count = column_count + 1
                self.x_err.append(xerr)
                yerr = 0
                for err_number, y_err_type in enumerate(self.y_err_types):
                    column_count = 0
                    if(y_err_type == "resolution"):
                        yerr += uncert_lib.resolution_uncert(float(plain_values[self.y_settings_columns[column_count]]),self.y_err_setting[err_number])
                        column_count = column_count + 1
                    if(y_err_type == "digit"):
                        yerr += uncert_lib.digit_uncert(plain_values[self.y_column],self.y_err_setting[err_number])
                    if(y_err_type == "percentage"):
                        yerr += uncert_lib.percent_uncert(float(plain_values[self.y_column]),self.y_err_setting[err_number])
                    if(y_err_type == "plain"):
                        yerr += float(self.y_err_setting[column_count])
                        column_count = column_count + 1
                self.y_err.append(yerr)

    def redefine_x(self,filename,column,formular,propagation,uncert_types,uncert_settings,uncert_settings_columns=[]):
        calc_values = []
        new_errs = []
        plain_values = []
        with open(filename) as file:
            for line_number, line in enumerate(file):
                plain_values.clear()
                for index, value in enumerate(line.split(",")):
                    plain_values.append(value.rstrip())
                calc_values.append(plain_values[column])
                new_errs.append(get_error(column,plain_values,uncert_types,uncert_settings,uncert_settings_columns))
        if(len(calc_values)==len(self.x_data)):
            for i,x in enumerate(self.xdata):
                self.x_err[i] = propagation(x,float(calc_values[i]),self.x_err[i],new_errs[i])
                self.x_data[i] = formular(x,float(calc_values[i]))
        elif(len(calc_values)==1):
            for i,x in enumerate(self.xdata):
                self.x_data[i] = formular(x,float(calc_values[0]))
        else:
            raise ValueError("SIZE OF DATASET SHOULD BE: %n OR 1 BUT IS: %n" % (len(self.x_data),len(calc_values)))

    def redefine_y(self,filename,column,formular,propagation,uncert_types,uncert_settings,uncert_settings_columns=[]):
        calc_values = []
        new_errs = []
        plain_values = []
        with open(filename) as file:
            for line_number, line in enumerate(file):
                plain_values.clear()
                for index, value in enumerate(line.split(",")):
                    plain_values.append(value.rstrip())
                calc_values.append(plain_values[column])
                new_errs.append(get_error(column,plain_values,uncert_types,uncert_settings,uncert_settings_columns))
        if(len(calc_values)==len(self.y_data)):
            for i,y in enumerate(self.y_data):
                self.y_err[i] = propagation(y,float(calc_values[i]),self.y_err[i],new_errs[i])
                self.y_data[i] = formular(y,float(calc_values[i]))
        elif(len(calc_values)==1):
            for i,y in enumerate(self.y_data):
                self.y_err[i] = propagation(y,float(calc_values[0]),self.y_err[i],new_errs[0])
                self.y_data[i] = formular(y,float(calc_values[0]))   
        else:
            raise ValueError("SIZE OF DATASET SHOULD BE: %n OR 1 BUT IS: %n" % (len(self.y_data),len(calc_values)))

    def check_cohearance(self):
        if not (isinstance(self.file, str) and isinstance(self.x_column, int) and isinstance(self.y_column, int) and isinstance(self.x_settings_columns, list) and isinstance(self.y_settings_columns, list)
                and isinstance(self.x_err_types, list) and isinstance(self.y_err_types, list) and isinstance(self.x_err_setting, list) and isinstance(self.y_err_setting, list)):
            raise ValueError("WRONG DATA TYPES IN FILE PARSER FOR %s" % (self.file))

        if(not os.path.exists(self.file)):
            raise ValueError("FILE: %s NOT FOUND!" % (self.file))

        if(self.x_column < 0):
            raise ValueError("X COLUMN INVALID!")

        if(self.y_column < 0):
            raise ValueError("Y COLUMN INVALID!")

    def get_data(self):
        return [self.x_data,self.y_data]
    def get_uncert(self):
        return [self.x_err,self.y_err]

    #self.file = ""
    #self.x_column = 0
    #self.y_column = 0
    #self.x_settings_columns = []
    #self.y_settings_columns = []
    #self.x_err_types = []
    #self.y_err_types = []
    #self.x_err_setting = []
    #self.y_err_setting = []
    #self.x_data = []
    #self.y_data = []
    #self.x_err = []
    #self.y_err = []

class ez_parser:
    def __init__(self):
        self.file_parsers = {}

    def setup_file(self, filename,x_column,y_column,x_settings_columns=[],y_settings_columns=[],x_err_types=[],y_err_types=[],x_err_setting=[],y_err_setting=[]):
        self.file_parsers[filename] = file_parser(filename,x_column,y_column,x_settings_columns,y_settings_columns,x_err_types,y_err_types,x_err_setting,y_err_setting)
    def err_plot(self, filenames, title="",x_label="",y_label="",legends=[],additional_legend=""):
        if not isinstance(filenames, list):
            filenames = [filenames]

        legends_length = len(legends)

        if legends_length<=0:
            for count in range(len(filenames)):
                legends.append("")

        if not isinstance(legends, list):
            legends = [legends]

        for parser_number, filename in enumerate(filenames):
            if filename in self.file_parsers:
                plt.errorbar(self.file_parsers[filename].get_data()[0],self.file_parsers[filename].get_data()[1],
                                xerr=self.file_parsers[filename].get_uncert()[0],yerr=self.file_parsers[filename].get_uncert()[1], label=legends[parser_number],
                                marker='x', linestyle="none", markersize=2, markeredgewidth=0.5, capsize=3, linewidth=0.5)
            else:
                raise ValueError("NO INITIALIZED PARSER FOR FILE: %s" % (filename))

        if(len(title)>0):
            plt.title(title)

        if(len(x_label)>0):
            plt.xlabel(x_label)

        if(len(y_label)>0):
            plt.ylabel(y_label)

        if(len(additional_legend)>0):
            plt.plot([], [], ls='none', label=additional_legend)

        if(legends_length>0):    
            plt.legend()

        plt.grid(linestyle='dotted')
        plt.show()

    def fit_plot(self, filenames, models, parameter_counts, colors=[], title="", x_label="", y_label="", legends_err=[], legends_fit=[], additional_legend="", override_start=[]):
        if not isinstance(filenames, list):
            filenames = [filenames]

        if not isinstance(models, list):
            models = [models]

        if not isinstance(parameter_counts, list):
            parameter_counts = [parameter_counts]

        if len(legends_err)<=0:
            for count in range(len(filenames)):
                legends_err.append("")

        if not isinstance(legends_err, list):
            legends_err = [legends_err]

        if len(legends_fit)<=0:
            for count in range(len(filenames)):
                legends_fit.append("")

        if not isinstance(legends_fit, list):
            legends_fit = [legends_fit]

        for parser_number, filename in enumerate(filenames):
            if filename in self.file_parsers:
                x = self.file_parsers[filename].get_data()[0]
                x_line = np.linspace(np.min(self.file_parsers[filename].get_data()[0]),np.max(self.file_parsers[filename].get_data()[0]),300)
                y = self.file_parsers[filename].get_data()[1]
                xerr = self.file_parsers[filename].get_uncert()[0]
                yerr = self.file_parsers[filename].get_uncert()[1]
                plt.errorbar(x,y,
                                xerr=xerr,yerr=yerr, label=legends_err[parser_number],
                                marker='x', linestyle="none", markersize=2, markeredgewidth=0.5, capsize=3, linewidth=0.5, color=colors[parser_number])
                regression = perform_odr(models[parser_number], parameter_counts[parser_number], x, y, xerr, yerr, override_start[parser_number])
                plt.plot(x_line, models[parser_number](regression.beta,x_line), alpha=0.25, linewidth="1.5", label=legends_fit[parser_number],color=colors[parser_number])
                label = ""
                for parameter_number, beta in enumerate(regression.beta):
                    label += "\n$" + ascii_lowercase[parameter_number] + " \\ = \\ " + str(beta) + "$" 
                    label += "\n$u_" + ascii_lowercase[parameter_number] + " \\ = \\ " + str(regression.sd_beta[parameter_number]) + "$" 
                label += "\n$\\chi^2 \\ = \\ " + str(regression.res_var) + "$"
                plt.plot([], [], ' ', label=label)
            else:
                raise ValueError("NO INITIALIZED PARSER FOR FILE: %s" % (filename))

        if(len(title)>0):
            plt.title(title)

        if(len(x_label)>0):
            plt.xlabel(x_label)

        if(len(y_label)>0):
            plt.ylabel(y_label)

        if(len(additional_legend)>0):
            plt.plot([], [], ls='none', label=additional_legend)

        if(len(legends_err)>0 or len(legends_fit)>0):    
            plt.legend()

        plt.grid(linestyle='dotted')
        plt.show()