import random
import json

def make_int():
  return random.randint(-1000000, 1000000)

def make_str():
  return ''.join(random.choice('1234567890-=][poiuytrewqasdfghjkl;/.,mnbvcxz\n\t !@#$%^&*()_+}{P|OIUYTREWQASDFGHJKL:"?><MNBVCXZ') for i in range(random.randint(0, 1000)))

def make_arr():
  return [make_obj(random.randint(0,1)) for i in range(random.randint(0,1000))]
  
def make_obj(obj_type=None):
  types = [ make_int, make_str, make_arr ]
  if obj_type is None:
    obj_type = random.randint(0,2)
  return types[obj_type]()

def make_name():
  return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(15))

def make_json(items_per_level=100, levels=50):
  obj = {}
  orig = obj
  while levels > 0:
    for i in range(random.randint(0, items_per_level - 1)):
      obj[make_name()] = make_obj()
    obj['next_level'] = {}
    obj = obj['next_level']
    levels -= 1
  return json.dumps(orig)

if __name__ == '__main__':
  with open('out', 'w') as f:
    f.write(make_json())
