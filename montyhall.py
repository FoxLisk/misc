import random

def trial(ndoors=3, should_change=True):
    '''does a trial where monty opens 1 door and you choose
    either to stick with your original choice or to switch to
    a random other door'''
    doors = range(ndoors)

    winner = random.choice(doors)

    initial_choice = random.choice(doors)

    if not should_change:
        return winner == initial_choice

    monty_options = [i for i in doors if i not in (initial_choice, winner)]
    monty_opens = random.choice(monty_options)

    doors.remove(monty_opens)

    if should_change:
        doors.remove(initial_choice)
        return random.choice(doors) == winner


def trial_remove_all(ndoors=3, should_change=True):
    '''does a trial where monty opens 1 door and you choose
    either to stick with your original choice or to switch to
    a random other door'''
    doors = range(ndoors)
    winner = random.choice(doors)
    initial_choice = random.choice(doors)

    if not should_change:
        return winner == initial_choice

    if should_change:
        return initial_choice != winner


def run_test(iterations, ndoors):
    change_wins = 0
    stay_wins = 0
    for i in xrange(iterations):
        if trial_remove_all(ndoors, True):
            change_wins += 1
    for i in xrange(iterations):
        if trial_remove_all(ndoors, False):
            stay_wins += 1

    print 'Wins with %d doors without changing: %f; with changing: %f' % (ndoors, float(stay_wins)/iterations, float(change_wins)/iterations)
    print 'Expected wins without changing: %f' % (1.0/ndoors)

run_test(10000, 100)
