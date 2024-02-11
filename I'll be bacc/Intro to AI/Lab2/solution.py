import sys
from copy import copy

history = {}
literals_to_print = [('NIL',)]


def print_result(result, goal, clauses_list):
    if result:
        s = ' v '
        s = s.join(list(goal))
        print_formatted(clauses_list)
        print(f'[CONCLUSION]: {s} is true')
    else:
        s = ' v '
        s = s.join(list(goal))
        print(f'[CONCLUSION]: {s} is unknown')


def print_formatted(clauses_list):
    for clause in clauses_list:
        s = ' v '
        s = s.join(list(clause))
        print(f'{s}')

    print('\n====================================\n')

    for literal in literals_to_print[::-1]:
        parents = []
        literals = ' v '
        literals = literals.join(list(literal))
        for clause in history[literal]:
            s = ' v '
            s = s.join(list(clause))
            parents.append(s)
        p = ' and '
        p = p.join(parents)
        print(f'{literals} from ({p})')


def determine_path(key):
    parents = history[key]

    for parent in parents:
        if parent in history and parent not in literals_to_print:
            literals_to_print.append(parent)
            determine_path(parent)
        else:
            return


def resolve(pair):
    global history
    if len(pair[0]) >= len(pair[1]):
        tuple1 = list(pair[0])
        tuple2 = list(pair[1])
    else:
        tuple1 = list(pair[1])
        tuple2 = list(pair[0])

    tuple1_copy = copy(tuple1)
    tuple2_copy = copy(tuple2)

    for literal1 in tuple1:
        for literal2 in tuple2:
            if literal1 == negate_literal(literal2):
                if literal1 in tuple1_copy:
                    tuple1_copy.remove(literal1)
                if literal2 in tuple2_copy:
                    tuple2_copy.remove(literal2)

    if len(tuple2_copy) > 0 and len(tuple2_copy) != len(tuple2):
        for el in tuple2_copy:
            tuple1_copy.append(el)
    return tuple(tuple1_copy)


# returns list of tuples of 2 sets
def select_clauses(clauses, ngoal, new_clauses):
    pairs = []

    if len(new_clauses) == 0:
        for clause1 in clauses:
            for clause2 in ngoal:
                if clause1 in ngoal:
                    continue
                pair = (clause1, clause2)
                pairs.append(pair)

    for clause1 in new_clauses:
        for clause2 in clauses:
            pair = (clause1, clause2)
            pairs.append(pair)

    return pairs


def refutation_resolution(clauses_list, ngoal):
    global history

    new = set()
    negated_goal = ngoal

    while True:
        original_new = copy(new)
        for pair in select_clauses(clauses_list, negated_goal, new):
            resolvent = resolve(pair)

            if resolvent not in clauses_list and resolvent not in new:
                if len(resolvent) == 0:
                    history[('NIL',)] = pair
                else:
                    history[resolvent] = pair

            if len(resolvent) == 0:
                determine_path(('NIL',))
                return True

            new.add(resolvent)
            new -= set(clauses_list)
        new -= original_new
        if new.issubset(set(clauses_list)):
            return False


def negate_literal(literal):
    if '~' in literal:
        return literal.replace('~', '')
    else:
        return f'~{literal}'


def negate_goal(clause):
    new_clauses = []
    for literal in clause:
        if '~' in literal:
            clause = {f'{literal[1]}'}
        else:
            clause = {f'~{literal}'}
        new_clauses.append(tuple(clause))
    return new_clauses


def remove_redundant(clauses_list):
    for clause1 in clauses_list[:-1]:
        for clause2 in clauses_list[:-1]:
            if set(clause1).issubset(set(clause2)) and clause1 != clause2:
                clauses_list.remove(clause2)

    return clauses_list


def isTautology(clause):
    for literal in clause:
        if literal in clause and negate_literal(literal) in clause:
            return True

    return False


def read_file(file_name):
    file = open(file_name)
    data = file.readlines()

    clauses_list = []

    for i in range(len(data)):
        clause = set(data[i].strip().lower().split(' v '))
        if data[i].startswith('#') or isTautology(tuple(clause)):
            continue
        clauses_list.append(tuple(clause))

    return clauses_list


def read_input_file(file_name):
    file = open(file_name)
    data = file.readlines()

    literals_commands = []

    for i in range(len(data)):
        clause_raw = [data[i].strip().lower().rsplit(" ", 1)[0]]
        clause = set(clause_raw[0].split(" v "))
        literals_commands.append((tuple(clause), data[i].strip().rsplit(" ", 1)[1]))

    return literals_commands


def determine_action(lc, clauses_list):
    literal = tuple(lc[0])
    command = lc[1]
    original_clauses_list = copy(clauses_list)

    print(f'User command: {literal} {command}')

    if command == '?':
        negated_goal = negate_goal(literal)
        for negated_literal in negated_goal:
            clauses_list.append(negated_literal)
        clauses_list = remove_redundant(clauses_list)
        result = refutation_resolution(clauses_list, negated_goal)
        print_result(result, goal=literal, clauses_list=clauses_list)
    elif command == '+':
        clauses_list.append(literal)
        print(f'Added {literal}')
        return clauses_list
    elif command == '-':
        clauses_list.remove(literal)
        print(f'Removed {literal}')
        return clauses_list

    return original_clauses_list


def cooking(clauses_list):
    input_file_name = sys.argv[3]
    literals_commands = read_input_file(input_file_name)

    for lc in literals_commands:
        clauses_list = determine_action(lc, clauses_list)


def resolution(clauses_list):
    goal = clauses_list.pop()
    negated_goal = negate_goal(goal)

    for literal in negated_goal:
        clauses_list.append(literal)

    clauses_list = remove_redundant(clauses_list)

    result = refutation_resolution(clauses_list, negated_goal)
    print_result(result, goal, clauses_list)


def main():
    file_name = sys.argv[2]
    clauses_list = read_file(file_name)

    if sys.argv[1] == 'cooking':
        cooking(clauses_list)
    elif sys.argv[1] == 'resolution':
        resolution(clauses_list)


if __name__ == '__main__':
    main()

