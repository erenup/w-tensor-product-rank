#!/usr/bin/env python3
"""Finite exact regressions only, not a proof of the quantified rank theorem.

Standard library only. Explicit failure paths also work with python -O.
Upper checks expand actual character sums in Q[zeta_N]. Lower checks
construct rational cubatures by interpolation and directly evaluate Gram
entries, independently of their predicted formulas.
"""

import argparse
import copy
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json
from math import comb, prod
from pathlib import Path


def require(condition, message):
    if not condition:
        raise SystemExit("REJECT: " + message)


def det(matrix):
    a = [list(map(F, row)) for row in matrix]
    n = len(a)
    if n == 0:
        return F(1)
    value = F(1)
    for j in range(n):
        p = next((p for p in range(j, n) if a[p][j]), None)
        if p is None:
            return F(0)
        if p != j:
            a[p], a[j] = a[j], a[p]
            value = -value
        pivot = a[j][j]
        value *= pivot
        for p in range(j + 1, n):
            ratio = a[p][j] / pivot
            for r in range(j + 1, n):
                a[p][r] -= ratio * a[j][r]
    return value


def adjugate(a):
    n = len(a)
    return [[int((-1) ** (i + j) * det([
        [a[r][s] for s in range(n) if s != i]
        for r in range(n) if r != j])) for j in range(n)] for i in range(n)]


def matvec(a, v):
    return [sum(x * y for x, y in zip(row, v)) for row in a]


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def polydiv(p, q):
    p = trim(p)
    q = trim(q)
    require(q[-1] == 1, "nonmonic polynomial division")
    out = [0] * max(1, len(p) - len(q) + 1)
    while len(p) >= len(q) and p != [0]:
        shift = len(p) - len(q)
        c = p[-1]
        out[shift] = c
        for j in range(len(q)):
            p[j + shift] -= c * q[j]
        p = trim(p)
    return trim(out), trim(p)


@lru_cache(None)
def cyclotomic(n):
    p = [-1] + [0] * (n - 1) + [1]
    for d in range(1, n):
        if n % d == 0:
            p, rem = polydiv(p, cyclotomic(d))
            require(rem == [0], "cyclotomic exact quotient")
    return tuple(p)


def characters(a, n):
    adj = adjugate(a)
    k = len(a)
    # Rows of adj(A) are columns of adj(A)^T, hence killed by A^T mod N.
    generators = [tuple(x % n for x in row) for row in adj]
    seen = {(0,) * k}
    queue = list(seen)
    for v in queue:
        for g in generators:
            w = tuple((x + y) % n for x, y in zip(v, g))
            if w not in seen:
                seen.add(w)
                queue.append(w)
                require(len(seen) <= n, "too many character vectors")
    require(len(seen) == n, "character cardinality")
    at = list(map(list, zip(*a)))
    require(all(all(x % n == 0 for x in matvec(at, r)) for r in seen),
            "character relation")
    return sorted(seen)


def upper(case, fault=None):
    aa, bb = case["a"], case["b"]
    k = len(aa)
    require(k == len(bb) and k >= 1, "exponent arity")
    require(all(type(a) is int and type(b) is int and a >= b >= 1
                for a, b in zip(aa, bb)), "exponent range")
    q = [b + 1 for b in bb]
    delta = [a - b for a, b in zip(aa, bb)]
    dd = [a + b for a, b in zip(aa, bb)]
    n = prod(q) + sum(delta[i] * prod(q[j] for j in range(k) if j != i)
                     for i in range(k))
    require(n == case["rank"], "claimed rank")
    a = [[q[i] * (i == j) + delta[i] for j in range(k)] for i in range(k)]
    if fault == "transpose":
        a = list(map(list, zip(*a)))
    require(det(a) == n, "lattice determinant")
    adj = adjugate(a)
    require(all(sum(a[i][r] * adj[r][j] for r in range(k)) == n * (i == j)
                for i in range(k) for j in range(k)), "adjugate identity")
    pts = characters(a, n)
    if fault == "remove_character":
        pts.pop()
    if fault == "corrupt_character":
        pts[0] = tuple([1] + [0] * (k - 1))
    target = list(aa)
    if fault == "phase":
        target[0] -= 1
    total_coefficients = 0
    phi = cyclotomic(n)
    for e in product(*(range(d + 1) for d in dd)):
        u = [e[i] - aa[i] for i in range(k)]
        member = all(x % n == 0 for x in matvec(adj, u))
        require(member == (list(e) == aa), "coefficient-box lattice collision")
        counts = [0] * n
        for r in pts:
            power = sum(r[i] * (e[i] - target[i]) for i in range(k)) % n
            counts[power] += 1
        _, remainder = polydiv(counts, phi)
        expected = [n] if list(e) == aa else [0]
        require(remainder == expected, "actual cyclotomic coefficient sum")
        # Includes binomial normalization; no recognition of floating numbers.
        coefficient = F(prod(comb(dd[i], e[i]) for i in range(k)),
                        n * prod(comb(dd[i], aa[i]) for i in range(k)))
        require(coefficient * remainder[0] == (list(e) == aa),
                "normalized target coefficient")
        total_coefficients += 1
    return {"a": aa, "b": bb, "rank": n, "coefficients": total_coefficients}


def polymul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def cubature(d, moments):
    # Interpolating on 0,...,d deliberately includes a zero node.
    nodes = list(map(F, range(d + 1)))
    weights = []
    for j, z in enumerate(nodes):
        poly = [F(1)]
        denominator = F(1)
        for r, y in enumerate(nodes):
            if r != j:
                poly = polymul(poly, [-y, F(1)])
                denominator *= z - y
        weights.append(sum(c * moments[e] for e, c in enumerate(poly)) / denominator)
    require(all(weights), "nonzero cubature weights")
    return nodes, weights


def lower(case, fault=None):
    dd, bb = case["d"], case["b"]
    k = len(dd)
    require(k == len(bb) and all(d >= 2 * b and b >= 1 for d, b in zip(dd, bb)),
            "moment degree range")
    tt = [F(i + 1, i + 3) for i in range(k)]
    mm = [[F(1, e + 1) if e <= b else F(0) for e in range(d + 1)]
          for d, b in zip(dd, bb)]
    univariate = [cubature(dd[i], mm[i]) for i in range(k)]
    indices = list(product(*(range(d + 1) for d in dd)))
    nodes = [tuple(univariate[i][0][ix[i]] for i in range(k)) for ix in indices]
    weights = [prod(univariate[i][1][ix[i]] for i in range(k)) for ix in indices]
    # Split one node into two identical ones, with both weights nonzero.
    # The full Gram verification now also tests repeated nodes directly.
    nodes.append(nodes[0])
    weights.append(weights[0] / 3)
    weights[0] *= F(2, 3)
    if fault == "weight":
        weights[0] += 1
    for ee in product(*(range(d + 1) for d in dd)):
        actual = sum(w * prod(z[i] ** ee[i] for i in range(k))
                     for z, w in zip(nodes, weights))
        require(actual == prod(mm[i][ee[i]] for i in range(k)), "cubature moment")
    hs = [tuple(1 + tt[i] * z[i] for i in range(k)) for z in nodes]
    require(all(all(h) for h in hs), "chart poles")
    wt = [w * prod(h[i] ** dd[i] for i in range(k)) for w, h in zip(weights, hs)]
    vectors, tags = [], []
    for ee in product(*(range(b + 1) for b in bb)):
        tags.append(("U", ee))
        vectors.append([prod(z[i] ** ee[i] / h[i] ** bb[i] for i in range(k))
                        for z, h in zip(nodes, hs)])
    for i in range(k):
        others = [j for j in range(k) if j != i]
        for s in range(bb[i] + 1, dd[i] - bb[i] + 1):
            for ee in product(*(range(bb[j] + 1) for j in others)):
                tags.append((i, s, ee))
                vectors.append([z[i] ** s / h[i] ** s * prod(
                    z[j] ** e / h[j] ** bb[j] for j, e in zip(others, ee))
                                for z, h in zip(nodes, hs)])
    n = prod(b + 1 for b in bb) + sum(
        (dd[i] - 2 * bb[i]) * prod(bb[j] + 1 for j in range(k) if j != i)
        for i in range(k))
    require(len(vectors) == n == case["rank"], "Gram list size")
    gram = [[F(0)] * n for _ in range(n)]
    for p in range(n):
        for r in range(p, n):
            value = sum(w * x * y for w, x, y in zip(wt, vectors[p], vectors[r]))
            gram[p][r] = gram[r][p] = value
            tp, tr = tags[p], tags[r]
            if tp[0] != tr[0]:
                require(value == 0, "cross-block Gram orthogonality")
            if tp[0] != "U" and tp[0] == tr[0] and tp[1] + tr[1] <= dd[tp[0]]:
                require(value == 0, "internal anti-triangular zero")
    if fault == "duplicate_vector":
        gram[-1] = gram[-2][:]
        for row in gram:
            row[-1] = row[-2]
    require(det(gram) != 0, "full evaluated Gram determinant")
    for d, b in zip(dd, bb):
        for z in (F(0), F(1), F(-2, 3)):
            t = F(5, 7)
            left = z ** (d + 1) / (1 + t * z)
            remainder = (-1) ** (d + 1 - b) * z ** b * t ** (-(d + 1 - b)) / (1 + t * z)
            if fault == "laurent_sign":
                remainder = -remainder
            right = sum((-1) ** (d - p) * z ** p * t ** (-(d + 1 - p))
                        for p in range(b, d + 1)) + remainder
            require(left == right, "finite Laurent division identity")
    return {"d": dd, "b": bb, "rank": n, "nodes_with_repeat": len(nodes),
            "zero_coordinates": True, "Gram_determinant_nonzero": True}


def rejects(name, operation):
    try:
        operation()
    except SystemExit as exc:
        require(str(exc).startswith("REJECT: "), "unexpected control exit")
        return {"control": name, "rejected": str(exc)}
    raise SystemExit("REJECT: negative control accepted: " + name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, default=Path(__file__).with_name("fixtures.json"))
    args = parser.parse_args()
    fixtures = json.loads(args.fixtures.read_text())
    require(set(fixtures) == {"upper", "lower"}, "fixture keys")
    upper_results = [upper(c) for c in fixtures["upper"]]
    lower_results = [lower(c) for c in fixtures["lower"]]
    unequal = next(c for c in fixtures["upper"] if c["a"] == [2, 4, 5])
    base = fixtures["upper"][0]
    bad = copy.deepcopy(base)
    bad["rank"] += 1
    controls = [rejects("wrong claimed rank", lambda: upper(bad))]
    for fault in ("transpose", "remove_character", "corrupt_character", "phase"):
        controls.append(rejects(fault, lambda fault=fault: upper(unequal, fault)))
    for fault in ("weight", "duplicate_vector", "laurent_sign"):
        controls.append(rejects(fault, lambda fault=fault: lower(fixtures["lower"][0], fault)))
    print(json.dumps({"status": "PASS", "scope": "finite exact regressions only",
                      "upper": upper_results, "lower": lower_results,
                      "negative_controls": controls}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
