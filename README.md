# covid19simulation

##  Intro

This project contains a small simulator for epidemic outbreaks and progress.

### Installation

You first need to install python3. Then install numpy using "pip install numpy". Then do a git clone of the repository.

### Configuration

The simulation is highly configurable. To understand you first need to take a look at the state diagram which is available as a Open Office Doc in the repo.

The configuration of the simulation is done directly in the code so far and provided as an bunch of arrays as parameters of the constructor for the simulator class. 

The parameters are described in the code. 

the parameters can be an array with just one field, if you would like to do the simulation for the whole population with the same params.

If you specify multiple values in each array, these values represent the parameter for one segment of the population, e.g. all elderly people or all people which have a different risk of dieing.

The examples included have parameters defined for a simulation of switzerland and the simulation for the wuhan out break of covid 19 with 2 groups of people defined, the index 0 is for people with high risk of dieing, the index 1, for poeple with low risk of dieing.



