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
        
        ''' Prameter Description
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
        self.R0=np.array(R0)
        self.time_incubation=np.array(time_incubation)
        self.time_recover_symtomatic=np.array(time_recover_symtomatic)
        self.time_recover_hospitalized=np.array(time_recover_hospitalized)
        self.time_die_symtpomatic=np.array(time_die_symtpomatic)
        self.time_die_hospitalized=np.array(time_die_hospitalized)
        self.time_hostpitalize=np.array(time_hostpitalize)
        self.time_immunisation=np.array(time_immunisation)
        self.share_hospitalizations=np.array(share_hospitalizations)
        self.share_deaths_symtomatic=np.array(share_deaths_symtomatic)
        self.share_deaths_hospitalized=np.array(share_deaths_hospitalized)
        self.share_asymptomatic=np.array(share_asymptomatic)
        self.count_uninfected=np.array(count_uninfected)
        self.count_infectious=np.array(count_infectious)
        self.count_asymptomatic=np.array(count_asymptomatic)
        self.count_symptomatic=np.array(count_symptomatic)
        self.count_hostpitalized=np.array(count_hostpitalized)
        self.count_immune=np.array(count_immune)
        self.count_dead=np.array(count_dead)
        self.infectious_factor_symtomatic=np.array(infectious_factor_symtomatic)
        self.infectious_factor_hostpitalized=np.array(infectious_factor_hospitalized)
        self.max_hospitalisations=0
        self.day=0
        
    def nextday(self):
        healed_hospital=self.count_hostpitalized*(1-self.share_deaths_hospitalized)/self.time_recover_hospitalized
        healed_symptomatic=self.count_symptomatic*(1-self.share_deaths_symtomatic)/self.time_recover_symtomatic
        immunized=self.count_asymptomatic/self.time_immunisation
        deaths_symptomatic=self.count_symptomatic*self.share_deaths_symtomatic/self.time_die_symtpomatic
        
        deaths_hospitalized=self.count_hostpitalized*self.share_hospitalizations/self.time_die_hospitalized
        
        infections=(self.R0.dot(
            self.count_infectious+self.count_asymptomatic+
            self.count_symptomatic*self.infectious_factor_symtomatic+
            self.count_hostpitalized*self.infectious_factor_hostpitalized)*
            (self.count_uninfected/
            (self.count_uninfected+self.count_immune+
             self.count_infectious+self.count_asymptomatic+
             self.count_hostpitalized+self.count_symptomatic)))/(self.time_incubation+self.time_immunisation)
          
        fall_ills=self.count_infectious*(1-self.share_asymptomatic)/self.time_incubation 
        stay_healthies=self.count_infectious*self.share_asymptomatic/self.time_incubation
        hospitalisations=self.count_symptomatic*self.share_hospitalizations/self.time_hostpitalize
        
        
        self.count_dead=self.count_dead+deaths_hospitalized+deaths_symptomatic
        self.count_infectious=self.count_infectious+infections-stay_healthies-fall_ills
        self.count_immune=self.count_immune+immunized+healed_hospital+healed_symptomatic
        self.count_hostpitalized=self.count_hostpitalized-healed_hospital-deaths_hospitalized+hospitalisations
        self.count_symptomatic=self.count_symptomatic-deaths_symptomatic-healed_symptomatic-hospitalisations+fall_ills
        self.count_asymptomatic=self.count_asymptomatic+stay_healthies-immunized
        self.count_uninfected=self.count_uninfected-infections
        i=sum(self.count_hostpitalized)
        if (self.max_hospitalisations<i):
            self.max_hospitalisations=i
            self.max_day=self.day
            
        self.day+=1
        
        format=('{"Day":%d,"Infections":%s,"Deaths":%s,"Total Deaths":%s,"Total Infectious People":%s,'+
               '"Total Immune People":%s,"Total hospitalized People":%s,"Total Symptomatic People":%s'+
               '"Total Asymptomatic People":%s,"Total Unifected People":%s,"Total Population":%s}'
               )
        
        print(format%(self.day,
                      infections.__str__(),
                      (deaths_hospitalized+deaths_symptomatic).__str__(),
                      self.count_dead.__str__(),
                      self.count_infectious.__str__(),
                      self.count_immune.__str__(),
                      self.count_hostpitalized.__str__(),
                      self.count_symptomatic.__str__(),
                      self.count_asymptomatic.__str__(),
                      self.count_uninfected.__str__(),
                      (self.count_infectious+self.count_immune+self.count_hostpitalized+self.count_symptomatic+self.count_asymptomatic+self.count_uninfected).__str__()
                      )
        )
        
        #print(json.dumps(self,default=lambda o: o.json()))
        
def main():
    #Schweiz
    minimalr0=0.01
    sim=simulator(
                # RO
                [[minimalr0,minimalr0],[minimalr0,minimalr0]],
                # time_incubation
                [5.2,5.2],
                # time_recover_symtomatic
                [15,15],
                # time_recover_hospitalized
                [10.5,10.5],
                # time_die_symtpomatic
                [15,15],
                # time_die_hospitalized
                [10.5,10.5],
                # time_hostpitalize
                [4.5,4.5],
                # time_immunisation
                [10,10],

                # share_hospitalizations                
                [.10,0.001], 
                # share_deaths_symtomatic
                [.10,0.0001],
                # share_deaths_hospitalized
                [.30,0.0001],
                # share_asymptomatic
                [0.5,.5],

                # count_uninfected
                [1600000,6900000],
                # count_infectious
                [10000,30000],
                # count_asymptomatic
                [10000,30000],
                # count_symptomatic
                [2000,7000],
                # count_hostpitalized
                [1450,50],
                # count_immune
                [10000,10000],
                # count_dead
                [130,0],
                
                # infectious_factor_symtomatic,
                [.2,.2],
                # infectious_factor_hospitalized
                [0.01,0.01]
                );
    # End of the full lockdown in days from the beginning of the simulation
    start_full_quarantine=20
    # End of the half lockdown (where no risk people start to move again) in days from the beginning of the simulation
    end_fullquarantine=150
    # End of the forced infection period for people at no risk in days from the beginning of the simulation
    forced_infection_end=330
    # Start of normalized life again in days from the beginning of the simulation
    normal_live_start=400
    # Full Quarantine time.
    for i in range(1,start_full_quarantine):
        sim.nextday()
    
    # Partial Quarantine with people at risk locked away
    sim.R0=np.array([[minimalr0,minimalr0],[minimalr0,2]])
    for i in range(start_full_quarantine,end_fullquarantine):
        sim.nextday()

    # Open Scools and shops, but keep people at risk away.    
    sim.R0=np.array([[minimalr0,minimalr0],[minimalr0,7]])
    for i in range(end_fullquarantine,forced_infection_end):
        sim.nextday()
    
    # Start of getting people at risk back to normal live
    sim.R0=np.array([[.7,.7],[.7,2.5]])
    for i in range(forced_infection_end,normal_live_start):
        sim.nextday()

    
    # This simulates a better methods of cure in hospitals.
    sim.share_deaths_hospitalized[0]=.1     
    # Start of normal live with minor safety precautions of people at risk    
    sim.R0=np.array([[1.5,1.5],[1.5,2.5]])
    for i in range(normal_live_start,1000):
        # This simulates the open boarders and imported infections
        # Hopefully the can be kept as low as this, which means only one person infected is
        # traveling to Switzerland without being caught at the border
        sim.count_infectious=sim.count_infectious+np.array([1/100,1/7])
        sim.nextday()
        
    print("Max Hospitalization %d after %d days"%(sim.max_hospitalisations,sim.max_day))
    
    #Wuhan
    minimalr0=0.01
    normalr0=3.5
    sim=simulator(
                # RO
                [[normalr0,normalr0],[normalr0,normalr0]],
                # time_incubation
                [6.4,6.4],
                # time_recover_symtomatic
                [15,15],
                # time_recover_hospitalized
                [10.5,10.5],
                # time_die_symtpomatic
                [15,15],
                # time_die_hospitalized
                [10.5,10.5],
                # time_hostpitalize
                [4.5,4.5],
                # time_immunisation
                [10,10],
                                
                # share_hospitalizations,                
                [.10,0.001], 
                # share_deaths_symtomatic,
                [.10,0.0001],
                # share_deaths_hospitalized,
                [.30,0.0001],
                # share_asymptomatic,
                [0.5,.5],

                
                # count_uninfected
                [2600000,8000000],
                # count_infectious,
                [200,200],
                # count_asymptomatic,
                [200,200],
                # count_symptomatic,
                [30,30],
                # count_hostpitalized,
                [7,0],
                # count_immune,
                [0,0],
                # count_dead,
                [130,0],
                
                # infectious_factor_symtomatic,
                [.2,.2],
                # infectious_factor_hospitalized
                [0.01,0.01]
                );
    # on Jan 23, 16 days after the start of the simulation the complete shutdown comes
    start_full_quarantine=16
    # on April 8 or 9 the people can start to go out again
    end_fullquarantine=90
    # Travelling to and away from Wuhan is allowed again.
    normal_live_start=120
    for i in range(1,start_full_quarantine):
        sim.nextday()
    
    sim.R0=np.array([[minimalr0,minimalr0],[minimalr0,minimalr0]])
    for i in range(start_full_quarantine,end_fullquarantine):
        sim.nextday()
         
    sim.R0=np.array([[.5,.5],[.5,.5]])
    for i in range(end_fullquarantine,normal_live_start):
        sim.nextday()
    
    sim.R0=np.array([[1.5,1.5],[1.5,2.5]])
    for i in range(normal_live_start,normal_live_start+20):
        # Import of infections start again, due to travelling
        sim.count_infectious=sim.count_infectious+np.array([.2,1])
        sim.nextday()
         
        
    print("Max Hospitalization %d after %d days"%(sim.max_hospitalisations,sim.max_day))
     
    
    
if __name__ == '__main__':
    main()


