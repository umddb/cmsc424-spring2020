from grading.models import Instructor, Course, Student, Assignment, Question, StudentAssignment
import datetime
from django.utils import timezone

i1 = Instructor(name="J. Smith", rank="Lecturer")
i2 = Instructor(name="K. Morgan", rank="Professor")
i1.save()
i2.save()

c1 = i1.course_set.create(title="Introduction to Programming", credits=3, description="Teaches how to program")
c2 = i1.course_set.create(title="Data Structures", credits=3, description="Covers data structures")
c3 = i2.course_set.create(title="Introduction to Philosophy", credits=3, description="History and origins of philosophy")

s1 = Student(name="W. Jonhnson")
s2 = Student(name="A. Jackson")
s1.save()
s2.save()

s1.courses.add(c1)
s1.courses.add(c2)
s2.courses.add(c2)
s2.courses.add(c3)

c1a1 = c1.assignment_set.create(assignment_no=1, due_date=datetime.datetime.strptime("09/18/2016 23:59", "%m/%d/%Y %H:%M"))
c1a2 = c1.assignment_set.create(assignment_no=2, due_date=datetime.datetime.strptime("10/01/2016 23:59", "%m/%d/%Y %H:%M"))
c2a1 = c2.assignment_set.create(assignment_no=1, due_date=datetime.datetime.strptime("09/23/2016 23:59", "%m/%d/%Y %H:%M"))
c3a1 = c3.assignment_set.create(assignment_no=1, due_date=datetime.datetime.strptime("09/28/2016 23:59", "%m/%d/%Y %H:%M"))

c1a1.question_set.create(question_no=1, question_text="1 + 1 = 2", trueorfalse = True)
c1a1.question_set.create(question_no=2, question_text="123 + 231 = 450", trueorfalse = False)
c1a2.question_set.create(question_no=1, question_text="PRIMES is in P", trueorfalse = True)
c1a2.question_set.create(question_no=2, question_text="(x or y) is not satisfiable", trueorfalse = True)
c2a1.question_set.create(question_no=1, question_text="Earth is flat", trueorfalse = False)
c2a1.question_set.create(question_no=2, question_text="It is turtles all the way the down", trueorfalse = True)
c3a1.question_set.create(question_no=1, question_text="Pluto is a planet", trueorfalse = False)
c3a1.question_set.create(question_no=2, question_text="A human hasn't walked on moon for more than 50 years", trueorfalse = True)
