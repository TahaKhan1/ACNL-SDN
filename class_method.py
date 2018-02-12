class UMass:
    def __init__(self, lowell):
        self.lowell=lowell
    @staticmethod
    def ball_hall(a, b):
        c = a + b
        print('Ball hall have Plastics and ECE Dept.')
        return c
d = UMass(10)
sum1=d.ball_hall(23, 10)
print(sum1)

class Northeastern(UMass):
    def __init__(self):
        super(Northeastern, self).__init__(self)
    def its_costly(self, e):
        self.e = e
        f = UMass.ball_hall(70,80)
        print("Its costly method from NorthEastern: {}".format(f))
instance_NE=Northeastern()
sum2=instance_NE.its_costly(12)

  
