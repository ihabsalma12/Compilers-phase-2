from tokens import *
from table import *
from stack import *

# tokenization class in 'tokens.py'
ts = TokenStream()

# parse table (grammar hard-coded) class in 'table.py'
ptable = Ptable()

# parse stack class in 'stack.py'
pstack = Pstack(ptable.updated_rules, ptable.Table, ptable.rows, ptable.cols, ts.token_type_list)
x = pstack.parse()
print("ans x =", x)
if x == 1:
    pass  # print 'accepted' + tree
else:
    pass  # print 'rejected'