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
        
        self.nof_red_flower = 0

    def run(self):
        world_state = self.agent_host.getWorldState()
        # Loop until mission ends:
        self.agent_host.sendCommand( "jumpstrafe 1" )
        tomb=0
        tomb2=0
        felfut=0
        oldal=0
        while world_state.is_mission_running:
            world_state = self.agent_host.getWorldState()
            valtakozva=0
            lava=0
            
            if world_state.number_of_observations_since_last_state != 0:
                sensations = world_state.observations[-1].text
                #print("    sensations: ", sensations)                
                observations = json.loads(sensations)
                nbr3x3x3 = observations.get("nbr3x3", 0)
                #print("    3x3x3 neighborhood of Steve: ", nbr3x3x3)
                valtakozva+=1
                print('_____')
                while tomb < len(nbr3x3x3):
                    print(tomb,': ',nbr3x3x3[tomb])
                    if ((nbr3x3x3[tomb] == "flowing_lava" or nbr3x3x3[tomb] == "lava") and felfut==0):
                        print("LÁVA")
                        lava=1
                        self.agent_host.sendCommand( "move -1" )
                        felfut=1
                    tomb+=1
                    
                tomb=0
                if valtakozva%2==0 and lava==0 and felfut ==0:
                    self.agent_host.sendCommand( "move 1" )
                if valtakozva%2==1 and lava==0 and felfut ==0:
                    self.agent_host.sendCommand( "jumpmove 1" )
                    
                time.sleep(0.5)
                sensations = world_state.observations[-1].text  
                if felfut==1:
                    self.agent_host.sendCommand( "turn 1" )
                    self.agent_host.sendCommand( "move 1" )
                    felfut+=1
                    
                lava2=0
                
                
                if (felfut>=2):
                    while tomb2 < len(nbr3x3x3):
                        world_state = self.agent_host.getWorldState()
                        if (nbr3x3x3[tomb2] == "flowing_lava" or nbr3x3x3[tomb2] == "lava"):
                            lava2=1
                            
                        tomb2+=1
                    tomb2=0
                    
                    if lava2==1:
                        print("LÁVAAAA____________________________________________")
                        self.agent_host.sendCommand( "jumpstrafe 1" )
                        self.agent_host.sendCommand( "move -1" ) 
                        if ((oldal==0 and nbr3x3x3[9] == "air" and nbr3x3x3[12] == "air" and nbr3x3x3[15] == "air" and nbr3x3x3[2] == "air" and nbr3x3x3[5] == "air" and nbr3x3x3[8] == "air") or (oldal==1 and nbr3x3x3[9] == "air" and nbr3x3x3[10] == "air" and nbr3x3x3[11] == "air" and nbr3x3x3[6] == "air" and nbr3x3x3[7] == "air" and nbr3x3x3[8] == "air") or (oldal==2 and nbr3x3x3[11] == "air" and nbr3x3x3[14] == "air" and nbr3x3x3[17] == "air" and nbr3x3x3[0] == "air" and nbr3x3x3[3] == "air" and nbr3x3x3[6] == "air") or (oldal==3 and nbr3x3x3[15] == "air" and nbr3x3x3[16] == "air" and nbr3x3x3[17] == "air" and nbr3x3x3[0] == "air" and nbr3x3x3[1] == "air" and nbr3x3x3[2] == "air")):
                            self.agent_host.sendCommand( "jumpstrafe 1" )
                            self.agent_host.sendCommand( "jumpstrafe 1" )
                            world_state = self.agent_host.getWorldState()
                            time.sleep(0.2)
                    
                       
                        
                    else:
                        world_state = self.agent_host.getWorldState()
                        if ((nbr3x3x3[9] == "dirt" and nbr3x3x3[12] == "dirt" and nbr3x3x3[15] == "dirt" and nbr3x3x3[10] == "dirt" and nbr3x3x3[11] == "dirt")  or  (nbr3x3x3[9] == "dirt" and nbr3x3x3[10] == "dirt" and nbr3x3x3[11] == "dirt" and nbr3x3x3[14] == "dirt" and nbr3x3x3[17] == "dirt") or (nbr3x3x3[11] == "dirt" and nbr3x3x3[14] == "dirt" and nbr3x3x3[15] == "dirt" and nbr3x3x3[16] == "dirt" and nbr3x3x3[17] == "dirt") or (nbr3x3x3[9] == "dirt" and nbr3x3x3[12] == "dirt" and nbr3x3x3[15] == "dirt" and nbr3x3x3[16] == "dirt" and nbr3x3x3[17] == "dirt")) :
                            self.agent_host.sendCommand( "jumpstrafe 1" )
                            self.agent_host.sendCommand( "move -1" )
                            self.agent_host.sendCommand( "turn 1" )
                            time.sleep(0.1)
                            if oldal==3:
                                oldal=-1
                            oldal+=1
                            print("LEFUT   ############################################     ",oldal, ". oldal")
                        else:
                            world_state = self.agent_host.getWorldState()
                            if oldal==0:
                                self.agent_host.sendCommand( "movenorth 1" )
                            if oldal>=1:
                                self.agent_host.sendCommand( "move 1" )
                            time.sleep(0.2)
                        
                        
                    
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