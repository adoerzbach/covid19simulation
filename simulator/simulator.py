'''
Created on 20 Mar 2020

@author: ado
'''

import numpy as np
import datetime
import json

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
                 infectious_factor_hospitalized,
                 simulation_startdate
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
        simulation_startdate: datetime object for the start of the simulation
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
        self.simulation_startdate=simulation_startdate;
        self.total_reported_cases = self.count_symptomatic + self.count_hostpitalized
        self.result=dict()
        
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
        self.result[self.day]=self.todict()

        
    def nextday(self):
        self.nextday_silent()
        outformat = ('{"Day":%s,"Infections":%s,"Deaths":%s,"Hospitalizations":%s,"Healed from Hospital":%s,Total Deaths":%s,"Total Infectious People":%s,' + 
                   '"Total Immune People":%s,"Total hospitalized People":%s,"Total Symptomatic People":%s' + 
                   '"Total Asymptomatic People":%s,"Total Unifected People":%s,"Total Population":%s}'
                   )
        print(outformat % ((self.simulation_startdate+datetime.timedelta(days=self.day)).strftime("%x"),
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
        
    def nextday_json(self):
        self.nextday_silent()
        print(self.tojson())
        
    def tojson(self):
        return json.dumps(self.todict())
    
    def todict(self):
        return {
             "Day": (self.simulation_startdate+datetime.timedelta(days=self.day)).strftime("%x"),
             "R0":self.R0.tolist(),
             "time_incubation":self.time_incubation.tolist(),
             "time_recover_symtomatic":self.time_recover_symtomatic.tolist(),
             "time_recover_hospitalized":self.time_recover_hospitalized.tolist(),
             "time_die_symtpomatic":self.time_die_symtpomatic.tolist(),
             "time_die_hospitalized":self.time_die_hospitalized.tolist(),
             "time_hostpitalize":self.time_hostpitalize.tolist(),
             "time_immunisation":self.time_immunisation.tolist(),
             "share_hospitalizations":self.share_hospitalizations.tolist(),
             "share_deaths_symtomatic":self.share_deaths_symtomatic.tolist(),
             "share_deaths_hospitalized":self.share_deaths_hospitalized.tolist(),
             "share_asymptomatic":self.share_asymptomatic.tolist(),
             "count_uninfected":self.count_uninfected.tolist(),
             "count_infectious":self.count_infectious.tolist(),
             "count_asymptomatic":self.count_asymptomatic.tolist(),
             "count_symptomatic":self.count_symptomatic.tolist(),
             "count_hostpitalized":self.count_hostpitalized.tolist(),
             "count_immune":self.count_immune.tolist(),
             "count_dead":self.count_dead.tolist(),
             "infectious_factor_symtomatic":self.infectious_factor_symtomatic.tolist(),
             "infectious_factor_hostpitalized":self.infectious_factor_hostpitalized.tolist(),
             "stay_healthies":self.stay_healthies.tolist(),
             "immunized":self.immunized.tolist(),
             "total_reported_cases":self.total_reported_cases .tolist(),
             "fall_ills":self.fall_ills.tolist()
        }
    def tocsv(self,columns):
        line="Day,"
        for c in columns:
            line=line+"%s,"%c
        print(line)    
        
        for k in self.result:
            line="%s,"%(self.simulation_startdate+datetime.timedelta(days=k)).strftime("%x")
            for c in columns:
                line=line+"%s,"%sum(self.result[k][c])   
            print(line)
                
       