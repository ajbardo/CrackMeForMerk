# Index

1. Objective
2. requirements and characteristics:
	* 2.1 Requirements
	* 2.2 Execution and configuration
		* 2.2.1 Configuration values
	* 2.3 Environment
3. Connection characteristics
4. Protocol phases
	* 4.1 Protocol characteristics:
	* 4.2 Phases
	* 4.3 Protocol flow diagram




# 1 Objective
Create n insecure transmission at application level for training university newcomers into the cyber-security area.

It´s recommended to not read the python code if you want to really break the communication playing like an external element

# 2 requirements and characteristics:
## 2.1 Requirements
R01 The protocol simulates a secure private key exchange and remote execution of commands in the objective                                          
R02 The protocol is split in phases with independent connections between them                                                                     
R03 The client and server have a pre-shared value the is represented as  “CommonValue”                                                                      
R04 The client and the server generates random privates values with lifetime, and they refresh that values when the lifetime ends                           

## 2.2 Execution and configuration
The normal execution of the software is done by the command : "python main.py" or "python3 main.py" depending on your environment configuration
The execution with the command admits arguments in order to change the behaviour of the software.
The arguments need to be separated by a blank space and composed of a specific identification before the assignment character ":" and the new value
In case of one or more missing configuration arguments in the command, the software will use the default values specified below.

### 2.2.1 Configuration values
#### Objective
The ip that represents the server                                        
Default value: "127.0.0.1"                                  
Identification for the argument: ip  

Example or argument:                                                 
* ip:127.0.0.1                                                         
* ip:192.168.0.1  
                                       
Example of command:                                          
* python main.py ip:127.0.0.1                                   
* python main.py ip:192.168.0.1                                         

#### Port
The port that will be used for the communication, has to match in the server and client
Default value: 4450
Identification for the argument: port

Example or argument:                                                 
* port:4450                                                         
* port:5000  
                                       
Example of command:                                          
* python main.py port:4450                                   
* python main.py port:5000    

#### cycles
Number of example connections between the client and the server.
Limiting both parts, the amount of sequential connections from a client to a server and the amount of connections that a server will serve.

Default value: 1
Identification for the argument: cycles

Example or argument:                                                 
* cycles:1                                                         
* cycles:15  
                                       
Example of command:                                          
* python main.py cycles:1                                   
* python main.py cycles:15   

#### delay
Determines the delay in seconds between sequential connections in the clients
Default value: 10
Identification for the argument: delay

Example or argument:                                                 
* delay:10                                                         
* delay:105  
                                       
Example of command:                                          
* python main.py delay:10                                   
* python main.py delay:105 

## 2.3 Environment
Executed with Python 3.8
Executed in Windows environments

# 3 Connection characteristics
C01 For each Client to Server connection, we have a data send from the client with the request and a response from the server with the data related to the request.
C02 After each server to client response each connection close.
C03 Each message between the client and the server are authenticated by a TimeFlag.

# 4 Protocol phases
In each phase the client opens a new connection with the server and in the end of the phase the connection is closed

## 4.1 Protocol characteristics:
4.1C01- There is always an identification header for each phase                                                                            
4.1C02- The TimeFlag has always the reserved value “/” before                                                                               
4.1C03- If we are sending data, after the identification header we have “:” and the data that we want to transfer                                            
4.1C04- The TimeFlag mandatory in all the messages                                                                                        

### 4.1.2 Characteristics of the execution windows
4.1.2C01 Each window has a defined randomized token                                                                                               
4.1.2C02 The windows are sequential one after another                                                                       
4.1.2C03 The lifetime of each window is defined by a random integer in the magnitude of seconds                                               
4.1.2C04 The server always send to the client the next operative window but only the starting moment                                           


## 4.2 Phases

### 4.2.0  Phase 01
#### -Schematic-
C->S	DH_1/TimeFlag                                                                                                                                   
S->C	DH_1:int(CommonValue + ServerPrivateValue)/TimeFlag
#### -Comment-
C->S;Petition from the client: Identifier "DH_1/"                                                                                                                              
S->C;Response from the server: Identifier "DH_1:" and common value pre-shared between them added to the private int value of the server


### 4.2.2  Phase 02
#### -Schematic-
C->S 	DH_2:int(ServerPrivateValue + ClientPrivateValue)/TimeFlag                                                                                           
S->C	DH_2:int(ClientPrivateValue+TimeToNexToken,ClientPrivateValue+Executiontoken)
#### -Comment-
C->S;Petition from the client: Identifier "DH_2:" and the sum of the private server value and the client private value                                         
S->C;Response of the server: Identifier "DH_2:" and the sums separated by “,” of :                                                               
1)ClientPrivateValue and TimeToNexToken                                                                                                                 
2)ClientPrivateValue and Executiontoken                                                                                                                    

### 4.2.3 Phase 03
#### -Schematic-
C->S	PVT_1:int(Executiontoken+CharDecValFromAscii1,Executiontoken+CharDecValFromAscii2,...)/TimeFlag                                                       
S->C 	PVT_1:int(ClientPrivateValue+CharDecValFromAscii1,ClientPrivateValue+CharDecValFromAscii2,...)/TimeFlag
#### -Comment-
C->S;Petition from the client: Identifier "PVT_1:" and the sum of the AscII value of each letter of our command add to the Executiontoken                    
S->C;Response of the server:  Identifier "PVT_1:" and the sum of the AscII value of each letter of the result add to the ClientPrivateValue
