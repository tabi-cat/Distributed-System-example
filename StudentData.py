
# StudentData (EOU student database) program

# Code for the TCP/IP connection was based on information
# from these two sites (full end-text reference in report)
# https://pymotw.com/3/socket/tcp.html
# https://stackoverflow.com/questions/24423162/how-to-send-an-array-over-a-socket-in-python

import socket
import sys

# Names are in uppercase, unit code letters are in uppercase
# Emails are in lowercase
# Student IDs are in lowercase

#The Grades for each student match the criteria for the program,
#with no more than 2 fails for each unit.
#A student with 7 units will have no more than 14 fails.
#There are no more than 30 and no less than 12 grades for each student.

StudentData = [{'StudentID': "csmith", 'Password': "Th3grandSmith", 'LastName': "SMITH", 'Email': "csmith@eou.edu.au", 'TotalUnits':9, 'Grades': [100,40,65,70,55,80,37,49,61,91,75,69]},
               {'StudentID': "bjohnson", 'Password': "123cake!", 'LastName': "JOHNSON", 'Email': "bjohnson@eou.edu.au", 'TotalUnits':12, 'Grades': [75,65,69,59,67,75,77,78,61,75,70,73]},
               {'StudentID': "jpmarron", 'Password': "Rover2019", 'LastName': "MARRON", 'Email': "jpmarron@eou.edu.au", 'TotalUnits':9, 'Grades': [31,44,71,49,65,38,70,49,52,80,37,49,70,43,84,20,75,32,60]},
               {'StudentID': "cpeale", 'Password': "ninjaCook", 'LastName': "PEALE", 'Email': "cpeale@eou.edu.au", 'TotalUnits':13, 'Grades': [46,34,72,80,90,100,100,74,63,71,75,76,76,81]},
               {'StudentID': "avaleric", 'Password': "divineHelmet", 'LastName': "VALERIC", 'Email': "avaleric@eou.edu.au", 'TotalUnits':14, 'Grades': [51,75,60,40,86,81,86,87,83,76,87,100,81,88,89]},
               {'StudentID': "hyaromir", 'Password': "H3art!", 'LastName': "YAROMIR", 'Email': "hyaromir@eou.edu.au", 'TotalUnits':14, 'Grades': [61,50,61,64,47,68,53,59,68,49,54,55,66,51,65,52]},
               {'StudentID': "gdimas", 'Password': "LakePledge", 'LastName': "DIMAS", 'Email': "gdimas@eou.edu.au", 'TotalUnits':20, 'Grades': [89,49,75,50,53,62,99,97,63,71,59,59,70,100,76,52,61,73,55,61,68]}
               ]
#The above is an array of dictionaries, one dictionary per student.
#It is not accessed by any program.
#It simply demonstrates what the arrays below represent.

StudentIDs = ["csmith","bjohnson","jpmarron","cpeale","avaleric","hyaromir","gdimas"]

Passwords = ["Th3grandSmith","123cake!","Rover2019","ninjaCook","divineHelmet","H3art!","LakePledge"]

LastNames = ["SMITH","JOHNSON","MARRON","PEALE","VALERIC","YAROMIR","DIMAS"]

Emails = ["csmith@eou.edu.au","bjohnson@eou.edu.au","jpmarron@eou.edu.au","cpeale@eou.edu.au","avaleric@eou.edu.au","hyaromir@eou.edu.au","gdimas@eou.edu.au"]

Grades = [[100,40,65,70,55,80,37,49,61,91,75,69],
          [75,65,69,59,67,75,77,78,61,75,70,73],
          [31,44,71,49,65,38,70,49,52,80,37,49,70,43,84,20,75,32,60],
          [46,34,72,80,90,100,100,74,63,71,75,76,76,81],
          [51,75,60,40,86,81,86,87,83,76,87,100,81,88,89],
          [61,50,61,64,47,68,53,59,68,49,54,55,66,51,65,52],
          [89,49,75,50,53,62,99,97,63,71,59,59,70,100,76,52,61,73,55,61,68]]


def FindStudent(details):

    IDcounter = 0
    foundID = -1
    
    for sID in StudentIDs:
        if sID == details[0]:
            foundID = IDcounter
            #finds the index of the StudentID that matches the input ID
        else:
            IDcounter += 1

       
    if foundID == -1: #runs if no matching ID is found
        msg = ['-1','-1']
        
    elif LastNames[foundID] != details[1]:
        #runs if that StudentID's last name doesn't match the input one
        msg = ['-1','-1']

    elif Emails[foundID] != details[2]:
        #runs if the StudentID's email doesn't match the input one
        msg = ['-1','-1']

    elif Passwords[foundID] != details[3]:
        #runs if the StudenID's password doesn't match the input one
        msg = ['-1','-1']

    else: #runs if everything is correct
        scoreList = Grades[foundID]
        studentID = StudentIDs[foundID]
        
        stringList = []
        for item in scoreList:
            stringList.append(str(item))
            
        stringList.insert(0,studentID) #grades are returned with studentID
        stringList.append("-1")
        msg = stringList


    return msg


# Creates a TCP/IP socket
StudentData = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binds the socket to the port
StudentData_address = ('localhost', 10001)
print('Starting up on {} port {}'.format(*StudentData_address))
StudentData.bind(StudentData_address)

# Begins listening for incoming connections
StudentData.listen(1)

while True:
    # Waits for a connection
    print('Waiting for a connection')
    connection, client_address = StudentData.accept()
    try:
        print('Connection from', client_address)

        # Receives the data, decodes it to string,
        # splits it back into an array, removing the $ separators
        dataIn = connection.recv(1024)
        dataIn = dataIn.decode()
        print('Received {!r}'.format(dataIn))
        dataList = dataIn.split('$')

        #Calls a module to process the received data
        result = FindStudent(dataList)
        #A result is returned, which contains student scores
        #if authentication was successful
        
        
        if dataIn:# if data was received, now a response will be sent
            print('Sending response back to the client')
            dataOut = '$'.join(result)
            connection.sendall((dataOut).encode())
            #encodes string message into bits and sends it
                
        else:
            print('No data from', client_address)
            break

    finally:
        # Cleans up the connection
        connection.close()

