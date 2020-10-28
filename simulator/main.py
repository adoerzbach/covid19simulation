'''
Created on 11 Apr 2020

@author: ado
'''

import numpy as np
import json
from datetime import datetime
from simulator import simulator
import random
r=dict()
def simschweiz_2nd_wave():
    # Schweiz start Simulation 25/07/2020
    minimalr0 = 1.78
    sim = simulator(
                # RO
                [[minimalr0/4.5, minimalr0/6], [minimalr0/6, minimalr0]],
                # time_incubation
                [5.2, 5.2],
                # time_recover_symtomatic
                [15, 15],
                # time_recover_hospitalized
                [16, 16],
                # time_die_symtpomatic
                [17, 17],
                # time_die_hospitalized
                [12.5, 12.5],
                # time_hostpitalize
                [4.5, 4.5],
                # time_immunisation
                [10, 10],

                # share_hospitalizations                
                [.061, 0.006],
                # share_deaths_symtomatic
                [.01, 0.00001],
                # share_deaths_hospitalized
                [.10, 0.0005],
                # share_asymptomatic
                [0.9, 0.92],

                # count_uninfected
                [1100000, 7300000],
                # count_infectious
                [200, 1000],
                # count_asymptomatic
                [600, 6000],
                # count_symptomatic
                [100, 900],
                # count_hostpitalized
                [80, 30],
                # count_immune
                [30000, 150000],
                # count_dead
                [0, 1693],
                
                # infectious_factor_symtomatic,
                [.2, .2],
                # infectious_factor_hospitalized
                [0.01, 0.01],
                #Startdate
                datetime(2020,7,25)
                );
    nextday=sim.nextday_silent
    # 
    # End of the full lockdown in days from the beginning of the simulation
    end_full_quarantine = 99
    # End of the half lockdown (where no risk people start to move again) in days from the beginning of the simulation
    start_forced_infection = 150
    # End of the forced infection period for people at no risk in days from the beginning of the simulation
    forced_infection_end = 300
    # Start of normalized life again in days from the beginning of the simulation
    normal_live_start = 10000
    # End of simulation in days from the beginning of the simulation
    end_of_simulation = 900
    # Full Quarantine time.
    for i in range(1, min([end_full_quarantine,end_of_simulation])):
        nextday()
    
    # Partial Quarantine with people at risk locked away
    sim.R0 = np.array([[minimalr0/4.5, minimalr0/6], [minimalr0/6, .8]])
    for i in range(end_full_quarantine,min([end_of_simulation, start_forced_infection])):
        nextday()        

    # Open Scools and shops, but keep people at risk away.    
    sim.R0 = np.array([[minimalr0/2, minimalr0/3], [minimalr0/3, minimalr0*.8]])
    for i in range(start_forced_infection, min([end_of_simulation,forced_infection_end])):
        nextday()
    
    # Start of getting people at risk back to normal live
    sim.R0 = np.array([[1.5, 1.5], [1.5, 2.5]])
    for i in range(forced_infection_end, min([end_of_simulation,normal_live_start])):
        nextday()
    
    # This simulates a better methods of cure in hospitals.
    sim.share_deaths_hospitalized[0] = .1     
    # Start of normal live with minor safety precautions of people at risk    
    sim.R0 = np.array([[1.5, 1.5], [1.5, 2.5]])
    for i in range(normal_live_start, end_of_simulation):
        # This simulates the open boarders and imported infections
        # Hopefully the can be kept as low as this, which means only one person infected is
        # traveling to Switzerland without being caught at the border
        sim.count_infectious = sim.count_infectious + np.array([1 / 100, 1 / 7])
        nextday()

    #print(json.dumps(sim.result,indent=4))
    sim.tocsv(["count_dead","count_immune","count_hostpitalized","immunized","total_reported_cases","fall_ills","stay_healthies"],timeformat="%d.%m.%Y")
    #print("Max Hospitalization %d after %d days" % (sim.max_hospitalisations, sim.max_day))

def simschweiz():
    # Schweiz start Simulation 23/03/2020
    minimalr0 = 0.1
    sim = simulator(
                # RO
                [[minimalr0, minimalr0], [minimalr0, minimalr0]],
                # time_incubation
                [5.2, 5.2],
                # time_recover_symtomatic
                [15, 15],
                # time_recover_hospitalized
                [16, 16],
                # time_die_symtpomatic
                [17, 17],
                # time_die_hospitalized
                [12.5, 12.5],
                # time_hostpitalize
                [4.5, 4.5],
                # time_immunisation
                [10, 10],

                # share_hospitalizations                
                [.25, 0.025],
                # share_deaths_symtomatic
                [.07, 0.0001],
                # share_deaths_hospitalized
                [.15, 0.005],
                # share_asymptomatic
                [0.6, 0.9],

                # count_uninfected
                [1600000, 6900000],
                # count_infectious
                [10000, 30000],
                # count_asymptomatic
                [14000, 49000],
                # count_symptomatic
                [2000, 7000],
                # count_hostpitalized
                [1450, 50],
                # count_immune
                [10000, 10000],
                # count_dead
                [130, 0],
                
                # infectious_factor_symtomatic,
                [.2, .2],
                # infectious_factor_hospitalized
                [0.01, 0.01],
                #Startdate
                datetime(2020,3,23)
                );
    nextday=sim.nextday_silent
    # 
    # End of the full lockdown in days from the beginning of the simulation
    end_full_quarantine = 65
    # End of the half lockdown (where no risk people start to move again) in days from the beginning of the simulation
    start_forced_infection = 100
    # End of the forced infection period for people at no risk in days from the beginning of the simulation
    forced_infection_end = 800
    # Start of normalized life again in days from the beginning of the simulation
    normal_live_start = 10000
    # End of simulation in days from the beginning of the simulation
    end_of_simulation = 200
    # Full Quarantine time.
    for i in range(1, min([end_full_quarantine,end_of_simulation])):
        nextday()
    
    # Partial Quarantine with people at risk locked away
    sim.R0 = np.array([[minimalr0*2, minimalr0*2], [minimalr0*2, 1.2]])
    for i in range(end_full_quarantine,min([end_of_simulation, start_forced_infection])):
        nextday()        

    # Open Scools and shops, but keep people at risk away.    
    sim.R0 = np.array([[minimalr0*4, minimalr0*4], [minimalr0*4, 1.5]])
    for i in range(start_forced_infection, min([end_of_simulation,forced_infection_end])):
        nextday()
    
    # Start of getting people at risk back to normal live
    sim.R0 = np.array([[.7, .7], [.7, 2.0]])
    for i in range(forced_infection_end, min([end_of_simulation,normal_live_start])):
        nextday()
    
    # This simulates a better methods of cure in hospitals.
    sim.share_deaths_hospitalized[0] = .1     
    # Start of normal live with minor safety precautions of people at risk    
    sim.R0 = np.array([[1.5, 1.5], [1.5, 2.5]])
    for i in range(normal_live_start, end_of_simulation):
        # This simulates the open boarders and imported infections
        # Hopefully the can be kept as low as this, which means only one person infected is
        # traveling to Switzerland without being caught at the border
        sim.count_infectious = sim.count_infectious + np.array([1 / 100, 1 / 7])
        nextday()

    #print(json.dumps(sim.result,indent=4))
    sim.tocsv(["count_dead","count_immune","count_hostpitalized","immunized","total_reported_cases","fall_ills","stay_healthies"],timeformat="%d.%m.%Y")
    #print("Max Hospitalization %d after %d days" % (sim.max_hospitalisations, sim.max_day))

def callibrate_modell():
    
    '''
    try to minimize to relativ error in hospitalisations and deaths and reported cases
    by changing values for minimalr0, share_hospitalizations share_deaths_xx, share_asymptotic
    '''
    # Start of simulation on 17/03/2020
    # Values reported for 31/3/2020
    reported_deaths = [47,53,75,91,110,137,158,190,233,267,307,343,399,469,526,579,639,711,758,812,866,932,984,1042,1083,1132,1163,1209,1261,1302,1327]
    reported_hospitalisations = [459,660,766,869,1060,1166,1306,1409,1558,1732,1811,1920,2120,2163,2261,2330,2326,2314,2304,2325,2259,2154,2089,2049,1966,1930,1924,1888,1769,1706,1629]
    reported_cases = [4116,5388,6516,7326,7939,9187,10185,11210,12452,13749,14662,15416,16449,17442,18451,19552,20476,21088,21572,22213,22842,23605,24263,24762,25229,25556,25779,26083,26387,26721,26929]
    simulation_days = 28
    param=[.05,0.3,0.02,.3,0.01,0.2,0.01,0.5,0.5]
    random.seed()
    for l in range(0,30):
        i=0
        while i<len(param):
            error = 10.0
            lasterror=20.0
            maxiterations=1000
            lastparam=param[i]*(1+(random.randint(0,9)-5)/100)
            firstchange=False
            
            while (1-error/lasterror)**2 > .00000001 and maxiterations>0:
                    tmperror=0
                    sim = simulator(
                        # RO
                        [[param[0], param[0]], [param[0],param[0]]],
                        # time_incubation
                        [5.2, 5.2],
                        # time_recover_symtomatic
                        [15, 15],
                        # time_recover_hospitalized
                        [10.5, 10.5],
                        # time_die_symtpomatic
                        [15, 15],
                        # time_die_hospitalized
                        [10.5, 10.5],
                        # time_hostpitalize
                        [4.5, 4.5],
                        # time_immunisation
                        [10, 10],
                        
                        # share_hospitalizations                
                        [param[1],param[2]],
                        # share_deaths_symtomatic
                        [param[3],param[4]],
                        # share_deaths_hospitalized
                        [param[5],param[6]],
                        # share_asymptomatic
                        [param[7],param[8]],
        
                        # count_uninfected
                        [1600000, 6900000],
                        # count_infectious
                        [3000, 5300],
                        # count_asymptomatic
                        [3000, 5300],
                        # count_symptomatic
                        [1000, 1778],
                        # count_hostpitalized
                        [270, 34],
                        # count_immune
                        [3000, 5300],
                        # count_dead
                        [30, 0],
                        
                        # infectious_factor_symtomatic,
                        [.2, .2],
                        # infectious_factor_hospitalized
                        [0.01, 0.01],
                        # Startdate
                        datetime(2020,3,17)
                        );
                    # End of the full lockdown in days from the beginning of the simulation
                    
                    # Full Quarantine time.
                    
                    for e in range(0, simulation_days):
                        sim.nextday_silent()
                        tmperror=(1-sum(sim.count_dead)/reported_deaths[e])**2+(1-sum(sim.count_hostpitalized)/reported_hospitalisations[e])**2+(1-sum(sim.total_reported_cases)/reported_cases[e])**2
                        
                    lasterror=error
                    tmpparam=param[i]
                    error=tmperror
                    if error<lasterror:
                        param[i]=param[i]*2-lastparam
                        #print("right direction, error=%1.4f, lasterror=%1.5f, param[%d]=%3.5f,lastparam=%3.5f"%(error,lasterror,i,param[i],lastparam))
                    else: 
                        if firstchange:
                            param[i]=2*lastparam-param[i]
                        else:
                            param[i]=(param[i]+lastparam)/2
                    if param[i]<0:
                        param[i]=0.01
                    if param[i]>1:
                        param[i]=.99
                        #print("wrong direction, error=%1.4f, lasterror=%1.5f, param[%d]=%3.5f,lastparam=%3.5f"%(error,lasterror,i,param[i],lastparam))
                    lastparam=tmpparam
                    maxiterations-=1
                    #print(i,param)
            i+=1
        print(param)
    
def simschweiz_ausbreitung():
    # Schweiz von 17.3.2020 (Shutdown Schweiz)
    minimalr0 = 0.1
    sim = simulator(
                # RO
                [[minimalr0, minimalr0], [minimalr0, minimalr0]],
                # time_incubation
                [5.2, 5.2],
                # time_recover_symtomatic
                [15, 15],
                # time_recover_hospitalized
                [10.5, 10.5],
                # time_die_symtpomatic
                [15, 15],
                # time_die_hospitalized
                [10.5, 10.5],
                # time_hostpitalize
                [4.5, 4.5],
                # time_immunisation
                [10, 10],

                # share_hospitalizations                
                [.20, 0.05],
                # share_deaths_symtomatic
                [.10, 0.0001],
                # share_deaths_hospitalized
                [.30, 0.0001],
                # share_asymptomatic
                [0.5, .5],

                # count_uninfected
                [1600000, 6900000],
                # count_infectious
                [9000, 15900],
                # count_asymptomatic
                [9000, 15900],
                # count_symptomatic
                [1000, 1778],
                # count_hostpitalized
                [244, 60],
                # count_immune
                [3000, 5300],
                # count_dead
                [30, 0],
                
                # infectious_factor_symtomatic,
                [.2, .2],
                # infectious_factor_hospitalized
                [0.01, 0.01],
                # startdate
                datetime(2020,3,17)
                );
    # End of the full lockdown in days from the beginning of the simulation
    end_full_quarantine = 33
    # End of the half lockdown (where no risk people start to move again) in days from the beginning of the simulation
    start_forced_infection = 13
    # End of the forced infection period for people at no risk in days from the beginning of the simulation
    forced_infection_end = 13
    # Start of normalized life again in days from the beginning of the simulation
    normal_live_start = 13
    # End of simulation in days from the beginning of the simulation
    end_of_simulation = 13
    # Full Quarantine time.
    for i in range(1, end_full_quarantine):
        sim.nextday()
    
    ''' 
    # Partial Quarantine with people at risk locked away
    sim.R0=np.array([[minimalr0,minimalr0],[minimalr0,2]])
    for i in range(end_full_quarantine,start_forced_infection):
        sim.nextday()

    # Open Scools and shops, but keep people at risk away.    
    sim.R0=np.array([[minimalr0,minimalr0],[minimalr0,5]])
    for i in range(start_forced_infection,forced_infection_end):
        sim.nextday()
    
    # Start of getting people at risk back to normal live
    sim.R0=np.array([[.7,.7],[.7,2.5]])
    for i in range(forced_infection_end,normal_live_start):
        sim.nextday()

    
    # This simulates a better methods of cure in hospitals.
    sim.share_deaths_hospitalized[0]=.1     
    # Start of normal live with minor safety precautions of people at risk    
    sim.R0=np.array([[1.5,1.5],[1.5,2.5]])
    for i in range(normal_live_start,end_of_simulation):
        # This simulates the open boarders and imported infections
        # Hopefully the can be kept as low as this, which means only one person infected is
        # traveling to Switzerland without being caught at the border
        sim.count_infectious=sim.count_infectious+np.array([1/100,1/7])
        sim.nextday()
    '''    
    print("Max Hospitalization %d after %d days" % (sim.max_hospitalisations, sim.max_day))


def simwuhan():  
        # Wuhan
    minimalr0 = 0.01
    normalr0 = 3.5
    sim = simulator(
                # RO
                [[normalr0, normalr0], [normalr0, normalr0]],
                # time_incubation
                [6.4, 6.4],
                # time_recover_symtomatic
                [15, 15],
                # time_recover_hospitalized
                [10.5, 10.5],
                # time_die_symtpomatic
                [15, 15],
                # time_die_hospitalized
                [10.5, 10.5],
                # time_hostpitalize
                [4.5, 4.5],
                # time_immunisation
                [10, 10],
                                
                # share_hospitalizations,                
                [.10, 0.001],
                # share_deaths_symtomatic,
                [.10, 0.0001],
                # share_deaths_hospitalized,
                [.30, 0.0001],
                # share_asymptomatic,
                [0.5, .5],
                
                # count_uninfected
                [2600000, 8000000],
                # count_infectious,
                [200, 200],
                # count_asymptomatic,
                [200, 200],
                # count_symptomatic,
                [30, 30],
                # count_hostpitalized,
                [7, 0],
                # count_immune,
                [0, 0],
                # count_dead,
                [130, 0],
                
                # infectious_factor_symtomatic,
                [.2, .2],
                # infectious_factor_hospitalized
                [0.01, 0.01],
                #startdate
                datetime(2020,1,7)
                );
    # on Jan 23, 16 days after the start of the simulation the complete shutdown comes
    start_full_quarantine = 16
    # on April 8 or 9 the people can start to go out again
    end_fullquarantine = 90
    # Traveling to and away from Wuhan is allowed again.
    normal_live_start = 120
    for i in range(1, start_full_quarantine):
        sim.nextday()
    
    sim.R0 = np.array([[minimalr0, minimalr0], [minimalr0, minimalr0]])
    for i in range(start_full_quarantine, end_fullquarantine):
        sim.nextday()
         
    sim.R0 = np.array([[.5, .5], [.5, .5]])
    for i in range(end_fullquarantine, normal_live_start):
        sim.nextday()
    
    sim.R0 = np.array([[1.5, 1.5], [1.5, 2.5]])
    for i in range(normal_live_start, normal_live_start + 20):
        # Import of infections start again, due to traveling
        sim.count_infectious = sim.count_infectious + np.array([.2, 1])
        sim.nextday()
        
    print("Max Hospitalization %d after %d days" % (sim.max_hospitalisations, sim.max_day))

         
def main():
    simschweiz_2nd_wave()
    # simwuhan() 
    # callibrate_modell()
    # simschweiz_ausbreitung()
        
    
if __name__ == '__main__':
    main()
