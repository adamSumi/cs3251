# cs3251
Spring 2023

Contributors:
Adam Sumilong (adamsumi@gatech.edu)
Gabby Calderon (gcalderon7@gatech.edu)

Steps for PA2
1. Client connects to tracker -- done
2. Client sends info to what chunks it has initially -- done
3. Tracker stores data with [client, chunk info] in a list(s?) -- basically done
4. Client asks for a chunk from tracker -- done
5. Tracker sends back unavailable, or ip/port of client with queried chunk -- half-done
5(a). ^^ if yes, tracker sends info to queried client with asker ip/port ^^
6. Asker intiates new socket, Queried accepts --TODO
7. queried sends data, asker recieves --TODO
8. C2C connection close --TODO


Add followign funcitonality
- Always check chunk_list first, if there add to chunk_list andstop, otherwise check check_list, if there are move both entities