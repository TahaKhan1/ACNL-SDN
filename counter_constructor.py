class topo(object):
  count_id=0
  '''def __init__(self,x):
    self.x=x
    topo.count_id +=1
    #print(topo.count_id)'''
    
  @staticmethod
  def hi(acbd):
    topo.count_id +=1;
    actions=[]
    actions.append(topo.count_id)
    print("Id's in action array : {}".format(topo.count_id))
    print(actions)
    
x=topo()
z=x.hi(10)
ab=x.hi(20)
print(z)
