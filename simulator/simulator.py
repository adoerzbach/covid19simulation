'''
Created on 20 Mar 2020

@author: ado
'''

import numpy as np


class simulator:

    def __init__(self,
                 R0,
                 
                 time_incubation,
                 time_recover_symtomatic,
                 time_recover_hospitalized,
                 time_die_symtpomatic,
                 time_die_hospitalized,
                 time_hostpitalize,
                 time_immunisation,
    
                 share_hospitalizations,
                 share_deaths_symtomatic,
                 share_deaths_hospitalized,
                 share_asymptomatic,
                 count_uninfected,
                 count_infectious,
                 count_asymptomatic,
                 count_symptomatic,
                 count_hostpitalized,
                 count_immune,
                 count_dead,
                 infectious_factor_symtomatic,
                 infectious_factor_hospitalized
                 ):
        
        ''' Parameter Description
        R0: matrix with the number of contacts to people which are infecting uninfected people between segments of population

        time_incubation: time in which poeple are infectious but have no symptoms
        time_recover_symtomatic: time to recover of poeple show symptoms not hospitalized
        time_recover_hospitalized: time to recover for poeple hospitalized
        time_die_symtpomatic: time until death of symptomatic people at home
        time_die_hospitalized: time until death after hospitalization
        time_hostpitalize: time between the first symptoms and the hospitalization
        time_immunisation: time of asymptomatic cases after the start to be infectious until they are immune

        share_hospitalizations: share of people which have symptoms and are getting hospitalized
        share_deaths_symtomatic: share of people which die without hospitalization
        share_deaths_hospitalized: share of people which die after hospitalization
        share_asymptomatic: share of people infectious which are not showing symptoms
        share_immune: share of people which are immune at start of simulation
        
        count_uninfected: number of not yet infected people
        count_infectious: number of infectious people during incubation time
        count_asymptomatic: number of people not showing any symptoms
        count_symptomatic: number of people with symptoms staying at home 
        count_hostpitalized: number of people hospitalized
        count_immune: number of poeple immune
        count_dead: number of poeple died
        infectious_factor_symtomatic: factor reducing R0 for people which have symptoms because of self quarantine.
        infectious_factor_hospitalized: factor reducing R0 for people which have been hospitalized
        '''
        self.R0 = np.array(R0)
        self.time_incubation = np.array(time_incubation)
        self.time_recover_symtomatic = np.array(time_recover_symtomatic)
        self.time_recover_hospitalized = np.array(time_recover_hospitalized)
        self.time_die_symtpomatic = np.array(time_die_symtpomatic)
        self.time_die_hospitalized = np.array(time_die_hospitalized)
        self.time_hostpitalize = np.array(time_hostpitalize)
        self.time_immunisation = np.array(time_immunisation)
        self.share_hospitalizations = np.array(share_hospitalizations)
        self.share_deaths_symtomatic = np.array(share_deaths_symtomatic)
        self.share_deaths_hospitalized = np.array(share_deaths_hospitalized)
        self.share_asymptomatic = np.array(share_asymptomatic)
        self.count_uninfected = np.array(count_uninfected)
        self.count_infectious = np.array(count_infectious)
        self.count_asymptomatic = np.array(count_asymptomatic)
        self.count_symptomatic = np.array(count_symptomatic)
        self.count_hostpitalized = np.array(count_hostpitalized)
        self.count_immune = np.array(count_immune)
        self.count_dead = np.array(count_dead)
        self.infectious_factor_symtomatic = np.array(infectious_factor_symtomatic)
        self.infectious_factor_hostpitalized = np.array(infectious_factor_hospitalized)
        self.max_hospitalisations = 0
        self.day = 0
        self.total_reported_cases = self.count_symptomatic + self.count_hostpitalized
        
    def nextday_silent(self):
        self.healed_hospital = self.count_hostpitalized * (1 - self.share_deaths_hospitalized) / self.time_recover_hospitalized
        self.healed_symptomatic = self.count_symptomatic * (1 - self.share_deaths_symtomatic) / self.time_recover_symtomatic
        self.immunized = self.count_asymptomatic / self.time_immunisation
        self.deaths_symptomatic = self.count_symptomatic * self.share_deaths_symtomatic / self.time_die_symtpomatic
        
        self.deaths_hospitalized = self.count_hostpitalized * self.share_hospitalizations / self.time_die_hospitalized
        
        self.infections = (self.R0.dot(
            self.count_infectious + self.count_asymptomatic + 
            self.count_symptomatic * self.infectious_factor_symtomatic + 
            self.count_hostpitalized * self.infectious_factor_hostpitalized) * 
            (self.count_uninfected / 
            (self.count_uninfected + self.count_immune + 
             self.count_infectious + self.count_asymptomatic + 
             self.count_hostpitalized + self.count_symptomatic))) / (self.time_incubation + self.time_immunisation)
          
        self.fall_ills = self.count_infectious * (1 - self.share_asymptomatic) / self.time_incubation 
        self.stay_healthies = self.count_infectious * self.share_asymptomatic / self.time_incubation
        self.hospitalisations = self.count_symptomatic * self.share_hospitalizations / self.time_hostpitalize
        
        self.count_dead = self.count_dead + self.deaths_hospitalized + self.deaths_symptomatic
        self.count_infectious = self.count_infectious + self.infections - self.stay_healthies - self.fall_ills
        self.count_immune = self.count_immune + self.immunized + self.healed_hospital + self.healed_symptomatic
        self.count_hostpitalized = self.count_hostpitalized - self.healed_hospital - self.deaths_hospitalized + self.hospitalisations
        self.count_symptomatic = self.count_symptomatic - self.deaths_symptomatic - self.healed_symptomatic - self.hospitalisations + self.fall_ills
        self.count_asymptomatic = self.count_asymptomatic + self.stay_healthies - self.immunized
        self.count_uninfected = self.count_uninfected - self.infections
        i = sum(self.count_hostpitalized)
        if (self.max_hospitalisations < i):
            self.max_hospitalisations = i
            self.max_day = self.day
            
        self.day += 1
        self.total_reported_cases = self.total_reported_cases + self.fall_ills
        
        
        # print(json.dumps(self,default=lambda o: o.json()))

    def nextday(self):
        self.nextday_silent()
        format = ('{"Day":%d,"Infections":%s,"Deaths":%s,"Hospitalizations":%s,"Healed from Hospital":%s,Total Deaths":%s,"Total Infectious People":%s,' + 
                   '"Total Immune People":%s,"Total hospitalized People":%s,"Total Symptomatic People":%s' + 
                   '"Total Asymptomatic People":%s,"Total Unifected People":%s,"Total Population":%s}'
                   )
            
        print(format % (self.day,
                          self.infections.__str__(),
                          (self.deaths_hospitalized + self.deaths_symptomatic).__str__(),
                          self.hospitalisations.__str__(),
                          self.healed_hospital.__str__(),
                          self.count_dead.__str__(),
                          self.count_infectious.__str__(),
                          self.count_immune.__str__(),
                          self.count_hostpitalized.__str__(),
                          self.count_symptomatic.__str__(),
                          self.count_asymptomatic.__str__(),
                          self.count_uninfected.__str__(),
                          (self.count_infectious + self.count_immune + self.count_hostpitalized + self.count_symptomatic + self.count_asymptomatic + self.count_uninfected).__str__()
                          )
        )
        

def simschweiz():
        # Schweiz
    minimalr0 = 0.01
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
                [.10, 0.001],
                # share_deaths_symtomatic
                [.10, 0.0001],
                # share_deaths_hospitalized
                [.30, 0.0001],
                # share_asymptomatic
                [0.5, .5],

                # count_uninfected
                [1600000, 6900000],
                # count_infectious
                [10000, 30000],
                # count_asymptomatic
                [10000, 30000],
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
                [0.01, 0.01]
                );
    # End of the full lockdown in days from the beginning of the simulation
    end_full_quarantine = 20
    # End of the half lockdown (where no risk people start to move again) in days from the beginning of the simulation
    start_forced_infection = 50
    # End of the forced infection period for people at no risk in days from the beginning of the simulation
    forced_infection_end = 180
    # Start of normalized life again in days from the beginning of the simulation
    normal_live_start = 290
    # End of simulation in days from the beginning of the simulation
    end_of_simulation = 350
    # Full Quarantine time.
    for i in range(1, end_full_quarantine):
        sim.nextday()
    
    # Partial Quarantine with people at risk locked away
    sim.R0 = np.array([[minimalr0, minimalr0], [minimalr0, 2]])
    for i in range(end_full_quarantine, start_forced_infection):
        sim.nextday()

    # Open Scools and shops, but keep people at risk away.    
    sim.R0 = np.array([[minimalr0, minimalr0], [minimalr0, 5]])
    for i in range(start_forced_infection, forced_infection_end):
        sim.nextday()
    
    # Start of getting people at risk back to normal live
    sim.R0 = np.array([[.7, .7], [.7, 2.5]])
    for i in range(forced_infection_end, normal_live_start):
        sim.nextday()
    
    # This simulates a better methods of cure in hospitals.
    sim.share_deaths_hospitalized[0] = .1     
    # Start of normal live with minor safety precautions of people at risk    
    sim.R0 = np.array([[1.5, 1.5], [1.5, 2.5]])
    for i in range(normal_live_start, end_of_simulation):
        # This simulates the open boarders and imported infections
        # Hopefully the can be kept as low as this, which means only one person infected is
        # traveling to Switzerland without being caught at the border
        sim.count_infectious = sim.count_infectious + np.array([1 / 100, 1 / 7])
        sim.nextday()
        
    print("Max Hospitalization %d after %d days" % (sim.max_hospitalisations, sim.max_day))


def callibrate_modell():
    
    '''
    try to minimize to relativ error in hospitalisations and deaths and reported cases
    by changing values for minimalr0, share_hospitalizations share_deaths_xx, share_asymptotic
    '''
    
    # Values reported for 30/3/2020
    reported_deaths = 370
    reported_hospitalisations = 1980
    reported_cases = 16026
    param=[.05,0.3,0.02,.3,0.01,0.2,0.01,0.5,0.5]
    param=[0.05202000000000001, 0.3015, 0.06038399999999937, 0.15206999999999993, 0.01010025, 0.20808000000000004, 0.010403999999999998, 0.22061249999999977, 0.007537499999988458]
    param=[0.05306040000000001, 0.298485, 0.11533343999999886, 0.08363850000000059, 0.01015075125, 0.4973111999999992, 0.010612079999999998, 0.15884099999999968, 0.0075751874999884]
    param=[0.1591811999999999, 0.259681950000001, 0.1384001279999985, 0.05645598749999983, 0.01020150500625, 0.7559130239999964, 0.010824321599999997, 0.14295689999999983, 0.007613063437488342]
    param=[0.3104033399999987, 0.21228999412500074, 0.1404761299199985, 0.05504458781249985, 0.01025251253128125, 0.7785904147199963, 0.011040808031999997, 0.08005586400000145, 0.007651128754675784]
    param=[0.3693799745999984, 0.1862844698446878, 0.13942255894559852, 0.05807204014218735, 0.010303775093937657, 0.7396608939839967, 0.011096012072159997, 0.03282290423999955, 0.007689384398449163]
    param=[0.3943131228854982, 0.17417597930478304, 0.1387254461508705, 0.059669021246097506, 0.010509850595816411, 0.7026778492847976, 0.011317932313603197, 0.006236351805599581, 0.007689384398449163]
    param=[0.40860697359009757, 0.16699122015846088, 0.13855203934318192, 0.06086240167101946, 0.010299653583900078, 0.6938943761687375, 0.011374521975171213, 0.006236351805599582, 0.00011534076597675795]
    param=[0.41728987177888716, 0.16438198234348486, 0.138032469195645, 0.06162318169190721, 0.01032540271785983, 0.6843533284964174, 0.011602012414674637, 0.00015590879513990158, 0.00011591746980664175]
    param=[0.4225059951761232, 0.16237857693367358, 0.13801090162233315, 0.061825382756833774, 0.010312495964462504, 0.6813592826842452, 0.01166002247674801, 0.0001566883391156011, 0.00011649705715567496]
    for l in range(0,10):
        i=0
        while i<len(param):
            error = 10.0
            lasterror=20.0
            maxiterations=200
            lastparam=param[i]*.99
            while (1-error/lasterror)**2 > .000001 and maxiterations>0:
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
                        [0.01, 0.01]
                        );
                    # End of the full lockdown in days from the beginning of the simulation
                    simulation_days = 13
                    # Full Quarantine time.
                    for e in range(1, simulation_days):
                        sim.nextday_silent()
                    lasterror=error
                    tmpparam=param[i]
                    error=(1-sum(sim.count_dead)/reported_deaths)**2+(1-sum(sim.count_hostpitalized)/reported_hospitalisations)**2+(1-sum(sim.total_reported_cases)/reported_cases)**2
                    if error<lasterror:
                        param[i]=param[i]*2-lastparam
                        #print("right direction, error=%1.4f, lasterror=%1.5f, param[%d]=%3.5f,lastparam=%3.5f"%(error,lasterror,i,param[i],lastparam))
                    else:
                        param[i]=(param[i]+lastparam)/2
                        #print("wrong direction, error=%1.4f, lasterror=%1.5f, param[%d]=%3.5f,lastparam=%3.5f"%(error,lasterror,i,param[i],lastparam))
                    lastparam=tmpparam
                    maxiterations-=1
                    #print(i,param)
            i+=1
        print(param)
    
def simschweiz_ausbreitung():
    # Schweiz von 17.3.2020 (Shutdown Schweiz)
    minimalr0 = 0.4
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
                [.20, 0.02],
                # share_deaths_symtomatic
                [.10, 0.0001],
                # share_deaths_hospitalized
                [.30, 0.0001],
                # share_asymptomatic
                [0.5, .5],

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
                [0.01, 0.01]
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
                [0.01, 0.01]
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
    # simschweiz()
    # simwuhan() 
    callibrate_modell()
    #simschweiz_ausbreitung()
        
    
if __name__ == '__main__':
    main()

