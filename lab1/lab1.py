import random
from math import gcd
from itertools import combinations
import numpy as np


def lcg(gen_seed, gen_m, gen_a, gen_c, n_rands):
    result = []
    gen_a = int(gen_a)
    gen_seed = int(gen_seed)
    gen_c = int(gen_c)
    gen_m = int(gen_m)
    for ind in range(n_rands):
        gen_seed = (gen_a * gen_seed + gen_c) % gen_m
        result.append(int(gen_seed))
    return result


def find_max_gcd(array):
    max_divisor = array[0]
    for el in array[1:]:
        max_divisor = gcd(max_divisor, el)
    return max_divisor


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = egcd(b % a, a)
        return g, y - (b // a) * x, x


def mulinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n


def get_m(rands):
    rands = rands
    t_n = [s1 - s0 for s0, s1 in zip(rands[:-1], rands[1:])]
    u_n = [t2 * t0 - t1 * t1 for t0, t1, t2 in zip(t_n[:-2], t_n[1:-1], t_n[2:])]
    m = find_max_gcd(u_n)
    return m


def get_a(list_rand, m):
    s0, s1, s2 = list_rand[:3]
    i = 1
    while s1 - s0 < 0:
        i += 1
        s0, s1, s2 = list_rand[i:3 + i]
    inv_mod = mulinv(s1 - s0, m)
    if inv_mod is not None:
        return (s2 - s1) * inv_mod % m
    return 1


def get_c(list_rand, a, m):
    s0, s1 = list_rand[:2]
    c = (s1 - a*s0) % m
    return c


def prime_factorization(x):
    from math import floor, sqrt
    if x < 2:
        if x <= 0:
            return [0]
        elif x == 1:
            return [x]
    ind = 2
    e = floor(sqrt(x))
    result = []
    while ind <= e:
        if x % ind == 0:
            result.append(ind)
            x /= ind
            e = floor(sqrt(x))
        else:
            ind += 1
    else:
        if x > 1:
            result.append(int(x))
            return result


def find_subsets(s, subset_len):
    return list(set(combinations(s, subset_len)))


def get_most_ms(rand_list, max_num):
    m_est = get_m(rand_list)
    small_primes = (
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
        109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
        233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359,
        367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491,
        499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641,
        643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787,
        797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
        947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063,
        1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201,
        1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319,
        1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471,
        1481, 1483, 1487, 1489, 1493, 1499, 1511, 1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1597,
        1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657, 1663, 1667, 1669, 1693, 1697, 1699, 1709, 1721, 1723,
        1733, 1741, 1747, 1753, 1759, 1777, 1783, 1787, 1789, 1801, 1811, 1823, 1831, 1847, 1861, 1867, 1871, 1873,
        1877, 1879, 1889, 1901, 1907, 1913, 1931, 1933, 1949, 1951, 1973, 1979, 1987, 1993, 1997, 1999, 2003, 2011,
        2017, 2027, 2029, 2039, 2053, 2063, 2069, 2081, 2083, 2087, 2089, 2099, 2111, 2113, 2129, 2131, 2137, 2141,
        2143, 2153, 2161, 2179, 2203, 2207, 2213, 2221, 2237, 2239, 2243, 2251, 2267, 2269, 2273, 2281, 2287, 2293,
        2297, 2309, 2311, 2333, 2339, 2341, 2347, 2351, 2357, 2371, 2377, 2381, 2383, 2389, 2393, 2399, 2411, 2417,
        2423, 2437, 2441, 2447, 2459, 2467, 2473, 2477, 2503, 2521, 2531, 2539, 2543, 2549, 2551, 2557, 2579, 2591,
        2593, 2609, 2617, 2621, 2633, 2647, 2657, 2659, 2663, 2671, 2677, 2683, 2687, 2689, 2693, 2699, 2707, 2711,
        2713, 2719, 2729, 2731, 2741, 2749, 2753, 2767, 2777, 2789, 2791, 2797, 2801, 2803, 2819, 2833, 2837, 2843,
        2851, 2857, 2861, 2879, 2887, 2897, 2903, 2909, 2917, 2927, 2939, 2953, 2957, 2963, 2969, 2971, 2999, 3001)
    result = [m_est]
    for prime in small_primes:
        if not m_est % prime and m_est//prime > max_num:
            result.append(m_est//prime)
    return result


def get_parameters(rand_list):
    result = []
    for m in get_most_ms(rand_list, max(rand_list)):
        # m_est = get_m(rand_list)
        a_est = get_a(rand_list, m)
        c_est = get_c(rand_list, a_est, m)
        result.append([m, a_est, c_est])
    return result


def test_lcg_predictions(n_tests):
    n = 15
    wynik = 0
    for j in range(n_tests):
        seed, m, a, c = [random.randint(1, 2 ** 32) for ind in range(4)]
        m = m if m % 2 != 0 else m+1
        lista = lcg(seed, m, a, c, n)
        new_seed = lista[-1]
        next_bits = np.array(lcg(new_seed, m, a, c, n))
        for el in get_parameters(lista):
            predicted_bits = np.array(lcg(new_seed, el[0], el[1], el[2], n))
            wynik += np.sum(next_bits == predicted_bits)
    print('LCG prediction precision', wynik/(n_tests*n))


class Glibc:
    def __init__(self, seed):
        self.r = [seed]
        for ind in range(30):
            self.r += [self.r[-1] * 16807 % 2147483647]
        for ind in range(3):
            self.r += [self.r[-31]]
        for ind in range(310):
            self.r += [(self.r[-3] + self.r[-31]) % 4294967296]

    def random(self):
        new_rand = (self.r[-3] + self.r[-31]) % 4294967296
        self.r.append(new_rand)
        return new_rand >> 1

    def create_base(self):
        self.random_values = []
        for ind in range(31):
            self.random_values.append(self.random())

    def predict(self):
        self.create_base()
        prediction = (self.random_values[-31] + self.random_values[-3]) % 2147483648
        rand_value = self.random()
        return prediction == rand_value


n_tests = 10000
test_lcg_predictions(n_tests)

glibc_result = 0
for ind in range(n_tests):
    glibc = Glibc(random.randint(1, 2 ** 32))
    glibc_result += glibc.predict()
print('GLIBC prediction precision', glibc_result/n_tests)
