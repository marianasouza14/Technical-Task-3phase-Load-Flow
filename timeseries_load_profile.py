import pandas as pd
import pandapower.control as control
import pandapower.timeseries as timeseries
from pandapower.timeseries.data_sources.frame_data import DFData
from load_flow_3phase import create_6bus_system

# load a pandapower network
net = create_6bus_system()
# number of time steps - 24 timesteps representing 1 day
n_ts = 96
# loading the timeseries from a file ( csv file)
df = pd.read_csv("load_profile.csv", index_col="time_step")

# creating the data source from it
ds = DFData(df)

const_load = control.ConstControl(
    net, 
    element='load', 
    element_index=net.load.index, 
    variable='p_mw', 
    data_source=ds, 
    profile_name=['load_0_p_mw', 'load_1_p_mw', 'load_2_p_mw', 'load_3_p_mw']  # substitua com os nomes corretos das colunas
)

# starting the timeseries simulation for one day -> 96 15 min values.
timeseries.run_timeseries(net, time_steps=n_ts, verbose=True)

# initialising the outputwriter to save data to excel files in the current folder. It can be saved in .json, .csv, or .pickle as well

output_file_name = "timeseries_results.csv"
ow = timeseries.OutputWriter(net, output_path='C:\\Users\\mariana.souza\\Documents\\ATE', output_file_type=".csv")
# adding vm_pu of all buses and line_loading in percent of all lines as outputs to be stored
ow.log_variable('res_bus', 'vm_pu')
ow.log_variable('res_line', 'loading_percent')


print(f"Results saved to '{output_file_name}'.")

