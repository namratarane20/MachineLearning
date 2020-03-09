from Teacher import Teacher

class Student(Teacher):
    def setMark(self,mark):
        self.mark=mark
    def getMark(self):
        return self.mark