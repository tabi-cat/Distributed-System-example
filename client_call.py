
# client_call (client-side) program

# Code for the Python TCP/IP connection was based on information
# from these two sites (full end-text reference in report)
# https://pymotw.com/3/socket/tcp.html
# https://stackoverflow.com/questions/24423162/how-to-send-an-array-over-a-socket-in-python

import socket
import sys

print("TINY BROWSER")
serverIP = input("Enter the IP of the server you wish to connect to: ")
print("")
# IP later used to call evaluator
# Must be the IP of the computer running the Evaluator program



def CheckUnits(code, mark, unitCodeList, passDict, failDict):

    unitCodeString = '  '.join(unitCodeList)
    unitString = ' '+unitCodeString+' '
    paddedCode = ' '+code+' '

    checkNum = unitString.count(paddedCode)
    #counts how many times unit code appears in the list of entered unit codes

    msg = 'Good'
    
    if checkNum == 3:
        msg = 'More3' #returned if that code has already been entered 3 times

    if int(mark) < 50 and failDict[code] == 2 and checkNum < 3:
        msg = 'threeFail' #returned if there are already 2 fails for a unit

    if int(mark) >= 50 and passDict[code] == 1 and checkNum < 3:
        msg = 'twoPass' #returned if that unit has already been passed

    return msg



def CheckGrade(grade):

    if grade > 100 or grade < 0:
        return False #checks that the grade is in a valid range
    else:
        return True
    


def NonStudentInput():

    codeScorePairs = [] #stores unit code, then score
    unitCodeList = [] #stores only the entered unit codes
    scoreList = [] #stores only the entered grades

    passDict = {} #stores unit codes as keys & number of passes as values
    failDict = {} #same, but for number of fails in that unit

    print("\nNext, enter each of the codes for the units you have completed,\nalong with the grade you got for them.")
    print("Enter -1 into both unit code and grade field to begin evaluation.")
    print("Enter -2 into the unit code or grade field to quit without evaluating.\n")
    print("If a message tells you your input was invalid, that input will not be counted,")
    print("however, all previous valid inputs will still be included in the evaluation.\n") 
    
    while True:

        inputCode = input("Enter a unit code: ")
        code = inputCode.upper() #unit code to uppercase, standardises input

        if code == '-2': #quits if -2 is entered for unit code
            print("\nYou have chosen to quit without evaluating.")
            scoreList = [0] # 0 will be returned, and not sent to evaluator
            break
        
        mark = input("Enter your grade for this unit: ")

        if mark == '-2': #quits if -2 is entered for grade
            print("\nYou have chosen to quit without evaluating.")
            scoreList = [0]
            break

        if code == '-1' or mark == '-1': #runs before evaluation

            if len(scoreList) < 12:
                print("You must enter at least 12 grades to evaluate.")
                print("Continue entering the rest of your grades or enter -2 to quit.")
                continue #does not register invalid input, allows re-entry
            else:
                scoreList.append(-1) 
                break #end-of-array symbol is appended, and scores are returned

        else:

            try:
                passDict[code] == -1 #throws an error if unit doesn't exist yet
            except:
                passDict[code] = 0
                #this is simply done to create a new key-value pair
                #for the unit, if it hasn't been entered before

            try:
                failDict[code] == -1
            except:
                failDict[code] = 0
                #same for fail grade dictionary
            
            try:
                test = int(mark)
                #exception if the grade entered cannot be converted to integer
            except:
                print("Grade must be an integer. Try again.")
                continue #does not count the invalid entry
            
            test2 = CheckGrade(int(mark))
            test3 = CheckUnits(code, mark, unitCodeList, passDict, failDict)

            if test2 == False:
                print("Grade must be between 0 and 100 inclusive. Try again.")
                continue

            if test3 == 'More3':
                print("Invalid entry. No more than 3 grades can be entered for a unit.\nPlease continue with different data.")
                continue
            elif test3 == 'threeFail':
                print("Invalid entry. A unit cannot have more than 2 grades below 50.\nPlease continue with different data.")
                continue
            elif test3 == 'twoPass':
                print("Invalid entry. A unit cannot have more than one grade above 50.\nPlease continue with different data.")
                continue
            #the above is printed if any of these invalid entry types occur
            #the invalid entries are not counted, and the user can continue
            
            codeScorePairs.append(code)
            codeScorePairs.append(mark)
            unitCodeList.append(code)
            scoreList.append(int(mark))
            #finally, the validated entries are added to the end of
            #the appropriate arrays

            if int(mark) >= 50:
                passDict[code] = passDict[code] + 1
            else:
                failDict[code] = failDict[code] + 1
            #if the current valid grade is a pass, number of passes
            #for that unit is incremented by 1
            #same for failDict if the grade is a fail

            if len(scoreList) == 30:
                print("30 grades is the maximum input. \nThese scores will now be evaluated.")
                scoreList.append(-1)
                break
            #once 30 grades are input, the program ends and the scores
            #will be automatically sent for evaluation
    
    return scoreList #only scores are returned to calling program     
        


def StudentInput(sID):

    name = input("Enter your last name: ")
    email = input("Enter your EOU student email: ")
    passwd = input("Enter your EOU login password: ")

    studentID = sID.lower() #studentID standardised to lowercase
    lastName = name.upper() #last name standardised to uppercase
    studentEmail = email.lower() #email standardised to lowercase

    details = ["*",studentID,lastName,studentEmail,passwd]
    # the mark * is added so the evaluator program will know
    # to interpret this data as being from a current EOU student
        
    return details



def EvaluatorCall(dataList):

    # The array of string items is joined into a single
    # string with '$' separators, in preparation for conversion to bits
    dataStream = '$'.join(dataList)
    
    # Creates a TCP/IP socket
    client_call = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connects the socket to the port where the server is listening
    evaluator_address = (serverIP, 10000)
    client_call.connect(evaluator_address)

    try:

        # Encodes the data into bits and sends the stream to the server
        client_call.sendall((dataStream).encode())

        # Waits to receive a response
        response = client_call.recv(1024)
        response = response.decode()#decodes the bits into a string


    finally:
        client_call.close()#closes the connection with evaluator

    return response



title = 'EOU Honours Enrolment Pre-assessment'
print('='*60)
print('|'+title.center(58)+'|')
print('='*60)
print('')


while True:

    print("------------------------------------------------------------")
    print("\nAre you a current or former EOU student?")
    entry = input("Enter Y for yes, N for no, or X to quit: ")
    print('')
    studentQuery = entry.upper() #standardises input to uppercase

    if studentQuery == 'Y':
        studentID = input("Enter your EOU student ID: ")
        studentDetails = StudentInput(studentID)

        print("Retrieving data...")
        evaluation = EvaluatorCall(studentDetails)#sends data to evaluator
        print("")
        print(evaluation)# prints the returned message from evaluator

    elif studentQuery == 'N':
        personID = input("Enter your name or student ID: ")
        scoreList = NonStudentInput() #calls score input & validation module
        
        if len(scoreList) != 1:
            #only runs if scoreList length shows that person did not quit
            #without wanting evaluation

            scoreList.insert(0,personID)#adds personID to beginning of scoreList
            enteredDetails = []
            for item in scoreList:
                enteredDetails.append(str(item))
                #turns all the scores to string for transmission
                
            print("Calculating...")
            evaluation = EvaluatorCall(enteredDetails) #sends data to evaluator
            print("")
            print(evaluation)# prints the returned message from evaluator
            
        else:
            continue
       
    elif studentQuery == 'X':
        break
    
    else:
        print("Invalid input, try again.")


