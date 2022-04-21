import copy
from pydoc import resolve
from wsgiref.util import request_uri
from sqlalchemy import true
from sympy import EX, And, Expr, Or, to_cnf, simplify
from belief_base import BeliefBase
from itertools import product


def dissociate(op, args):
    """Given an associative op, return a flattened list result such
    that Expr(op, *result) means the same as Expr(op, *args).
    >>> dissociate('&', [A & B])
    [A, B]
    """
    res = []

    for arg in args:
        if isinstance(arg, op):
            res.extend(*conjuncts(arg.args))
        else:
            res.append(arg)

    return res

def associate(op, args):
    args = dissociate(op, args)
    if len(args) == 0:
        return op.identity
    elif len(args) == 1:
        return args[0]
    else:
        return op(*args)

def conjuncts(formula: Expr) -> list:
    """Return a list of the conjuncts in the sentence s.
    >>> conjuncts(A & B)
    [A, B]
    >>> conjuncts(A | B)
    [(A | B)]
    """
    return dissociate(And, [formula])

def disjuncts(formula: Expr) -> list:
    """Return a list of the disjuncts in the sentence s.
    >>> disjuncts(A | B)
    [A, B]
    >>> disjuncts(A & B)
    [(A & B)]
    """
    return dissociate(Or, [formula])

class Clause:
    def __init__(self, clause, order, parents = []):
        self.clause = clause
        self.order = order
        self.parents = parents

    def __repr__(self):
        return f"{self.clause}"

    def __eq__(self, other):
        return self.clause == other

    def __hash__(self):
        return hash(self.clause)

def pl_resolution(belief_base: BeliefBase, formula: str) -> bool:
    formula: Expr = to_cnf(formula)
    contradiction = to_cnf(~formula)
    clauses_all = []
    final_caluses = set()
    current_order = 0
    new = set()

    belief_base.clauses.update(set(conjuncts(contradiction)))
    clauses_all = list(belief_base.clauses)
    # print('clauses_all: ', clauses_all)
    while True:
        n = len(clauses_all)
        pairs = [(clauses_all[i], clauses_all[j]) for i in range(n) for j in range(i+1, n)]
        for ci, cj in pairs:
            resolvents = pl_resolve(ci, cj)
            if False in resolvents:
                return True
            new = new.union(set(resolvents))
        if new.issubset(clauses_all):
            return False
        for c in new:
            if c not in clauses_all:
                clauses_all.append(c)


def pl_resolve(ci: Expr, cj: Expr)-> list: 
    clauses = []
    disjunct_1 = disjuncts(ci)
    disjunct_2 = disjuncts(cj)

    for dc1, dc2 in product(disjunct_1, disjunct_2):
        if dc1 == ~dc2 or ~dc1 == dc2:
            resolve_p1 = [f for f in disjunct_1 if f != dc1]
            resolve_p2 = [f for f in disjunct_2 if f != dc2]
            parts = resolve_p1 + resolve_p2
            parts = list(set(parts))
            clauses.append(associate(Or, parts))
    return clauses

