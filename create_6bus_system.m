function mpc = create_6bus_system
    
% Create an empty network in MATPOWER format
    mpc.version = '2';
    
    %%-----  Power Flow Data  -----%%
    %% system MVA base
    mpc.baseMVA = 100;
    

    %%-----  3 Phase Model Data  -----%%
    %% system data
    mpc.freq = 50;      %% frequency, Hz
    mpc.basekVA = 1000; %% system kVA base
 

    %% bus data
   %   busid   type    basekV  Vm1     Vm2     Vm3     Va1     Va2     Va3
    mpc.bus3p =[
    1   3   11   1.00   1.00    1.00     0.0    0.0    0.0    0.0;   % Bus 1 (slack bus)
    2   2   11   1.00   1.00    1.00     0.0    0.0    0.0    0.0;   % Bus 2 (voltage controlled)
    3   1   0.4  1.00   1.00    1.00     0.0    0.0    0.0    0.0;   % Bus 3 (load)
    4   1   0.4  1.00   1.00    1.00     0.0    0.0    0.0    0.0;   % Bus 4 (load)
    5   1   0.4  1.00   1.00    1.00     0.0    0.0    0.0    0.0;   % Bus 5 (load)
    6   1   0.4  1.00   1.00    1.00     0.0    0.0    0.0    0.0;   % Bus 6 (load)
    ];

    %% branch data
    %% branch data
%   brid    fbus    tbus    status  lcid    len
    mpc.line3p = [
    1   3   5   1   1   0.0373   0.04;   % Line from Bus 1 to Bus 3 with length and impedance
    2   5   6   1   1   0.0373   0.04;   % Line from Bus 2 to Bus 4
    3   4   2   1   1   0.0373   0.04    % Line from Bus 1 to Bus 2
];

    %% generator data
   %   genid   gbus    status  Vg1     Vg2     Vg3     Pg1     Pg2     Pg3     Qg1     Qg2     Qg3
    mpc.gen3p = [
    1       1       1       1       1       1          0       0       0    0       0       0;
    2       2       1       1       1       1          0       0       0    0       0       0;
];

    %% load data
%   ldid    ldbus   status  Pd1     Pd2     Pd3     ldpf1   ldpf2   ldpf3
mpc.load3p = [
    1       1       1       0.4     0.4     0.4     0.85    0.9     0.95;  % MV Load 1 at Bus 1
    2       2       1       0.2     0.2     0.2     0.85    0.9     0.95;  % MV Load 2 at Bus 2
    3       5       1       0.03    0.03    0.03    0.85    0.9     0.95;  % LV Load 3 at Bus 5
    4       6       1       0.09    0.09    0.09    0.85    0.9     0.95;  % LV Load 4 at Bus 6
];

    %% Transformer data (From Bus, To Bus, Resistance, Reactance, Rating)
    % Transformers connecting high and low voltage buses
    %   xfid    fbus    tbus    status  R       X       basekVA basekV
    mpc.xfmr = [
    1   3   0.01   0.05   0.63   11   0.4   1; % Transformer from Bus 1 to Bus 3
    2   4   0.01   0.05   0.63   11   0.4   1; % Transformer from Bus 2 to Bus 4
    ];

    %% line construction
    %   lcid    R11     R21     R31     R22     R32     R33     X11     X21     X31     X22     X32     X33     C11     C21     C31     C22     C32     C33
    mpc.lc = [
    1       0.048   0.048   0.048   0.048   0.048   0.048   0.0064   0.0064   0.0064   0.0064   0.0064   0.0064   16.8   16.8   16.8   16.8   16.8   16.8; % Line 1: Bus 3 to Bus 5
    2       0.048   0.048   0.048   0.048   0.048   0.048   0.0064   0.0064   0.0064   0.0064   0.0064   0.0064   16.8   16.8   16.8   16.8   16.8   16.8; % Line 2: Bus 5 to Bus 6
    3       0.048   0.048   0.048   0.048   0.048   0.048   0.0064   0.0064   0.0064   0.0064   0.0064   0.0064   16.8   16.8   16.8   16.8   16.8   16.8; % Line 3: Bus 6 to Bus 4
    ];

end
