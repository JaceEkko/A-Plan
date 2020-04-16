#The order in the csv file: 
#name,course_titile,Session,Class_Number,Career,Units,Grading,Description,
#Add_Consent,Instructor,Meets,Dates,Room,Instruction_Mode,Campus,Location,
#Components,Status
import pandas as pd
import itertools as it

data = pd.read_csv("new_cs_spring2020.csv")

class FinalSchedule:
    courseTitles = ""
    calendars = ""

class Course:
    courseNum = ""
    courseTitle = ""
    preReq = ""
    coReq = ""
    lab = ""
    unitsNum = ""
    classNum = ""
    sectionNum = ""
    status = ""
    mode = "" #In-person or online??
    comp = "" #recitation or lab component??
    meetingTimes = ""
    timesArray = ""
    room = ""
    instructor = ""
    calendar = ""

courseNumS = data.name
courseTitleS = data.course_titile
unitsNumS = data.Units
classNumS = data.Class_Number
sectionNumS = data.Section
statuS = data.Status
modeS = data.Instruction_Mode
timesArrayS = data.Meets
roomS = data.Room
instructorS = data.Instructor


def findDay(structCourse):
    Day = [0,0] # what days the class will be held on
    if len(structCourse.timesArray) == 5:
        if structCourse.timesArray[0] == 'Mon':
            Day[0] = 0
        elif structCourse.timesArray[0] == 'Tue':
            Day[0] = 1
        elif structCourse.timesArray[0] == 'Wed':
            Day[0] = 2
        elif structCourse.timesArray[0] == 'Thu':
            Day[0] = 3
        elif structCourse.timesArray[0] == 'Fri':
            Day[0] = 4
    if len(structCourse.timesArray) == 6:
        if structCourse.timesArray[0] == 'Mon':
            Day[0] = 0
            Day[1] = 2
        elif structCourse.timesArray[0] == 'Tue':
            Day[0] = 1
            Day[1] = 3

    return Day



def findTimes(structCourse):
    timeArray = [8.0,8.3,9.0,9.3,10.0,10.3,11.0,11.3,12.0,12.3,13.0,13.3,14.0,14.3,15.0,15.3,16.0,16.3,17.0,17.3,18.0,18.3,19.0,19.3,20.0,20.3,21.0,21.3,22.0,22.3,23.0,23.3];
    
    classDays = findDay(structCourse)

    scheduleCourse = [[0 for i in range(31)] for j in range(5) ] #2D array that reps a calendar RETURN VALUE

    dayShift = 0
    if structCourse.timesArray != ['TBA']:
        if len(structCourse.timesArray) == 6: #all the +dayshifts were one more than they are now
            print("it's six")
            dayShift = 1

        x1 = structCourse.timesArray[1+dayShift] 
        x2 = float(x1)

        #add 12 to any "PM" times to convert to military time
        x3 = ''.join(structCourse.timesArray[2+dayShift])
        x3 = x3.replace(" ", "")
        if x3 == "PM" and x2 < 12:
            x2 = x2 + 12

        xStart = x2

        x4 = structCourse.timesArray[3+dayShift] 
        x5 = float(x4)

        x6 = ''.join(structCourse.timesArray[4+dayShift])
        x6 = x6.replace(" ", "")
        if x6 and x5 < 12:
            x5 = x5 + 12

        xStop = x5

        switchClassBool = False
        #print(len(classDays), " ", classDays) 
        for i in range(len(classDays)):
            for timeSlot in range(31):
                if timeArray[timeSlot] == xStart and switchClassBool == False:
                    scheduleCourse[classDays[i]][timeSlot] = 1
                    switchClassBool = True
                if timeArray[timeSlot] < xStop and switchClassBool == True:
                    scheduleCourse[classDays[i]][timeSlot] = 1
                if timeArray[timeSlot] > xStop and switchClassBool == True:
                    switchClassBool = False

    return scheduleCourse

def andGate(A,B):
    C = -1
    if A==0 and B==0:
        C=0
    if A==0 and B==1:
        C=0
    if A==1 and B==0:
        C=0
    if A==1 and B==1:
        C=1
    return C

def orGate(A,B):
    C = -1
    if A==0 and B==0:
        C=0
    if A==0 and B==1:
        C=1
    if A==1 and B==0:
        C=1
    if A==1 and B==1:  
        C=1
    return C
        

#MAIN LOOP++++++++++++++++++++++++++++++++++++++++++++++++++++++++

courseList = list()

for c in range(0, 33): # append courses to the list
    newCourse = Course() # create new instance of Course
    
    newCourse.courseNum = courseNumS[c]
    newCourse.courseTitle = courseTitleS[c]
    newCourse.unitsNum = unitsNumS[c]
    newCourse.classNum = classNumS[c]
    newCourse.sectionNum = sectionNumS[c]
    newCourse.status = statuS[c]
    newCourse.mode = modeS[c]
    #newCourse.meetingTimes = meetingTimeS[c]
    newCourse.room = roomS[c]
    newCourse.instructor = instructorS[c]
    newCourse.timesArray = timesArrayS[c].split(" ")
    calendarTmp = findTimes(newCourse)
    newCourse.calendar = calendarTmp
    #print(newCourse.calendar)
    courseList.append(newCourse)

    
courseListCombine = it.permutations(courseList, 4)
allSchedules = list()
for combination in courseListCombine: # check compatability for each combination
    newSchedule = [[0 for i in range(31)] for j in range(5)] 
    for c in combination:
        #print(c.calendar)
        tmpSchedule = [[0 for i in range(31)] for j in range(5)] 
        #print(tmpSchedule)
        for i in range(0,5): #check for conflicts
            for j in range(0,31):
                tmpSchedule[i][j] = andGate(c.calendar[i][j], newSchedule[i][j]) # check if array indices contain a 1
        totalConflicts = 0
        for i in range(5): #gather number of conflicts
            for j in range(31):
                totalConflicts =  totalConflicts + tmpSchedule[i][j]
        if totalConflicts == 0: # there are no conflicts
            print("it's zero") # just a check
            for i in range(5):
                for j in range(31):
                    newSchedule[i][j] =  orGate(c.calendar[i][j], newSchedule[i][j]) # add the course to the schedule
            print(newSchedule)
            allSchedules.append(newSchedule) # add finalize schedule to list
                
