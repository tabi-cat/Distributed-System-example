
# evaluator (server-side) program

# Code for the Python TCP/IP connection was based on information
# from these two sites (full end-text reference in report)
# https://pymotw.com/3/socket/tcp.html
# https://stackoverflow.com/questions/24423162/how-to-send-an-array-over-a-socket-in-python

import socket
import sys

print("SERVER CONFIGURATION")
serverIP = input("Enter the IP of your server-hosting machine: ")
print("")
# The IP of the computer you are running the program on



def Average(scores):
#calculates an average and returns a value rounded to 2 decimal places
    ctr = 0
    total = 0

    while scores[ctr] != -1:
        currentMark = scores[ctr]
        total = total + currentMark
        ctr += 1

    averageMark = total / ctr
    roundedMark = round(averageMark, 2)
    
    return roundedMark



def FailCount(scores):
# counts the total amount of fails in the list of scores
    ctr = 0
    failTotal = 0

    while scores[ctr] != -1:
        if scores[ctr] < 50:
            failTotal += 1
        ctr += 1

    return failTotal


       
def BestMarksAv(scores):

    ctr = 0
    scores.remove(-1)# makes sure to remove the end-of-array mark
    scores.sort(reverse=True)# sorts array from highest to lowest
    bestMarks = []

    while ctr != 8:# only takes the 8 highest from the sorted array
        bestMarks.append(scores[ctr])
        ctr += 1
    bestMarks.append(-1)# replaces the end-of-array mark
    bmAverage = Average(bestMarks)
    # calls the Average module to find the average of the best 8 scores

    return bmAverage



def Evaluate(studentID,scores):
# calls the modules to evaluate the scores, then returns the appropriate message
    personID = str(studentID)
    courseAv = Average(scores)
    failTotal = FailCount(scores)
    bestAv = BestMarksAv(scores)

    if failTotal >= 6: # 6 or more fails
        msg = personID+", course average "+str(courseAv)+", with 6 or more fails! \nDOES NOT QUALIFY FOR HONOURS STUDY!"

    elif courseAv >= 70: #course average 70 or greater
        msg = personID+", course average "+str(courseAv)+", \nQUALIFIED FOR HONOURS STUDY!"

    # course average 65 or greater, best eight average 80 or greater
    elif courseAv >= 65 and bestAv >= 80:
        msg = personID+", course average "+str(courseAv)+", \nQUALIFIED FOR HONOURS STUDY!"

    # course average 65 or greater, best eight average less than 80
    elif courseAv >= 65 and bestAv < 80:
        msg = personID+", course average "+str(courseAv)+", best 8 average "+str(bestAv)+", \nMAY HAVE GOOD CHANCE! Need further assessment!"

    # course average 60 or greater, best eight average 80 or greater
    elif courseAv >= 60 and bestAv >= 80:
        msg = personID+", course average "+str(courseAv)+", best 8 average "+str(bestAv)+", \nMAY HAVE A CHANCE! Must be carefully reassessed and get the coordinator's permission!"

    else: #unqualified
        msg = personID+", course average "+str(courseAv)+", \nDOES NOT QUALIFY FOR HONOURS STUDY!"

    return msg



def StudentEval(studentDetails):

    dataStream = '$'.join(studentDetails)
    
    # Creates a TCP/IP socket, this time Evaluator is the client
    clientEvaluator = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connects the socket to the port where StudentData is listening
    StudentData_address = ('localhost', 10001)
    print("Connecting to the database...")
    clientEvaluator.connect(StudentData_address)

    try:

        # Encodes the data into bits and sends the stream to the server
        print("Requesting data...")
        clientEvaluator.sendall((dataStream).encode())

        # Waits to receive a response
        response = clientEvaluator.recv(1024)
        response = response.decode()#decodes the bits into a string
        print('Response received:{!r}'.format(response))
        responseList = response.split('$')

    finally:
        print("Closing connection to database...")
        clientEvaluator.close()#closes the connection with StudentData


    if responseList[0] == "-1":
        message = "EVALUATION UNAUTHORISED. One or more details entered were not valid."
        #returned if student details not found in database
    else:
        studentID = responseList[0]#takes studentID from beginning of list
        del responseList[0]#deletes studentID from the response list
        scoreList = []#makes new score list
        for item in responseList:
            scoreList.append(int(item))
            #converts string scores to integer and adds to new score list
            
        message = Evaluate(studentID, scoreList)
        #runs evaluate module and returns a string message
        
    return message



# Creates a TCP/IP socket for the evaluator server
evaluator = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binds the socket to the port
evaluator_address = (serverIP, 10000)
print('Starting up on {} port {}'.format(*evaluator_address))
evaluator.bind(evaluator_address)

# Begins listening for incoming connections
evaluator.listen(1)

while True:
    # Waits for a connection
    print('Waiting for a connection')
    connection, client_address = evaluator.accept()
    try:
        print('Connection from', client_address)

        # Receives the data, decodes it to string,
        # splits it back into an array, removing the $ separators
        dataIn = connection.recv(1024)
        dataIn = dataIn.decode()
        print('Received {!r}'.format(dataIn))
        dataList = dataIn.split('$')

        if dataList[0] == "*":
            dataList.remove("*")
            evaluation = StudentEval(dataList)

        else:
            personID = dataList[0]#takes personID from beginning of list
            del dataList[0]#deletes personID from the score list
            scoreList = []#makes new score list
            for item in dataList:
                scoreList.append(int(item))
                #converts string scores to integer and adds to new score list
            
            evaluation = Evaluate(personID, scoreList)
            #runs evaluate module and returns a string message
        
        if dataIn:# if data was received, now a response will be sent
            print('Sending response back to the client')
            dataOut = evaluation
            connection.sendall((dataOut).encode())
            #encodes string message into bits and sends it
                
        else:
            print('No data from', client_address)
            break

    finally:
        # Cleans up the connection
        connection.close()
