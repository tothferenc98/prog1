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

# Added modifications by Norbert Bátfai (nb4tf4i) batfai.norbert@inf.unideb.hu, mine.ly/nb4tf4i.1
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
        blokk=9
        oldal=0
        self.agent_host.sendCommand( "move -1" )
        time.sleep(0.05)
        self.agent_host.sendCommand( "move -1" )
        time.sleep(0.05)
        self.agent_host.sendCommand( "jumpstrafe -1" )
        time.sleep(0.05)
        self.agent_host.sendCommand( "jumpstrafe -1" )
        time.sleep(0.05)
        self.agent_host.sendCommand( "jumpstrafe -1" )
        time.sleep(0.05)
        self.agent_host.sendCommand( "jumpstrafe -1" )
        time.sleep(0.05)
        self.agent_host.sendCommand( "jumpstrafe -1" )
        time.sleep(0.05)
        self.agent_host.sendCommand( "look 1" )
        
        while world_state.is_mission_running:
            print("--- nb4tf4i arena -----------------------------------\n")
            for x in range(0, blokk):
                self.agent_host.sendCommand( "move 1" )
                time.sleep(0.1)
                print("Előre\n")
            
            
            if oldal%4==0:
                blokk+=4
                agent_host.sendCommand("jumpmove 1")
                print("Fel\n")
                time.sleep(0.1)
                for x in range(0, 2):
                    self.agent_host.sendCommand( "move 1" )
                    print("+2\n")
                    time.sleep(0.1)
            agent_host.sendCommand("turn 1")
            print("FORDUL\n")
            oldal+=1








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
