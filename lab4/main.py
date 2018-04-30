import random
import pickle
import time
import os


def verify(a, x, p, h):
    # a ^ x mod p == h
    return pow(a, x, p) == h


def gen_file(a, p, n, name):
    # time = 40 sec
    s = time.time()
    with open(name, 'wb') as f:
        puzzle = gen_puzzle(a, p, n)
        pickle.dump(puzzle, f)
    e = time.time()
    print('Generating took {} seconds'.format(str(e-s)))


def load_file(name):
    # time = 11 sec
    with open(name, 'rb') as f:
        return pickle.load(f)


def is_prime(n):
    if n < 2:
        return False
    elif n < 4:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i = i + 6
    return True


def get_correct_p(start):
    while is_prime(start) and is_prime(2*start+1):
        start += 1
    return 2*start+1


def crack_all(a, p, puzzle_list):
    n = len(puzzle_list)
    s = time.time()
    for i in range(n):
        if i % 167772 == 0:
            e = time.time()
            print('{} % wykonane w czasie: {}'.format(str(i/167772), str(e-s)))
        crack_one(i, a, p, puzzle_list)


def crack_one(index, a, p, puzzle_list):
    b = puzzle_list[index][1]
    x = 0
    while not pow(a, x, p) == b:
        x += 1
    return x, index


def gen_puzzle(a, p, n):
    puzzle_list = []
    n = 2 ** n
    start = n
    stop = start - n
    for x in range(start, stop, -1):
        # a ^ x mod p = b
        b1 = pow(a, x, p)
        puzzle1 = [x, b1]
        puzzle_list.append(puzzle1)
    return puzzle_list


n = 24
a = 2
p = get_correct_p(400)
name = '{}-{}-{}.txt'.format(n, a, p)
ind = random.randint(0, 2**n)
gen_file(a, p, n, name)
puzzle_list = load_file(name)
print('[a, x, p, b] = [{}, {}, {}, {}]'.format(a, puzzle_list[ind][0], p, puzzle_list[ind][1]))
print('{} ^ {} mod {} = {}'.format(a, puzzle_list[ind][0], p, pow(a, puzzle_list[ind][0], p)))


s = time.time()
crack_one(ind, a, p, puzzle_list)
e = time.time()
print('Cracking one took {}'.format(str(e-s)))

s = time.time()
crack_all(a, p, puzzle_list)
e = time.time()
print('Cracking all took {}'.format(str(e-s)))

