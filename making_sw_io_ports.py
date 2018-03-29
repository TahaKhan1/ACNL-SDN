link_ids={(1,2):(1,1),
          (1,3):(2,1),
          (2,1):(1,1),
          (2,3):(2,2),
          (3,1):(1,2),
          (3,2):(2,2)
}
converted_dick=dict()
for key,value in link_ids.items():
  if str(key[0]) in converted_dick:
    temp=converted_dick.get(str(key[0]))
    temp[str(key[1])]=value[0];
  else:
    temp=dict()
    temp[str(key[1])]=value[0];
    converted_dick[str(key[0])]=temp;
    
for key,value in converted_dick.items():
  pass

print(converted_dick)
