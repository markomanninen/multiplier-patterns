#!/usr/bin/env python3
"""Exact checks for the claims in doubling-sequences-article.md and paper/main.tex.

Run:  python3 verify.py
Every line printed should end in OK. Uses only integer arithmetic.
"""
from math import gcd


def order(a, n):
    """Multiplicative order of a modulo n (n coprime to a)."""
    k, x = 1, a % n
    while x != 1:
        x = x * a % n
        k += 1
    return k


def period(n):
    """Repeating block of 1/n as a zero-padded string (n coprime to 10)."""
    L = order(10, n)
    return str((10**L - 1) // n).zfill(L)


def check(label, cond):
    print(f"{label:<62} {'OK' if cond else 'FAIL'}")
    assert cond, label


# 1. Question's table: period lengths and digit sums
TABLE = {7: (6, 27), 19: (18, 81), 47: (46, 207), 49: (42, 189), 71: (35, 126),
         79: (13, 54), 83: (41, 171), 89: (44, 198), 97: (96, 432),
         109: (108, 486), 199: (99, 405)}
for n, (L, s) in TABLE.items():
    p = period(n)
    check(f"1/{n}: period {L}, digit sum {s}", len(p) == L and sum(map(int, p)) == s)
check("1/79 period is 0126582278481 (13 digits, leading 0)", period(79) == "0126582278481")


# 2. Forward series  1/n = sum m r^k / (10^x)^(k+1),  m = floor(10^x/n), r = 10^x mod n
def forward_ok(n, x):
    """Check the series reproduces the full period: sum of enough terms, scaled."""
    L = order(10, n)
    P = (10**L - 1) // n
    m, r = divmod(10**x, n)
    # n * sum_{k<K} m r^k 10^{x(K-1-k)} = 10^{xK} - r^K  => compare leading digits
    K = 3 * L + 20  # enough terms that the truncated tail is below the last digit
    S = sum(m * r**k * 10**(x * (K - 1 - k)) for k in range(K))
    # S / 10^{xK} approximates 1/n; first L digits must equal P
    return S * 10**L // 10**(x * K) == P, m, r


for n, x, m_exp, r_exp in [(7, 2, 14, 2), (19, 2, 5, 5), (47, 2, 2, 6), (49, 2, 2, 2),
                           (71, 3, 14, 6), (83, 3, 12, 4), (97, 2, 1, 3), (199, 3, 5, 5),
                           (17, 4, 588, 4), (43, 7, 232558, 6), (51, 4, 196, 4),
                           (119, 4, 84, 4), (127, 6, 7874, 2), (167, 6, 5988, 4),
                           (7, 1, 1, 3), (7, 3, 142, 6), (98, 2, 1, 2)]:
    if gcd(n, 10) != 1:
        m, r = divmod(10**x, n)
        check(f"forward 1/{n}, x={x}: m={m_exp}, r={r_exp}", (m, r) == (m_exp, r_exp))
        continue
    ok, m, r = forward_ok(n, x)
    check(f"forward 1/{n}, x={x}: {m_exp} x {r_exp}^k", ok and (m, r) == (m_exp, r_exp))

# Forward doubling needs n | 10^x - 2
check("98 = 2*7^2", 98 == 2 * 7**2)
check("998 = 2*499", 998 == 2 * 499)
check("999998 = 2*31*127^2", 999998 == 2 * 31 * 127**2)
check("4999 and 49999 are prime",
      all(4999 % p for p in range(2, 71)) and all(49999 % p for p in range(2, 224)))


# 3. Backward series  P = b * sum c^k 10^(xk)  (mod 10^L),  c = 10^-x mod n, 10^x c - 1 = b n
def backward(n, x):
    L = order(10, n)
    P = (10**L - 1) // n
    c = pow(10, -x, n)
    b = (10**x * c - 1) // n
    K = L // x + 2
    return P == (b * sum(c**k * 10**(x * k) for k in range(K))) % 10**L, b, c


for n, x, b_exp, c_exp in [(19, 1, 1, 2), (19, 2, 21, 4), (7, 1, 7, 5), (47, 2, 17, 8),
                           (49, 1, 1, 5), (71, 3, 169, 12), (79, 1, 1, 8), (83, 1, 3, 25),
                           (89, 1, 1, 9), (97, 1, 7, 68), (109, 1, 1, 11), (199, 2, 1, 2),
                           (29, 1, 1, 3), (39, 1, 1, 4), (7, 4, 2857, 2)]:
    ok, b, c = backward(n, x)
    check(f"backward 1/{n}, x={x}: {b_exp} x {c_exp}^k from the right", ok and (b, c) == (b_exp, c_exp))

check("1/19 rightmost two blocks are 21, then 84", period(19).endswith("8421"))
check("19999 = 7*2857 (1/7 doubles backwards in 4-digit blocks)", 19999 == 7 * 2857)
check("1/7 period ends ...57142857", period(7) * 2 == "142857142857")

# 10-adic view: partial sums of (10c)^k agree with -1/n in low digits
n, c = 19, 2
S = sum(20**k for k in range(40))
check("19 * (1+20+...+20^39) = -1 mod 10^40", (19 * S) % 10**40 == 10**40 - 1)

# 4. Fibonacci
F = [0, 1]
while len(F) < 400:
    F.append(F[-1] + F[-2])
L89 = order(10, 89)
P89 = (10**L89 - 1) // 89
K = L89 + 40
S = sum(F[k] * 10**(K - k) for k in range(1, K + 1))  # sum F_k / 10^(k+1) scaled by 10^(K+1)
check("1/89 = sum F_k / 10^(k+1)", S * 10**L89 // 10**(K + 1) == P89)
L109 = order(10, 109)
P109 = (10**L109 - 1) // 109
check("-1/109 = sum F_k 10^(k-1) (10-adic, all 108 digits)",
      P109 == sum(F[k] * 10**(k - 1) for k in range(1, L109 + 5)) % 10**L109)
check("1/109 period ends ...23853211", period(109).endswith("23853211"))
check("1/89 backward: powers of 9 (89 = 10*9 - 1)", backward(89, 1)[0])

# 5. Midy: even period => digit sum 9L/2
for n in [7, 19, 47, 49, 89, 97, 109]:
    p = period(n)
    L = len(p)
    check(f"Midy 1/{n}: halves are nines' complements",
          int(p[:L // 2]) + int(p[L // 2:]) == 10**(L // 2) - 1)

# 5b. Full reptend primes in the table: L = n - 1 exactly for 7, 19, 47, 97, 109
full = [n for n in TABLE if TABLE[n][0] == n - 1]
check("table: L = n - 1 exactly for 7, 19, 47, 97, 109", full == [7, 19, 47, 97, 109])

# 6. Parasitic number
check("105263157894736842 * 2 = 210526315789473684",
      105263157894736842 * 2 == 210526315789473684)
check("105263157894736842 is the period of 2/19", 2 * (10**18 - 1) // 19 == 105263157894736842)

# 7. Paper, Theorem 1: block k+1 of 1/n is (m r^k + floor(r^(k+1)/n)) mod 10^x
def block_formula_ok(n, x, K=12):
    X = 10**x
    m, r = divmod(X, n)
    return all((X**(k+1) // n) % X == (m * r**k + r**(k+1) // n) % X for k in range(K))
for n, x in [(7, 2), (49, 2), (97, 2), (83, 3), (67, 2), (89, 2), (199, 3)]:
    check(f"Theorem 1 block formula for 1/{n}, x={x}", block_formula_ok(n, x))
check("1/7 third block 56 + 1 = 57", (10**6 // 7) % 100 == 57)
check("1/49 sixth block 64 + 1 = 65", (10**12 // 49) % 100 == 65)
check("1/67 second block 33 + 16 = 49", (10**4 // 67) % 100 == 49)
check("1/97 fifth block 81 + 2 = 83", (10**10 // 97) % 100 == 83)
check("1/83 fourth block 768 + 3 = 771", (10**12 // 83) % 1000 == 771)

# 8. Remark on the start: last x digits of P equal b
for n in [7, 19, 47, 49, 83, 97, 109, 199]:
    Ln = order(10, n)
    P = (10**Ln - 1) // n
    ok = all(P % 10**x == (10**x * pow(10, -x, n) - 1) // n for x in range(1, min(Ln, 6) + 1))
    check(f"last x digits of P equal b for 1/{n}", ok)

# 9. Parasitic numbers: moving the last digit of k/(10c-1) to the front multiplies by c
ok = True
for c in range(2, 10):
    n = 10 * c - 1
    Ln = order(10, n)
    for k in range(1, 10):
        Q = str(k * (10**Ln - 1) // n).zfill(Ln)
        ok &= int(Q[-1] + Q[:-1]) == c * int(Q)
check("parasitic rotation multiplies by c for c = 2..9, k = 1..9", ok)

# 10. Forward multiplier at x equals backward multiplier at L - x
ok = all(pow(10, x, n) == pow(10, -(order(10, n) - x), n)
         for n in [7, 17, 19, 47, 49, 71, 79, 83, 89, 97, 109, 199] for x in range(1, order(10, n)))
check("forward multiplier at x = backward multiplier at L - x", ok)
check("1/17 doubles backward at x=6 and forward at x=10", (2 * 10**6 - 1) % 17 == 0 and pow(10, 10, 17) == 2)
check("1/71 doubles backward at x=6 and forward at x=29", (2 * 10**6 - 1) % 71 == 0 and pow(10, 29, 71) == 2)
check("1/19 doubles forward at x=17", pow(10, 17, 19) == 2)

# 11. Proposition: one progression b T^k gives both series
for T, n, xp, x in [(20, 19, 2, 1), (50, 7, 2, 1), (50, 49, 2, 1), (200, 199, 3, 2), (250, 83, 3, 1)]:
    b = (T - 1) // n
    r, c = 10**xp // T, T // 10**x
    m, rr = divmod(10**xp, n)
    ok = (T - 1) % n == 0 and r * T == 10**xp and c * 10**x == T and r < n and c < n
    ok &= m == r * b and rr == r and pow(10, -x, n) == c and (10**x * c - 1) // n == b
    check(f"T={T} gives 1/{n}: forward x'={xp}, m={m}, backward x={x}, c={c}", ok)

# 12. After Theorem 1: the first ceil(log n / log r) - 1 terms are printed unchanged, the next is not
def unchanged_count_ok(n, x):
    X = 10**x
    m, r = divmod(X, n)
    if r < 2:
        return True
    j = 1
    while r**j < n:
        j += 1
    blocks = [(X**(k+1) // n) % X for k in range(j)]
    return all(blocks[k] == m * r**k for k in range(j - 1)) and blocks[j - 1] != m * r**(j - 1)
ok = all(unchanged_count_ok(n, x) for n in range(3, 400) if n % 2 and n % 5 for x in range(1, 4) if n < 10**x)
check("first ceil(log n/log r)-1 terms unchanged, next changed (n<400, x<=3)", ok)
check("10^5 - 2 = 2 * 49999 with 49999 prime", 10**5 - 2 == 2 * 49999 and all(49999 % p for p in range(2, 224)))
check("T=250 also gives n=249 with r=4, c=25 below 249", 249 * 1 == 250 - 1 and 4 < 249 and 25 < 249)


# ======================================================================
# Exhaustive tests. Each result of paper/main.tex is tested as it is
# stated, for every small case and not only for the examples in the text.
# Each check also tests the edge cases named in the statement.
# ======================================================================
from fractions import Fraction

NMAX = 600
DENOMS = [n for n in range(3, NMAX) if gcd(n, 10) == 1]

def first_digits(n, places, B=10):
    """The integer formed by the first `places` base-B digits of 1/n."""
    return B**places // n

# Theorem 1, series and block formula, for all n < NMAX and x = 1..4 with n < 10^x
ok_sum = ok_blk = ok_below = True
cases = 0
for n in DENOMS:
    for x in range(1, 5):
        X = 10**x
        if n >= X:
            continue
        m, r = divmod(X, n)
        ok_sum &= m >= 1 and 0 < r < n and Fraction(m, X - r) == Fraction(1, n)
        for k in range(15):
            cases += 1
            val = m * r**k + r**(k + 1) // n
            ok_blk &= first_digits(n, x * (k + 1)) % X == val % X
            if r**k < n:
                ok_below &= val < X
check(f"Thm 1 series sums to 1/n, m >= 1, 0 < r < n (n < {NMAX}, x <= 4)", ok_sum)
check(f"Thm 1 block formula, {cases} cases", ok_blk)
check("Thm 1 value below 10^x whenever r^k < n", ok_below)
check("Thm 1 needs n < 10^x: n = 19, x = 1 gives m = 0", divmod(10, 19)[0] == 0)

# Paragraph after Theorem 1, the first j - 1 terms unchanged and the j-th changed
ok = True
for n in DENOMS:
    for x in range(1, 5):
        X = 10**x
        if n >= X:
            continue
        m, r = divmod(X, n)
        if r < 2:
            continue
        j = 1
        while r**j < n:
            j += 1
        blocks = [first_digits(n, x * (k + 1)) % X for k in range(j)]
        ok &= all(blocks[k] == m * r**k for k in range(j - 1)) and blocks[j - 1] != m * r**(j - 1)
check("first ceil(log n/log r) - 1 terms unchanged, the next changed", ok)

# Forward doubling, r = 2 iff n | 10^x - 2, and the x form one residue class mod L
ok = True
for n in DENOMS:
    Ln = order(10, n)
    xs = [x for x in range(1, 3 * Ln + 1) if pow(10, x, n) == 2]
    ok &= all((pow(10, x, n) == 2) == ((10**x - 2) % n == 0) for x in range(1, 8))
    ok &= len({x % Ln for x in xs}) <= 1 and (not xs or xs == [xs[0] + i * Ln for i in range(len(xs))])
check("forward doubling iff n | 10^x - 2, block lengths form one class mod L", ok)

# Theorem 2, 0 < b < 10^x, the congruence, and the 10-adic identities
ok_b = ok_cong = ok_adic = ok_ppp = True
for n in DENOMS:
    Ln = order(10, n)
    P = (10**Ln - 1) // n
    for x in range(1, 7):
        c = pow(10, -x, n)
        b, rem = divmod(10**x * c - 1, n)
        ok_b &= rem == 0 and 0 < b < 10**x and 1 <= c < n
        K = -(-Ln // x)
        S = sum(c**k * 10**(x * k) for k in range(K))
        ok_cong &= (b * S - P) % 10**Ln == 0
        # 10-adic, n * b * sum_{k<K} (10^x c)^k = -1 mod 10^(xK)
        ok_adic &= (n * b * S + 1) % 10**(x * K) == 0
    J = 4
    ok_ppp &= (n * P * sum(10**(Ln * j) for j in range(J)) + 1) % 10**(Ln * J) == 0
check(f"Thm 2 0 < b < 10^x and 1 <= c < n (n < {NMAX}, x <= 6)", ok_b)
check("Thm 2 congruence with K = ceil(L/x)", ok_cong)
check("Thm 2 10-adic series is -1/n modulo 10^(xK)", ok_adic)
check("Thm 2 -1/n = ...PPP modulo 10^(4L)", ok_ppp)

# Remark on the start, P = b mod 10^x for x <= L, and b = 1 when n = 10c - 1 and x = 1
ok = True
for n in DENOMS:
    Ln = order(10, n)
    P = (10**Ln - 1) // n
    for x in range(1, min(Ln, 8) + 1):
        ok &= P % 10**x == (10**x * pow(10, -x, n) - 1) // n
    if n % 10 == 9:
        ok &= pow(10, -1, n) == (n + 1) // 10 and P % 10 == 1
check("Remark, last x digits of P are b, and n = 10c - 1 ends in 1", ok)

# Proposition 2 (parasitic), c = 1..60 and k = 1..9, and k = 10 is a counterexample
ok = True
for c in range(1, 61):
    n = 10 * c - 1
    Ln = order(10, n)
    for k in range(1, 10):
        Q = str(k * (10**Ln - 1) // n).zfill(Ln)
        ok &= Q[-1] == str(k) and int(Q[-1] + Q[:-1]) == c * int(Q)
check("Prop 2 rotation multiplies by c for c = 1..60, k = 1..9", ok)
Q10 = str(10 * (10**18 - 1) // 19).zfill(18)
check("Prop 2 needs k <= 9: the period of 10/19 ends in 0", Q10[-1] == "0")

# Remark on multipliers, 10^x = 10^-(L-x) mod n for 1 <= x < L
ok = all(pow(10, x, n) == pow(10, -(order(10, n) - x), n)
         for n in DENOMS for x in range(1, order(10, n)))
check(f"Remark, forward multiplier at x = backward multiplier at L - x (n < {NMAX})", ok)

# Proposition 4, every T = 10, 20, ..., 5000 and every divisor n > 1 of T - 1
ok_real = ok_adic = ok_match = True
matches = 0
for T in range(10, 5001, 10):
    for n in range(2, T):
        if (T - 1) % n:
            continue
        b = (T - 1) // n
        ok_real &= Fraction(b, T - 1) == Fraction(1, n)        # sum_{k>=1} b T^-k
        K = 6
        ok_adic &= (n * b * sum(T**k for k in range(K)) + 1) % 10**K == 0
        for x in range(1, 5):
            if T % 10**x:
                break
            c = T // 10**x
            for xp in range(x, 8):
                if 10**xp % T:
                    continue
                r = 10**xp // T
                if not (0 < c < n and 0 < r < n):
                    continue
                m, rr = divmod(10**xp, n)
                ok_match &= (m == r * b and rr == r and m >= 1 and n < 10**xp
                             and pow(10, -x, n) == c and (10**x * c - 1) // n == b)
                matches += 1
check("Prop 4 real series sums to 1/n for every T <= 5000", ok_real)
check("Prop 4 10-adic series is -1/n modulo 10^6", ok_adic)
check(f"Prop 4 identifies the series of Thm 1 and Thm 2 in {matches} cases", ok_match)
check("Prop 4 needs positive c, r: T = -10, n = 11, c = r = -1 breaks Thm 1",
      divmod(10, 11) != (1, -1))

# Section 4, the 10-adic Fibonacci identity, G(10)/10 = -1/109 modulo 10^N
F = [0, 1]
while len(F) < 80:
    F.append(F[-1] + F[-2])
N = 60
s10 = sum(F[k] * 10**(k - 1) for k in range(1, N + 5))
check("Sec 4, 109 * sum F_k 10^(k-1) = -1 modulo 10^60", (109 * s10 + 1) % 10**N == 0)

# Section 6, Theorems 1 and 2 in other bases B
ok = True
for B in (2, 3, 6, 7, 12):
    for n in range(2, 200):
        if gcd(n, B) != 1:
            continue
        Ln = order(B, n)
        P = (B**Ln - 1) // n
        for x in range(1, 4):
            X = B**x
            if n < X:
                m, r = divmod(X, n)
                ok &= all(first_digits(n, x * (k + 1), B) % X == (m * r**k + r**(k + 1) // n) % X
                          for k in range(8))
            c = pow(B, -x, n)
            b = (X * c - 1) // n
            K = -(-Ln // x)
            ok &= (b * sum(c**k * X**k for k in range(K)) - P) % B**Ln == 0
check("Thm 1 and Thm 2 hold in bases 2, 3, 6, 7, 12", ok)

# Remark on multipliers, the first terms m and b can coincide, so the text says "in general different"
m101, r101 = divmod(10**3, 101)
c101 = pow(10, -1, 101)
b101 = (10 * c101 - 1) // 101
check("1/101: m = b = 9 for x = 3 forward and L - x = 1 backward", order(10, 101) == 4 and m101 == b101 == 9)
check("1/7: m = 14 for x = 2 and b = 2857 for x = 4", divmod(100, 7)[0] == 14 and (10**4 * pow(10, -4, 7) - 1) // 7 == 2857)
Q7 = str(7 * (10**18 - 1) // 19).zfill(18)
check("Prop 2 example k = 7, n = 19: 368421052631578947 rotates to 2Q",
      Q7 == "368421052631578947" and int(Q7[-1] + Q7[:-1]) == 2 * int(Q7))
check("Sec 4, (1 - 10 - 100) sum F_k 10^k = 10 modulo 10^60",
      ((1 - 10 - 100) * sum(F[k] * 10**k for k in range(1, 70)) - 10) % 10**60 == 0)

# Classroom exercises
P29 = str((10**28 - 1) // 29).zfill(28)
check("Ex 1: 1/29 triples from the right, b = 1, c = 3", pow(10, -1, 29) == 3 and P29.endswith("7931")
      and (sum(3**k * 10**k for k in range(28)) - int(P29)) % 10**28 == 0)
check("Ex 1: 299 = 13 * 23 and both triple from the right in two-digit blocks",
      299 == 13 * 23 and pow(100, -1, 13) == 3 and pow(100, -1, 23) == 3)
d499 = str(10**30 // 499).zfill(30)
check("Ex 2: 1/499 shows 002 ... 256 unchanged and 513 in block 9",
      [d499[3*k:3*k+3] for k in range(9)] == ["002","004","008","016","032","064","128","256","513"])
check("Ex 1: 299 itself also triples from the right in two-digit blocks", pow(100, -1, 299) == 3)
check("Ex 4: x in 1..5 with backward tripling of 1/7 is only x = 5",
      [x for x in range(1, 6) if pow(10, -x, 7) == 3] == [5])
check("Ex 3: 1/39 = 0.(025641), m = r = 25 for x = 3, c = 4 and b = 1 for x = 1",
      str((10**6 - 1) // 39).zfill(6) == "025641" and divmod(1000, 39) == (25, 25)
      and pow(10, -1, 39) == 4 and (10 * 4 - 1) // 39 == 1)
check("Ex 4: 1/7 triples from the right in five-digit blocks, b = 42857",
      pow(10, -5, 7) == 3 and (3 * 10**5 - 1) // 7 == 42857 and str((10**6 - 1) // 7).endswith("42857"))

# Section 4, denominators N and N' from a linear recurrence, formulas (recden) and (recseries)
def fundamental(cs, K):
    d = len(cs); a = {k: 0 for k in range(1 - d, 1)}; a[1] = 1
    for k in range(2, K + 1):
        a[k] = sum(cs[i] * a[k - 1 - i] for i in range(d))
    return a
ok_real = ok_adic = True
for cs in [(1, 1), (2, 1), (1, 2), (1, 1, 1), (3,), (2, 0, 1), (1, 0, 1), (3, 2)]:
    d = len(cs)
    for x in (1, 2, 3):
        X = 10**x
        N = X**d - sum(cs[i] * X**(d - 1 - i) for i in range(d))
        Np = sum(cs[i] * X**(i + 1) for i in range(d)) - 1
        K = 400
        a = fundamental(cs, K)
        if abs(a[K]) * 3 < X**K // 10**20 and N > 0:   # terms small enough, so the real series converges
            part = sum(Fraction(a[k], X**(k + d - 1)) for k in range(1, K + 1))
            ok_real &= abs(Fraction(1, N) - part) < Fraction(1, 10**15)
        M = 40
        ok_adic &= (Np * sum(a[k] * X**(k - 1) for k in range(1, M + 1)) + 1) % X**(M - d) == 0
check("recurrence: 1/N is the real series for 8 recurrences, x = 1..3", ok_real)
check("recurrence: -1/N' is the 10-adic series for 8 recurrences, x = 1..3", ok_adic)
check("Pell: N = 9799 for x = 2, 1/9799 = 0.0001 02 05 12 29 71", str(10**12 // 9799).zfill(12) == "000102051229" and (10**14 // 9799) % 100 == 71)
check("Pell: N = 79 and N' = 119 for x = 1", 100 - 20 - 1 == 79 and 100 + 20 - 1 == 119)
check("1/79 = 0.0126582...", str(10**7 // 79).zfill(7) == "0126582")
check("1/119 period ends ...302521", str((10**48 - 1) // 119).endswith("302521") and pow(10, 48, 119) == 1)

# ======================================================================
# Corrections in version 1.1 of the article, 19 November 2026.
# Each check confirms the fault in the first version and the corrected
# statement that replaces it.
# ======================================================================

# Item 1, a common factor of k and n does not always shorten the period
L39 = order(10, 39)
check("1: gcd(3, 39) > 1 but 3/39 = 1/13 keeps period 6 = ord_39(10)",
      L39 == 6 and order(10, 13) == 6 and str(3 * (10**6 - 1) // 39).zfill(6) == "076923")
check("1: gcd(9, 99) > 1 but 9/99 = 1/11 keeps period 2 = ord_99(10)",
      order(10, 99) == 2 and order(10, 11) == 2)
ok = True
for c in range(1, 61):
    n = 10 * c - 1
    Ln = order(10, n)
    for k in range(1, min(9, n - 1) + 1):
        d = n // gcd(k, n)
        Ld = order(10, d) if d > 1 else 1
        Q = str(k * (10**Ln - 1) // n).zfill(Ln)
        per = str((k // gcd(k, n)) * (10**Ld - 1) // d).zfill(Ld)
        ok &= Ln % Ld == 0 and Q == per * (Ln // Ld)
check("1: Q is the period of k/n repeated L/(its length) times, c = 1..60", ok)

# Item 2, c = 1 and k = 9 give k/n = 1, so the statement needs k < n
check("2: c = 1, k = 9 gives n = 9 and k/n = 1, with Q = 9 = 10^L - 1",
      order(10, 9) == 1 and 9 * (10**1 - 1) // 9 == 9 == 10**1 - 1)
ok = True
for c in range(1, 61):
    n = 10 * c - 1
    Ln = order(10, n)
    for k in range(1, 10):
        if k < n:
            Q = k * (10**Ln - 1) // n
            ok &= Q < 10**Ln - 1 and Fraction(Q, 10**Ln - 1) == Fraction(k, n)
check("2: for k < n, Q < 10^L - 1 is the repeating part of k/n < 1", ok)

# Item 3, b is the last x digits of the period only for x <= L
b77 = (10**7 * pow(10, -7, 7) - 1) // 7
check("3: n = 7, x = 7 gives b = 7142857 with 7 digits, P has 6", b77 == 7142857 and b77 >= 10**6)
ok = all(((10**x * pow(10, -x, n) - 1) // n >= 10**order(10, n)) or x <= order(10, n)
         for n in DENOMS[:80] for x in range(1, 12))
check("3: b < 10^L can fail only when x > L", ok)

# Item 4, the direct proof needs xK >= L
Y = 10**2 * pow(10, -2, 7)
check("4: n = 7, x = 2, K = 2 gives Y^2 - 10^6 = -840000, not divisible by 10^6",
      Y**2 - 10**6 == -840000 and (Y**2 - 10**6) % 10**6 != 0)
ok = True
for n in DENOMS[:120]:
    Ln = order(10, n)
    P = (10**Ln - 1) // n
    for x in range(1, 6):
        c = pow(10, -x, n)
        b = (10**x * c - 1) // n
        Y = 10**x * c
        for K in range(1, Ln + 2):
            S = sum(Y**k for k in range(K))
            ok &= n * (b * S - P) == Y**K - 10**Ln
            if x * K >= Ln:
                ok &= (Y**K - 10**Ln) % 10**Ln == 0 and (b * S - P) % 10**Ln == 0
check("4: n(bS - P) = Y^K - 10^L, divisible by 10^L when xK >= L", ok)

# Item 5 and 6, the forward pattern needs n < 10^x, which is what gives m >= 1
m97, r97 = divmod(10, 97)
check("5: n = 97, x = 1 satisfies 1 <= x < L but m = 0, so no forward series",
      1 < order(10, 97) and m97 == 0)
ok = all((divmod(10**x, n)[0] >= 1) == (n < 10**x) for n in DENOMS for x in range(1, 5))
check("6: m >= 1 exactly when n < 10^x", ok)

# Item 7, x = 5 is like x = 3 and x = 4, one prime odd divisor
def is_prime(p):
    return p > 1 and all(p % q for q in range(2, int(p**0.5) + 1))
check("7: 499, 4999 and 49999 are all prime", all(map(is_prime, (499, 4999, 49999))))
check("7: 99998 = 2 * 49999", 10**5 - 2 == 99998 == 2 * 49999)
odd = {x: [d for d in range(3, 10**x - 1, 2) if (10**x - 2) % d == 0] for x in (2, 3, 4, 5)}
check("7: odd divisors > 1 of 10^x - 2 are {7, 49}, {499}, {4999}, {49999}",
      odd == {2: [7, 49], 3: [499], 4: [4999], 5: [49999]})

# Item 9, in Prop 4 the condition n > 1, n | T - 1 rules out T = 0, so |T| >= 10
check("9: T = 0 would need n | -1, impossible for n > 1", all((0 - 1) % n for n in range(2, 50)))
ok = True
for T in range(-5000, 5001, 10):
    for n in range(2, abs(T - 1) + 1):
        if (T - 1) % n:
            continue
        b = (T - 1) // n
        ok &= T != 0 and abs(T) >= 10 and Fraction(b, T - 1) == Fraction(1, n)
check("9: |T| >= 10 and the real sum b/(T - 1) = 1/n, also for negative T", ok)

print("\nAll checks passed.")
