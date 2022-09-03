#Code to run the simulation

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from Body import Body
#Creates a class which handles all of the simulating
class Simulation(object):
    #Method to initialise and set the required variables
    def __init__(self):
        filename = str(input("Please input the name of the file which contains the solar system data: "))
        self.dt = float(input("Please input the timestep for the simulation in seconds: "))
        self.bodyList = []
        self.CoMPositionsx = np.array([])
        self.CoMPositionsy = np.array([])
        self.T = 0.0
        #Creates a list of "Body" objects which represent the planets, reading in their details from a file
        filein = open(filename, "r")
        for line in filein.readlines():
            tokens = line.split(", ")
            self.bodyList.append(Body(str(tokens[0]), float(tokens[1]), float(tokens[2]), str(tokens[3]), float(tokens[4]), float(tokens[5]), float(tokens[6]), float(tokens[7])))
        filein.close()
        #Opens a file which will be used to write the total energy to
        self.fileout = open("energy.txt","w")
    #Method to move each body, updating each variable in lock-step across the whole simualtion
    def move(self):
        #These changes to the code shift the simulation such that it is in the frame of reference of the centre of mass of the whole system, the position of which is constant over time
        CoM_Position = self.getCoM()
        for i in range(len(self.bodyList)):
            self.bodyList[i].setPos(self.dt, self.T, CoM_Position)
        for i in range(len(self.bodyList)):
            self.bodyList[i].setAcc(self.bodyList)
        for i in range(len(self.bodyList)):
            self.bodyList[i].setVel(self.dt)

        for i in range(len(self.bodyList)):
            self.bodyList[i].stepForward()
    #Method to animate the bodies
    def animate(self, i):
        self.move()
        self.T = (self.T + self.dt)
        temp2 = (self.getCoM())
        self.CoMPositionsx = np.append(self.CoMPositionsx, temp2[0])
        self.CoMPositionsy = np.append(self.CoMPositionsy, temp2[1])
        temp = (self.getTE())
        #Writes time and total energy to a file
        self.fileout = open("energy.txt", "w")
        self.fileout.write(str(self.T/86400) + ", " + str(temp) + "\n")            
        #Updates the patches
        for i in range(len(self.bodyList)):
            self.patches[i].center = (self.bodyList[i].p[0], self.bodyList[i].p[1])

        return(self.patches)
    #Method to display the animation, using "on the fly" style animating
    def dispAnim(self):
        #Creates the figure which the animation will happen on
        self.figure = plt.figure()
        self.axes = plt.axes()
        self.axes.axis('scaled')
        self.axes.set_xlim(-float(3e9), float(3e9))
        self.axes.set_ylim(-float(3e9), float(3e9))
        self.axes.set_xlabel("x / m")
        self.axes.set_ylabel("y / m")

        self.patches = []
        #Adds circles to the figure to represent each body, makes sure that they are the right size so they can all be seen
        for i in range(len(self.bodyList)):
            if self.bodyList[i].name == "Sun":
                self.patches.append(plt.Circle((self.bodyList[i].p[0], self.bodyList[i].p[1]), 10.0 * self.bodyList[i].r, color = self.bodyList[i].colour, animated = True))
            else:
                self.patches.append(plt.Circle((self.bodyList[i].p[0], self.bodyList[i].p[1]), 10.0 * self.bodyList[i].r, color = self.bodyList[i].colour, animated = True))
                
        for i in range(0, len(self.patches)):
            self.axes.add_patch(self.patches[i])
        #The actual animation, done using FuncAnimation
        self.animation = FuncAnimation(self.figure, self.animate, frames = 2500, repeat = True, interval = 20, blit = True)
                                
        plt.show()
    #Small method to calculate the total energy of the system
    def getTE(self):
        TE = 0.0
        for i in range(len(self.bodyList)):
            t = self.bodyList[i].getKE() + (0.5 * self.bodyList[i].getGPE(self.bodyList))
            TE = TE + t
        return(TE)

    #Method to calculate the centre of mass of the system
    def getCoM(self):
        #Calculate the total mass of the system
        total_mass = 0.0
        for i in range(len(self.bodyList)):
            dm = self.bodyList[i].m
            total_mass = total_mass + dm

        CoM_r = np.array([0.0, 0.0])
        for i in range(len(self.bodyList)):
            dr = (self.bodyList[i].m) * (self.bodyList[i].p)
            CoM_r = CoM_r + dr

        CoM_r = CoM_r / total_mass
        return(CoM_r)

    #Method to plot graphs of the centre of mass position over time
    def CoMGraphs(self):
        time_steps = len(self.CoMPositionsx)
        print(time_steps)
        time_array = np.arange(time_steps)

        plt.plot(time_array, self.CoMPositionsx, "g")
        plt.title("Graph of the x-coordinate of the centre of mass over time")
        plt.xlabel("Time")
        plt.ylabel("x-coordinate")
        plt.show()

        plt.plot(time_array, self.CoMPositionsy, "g")
        plt.title("Graph of the y-coordinate of the centre of mass over time")
        plt.xlabel("Time")
        plt.ylabel("y-coordinate")
        plt.show()
    
    #Method to plot a graph of the total energy against time
    def eGraph(self):
        tData = []
        EData = []
        filein = open("energy.txt", "r")
        for line in filein.readlines()[1:]:
            tokens = line.split(", ")
            tData.append(tokens[0])
            EData.append(tokens[1])
        filein.close()

        plt.plot(tData,EData,"g")
        plt.title("Graph of Total System Energy vs Time")
        plt.xlabel("Time / Earth Days")
        plt.ylabel("Energy / J")
        plt.show()
#Main method to execute and control everything
def main():
    sim = Simulation()
    sim.dispAnim()
    sim.fileout.close()
    #sim.CoMGraphs()
    #sim.eGraph()

main()


