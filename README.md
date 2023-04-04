# cs3251
Spring 2023

Contributors:
Adam Sumilong (adamsumi@gatech.edu)
Gabby Calderon (gcalderon7@gatech.edu)

Steps for PA2
1. Client connects to tracker -- good
2. Client sends info to what chunks it has initially -- good
3. Tracker stores data with [client, chunk info] in a list(s?) --TODO
4. Client asks for a chunk from tracker -- good
5. Tracker sends back unavailable, or ip/port of client with queried chunk -- half-done
6. ^^ if yes, tracker sends info to queried client with asker ip/port ^^
7. Asker intiates new socket, Queried accepts --TODO
8. queried sends data, asker recieves --TODO
9. C2C connection close --TODO
