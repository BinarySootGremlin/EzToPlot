import EzToPlot as ez

plotter = ez.ez_parser()

filenames_01 = [["jns_task01_3.ini","jns_task01_4.ini","jns_task01_5.ini"],["lks_task01_3.ini","lks_task01_4.ini","lks_task01_5.ini"],["flo_task01_3.ini","flo_task01_4.ini","flo_task01_5.ini"]]

for count, filenames in enumerate(filenames_01):
    plotter.setup_file(filenames[0],0,1,y_err_types=["add"],y_settings_columns=[2],x_err_types=["percentage","digit"],x_err_setting=[1.5,5])
    plotter.stretch_y(filenames[0],0.002)
    plotter.setup_file(filenames[1],0,1,y_err_types=["plain"],y_err_setting=[0.5],x_err_types=["percentage","digit"],x_err_setting=[1.5,5])
    plotter.stretch_y(filenames[1],0.002)
    plotter.setup_file(filenames[2],0,1,y_err_types=["plain"],y_err_setting=[0.5],x_err_types=["percentage","digit"],x_err_setting=[1.5,5])
    plotter.stretch_y(filenames[2],0.002)

plotter.describe()