from enum import Enum
import numpy as np

Days = Enum('Days', 'M T W Th F')
    
class Schedule:
    def __init__(self):
        self.courseSch = np.full((5,12),0)

    def addCourse(self, course):  #WRITE CODE
        print("adding course")

    def checkTimeConflict(self, ts_cour): # variable is arrays for a specific day
        print("checks if acourse can fit into the schedule")
    
class Course:
    def __init__(self, name="", days="M", times="0", priority="1"):
        self.name = name
        self.days = days
        self.times = times
        self.priority = priority
        self.courseSch = np.full((5,12),0)
    
    def setTimeSlot(self, d, t):
        for ts in range(8,12):
            self.courseSch[ Days[d].value - 1 ][ts] = 1
        print(Days[d].name, " ", self.courseSch[ Days[d].value - 1 ])

S1 = Schedule()

C4 = Course(name = "CS1114", days = "T") #created test course
C5 = Course(name = "EG1003", days = "W") #created test course

def time_conflict(a, b):
  if a + b > 1:
    return True
  else:
    return False

def fill_schedule(course):
  for i in range(0, 2):
    for j in range(0, 4):
      print("i,j: ",i," ",j)
      if time_conflict(CSch[i][j], course[i][j]) == False:
        CSch[i][j] += course[i][j]
      else:
        print("ErrorLog: Time Conflict")

print("C4: ",C4.courseSch)
print("C5: ",C5.courseSch)
print(Days['M'].value)
C4.setTimeSlot(C4.days, C4.times)
C5.setTimeSlot(C5.days, C5.times)
print("C4: ",C4.courseSch)
print("C5: ",C5.courseSch)
#print(C4.name , "\n" , C4.courseSch)
#print(C5.name , "\n" , C5.courseSch)

