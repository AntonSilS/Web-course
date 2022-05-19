class Meta(type):
    def __new__(cls, name, bases, attrs):
        
        attrs["class_number"] = Meta.children_number
        Meta.children_number += 1
        
        return super().__new__(cls, name, bases, attrs)

 

Meta.children_number = 0

 

class Cls1(metaclass=Meta):

    def __init__(self, data):
        self.data = data
 

 

class Cls2(metaclass=Meta):

    def __init__(self, data):
        self.data = data


class Cls3(metaclass=Meta):

    def __init__(self, data):
        self.data = data

class Cls4(metaclass=Meta):

    def __init__(self, data):
        self.data = data

 
if __name__ == "__main__":
    
    assert (Cls1.class_number, Cls2.class_number, Cls3.class_number, Cls4.class_number) == (0, 1, 2, 3)

    a, b, c, d = Cls1(''), Cls2(''), Cls3(''), Cls4('')

    assert (a.class_number, b.class_number, c.class_number, d.class_number) == (0, 1, 2, 3)

    print("Classes number: ", Cls1.class_number, Cls2.class_number, Cls3.class_number, Cls4.class_number)
    print("Instances number: ", a.class_number, b.class_number, c.class_number, d.class_number)
