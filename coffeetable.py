num_tables = 3
seats_per_table = 3
num_people = 9

seen_at_a_time = seats_per_table - 1
changes_to_see_all = (num_people - 1) / seen_at_a_time
if changes_to_see_all * seen_at_a_time < num_people - 1:
  changes_to_see_all += 1

class Person(object):
  def __init__(self, num):
    self.seen = set([self])
    self.num = num

  def __eq__(self, other):
    return self is other

  def __str__(self):
    return str(self.num)

people = [Person(i+1) for i in range(num_people)]

def seat_people(seatings):
    '''seatings is form [ [person, person, person...] ]'''
    for table in seatings:
        for person in table:
            person.seen.update(table)

def solved(people):
    speople = set(people)
    for person in people:
        if person.seen != speople:
            return False
    return True

def gen_seating(people, offset):
    tables = []
    people = set(people)

    print 'picking tables'
    for i in range(num_tables):
      table = [people.pop()]
      print 'starting with [%d]' % table[0].num
      for person in people:
        if any(map(lambda p: person in p.seen, table)):
          print 'Someone has already seen %s' % person
          #this person has been seen, so hopefully the next one is better
          continue
        else:
          print 'Adding %s to table' % person
          table.append(person)
          if len(table) == seats_per_table:
            break
      for person in table[1:]:
        people.remove(person)
      while len(table) < seats_per_table:
        table.append(people.pop())
      tables.append(table)
    return tables

def print_seating(seating):
    for table in seating:
        print [p.num for p in table]
    print ''

print 'Best possible solution: %d' % changes_to_see_all
seatings = [
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    [[2, 4, 7], [3, 5, 8], [6, 1, 9]],
    [[3, 4, 9], [5, 1, 7], [6, 2, 8]],
    [[4, 1, 8], [5, 2, 9], [6, 3, 7]]]
for seating in seatings:
  for row in seating:
    for i, seat in enumerate(row):
      for p in people:
        if p.num == seat:
          row[i] = p
          break

for seating in seatings:
  print_seating(seating)
  seat_people(seating)
if solved(people):
  print 'woohoo!'

#for i in range(2 * changes_to_see_all):
#  seatings = gen_seating(people, i)
#  print_seating(seatings)
#  seat_people(seatings)
#  if solved(people):
#    print 'Solved after %d moves' % i
#    break
#else:
#  for person in people:
#    to_see = set(people) - person.seen
#    if to_see:
#      print 'person %d needs to see %s' % (person.num, [p.num for p in to_see])


'''
given t, c, n, let H = {1, 2... n}
Let S = {s1, s2... st} such that the union of s in S is H, and the intersection of si and sj = {} if i != j (a seating)
Let G = {S1, S2... Sk} where Si != Sj for i != j

Construct G such that k is minimized, under the constraint that:
  For all n in H,
    For all m in H,
      There is a set s in some S in G such that n and m are both in s.
'''

'''strategy:
  start with person1, find the first set of people he's not seen yet, build tables. move onto the first person not yet seen and do the same til you fill up all tables
  for second seating, start with person2, then person3, etc'''
