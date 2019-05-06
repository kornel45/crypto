import numba


@numba.jit(nopython=True)
def get_possible_points(d, p):
    s = set()
    for x in range(p):
        for y in range(p):
            if (x ** 2 + y ** 2) % p == (1 + d * x ** 2 * y ** 2) % p:
                s.add((x, y))
    return list(s)


if __name__ == '__main__':
    p = 4021
    d = 5
    result = get_possible_points(d, p)
    print(result)
