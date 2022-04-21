#External disturbances imitation program
#Programmer Chetyrbok Ivan
#v 1.0
#08.12.2021

from math import sin, cos, pi, atan, exp

#NOTE: Forces are positive forvard in surge, to port in sway and  counter-clockwise in yaw.
#NOTE: Force direction 0 derees to push forward and 90 to push port
def wind_loads (rho_air: float , V_wind: float, A_f_wind: float, A_l_wind: float,
              wind_angle: float, x_l_air: float, Lpp: float) -> set:
    """"The wind_loads function calculates a set of two wind forces along x and y 
    axis and the moment along Z-axis. 
    Here are:
        rho_air = air density. Mean value of air density for temperature = 15 C
                  is near by 1.226 kg/m^3
        V_wind = wind speed in meters per second
        A_f_wind = vessel frontal projected wind area
        A_l_wind = vessel lateral projected wind area
        wind_angle = wind coming from direction in relation to the ship 
                  in degrees
        x_l_air = longitudal position of A_l_wind center
        Lpp = ship length betwin perpendiculars"""
   
    ##convert wind angle from degrees to radians
    wind_angle = wind_angle / 180 * pi
                
    F_x_wind = .5 * rho_air * V_wind**2 * A_f_wind * (-.7 * cos(wind_angle))
    F_y_wind = .5 * rho_air * V_wind**2 * A_l_wind * (.9 * sin(wind_angle))
    
    if pi <= wind_angle <= 2 * pi:
        wind_angle = 2 * pi - wind_angle
    
    M_z_wind = F_y_wind * (x_l_air + .3 * (1 - 2 * wind_angle / pi) * Lpp)
    
    return [F_x_wind, F_y_wind, M_z_wind]

def current_loads (rho: float, V_curr: float, Bwl: float, Tm: float, A_l_hull: float,
              curr_angle: float, x_l_curr: float, Lpp: float, wind_angle: float,
              V_wind_curr: float, curr_method: bool) -> set:
    """"The current_loads function calculates a set of two forces along x and y 
    axis induced by the current and the moment along Z-axis. 
    Here are:
        rho = water density. Mean value of sea water density for temperature 
                    = 5...25 C is near by 1025 kg/m^3 with sufficient accuracy
        V_curr = current speed in meters per second
        Bwl = vessel maximal breath at the waterline
        Tm = vessel midship draft 
        A_l_hull = vessel lateral projected submerged area
        curr_angle = current coming from direction in relation to the ship 
                  in degrees
        x_l_curr = longitudal position of A_l_hull center
        Lpp = ship length betwin perpendiculars"""
   
    # NOTE: formulas below are applicable up to moderate carrent speeds
    # with Froud number less 0.1, i.e. V_curr < 0.1 * (g * Bwl) ^ 0.5
    # therefore  if Froude number for V_curr is more than 0.1 formulas below
    # have to be used with care
   
    #convert current angle from degrees to radians
    curr_angle = curr_angle / 180 * pi
    
    if curr_method == True:
        V_s_curr = (V_curr**2 + V_wind_curr**2 - 2 * V_curr * V_wind_curr)**.5
        curr_s_angle = atan((V_curr * sin(curr_angle) + V_wind_curr * sin(wind_angle)) 
                          / (V_curr * cos(curr_angle) + V_wind_curr * cos(wind_angle)))
    else:
        V_s_curr = V_curr
        curr_s_angle = curr_angle
                
    F_x_curr = .5 * rho * V_s_curr**2 * Bwl * Tm * (-.07 * cos(curr_s_angle))
    F_y_curr = .5 * rho * V_s_curr**2 * A_l_hull * (.6 * sin(curr_s_angle))
    
    if pi <= curr_s_angle <= 2 * pi:
        curr_s_angle = 2 * pi - curr_s_angle
    
    M_z_curr = F_y_curr * (x_l_curr + max(min(.4 * (1 - 2 * curr_s_angle / pi), 
                                              .25), -.2) * Lpp)
    
    return [F_x_curr, F_y_curr, M_z_curr]

def waves_loads (rho: float, bow_angle: float, Awl_aft: float, Tz: float,
                 waves_angle: float, Bwl: float, Los: float, Lpp: float, 
                 x_Los: float) -> set:
    """"The waves_loads function calculates a set of two forces along x and y 
    axis induced by the current and the moment along Z-axis. 
    Here are:
        rho = water density. Mean value of sea water density for temperature 
                    = 5...25 C is near by 1025 kg/m^3 with sufficient accuracy            
        scale_table = the table of Beaufort scale wind, wave hight, wave period 
                    and current speed
        bow_angle = angle between the vessel center line and a line drawn from 
                    the foremost point in the water line to the point at y = Bwl/4.
                    Therefore bow_angle = atan(B/(4 * (xmax - xb4))
        Awl_aft = water plane area for x < 0 (aft midship)
        Hs = significant wave hight
        waves_angle = waves coming from direction in degrees with respect to vessel
        Bwl = vessel maximal breath at the waterline
        b_points = Beaufort weather estimation
        x_Los = longitudal position of Los / 2 
        Los = distance between for most and aft most point under water 
        Lpp = vessel length betwin perpendiculars
        g = gravity acceleration 9.81 m/c^2"""
    
    g = 9.81 
    
    bow_angle = bow_angle * pi / 180
    h_1A = .8 * bow_angle**.45
    Cwl_aft = Awl_aft * 2 * Bwl / Lpp
    
    if Cwl_aft < .85:
        Cwl_aft = .85
    elif Cwl_aft > 1.15:
        Cwl_aft = 1.15
        
    h_1B = .7 * Cwl_aft**2
    
    #convert waves angele from degrees to radians
    waves_angle = waves_angle / 180 * pi
    if pi <= waves_angle <= 2 * pi:
        direction = 2 * pi - waves_angle
    else:
        direction = waves_angle
    
    h_1 = h_1A + direction / pi * (h_1B - h_1A)
    h_2 = .05 + .95 * atan(1.45 * direction - 1.75)
    h = .09 * h_1 * h_2
    
    T_sway = Tz / .75 / Bwl**.5
    if T_sway < 1:
        f_sway = 1
    else:
        f_sway = T_sway**-3 * exp(1 - T_sway**-3)
    
    T_surge = Tz / .9 / Lpp**.33   
    
    if T_surge < 1:
        f_surge = 1
    else:
        f_surge = T_surge**-3 * exp(1 - T_surge**-3)
    
    Hs = scale_table['Peak wave period, s'][b_points]
    
    F_x_waves = .5 * rho * g * Hs**2 * Bwl * h * f_surge 
    F_y_waves = .5 * rho * g *Hs**2 * Los * (0.09 * sin(waves_angle)) * f_sway
    M_z_waves = F_y_waves * (x_Los + (.05 - .14 * direction / pi) * Los)  
        
    return [F_x_waves, F_y_waves, M_z_waves]

def summary_loads(c_loads: set, w_loads: set, wv_loads: set) -> set:
    sum_loads = [a + c + w for a, c, w in zip (c_loads, w_loads, wv_loads)]
    return sum_loads
    
def water_density_by_temp (t: float) -> float:    
    """See https://docs.cntd.ru/document/1200105587 
    water_density_by_temp calculates ocean water density dependind on the temperature
    NOTE: model of ocean water density is true for temperature in interval -2...42 C
    Returns water density in kg|m^3"""
    # Average ocean salinity is about 35 ppm
    S = 35
    #forming of required vectors
    T = (1, t, t**2, t**3, t**4, t**5)
    A = (999.842594, 6.793952 * 10**-2, -9.09529 * 10**-3, 1.001685 * 10**-4, 
         -1.120083 * 10**-6, 6.536332 * 10**-9)
    B = (.824493, -4.0899 * 10**-3, 7.6438 * 10**-5, -8.2467 * 10**-7, 5.3875 * 10**-9)
    C = (-5.72466 * 10**-3, 1.0277 * 10**-4, -1.6546 * 10**-6)
    D = 4.8314 * 10**-4
      
    #below is a scalar multiple of two vectors
    rho_w = sum(a*t for a, t in zip(A, T))
    rho = rho_w + sum(b*t for b, t in zip(B, T)) * S 
    + sum(c*t for c, t in zip(C, T)) * S**1.5 + D * S**2
    
    return rho

def air_density_by_temp_press_humid (t: float, p: float, phi: float) -> float:
    """See https://en.wikipedia.org/wiki/Density_of_air
    air_density_by_temp_press_humid calculates air density dependind on the temperature,
    pressure and humidity using ideal gas law model. Returns air density in kg|m^3"""
    M_dry_air =  0.0289652  #kg/mol
    M_vapor = 0.018016      #kg/mol
    T = t + 273.15          #degrees K
    R = 8.31446             #universal gas constant J/(K * mol)
    
    #water vapor partial pressure
    p_vapor = phi * 6.1078 * 10**((7.5 * t)/(t + 237.3))
    #dry air partial pressure
    p_dry_air = p - p_vapor
    rho_air = (p_dry_air * M_dry_air + p_vapor * M_vapor)/(T * R)
    
    return rho_air

def beuafort_scale():
    """Here is a Beuafort scale table in dictionary format""" 
    
    scale_table = dict()
    scale_table['Beuafort number'] = [i for i in range(12)]
    scale_table['Beuafort description'] = ['Calm', 'light air', 'Light breeze',
                                           'Gentle breeze', 'Moderate breeze',
                                           'Fresh breeze', 'Strong breeze', 
                                           'Moderate gale', 'Gale', 'Strong gale',
                                           'Storm', 'Violent storm']
    scale_table['Wind speed, m/s'] = [0, 1.5, 3.4, 5.4, 7.9, 10.7, 13.8, 17.1,
                                      20.7, 24.4, 28.4, 32.6]
    scale_table['Current speed, m/s'] = [0, .25, .5, .75, .75, .75, .75, .75, 
                                         .75, .75, .75, .75]
    scale_table['Peak wave period, s'] = [None, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 
                                          9, 10, 10.5, 11.5, 12]
    scale_table['Significant wave heighr, m'] = [0, .1, .4, .8, 1.3, 2.1, 3.1, 
                                                 4.2, 5.7, 7.4, 9.5, 12.1]
    return scale_table

#forming the Beuafort scale table for weather conditions
scale_table = beuafort_scale()
#initial weather data
print('Please, insert air temperature and water temperature in Celsius degrees:')
air_temperature, water_temperature = float(input()), float(input())
print('\nPlease, insert air pressure in Pa:')
pressure = float(input())  
print('\nPlease, insert air relative humidity in percentes:')
humidity = float(input())  
print('\nPlease, insert weather conditions in Beuafort points:')
b_points = int(input()) - 1
print('\nPlease, insert wind, current and wave angles in degrees:')
wind_angle, curr_angle, waves_angle = float(input()), float(input()), float(input())
print('\nPlease, insert current speed in m/s:')
V_curr = float(input())

#Lets define wind speed, wind induced current speed and peak wave period by Beuafort
V_wind = scale_table['Wind speed, m/s'][b_points]   
V_wind_curr = scale_table['Current speed, m/s'][b_points]   
Tz = scale_table['Peak wave period, s'][b_points]

#Lets calculate air and water densities for current weather
rho = water_density_by_temp (water_temperature)
rho_air =  air_density_by_temp_press_humid(air_temperature, pressure, humidity)

#Insert vessel particulars
print('\nPlease, insert front and lateral wind area in m^2: ')
A_f_wind, A_l_wind = float(input()), float(input())
print('\nPlease, insert  wind force lateral application point in m: ')
x_l_air = float(input())
print('\nPlease, insert vessel length between perpendiculars and distance between for most and aft most point under water in m: ')
Lpp, Los = float(input()), float(input())
print('\nPlease, insert x_Los coordinate point from midship in m: ')
x_Los = float(input())
print('\nPlease, insert waterline max breadth and draft in m: ')
Bwl, Tm = float(input()), float(input())
print('\nPlease, insert lateral submerged hull area in m^2: ')
A_l_hull = float(input())
print('\nPlease, insert hydrodinamic force lateral application point in m: ')
x_l_hull = float(input())
print('\nPlease, insert bow_angle in degreese: ')
bow_angle = float(input())
print('\nPlease, insert a water plane area for x < 0 (aft midship): ')
Awl_aft = float(input())

print('\nChoose current  calculus method (0, False or None - without wind indused): ')
curr_method = input()
if curr_method == '0' or curr_method.lower() == 'false' or curr_method.lower() == 'none':
    curr_method = False
else:
    curr_method == True


w_loads = wind_loads (rho_air, V_wind, A_f_wind, A_l_wind, wind_angle, x_l_air,
                      Lpp)
c_loads = current_loads (rho, V_curr, Bwl, Tm, A_l_hull, curr_angle, x_l_hull,
                         Lpp, wind_angle, V_wind_curr, curr_method)
wv_loads = waves_loads (rho, bow_angle, Awl_aft, Tz, waves_angle, Bwl, Lpp, Los, x_Los)
s_loads = summary_loads(c_loads, w_loads, wv_loads)