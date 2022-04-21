from sympy import O, cot
from belief_base import *
from entailment import *
from sympy import to_cnf, simplify

if __name__ == "__main__":
    belief_base = BeliefBase()
    # b1=Belief("r >> (p|s)",0.5)
    # belief_base.add_belief(b1)
    # b2=Belief("(p|s) >> r",0.5)
    # belief_base.add_belief(b2)
    # b3=Belief("~r",0.4)
    # belief_base.add_belief(b3)
    b4 = Belief("p|q")
    belief_base.add_belief(b4)
    b5 = Belief("p>>q")
    belief_base.add_belief(b5)
    b6 = Belief("q>>p")
    belief_base.add_belief(b6)
    
    # belief_base.add_belief(Belief('~p >> q & q >> p & p >> r & s'))
    belief_base.display('base')
    result = pl_resolution(belief_base, 'p')
    print(result)