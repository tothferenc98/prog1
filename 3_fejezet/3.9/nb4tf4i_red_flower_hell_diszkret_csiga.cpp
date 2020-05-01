// --------------------------------------------------------------------------------------------------
//  Copyright (c) 2016 Microsoft Corporation
//  
//  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
//  associated documentation files (the "Software"), to deal in the Software without restriction,
//  including without limitation the rights to use, copy, modify, merge, publish, distribute,
//  sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
//  furnished to do so, subject to the following conditions:
//  
//  The above copyright notice and this permission notice shall be included in all copies or
//  substantial portions of the Software.
//  
//  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
//  NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
//  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
//  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
// --------------------------------------------------------------------------------------------------

// Malmo:
#include <AgentHost.h>
#include <ClientPool.h>
using namespace malmo;

// STL:
#include <cstdlib>
#include <exception>
#include <iostream>
using namespace std;

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/foreach.hpp>

vector<string> GetItems(WorldState world_state,std::stringstream & ss, boost::property_tree::ptree & pt)
{
    vector<string> nbr3x3;

    ss.clear();
    pt.clear();

    ss << world_state.observations.at(0).get()->text;
    boost::property_tree::read_json(ss, pt);
    BOOST_FOREACH(boost::property_tree::ptree::value_type &v, pt.get_child("nbr3x3"))
    {
        assert(v.first.empty());
        nbr3x3.push_back(v.second.data());
    }

    return nbr3x3;
}

int main(int argc, const char **argv)
{
    AgentHost agent_host;

    try
    {
        agent_host.parseArgs(argc, argv);
    }
    catch( const exception& e )
    {
        cout << "ERROR: " << e.what() << endl;
        cout << agent_host.getUsage() << endl;
        return EXIT_SUCCESS;
    }
    if( agent_host.receivedArgument("help") )
    {
        cout << agent_host.getUsage() << endl;
        return EXIT_SUCCESS;
    }

    std::ifstream xmlf{"nb4tf4i_d.xml"};
    std::string xml{std::istreambuf_iterator<char>(xmlf),std::istreambuf_iterator<char>()};
    
    MissionSpec my_mission{xml, true};

    MissionRecordSpec my_mission_record("./saved_data.tgz");

    int attempts = 0;
    bool connected = false;
    do {
        try {
            agent_host.startMission(my_mission, my_mission_record);
            connected = true;
        }
        catch (exception& e) {
            cout << "Error starting mission: " << e.what() << endl;
            attempts += 1;
            if (attempts >= 3)
                return EXIT_FAILURE;    // Give up after three attempts.
            else
                boost::this_thread::sleep(boost::posix_time::milliseconds(1000));   // Wait a second and try again.
        }
    } while (!connected);

    WorldState world_state;

    cout << "Waiting for the mission to start" << flush;
    do {
        cout << "." << flush;
        boost::this_thread::sleep(boost::posix_time::milliseconds(100));
        world_state = agent_host.getWorldState();
        for( boost::shared_ptr<TimestampedString> error : world_state.errors )
            cout << "Error: " << error->text << endl;
    } while (!world_state.has_mission_begun);
    cout << endl;
    
    
    int blokk=9;
    int oldal=0;
    
    agent_host.sendCommand( "move -1" );
    boost::this_thread::sleep(boost::posix_time::milliseconds(50));
    agent_host.sendCommand( "move -1" );
    boost::this_thread::sleep(boost::posix_time::milliseconds(50));
    agent_host.sendCommand( "move -1" );
    boost::this_thread::sleep(boost::posix_time::milliseconds(50));
    agent_host.sendCommand( "jumpstrafe -1" );
    boost::this_thread::sleep(boost::posix_time::milliseconds(50));
    agent_host.sendCommand( "jumpstrafe -1" );
    boost::this_thread::sleep(boost::posix_time::milliseconds(50));
    agent_host.sendCommand( "jumpstrafe -1" );
    boost::this_thread::sleep(boost::posix_time::milliseconds(50));
    agent_host.sendCommand( "jumpstrafe -1" );
    boost::this_thread::sleep(boost::posix_time::milliseconds(50));
    agent_host.sendCommand( "jumpstrafe -1" );
    boost::this_thread::sleep(boost::posix_time::milliseconds(50));
    agent_host.sendCommand( "look 1" );
    
    // main loop:
    do {
        
        for(int i = 0; i< blokk; i++)
        {
            agent_host.sendCommand( "move 1" );
            boost::this_thread::sleep(boost::posix_time::milliseconds(100));
            if(i==1)
                cout << "Megy előre" << endl;
        }
        
        if(oldal%4==0)
        {
            blokk+=4;
            agent_host.sendCommand("jumpmove 1");
            cout << "Ugrás" << endl;
            boost::this_thread::sleep(boost::posix_time::milliseconds(100));
            agent_host.sendCommand( "move 1" );
            boost::this_thread::sleep(boost::posix_time::milliseconds(20));
            agent_host.sendCommand( "move 1" );
            boost::this_thread::sleep(boost::posix_time::milliseconds(20));
        }
        
        agent_host.sendCommand("turn 1");
        cout << "Fordul" << endl;
        boost::this_thread::sleep(boost::posix_time::milliseconds(100));
        oldal+=1;
        
        
        world_state = agent_host.getWorldState();
        for( boost::shared_ptr<TimestampedReward> reward : world_state.rewards )
            cout << "Summed reward: " << reward->getValue() << endl;
        for( boost::shared_ptr<TimestampedString> error : world_state.errors )
            cout << "Error: " << error->text << endl;
    } while (world_state.is_mission_running);

    cout << "Mission has stopped." << endl;

    return EXIT_SUCCESS;
}
