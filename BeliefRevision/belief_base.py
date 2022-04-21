from sympy import Expr, sympify, symbols, to_cnf
from sortedcontainers import SortedList

class Belief:
    formula: Expr
    order: float
    variables = set()

    def __init__(self, formula: str, order: float = 0) -> None:
        self.formula = sympify(formula)
        self.order = order
        self.variables = self.add_variables(formula)

    def add_variables(self, formula: str):
        variables = set()
        for char in formula:
            if ord(char) >= 65 and ord(char) <= 90 or ord(char) >= 97 and ord(char) <= 122:
                char = symbols(char)
                variables.add(char)
        return variables

    def display(self):
        print(self.formula, self.order, self.variables)

class BeliefBase:
    """A Belief Knowledge Base fr propositional logic."""

    def __init__(self) -> None:
        self.clauses = set()
        self.BeliefBase = {}
        self.variables = set()
    def add_belief(self, belief: Belief):
        from entailment import conjuncts
        self.BeliefBase[belief.formula] = belief.order
        self.variables = self.variables.union(belief.variables)
        self.clauses.update(conjuncts(to_cnf(belief.formula)))

    def display(self, option: str = 'all'):
        if option == 'base':
            print('BeliefBase:',self.BeliefBase)
        elif option == 'var':
            print('variables:', self.variables)
        elif option == 'clauses':
            print('clauses', self.clauses)
        elif option == 'all':
            print('BeliefBase:',self.BeliefBase, '\n', 'variables:', self.variables,'\n', 'clauses', self.clauses)

