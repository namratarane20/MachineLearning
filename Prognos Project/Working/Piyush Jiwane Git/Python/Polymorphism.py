from Circle import Circle

class Rectangle(Circle):
    def draw(self):
        print("from Rectangle")


r=Rectangle()
r.draw()