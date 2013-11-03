import random
import time
import math
import pylab as pl

from grid import Grid

# simulated annealing algorithm
class SimulatedAnnealing:

    # tau: agitation factor (the higher the warmer and the more agitation)
    # grid: a grid object initialized previously
    # equilibrium: parameters used to decide if we reached thermodynamic equilibrium
    # diminish: factor by which we're going to decrease temperature every iteration
    # init: how many iterations to use for first initialization
    def __init__(self, tau, grid, equilibrium=[12, 100], diminish=0.9, init=100, color='blue'):
        self.tau = tau;
        self.grid = grid; 
        self.init = init;
        self.decision = self.grid.horizontal*self.grid.vertical*2;
        self.equilibre = equilibrium;
        self.diminish = diminish
        self.color = color;
            
    # initial temperature based on the value of the agitation factor
    def initialTemp(self):
        deltae = [];
        curenergie = self.grid.objective;
        
        for i in range(self.init):
            rd1 = random.randint(1, len(self.grid.tiles)+1);
            rd2 = random.randint(1, len(self.grid.tiles)+1);
            while (rd2 == rd1):
                rd2 = random.randint(1, len(self.grid.tiles)+1);
            
            self.grid.move(rd1, rd2);
            
            deltae.append(abs(self.grid.objective - curenergie));
            
            self.grid.move(rd1, rd2);
            
        mean = pl.mean(deltae);
        
        self.temp = mean * (-1) / math.log(self.tau)
        
    # main loop of the simulated annealing algorithm
    def run(self, verbose, analyze):
        # initialize temperature
        self.initialTemp();
        
        cptpa = 0;
        cptpt = 0;
        spy = 0;
        
        curTime = time.time();
        plotE = [];
        plotT = [];
        plotTemp = [];
        
        cptiter = 0;
        
        histogram = [0, 0];
        
        # display the initial grid if allowed
        if verbose >= 1:
            self.grid.displayGrid(self.temp, cptiter, self.tau, self.equilibre[0], self.equilibre[1]);
        
        # main loop
        while 1:
            plotE.append(self.grid.objective);
            plotT.append(time.time() - curTime);
            plotTemp.append(self.temp);
            
            # generate 2 random numbers representing perturbation
            rd1 = random.randint(1, len(self.grid.tiles)+1);
            rd2 = random.randint(1, len(self.grid.tiles)+1);
            while (rd2 == rd1):
                rd2 = random.randint(1, len(self.grid.tiles)+1);
            
            # energy before perturbation
            curenergie = self.grid.objective;
            
            # transition to the next state
            self.grid.move(rd1, rd2);
            
            # energy after perturbation
            perturbenergie = self.grid.objective;
            
            # if energy variation is less than or equal to 0
            if perturbenergie <= curenergie:
                if perturbenergie != curenergie:
                    
                    cptpa += 1;
                    cptpt += 1;
                    spy += 1;
                    
                    # if we reached equilibrium state
                    if cptpa >= self.equilibre[0]*self.decision or cptpt >= self.equilibre[1]*self.decision:
                        
                        cptpa = 0;
                        cptpt = 0;
                        
                        # if the system is frozen
                        if histogram[1] == spy and histogram[0] >= 3:
                            break;
                        
                        else:
                            cptiter += 1;
                            if verbose >= 2:
                                self.grid.displayGrid(self.temp, cptiter, self.tau, self.equilibre[0], self.equilibre[1]);
                            print 'Iteration ' + str(cptiter) + ' : ' + str(histogram[1]) + ' vs ' + str(spy)
                            
                            if histogram[1] == spy:
                                histogram[0] += 1;
                            else:
                                histogram[0] = 1;
                                histogram[1] = spy;
                                
                            # decrease temperature based on the coefficient
                            self.temp = self.diminish*self.temp;

            # if energy variation is postivie
            else:
                # get a random uniform number to check if acceptation probability is verified
                rd = random.uniform(0, 1);
                
                # if acceptation realized
                if rd <= math.exp(-(perturbenergie - curenergie) / self.temp):

                    cptpa += 1;
                    cptpt += 1;
                    spy += 1;

                    # check if we are at the thermodynamic equilibrium
                    if cptpa >= self.equilibre[0]*self.decision or cptpt >= self.equilibre[1]*self.decision:
                        cptpa = 0;
                        cptpt = 0;
                        if histogram[1] == spy and histogram[0] >= 3:
                            break;
                        else:
                            cptiter += 1;
                            if verbose >= 2:
                                self.grid.displayGrid(self.temp, cptiter, self.tau, self.equilibre[0], self.equilibre[1]);
                            print 'Iteration ' + str(cptiter) + ' : ' + str(histogram[1]) + ' vs ' + str(spy)
                            if histogram[1] == spy:
                                histogram[0] += 1;
                            else:
                                histogram[0] = 1;
                                histogram[1] = spy;
                            self.temp = self.diminish*self.temp;

                # if acceptation not realized
                else:
                    cptpt += 1;
                    
                    # do the opposite move since it was not accepted
                    self.grid.move(rd1, rd2);
                    
                    # check if we are at the thermodynamic equilibrium
                    if cptpa >= self.equilibre[0]*self.decision or cptpt >= self.equilibre[1]*self.decision:
                        cptpa = 0;
                        cptpt = 0;
                        if histogram[1] == spy and histogram[0] >= 3:
                            break;
                        else:
                            cptiter += 1;
                            if verbose >= 2:
                                self.grid.displayGrid(self.temp, cptiter, self.tau, self.equilibre[0], self.equilibre[1]);
                            print 'Iteration ' + str(cptiter) + ' : ' + str(histogram[1]) + ' vs ' + str(spy)
                            if histogram[1] == spy:
                                histogram[0] += 1;
                            else:
                                histogram[0] = 1;
                                histogram[1] = spy;
                            self.temp = self.diminish*self.temp;
            
                
        # simulated annealing has converged
        print 'Simulated Annealing has converged : objective=' + str(self.grid.objective)
        self.cptpalier = cptiter;
        
        if analyze:
            self.plots = pl.plot(plotT, plotE, color=self.color);
            
        # print final grid
        if verbose >= 1:
            self.grid.displayGrid(self.temp, cptiter, self.tau, self.equilibre[0], self.equilibre[1]);