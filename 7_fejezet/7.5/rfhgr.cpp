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

    // main loop:
    agent_host.sendCommand("look 1");
    agent_host.sendCommand("look 1");
    
    int db=0;
    int y2=0;
    double yaw=0;
    bool felfele=true;
    bool elsofordul=false;
    int dbf=0;
    int fordul=0;
    int dblep =0;
    bool viragvalahol=false;
    double front_of_me_idx = 0;
    double front_of_me_idxr = 0;
    double front_of_me_idxl = 0 ;       
    double right_of_me_idx = 0;
    double left_of_me_idx = 0  ;  
    int viraghatra=0;
    
    
    do {
        
        
        //agent_host.sendCommand("move 1");
        //boost::this_thread::sleep(boost::posix_time::milliseconds(500));
        
        for(std::vector<boost::shared_ptr<TimestampedString>>::iterator it=world_state.observations.begin(); it!=world_state.observations.end(); ++it)
        {
            
            
            //std::cout << (*it)->text << std::endl;
            boost::property_tree::ptree pt2;
            std::istringstream iss((*it)->text);

            
            boost::property_tree::read_json(iss, pt2);
            std::string x = pt2.get<std::string>("XPos");
            std::string y = pt2.get<std::string>("YPos");
            y2=stoi(pt2.get<std::string>("YPos"));
            std::string z = pt2.get<std::string>("ZPos");
            //std::string yaw = pt2.get<std::string>("Yaw");
            yaw=stod(pt2.get<std::string>("Yaw"));
            std::string pitch = pt2.get<std::string>("Pitch");
            /*
            std::cout << " x = " << x << std::endl;
            std::cout << " y = " << y << std::endl;
            std::cout << " z = " << z << std::endl;
            std::cout << " yaw = " << yaw << std::endl;
            std::cout << " pitch = " << pitch << std::endl;
            */
            
            
        if(yaw >= 180-22.5 && yaw <= 180+22.5){
            front_of_me_idx = 1;
            front_of_me_idxr = 2;
            front_of_me_idxl = 0;
            right_of_me_idx = 5;
            left_of_me_idx = 3  ;          
        }
        else if( yaw >= 180+22.5 && yaw <= 270-22.5){
            front_of_me_idx = 2 ;
            front_of_me_idxr = 5;
            front_of_me_idxl =1  ;           
            right_of_me_idx = 8;
            left_of_me_idx = 0  ;          
        }
        else if (yaw >= 270-22.5 && yaw <= 270+22.5){
            front_of_me_idx = 5;
            front_of_me_idxr = 8;
            front_of_me_idxl = 2;
            right_of_me_idx = 7;
            left_of_me_idx = 1  ;                      
        }
        else if (yaw >= 270+22.5 && yaw <= 360-22.5){
            front_of_me_idx = 8  ;          
            front_of_me_idxr = 7;
            front_of_me_idxl = 5 ;         
            right_of_me_idx = 6;
            left_of_me_idx = 2  ;                      
        }
        else if (yaw >= 360-22.5 || yaw <= 0+22.5){
            front_of_me_idx = 7;
            front_of_me_idxr = 6;
            front_of_me_idxl = 8;
            right_of_me_idx = 3;
            left_of_me_idx = 5  ;                      
        }
        else if (yaw >= 0+22.5 && yaw <= 90-22.5) {
            front_of_me_idx = 6;
            front_of_me_idxr = 3;
            front_of_me_idxl = 7 ;         
            right_of_me_idx = 0;
            left_of_me_idx = 8  ;                      
        }
        else if (yaw >= 90-22.5 && yaw <= 90+22.5 ){
            front_of_me_idx = 3;
            front_of_me_idxr = 0;
            front_of_me_idxl = 6;
            right_of_me_idx = 1;
            left_of_me_idx = 7  ;                      
        }
        else if (yaw >= 90+22.5 && yaw <= 180-22.5){
            front_of_me_idx = 0;
            front_of_me_idxr = 1;
            front_of_me_idxl = 3;
            right_of_me_idx = 2;
            left_of_me_idx = 6  ;                      
        }
            
            
            std::stringstream ss;
            ss << world_state.observations.at(0).get()->text;
            boost::property_tree::ptree pt;
            boost::property_tree::read_json(ss, pt);

            vector<std::string> nbr3x3;

            nbr3x3 = GetItems(world_state,ss,pt);
            
            
            for(unsigned int i=0;i<nbr3x3.size();i++)
            {
                if(nbr3x3[i]=="red_flower")
                {
                    viragvalahol=true;
                    //cout <<"VALAHOLVIRAG TRUE " << endl;
                    //if(nbr3x3[10]=="red_flower")
                }
            }
            
            if(viragvalahol==true)
            {
                
                if(nbr3x3[13]=="red_flower"){
                    cout <<"alattam egy virág van " << endl;
                    boost::this_thread::sleep(boost::posix_time::milliseconds(20));
                    agent_host.sendCommand("move -1");
                    agent_host.sendCommand("move -1");
                    boost::this_thread::sleep(boost::posix_time::milliseconds(20));
                    agent_host.sendCommand("attack 1");
                    boost::this_thread::sleep(boost::posix_time::milliseconds(500));
                    agent_host.sendCommand("jumpmove -1");
                    boost::this_thread::sleep(boost::posix_time::milliseconds(20));
                    agent_host.sendCommand("jumpmove -1");
                    boost::this_thread::sleep(boost::posix_time::milliseconds(20));
                    agent_host.sendCommand("jumpmove -1");
                    boost::this_thread::sleep(boost::posix_time::milliseconds(20));
                    agent_host.sendCommand("jumpmove -1");
                    boost::this_thread::sleep(boost::posix_time::milliseconds(20));
                    agent_host.sendCommand("move -1");
                    boost::this_thread::sleep(boost::posix_time::milliseconds(20));
                    agent_host.sendCommand("jumpstrafe 1");
                    boost::this_thread::sleep(boost::posix_time::milliseconds(20));
                    agent_host.sendCommand("jumpstrafe 1");
                    boost::this_thread::sleep(boost::posix_time::milliseconds(20));
                    viragvalahol=false;
                    viraghatra=0;
                }
                else if(nbr3x3[right_of_me_idx+9]=="red_flower"){
                    cout <<"Jobbra egy virág van " << endl;
                    boost::this_thread::sleep(boost::posix_time::milliseconds(20));
                    agent_host.sendCommand("move 1");
                    agent_host.sendCommand("move 1");
                    boost::this_thread::sleep(boost::posix_time::milliseconds(20));
                    agent_host.sendCommand("turn 1");
                    boost::this_thread::sleep(boost::posix_time::milliseconds(20));
                    agent_host.sendCommand("move 1");
                    boost::this_thread::sleep(boost::posix_time::milliseconds(20));
                    agent_host.sendCommand("attack 1");
                    //cout<<"itt kell ütni"<<endl;
                    boost::this_thread::sleep(boost::posix_time::milliseconds(500));
                    agent_host.sendCommand("attack 1");
                    //cout<<"itt is kell ütni"<<endl;
                    boost::this_thread::sleep(boost::posix_time::milliseconds(500));
                    agent_host.sendCommand("jumpmove 1");
                    boost::this_thread::sleep(boost::posix_time::milliseconds(20));
                    boost::this_thread::sleep(boost::posix_time::milliseconds(50));
                    agent_host.sendCommand("jumpstrafe 1");
                    boost::this_thread::sleep(boost::posix_time::milliseconds(20));
                    agent_host.sendCommand("jumpstrafe 1");
                    boost::this_thread::sleep(boost::posix_time::milliseconds(20));
                    viragvalahol=false;
                    viraghatra=0;
                }
                else if(nbr3x3[front_of_me_idx+9]=="red_flower"){
                
                        cout <<"Előttem egy virág van " << endl;
                        boost::this_thread::sleep(boost::posix_time::milliseconds(20));
                        agent_host.sendCommand("move 1");
                        boost::this_thread::sleep(boost::posix_time::milliseconds(20));
                        agent_host.sendCommand("attack 1");
                        boost::this_thread::sleep(boost::posix_time::milliseconds(100));
                        agent_host.sendCommand("move -1");
                        boost::this_thread::sleep(boost::posix_time::milliseconds(500));
                        agent_host.sendCommand("jumpmove -1");
                        boost::this_thread::sleep(boost::posix_time::milliseconds(100));
                        agent_host.sendCommand("jumpmove -1");
                        boost::this_thread::sleep(boost::posix_time::milliseconds(100));
                        agent_host.sendCommand("jumpmove -1");
                        boost::this_thread::sleep(boost::posix_time::milliseconds(100));
                        agent_host.sendCommand("jumpmove -1");
                    
                        boost::this_thread::sleep(boost::posix_time::milliseconds(100));
                        agent_host.sendCommand("jumpstrafe 1");
                        boost::this_thread::sleep(boost::posix_time::milliseconds(100));
                        agent_host.sendCommand("jumpstrafe 1");
                        boost::this_thread::sleep(boost::posix_time::milliseconds(100));
                        viragvalahol=false;
                        viraghatra=0;
                    
                }
               
                
            }
            
            
            
            /*
            cout <<"Előttem:  " << nbr3x3[front_of_me_idx+9] << "  Értéke: "<< front_of_me_idx+9 <<  endl;
            cout <<"Balra előttem:  " << nbr3x3[front_of_me_idxl+9] << "  Értéke: "<< front_of_me_idxl+9 <<  endl;
            cout <<"Jobbra előttem:  " << nbr3x3[front_of_me_idxr+9] << "  Értéke: "<< front_of_me_idxr+9 <<  endl;
            cout <<"Balra:  " << nbr3x3[left_of_me_idx+9] << "  Értéke: "<< left_of_me_idx+9 <<  endl;
            cout <<"Jobbra : " << nbr3x3[right_of_me_idx+9] << "  Értéke: "<< right_of_me_idx+9 <<  endl;
            */
            
            
            if(y2<=29 && elsofordul==false){
                if(y2==29){
                    felfele=false;
                    elsofordul=true;
                    
                }
                agent_host.sendCommand("jumpmove 1");
                boost::this_thread::sleep(boost::posix_time::milliseconds(20));
 
                //agent_host.sendCommand("move 1");
                //boost::this_thread::sleep(boost::posix_time::milliseconds(100));
            }
            if(elsofordul==true && dbf==0){
                agent_host.sendCommand("turn 1");
                boost::this_thread::sleep(boost::posix_time::milliseconds(200));
                dbf+=1;
                elsofordul=false;
            }
		
            if(felfele==false && viragvalahol==false){
                
                agent_host.sendCommand("move 1");
                dblep++;
                boost::this_thread::sleep(boost::posix_time::milliseconds(5));
                if(nbr3x3[front_of_me_idx+9]=="dirt" && nbr3x3[front_of_me_idxl+9]=="dirt"&&dblep>2){
                    //cout <<"FORDULJ " << endl;
                    agent_host.sendCommand("turn 1");
                    fordul=fordul+1;
                    dblep=0;
                    boost::this_thread::sleep(boost::posix_time::milliseconds(100));
                }
                else
                {
                    //cout <<"NEM FORDUL " << endl;
                }
                
                /*
                if(nbr3x3[left_of_me_idx+9]!="dirt")
                {
                    agent_host.sendCommand("strafe -1");
                    boost::this_thread::sleep(boost::posix_time::milliseconds(100));
                    
                }*/
                 
                dblep+=1;
                
                //std::cout << " elöre " <<std::endl;
                if(fordul>=1){
                    //boost::this_thread::sleep(boost::posix_time::milliseconds(200));
                    fordul=0;
                    boost::this_thread::sleep(boost::posix_time::milliseconds(200));
                    
                }
            }
            
            
        }
            
        
        
        //agent_host.sendCommand("turn 1");
        //boost::this_thread::sleep(boost::posix_time::milliseconds(500));
        
        world_state = agent_host.getWorldState();
        
        for( boost::shared_ptr<TimestampedString> error : world_state.errors )
            cout << "Error: " << error->text << endl;
    } while (world_state.is_mission_running);

    cout << "Mission has stopped." << endl;

    return EXIT_SUCCESS;
}
