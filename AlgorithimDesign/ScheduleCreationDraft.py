A = [0,0,1,0] #B = [0,1,1,0]
B = [0,1,1,0]
C = [1,0,1,0] #D = [0,0,0,0]
D = [0,0,0,0]
E = [0,1,0,0] #D = [0,1,0,0]
F = [0,1,0,0]

Times = [0,0,0,0,0,0,0,0,0,0,0,0,0]

C1 = [A,B]
C2 = [C,D]
C3 = [E,F]
CSch = [[0,0,0,0], [0,0,0,0]]

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

print("Course1: ", C1)
print("Current Schedule: ", CSch);
fill_schedule(C1)
print("Course1: ", C2)
print("Current Schedule: ", CSch);
fill_schedule(C2)
print("Course1: ", C3)
print("Current Schedule: ", CSch);
fill_schedule(C3)
print("Final Schedule: ", CSch);
