from __future__ import print_function
# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

# Tutorial sample #2: Run simple mission using raw XML

# Added modifications by Norbert BĂĄtfai (nb4tf4i) batfai.norbert@inf.unideb.hu, mine.ly/nb4tf4i.1
# 2018.10.18, https://bhaxor.blog.hu/2018/10/18/malmo_minecraft
# 2020.02.02, NB4tf4i's Red Flowers, http://smartcity.inf.unideb.hu/~norbi/NB4tf4iRedFlowerHell


from builtins import range
import MalmoPython
import os
import sys
import time
import random
import json
import math

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

# Create default Malmo objects:

agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print('ERROR:',e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)

# -- set up the mission -- #
missionXML_file='nb4tf4i_d.xml'
with open(missionXML_file, 'r') as f:
    print("NB4tf4i's Red Flowers (Red Flower Hell) - DEAC-Hackers Battle Royale Arena\n")
    print("NB4tf4i vĂśrĂśs pipacsai (VĂśrĂśs Pipacs Pokol) - DEAC-Hackers Battle Royale Arena\n\n")
    print("The aim of this first challenge, called nb4tf4i's red flowers, is to collect as many red flowers as possible before the lava flows down the hillside.\n")
    print("Ennek az elsĹ, az nb4tf4i vĂśrĂśs virĂĄgai nevĹą kihĂ­vĂĄsnak a cĂŠlja ĂśsszegyĹąjteni annyi piros virĂĄgot, amennyit csak lehet, mielĹtt a lĂĄva lefolyik a hegyoldalon.\n")    
    print("Norbert BĂĄtfai, batfai.norbert@inf.unideb.hu, https://arato.inf.unideb.hu/batfai.norbert/\n\n")    
    print("Loading mission from %s" % missionXML_file)
    mission_xml = f.read()
    my_mission = MalmoPython.MissionSpec(mission_xml, True)
    my_mission.drawBlock( 0, 0, 0, "lava")


class Hourglass:
    def __init__(self, charSet):
        self.charSet = charSet
        self.index = 0
    def cursor(self):
        self.index=(self.index+1)%len(self.charSet)
        return self.charSet[self.index]

hg = Hourglass('|/-\|')

class Steve:
    def __init__(self, agent_host):
        self.agent_host = agent_host
        
        self.x = 0
        self.y = 0
        self.z = 0
        self.yaw = 0
        self.pitch = 0
        
        self.front_of_me_idx = 0
        self.front_of_me_idxr = 0
        self.front_of_me_idxl = 0        
        self.right_of_me_idx = 0
        self.left_of_me_idx = 0        
        
        self.nof_red_flower = 0
        self.lookingat = ""
        self.attackLvl = 0
        
        self.collectedFlowers = {}
        for i in range(100):
            self.collectedFlowers[i] = False

        self.collectedFlowers[1] = True
        self.collectedFlowers[2] = True

    def felfut(self):
        for x in range(0, 28):
            self.agent_host.sendCommand( "move 1" )
            self.agent_host.sendCommand( "jumpmove 1" )
            time.sleep(.05)
        self.agent_host.sendCommand( "turn 1" )
    def virag(self,sarok):    
        print("PIPACS")
        self.agent_host.sendCommand( "look 1" )
        time.sleep(0.1)
        self.agent_host.sendCommand( "attack 1" )
        self.nof_red_flower+=1
        time.sleep(0.5)
        self.agent_host.sendCommand( "look -1" )
        time.sleep(.1)
        if sarok>2:
            self.agent_host.sendCommand( "jumpmove -1" )
            time.sleep(.1)
            self.agent_host.sendCommand( "jumpmove -1" )
        else:
            self.agent_host.sendCommand( "jumpmove 1" )
            time.sleep(.1)
            self.agent_host.sendCommand( "jumpmove 1" )
        time.sleep(.1)
        self.agent_host.sendCommand( "jumpstrafe 1" )
        time.sleep(.1)
        self.agent_host.sendCommand( "strafe 1" )
    
    def whatMyPos(self, observations):
        if "Yaw" in observations:
            self.yaw = int(observations["Yaw"])
        if "Pitch" in observations:
            self.pitch = int(observations["Pitch"])
        if "XPos" in observations:
            self.x = int(observations["XPos"])
        if "ZPos" in observations:
            self.z = int(observations["ZPos"])        
        if "YPos" in observations:
            self.y = int(observations["YPos"])        
    
    def calcNbrIndex(self):
        if self.yaw >= 180-22.5 and self.yaw <= 180+22.5 :
            self.front_of_me_idx = 1
            self.front_of_me_idxr = 2
            self.front_of_me_idxl = 0
            self.right_of_me_idx = 5
            self.left_of_me_idx = 3            
        elif self.yaw >= 180+22.5 and self.yaw <= 270-22.5 :
            self.front_of_me_idx = 2 
            self.front_of_me_idxr = 5
            self.front_of_me_idxl =1             
            self.right_of_me_idx = 8
            self.left_of_me_idx = 0            
        elif self.yaw >= 270-22.5 and self.yaw <= 270+22.5 :
            self.front_of_me_idx = 5
            self.front_of_me_idxr = 8
            self.front_of_me_idxl = 2
            self.right_of_me_idx = 7
            self.left_of_me_idx = 1                        
        elif self.yaw >= 270+22.5 and self.yaw <= 360-22.5 :
            self.front_of_me_idx = 8            
            self.front_of_me_idxr = 7
            self.front_of_me_idxl = 5          
            self.right_of_me_idx = 6
            self.left_of_me_idx = 2                        
        elif self.yaw >= 360-22.5 or self.yaw <= 0+22.5 :
            self.front_of_me_idx = 7
            self.front_of_me_idxr = 6
            self.front_of_me_idxl = 8
            self.right_of_me_idx = 3
            self.left_of_me_idx = 5                        
        elif self.yaw >= 0+22.5 and self.yaw <= 90-22.5 :
            self.front_of_me_idx = 6
            self.front_of_me_idxr = 3
            self.front_of_me_idxl = 7          
            self.right_of_me_idx = 0
            self.left_of_me_idx = 8                        
        elif self.yaw >= 90-22.5 and self.yaw <= 90+22.5 :
            self.front_of_me_idx = 3
            self.front_of_me_idxr = 0
            self.front_of_me_idxl = 6
            self.right_of_me_idx = 1
            self.left_of_me_idx = 7                        
        elif self.yaw >= 90+22.5 and self.yaw <= 180-22.5 :
            self.front_of_me_idx = 0
            self.front_of_me_idxr = 1
            self.front_of_me_idxl = 3
            self.right_of_me_idx = 2
            self.left_of_me_idx = 6                        
        else:
            print("There is great disturbance in the Force...")  
    
    def run(self):
        world_state = self.agent_host.getWorldState()
        # Loop until mission ends:
        self.agent_host.sendCommand( "look 1" )
        self.agent_host.sendCommand( "strafe -1" )
        self.agent_host.sendCommand( "strafe -1" )
        self.agent_host.sendCommand( "strafe -1" )
        self.agent_host.sendCommand( "strafe -1" )
        self.agent_host.sendCommand( "strafe -1" )
        felfut=0
        sarok=0
        ketvirag=0
        muszaj18_23=0
        lementett_x=50
        lementett_y=50
        lementett_z=50
        while world_state.is_mission_running:
            #print("---------------------\n")
            world_state = self.agent_host.getWorldState()
            if world_state.number_of_observations_since_last_state != 0:
                
                sensations = world_state.observations[-1].text           
                observations = json.loads(sensations)
                nbr3x3x3 = observations.get("nbr3x3", 0)
                self.calcNbrIndex()  
                self.whatMyPos(observations)
                print("Koordináták: ", self.x, self.y, self.z, end='\n')
                if felfut==0:
                    self.felfut()
                    felfut=1
                    time.sleep(1)
                
                if felfut==1:
                    if (nbr3x3x3[self.front_of_me_idx+9]=="dirt"):
                        print("FORDUL\n")
                        self.agent_host.sendCommand( "move -1" )
                        time.sleep(0.1)
                        self.agent_host.sendCommand( "turn 1" )
                        time.sleep(0.1)
                        self.agent_host.sendCommand( "move -1" )
                        time.sleep(0.1)
                        sarok=0
                    
                    if (nbr3x3x3[self.front_of_me_idxl+9]=="red_flower" or nbr3x3x3[self.front_of_me_idxl+18]=="red_flower"):
                        print("PIPACS\n")
                        self.agent_host.sendCommand( "strafe -1" )
                        time.sleep(0.1)
                        self.agent_host.sendCommand( "move 1" )
                        time.sleep(0.1)
                        self.agent_host.sendCommand( "look 1" )
                        time.sleep(0.1)
                        self.agent_host.sendCommand( "attack 1" )
                        self.nof_red_flower+=1
                        time.sleep(0.5)
                        self.agent_host.sendCommand( "look -1" )
                        time.sleep(.1)
                        if sarok>2:
                            self.agent_host.sendCommand( "jumpmove -1" )
                            time.sleep(.1)
                            self.agent_host.sendCommand( "jumpmove -1" )
                            time.sleep(.1)
                        else:
                            self.agent_host.sendCommand( "jumpmove 1" )
                            time.sleep(.1)
                            self.agent_host.sendCommand( "jumpmove 1" )
                            time.sleep(.1)
                        self.agent_host.sendCommand( "strafe 1" )
                        time.sleep(.1)
                        self.agent_host.sendCommand( "strafe 1" )
                        time.sleep(.1)
                        if ketvirag>=1:
                            print("Kétszer JOBBRA\n")
                            self.agent_host.sendCommand( "strafe 1" )
                            self.agent_host.sendCommand( "strafe 1" )
                            time.sleep(.1)
                            ketvirag=0
                        print("BAL OLDALI PIPA\n")
                        
                    elif (nbr3x3x3[self.front_of_me_idxr]=="red_flower" or nbr3x3x3[self.front_of_me_idxr+9]=="red_flower"):
                        print("PIPACS\n")
                        self.agent_host.sendCommand( "strafe 1" )
                        time.sleep(0.1)
                        self.agent_host.sendCommand( "move 1" )
                        time.sleep(0.1)
                        self.agent_host.sendCommand( "look 1" )
                        time.sleep(0.1)
                        self.agent_host.sendCommand( "attack 1" )
                        self.nof_red_flower+=1
                        time.sleep(0.5)
                        self.agent_host.sendCommand( "look -1" )
                        time.sleep(.1)
                        if sarok>2:
                            self.agent_host.sendCommand( "jumpmove -1" )
                            time.sleep(.1)
                            self.agent_host.sendCommand( "jumpmove -1" )
                            time.sleep(.1)
                        else:
                            self.agent_host.sendCommand( "jumpmove 1" )
                            time.sleep(.1)
                            self.agent_host.sendCommand( "jumpmove 1" )
                            time.sleep(.1)
                        print("JOBB OLDALI PIPA\n")
                        self.agent_host.sendCommand( "jumpstrafe -1" )
                        time.sleep(0.1)
                        self.agent_host.sendCommand( "jumpstrafe -1" )
                        time.sleep(0.1)
                        ketvirag+=1
                    else:
                        self.whatMyPos(observations)
                        self.calcNbrIndex()  
                        if (self.x!=lementett_x or self.y!=lementett_y or self.z!=lementett_z):
                            self.agent_host.sendCommand( "move 1" )
                            time.sleep(0.1)
                            muszaj18_23+=1
                            if ((self.y==18 or self.y==11) and muszaj18_23>3):
                                print("18v23")
                                self.agent_host.sendCommand( "strafe 1" )
                                time.sleep(.1)
                                muszaj18_23=0 
                            lementett_x=self.x
                            lementett_y=self.y
                            lementett_z=self.z
                            if (nbr3x3x3[self.left_of_me_idx+9]=="dirt"):
                                print("CSÚSZÁS\n")
                                self.agent_host.sendCommand( "strafe 1" )
                                time.sleep(0.1)
                        else:
                            print("lementett_x: ",lementett_x," | lementett_y: ",lementett_y," | lementett_z: ",lementett_z)
                            self.agent_host.sendCommand( "move 1" )
                            time.sleep(0.2)
                            
                        sarok+=1
                        
                
num_repeats = 1
for ii in range(num_repeats):

    my_mission_record = MalmoPython.MissionRecordSpec()

    # Attempt to start a mission:
    max_retries = 6
    for retry in range(max_retries):
        try:
            agent_host.startMission( my_mission, my_mission_record )
            break
        except RuntimeError as e:
            if retry == max_retries - 1:
                print("Error starting mission:", e)
                exit(1)
            else:
                print("Attempting to start the mission:")
                time.sleep(2)

    # Loop until mission starts:
    print("   Waiting for the mission to start ")
    world_state = agent_host.getWorldState()

    while not world_state.has_mission_begun:
        print("\r"+hg.cursor(), end="")
        time.sleep(0.15)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:",error.text)

    print("NB4tf4i Red Flower Hell running\n")
    steve = Steve(agent_host)
    steve.run()
    print("Number of flowers: "+ str(steve.nof_red_flower))

print("Mission ended")
# Mission has ended.
