num_tables = 7
seats_per_table = 7
num_people = 49

class Person(object):
    def __init__(self, num):
        self.seen = set([self])
        self.num = num

    def __eq__(self, other):
        return self is other

people = [Person(i) for i in range(num_people)]

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
    for i in range(num_tables):
        tables.append([p for p in people if ((p.num + offset) % num_tables) == i])
    return tables

def print_seating(seating):
    for table in seating:
        print [p.num for p in table]
    print ''

for i in range(10):
    seatings = gen_seating(people, i)
    print_seating(seatings)
    seat_people(seatings)
    if solved(people):
        print 'Solved after %d moves' % i
        break
