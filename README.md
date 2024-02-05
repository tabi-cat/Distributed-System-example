# Distributed-System-example
Created for a university project. Basic communication between a 'client', 'server' and 'database' program.
The program either retrieves student grades from a database, or retrieves a series of grades input by the user, evaluates them, and returns a message letting the user know whether they are qualified for Honours Study.

All three programs should be running at the same time. I usually set up the server and database programs before the client one. 
The server and database programs should be running on the same machine. The client program is able to run on a different machine in the same local area network. 
The local IPv4 address of the machine running the server program should be input into both the server program and the client program. This will be the first thing each program asks for.

Below are the sample student details stored in the database. These details should be used if answering Y to the question 'are you a current or former EOU student'.

StudentID: csmith
LastName: Smith
Email: csmith@eou.edu.au
Password: Th3grandSmith

StudentID: bjohnson
LastName: Johnson
Email: bjohnson@eou.edu.au
Password: 123cake!

StudentID: jpmarron
LastName: Marron
Email: jpmarron@eou.edu.au
Password: Rover2019

StudentID: cpeale 
LastName: Peale
Email: cpeale@eou.edu.au
Password: ninjaCook

StudentID: avaleric
LastName: Valeric
Email: avaleric@eou.edu.au
Password: divineHelmet

StudentID: hyaromir
LastName: Yaromir
Email: hyaromir@eou.edu.au
Password: H3art!

StudentID: gdimas
LastName: Dimas
Email: gdimas@eou.edu.au
Password: LakePledge
