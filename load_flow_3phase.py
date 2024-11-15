import pandapower as pp
import math
from pandapower.pf.runpp_3ph import runpp_3ph  #function for 3phase load flow
from pandapower.plotting import simple_plot
import pandas as pd

def create_6bus_system():
    
    #Create an empty network in pandapower
    net = pp.create_empty_network()

    #Add zero impedance parameters to run the 3phase load flow
    pp.add_zero_impedance_parameters(net)

    #Buses
    bus1 = pp.create_bus(net, vn_kv=11, type="b", name="Bus 1")
    bus2 = pp.create_bus(net, vn_kv=11, type="b",name="Bus 2")
    bus3 = pp.create_bus(net, vn_kv=0.4, type="n",name="Bus 3")
    bus4 = pp.create_bus(net, vn_kv=0.4, type="n",name="Bus 4")
    bus5 = pp.create_bus(net, vn_kv=0.4, type="b",name="Bus 5")
    bus6 = pp.create_bus(net, vn_kv=0.4, type="b",name="Bus 6")

    #Geodata to plot the grid
    net.bus_geodata.loc[bus1, ['x', 'y']] = [0, 7] 
    net.bus_geodata.loc[bus2, ['x', 'y']] = [3, 7]  
    net.bus_geodata.loc[bus3, ['x', 'y']] = [3, 5]  
    net.bus_geodata.loc[bus4, ['x', 'y']] = [6, 5]  
    net.bus_geodata.loc[bus5, ['x', 'y']] = [4, 3]  
    net.bus_geodata.loc[bus6, ['x', 'y']] = [6, 3] 

    
    #Sources
    pp.create_ext_grid(net, 
        bus=bus1, 
        vm_pu=1.0,
        va_degree=0, 
        rx_max=0.0001,
        x0x_max=0.0001,
        r0x0_max=0.0001,
        name="Source 1",
        s_sc_max_mva=1000, 
        slack=True)

    pp.create_ext_grid(net, 
        bus=bus2,
        va_degree=0,
        rx_max=0.0001,
        x0x_max=0.0001,
        r0x0_max=0.0001,
        name="Source 2",
        s_sc_max_mva=1000,
        slack=False)
    
    #Add the solar generator
    #pp.create_gen(net, bus=bus3, p_mw=0.06, vm_pu=1.0, min_p_mw=0, max_p_mw=10, max_q_mvar=10, min_q_mvar=-10, controllable=True, name="Solar DG")
    
    #Transformers
    pp.create_transformer_from_parameters(
        net,
        hv_bus=bus1,           # High-voltage bus
        lv_bus=bus3,           # Low-voltage bus
        name="Transformer 1",  # Transformer name
        sn_mva=0.63,            # Adjusted rated power (in MVA)
        vn_hv_kv=11.0,         # High-voltage nominal voltage (in kV)
        vn_lv_kv=0.4,          # Low-voltage nominal voltage (in kV)
        vk_percent=6,          # Voltage drop on the HV side
        vkr_percent=0.1,       # Adjusted resistance voltage drop (in %)
        pfe_kw=0.1,            # Adjusted no-load losses (in kW)
        i0_percent=0.1,       # Adjusted no-load current (in %)
        shift_degree=30,       # Phase shift (in degrees)
        vector_group='Yzn',    # Transformer vector group (adjustable)
        vk0_percent=5,         # Low-voltage side voltage drop (in %)
        vkr0_percent=0.1,       # Low-voltage side resistance drop (in %)
        mag0_percent=10,      # Magnetizing current (in %)
        mag0_rx=1.0,           # Magnetizing reactance (in pu)
        si0_hv_partial=0.9     # Distribution of zero sequence leakage impedances for HV side
    )

    pp.create_transformer_from_parameters(
        net,
        hv_bus=bus2,           # High-voltage bus
        lv_bus=bus4,           # Low-voltage bus
        name="Transformer 2",  # Transformer name
        sn_mva=0.63,            # Adjusted rated power (in MVA)
        vn_hv_kv=11.0,         # High-voltage nominal voltage (in kV)
        vn_lv_kv=0.4,          # Low-voltage nominal voltage (in kV)
        vk_percent=6,          # Voltage drop on the HV side
        vkr_percent=0.1,       # Adjusted resistance voltage drop (in %)
        pfe_kw=0.1,            # Adjusted no-load losses (in kW)
        i0_percent=0.1,       # Adjusted no-load current (in %)
        shift_degree=30,       # Phase shift (in degrees)
        vector_group='Yzn',    # Transformer vector group (adjustable)
        vk0_percent=5,         # Low-voltage side voltage drop (in %)
        vkr0_percent=0.1,      # Low-voltage side resistance drop (in %)
        mag0_percent=10,      # Magnetizing current (in %)
        mag0_rx=1.0,           # Magnetizing reactance (in pu)
    )

    #Loads
    pp.create_load(net, bus=bus1, p_mw=0.4, q_mvar=0.04, name="MV Load 1")
    pp.create_load(net, bus=bus2, p_mw=0.2, q_mvar=0.04, name="MV Load 2")
    pp.create_load(net, bus=bus5, p_mw=0.03, q_mvar=0.001, name="LV Load 3")
    pp.create_load(net, bus=bus6, p_mw=0.09, q_mvar=0.001, name="LV Load 4")

    #Lines
    pp.create_line_from_parameters(net, from_bus=bus3, to_bus=bus5, length_km=0.08, r_ohm_per_km=0.6, x_ohm_per_km=0.08, c_nf_per_km=210, max_i_ka=0.142, r0_ohm_per_km=0.01, c0_nf_per_km=100, x0_ohm_per_km=0.1, name="Line Bus3 to Bus5")
    pp.create_line_from_parameters(net, from_bus=bus5, to_bus=bus6, length_km=0.08, r_ohm_per_km=0.6, x_ohm_per_km=0.08, c_nf_per_km=210, max_i_ka=0.142, r0_ohm_per_km=0.01, c0_nf_per_km=100, x0_ohm_per_km=0.1, name="Line Bus5 to Bus6")
    pp.create_line_from_parameters(net, from_bus=bus6, to_bus=bus4, length_km=0.08, r_ohm_per_km=0.6, x_ohm_per_km=0.08, c_nf_per_km=210, max_i_ka=0.142, r0_ohm_per_km=0.01, c0_nf_per_km=100, x0_ohm_per_km=0.1, name="Line Bus6 to Bus4")
   

    #Switch
    pp.create_switch(net, bus=bus5, element=bus6, et="b", closed=True, name="Switch 1")

    return net


net = create_6bus_system()


pp.diagnostic(net, report_style='detailed')


runpp_3ph(net, init='flat', tolerance='auto', max_iteration='auto')



print(net)


#Export Results

bus_voltages = net.res_bus[['vm_pu', 'va_degree']].copy()
bus_voltages['Category'] = 'Bus Voltages'


bus_voltages = net.res_bus[['vm_pu', 'va_degree']].copy()
bus_voltages.insert(0, 'Bus Name', net.bus.index)  # Add Bus Name as the first column


transformer_data = net.res_trafo[['p_hv_mw', 'q_hv_mvar', 'p_lv_mw', 'q_lv_mvar', 'loading_percent']].copy()
transformer_data.insert(0, 'Transformer Name', net.trafo.index)  # Add Transformer Name as the first column


line_data = net.res_line[['loading_percent', 'i_ka']].copy()
line_data.insert(0, 'Line Name', net.line.index)  # Add Line Name as the first column


output_path = r"C:\\Users\\mariana.souza\\Documents\\AITL_LSBU\\network_results.xlsx"
with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    bus_voltages.to_excel(writer, sheet_name='Bus Voltages', index=False)
    transformer_data.to_excel(writer, sheet_name='Transformer Data', index=False)
    line_data.to_excel(writer, sheet_name='Line Data', index=False)

print(f"Results exported to Excel at {output_path}")

print(f"All results exported to {output_path}")



simple_plot(net, 
            respect_switches=True, 
            line_width=3.0, 
            bus_size=3.0, 
            ext_grid_size=5.0, 
            trafo_size=1.0, 
            plot_loads=True, 
            plot_gens=True, 
            plot_sgens=False, 
            load_size=4.0, 
            gen_size=4.0, 
            sgen_size=6.0, 
            switch_size=5.0, 
            switch_distance=1.0, 
            plot_line_switches=True, 
            scale_size=True, 
            bus_color='b', 
            line_color='grey', 
            dcline_color='c', 
            trafo_color='black', 
            ext_grid_color='y', 
            switch_color='k', 
            library='igraph', 
            show_plot=True, 
           )


