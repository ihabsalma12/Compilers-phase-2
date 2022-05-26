
class Pstack:
    def __init__(self, rules, parsing_table, rows, cols, token_stream):
        print("\nmade stack!!")
        self.rows = rows
        self.cols = cols
        self.rules = rules
        self.Table = parsing_table
        self.ipstr = token_stream
        self.ipstr.append('$')

        self.parse_stack = []
        self.actions = []
        self.ipstr_ptr = 0
        self.ipstr_ptr_char = self.ipstr[self.ipstr_ptr]
        self.parse_stack.append(0)
        self.exit_flag = 0

    def shift(self):
        self.parse_stack.append(self.ipstr_ptr_char)
        self.ipstr_ptr += 1
        self.ipstr_ptr_char = self.ipstr[self.ipstr_ptr]
        s = self.Table[self.i][self.j]
        new_state = ''.join(i for i in s if i.isdigit())
        self.parse_stack.append(int(new_state))
        self.actions.append("shift " + str(new_state))

    def reduce(self):
        s = self.Table[self.i][self.j]
        num = int(''.join(i for i in s if i.isdigit()))
        print("rules:", self.rules)
        print("reduce product num=", num)
        prod_num = self.rules[int(num)]  # Rnum in table
        print("prod_num=", prod_num)
        LHSprod = prod_num[0]  # non-term string
        RHSprod = prod_num[1]  # list of strings
        pop_length = len(RHSprod) * 2
        print("LHSprod=", LHSprod, "RHSprod=", RHSprod, "pop_length=", pop_length)
        while (pop_length > 0):
            del self.parse_stack[-1]
            pop_length -= 1
        old_state = self.parse_stack[-1]
        try:
            col = self.cols.index(LHSprod)
            print("old_state:", old_state, "col:", col, "(symbol=", LHSprod, ")")
        except:
            self.reject()
            return
        try:
            s = self.Table[old_state][col]
            print("s=",s)
            new_state = int(''.join(i for i in s if i.isdigit()))
        except:
            self.reject()
            return
        self.parse_stack.append(LHSprod)
        self.parse_stack.append(new_state)
        str_RHSprod = ' '.join(RHSprod)
        self.actions.append("reduce by " + LHSprod + " -> " + str_RHSprod)


    def accept(self):
        self.actions.append("accept")
        print("accepted")
        self.exit_flag = 1

    def reject(self):
        self.actions.append("reject")
        print("rejected")
        self.exit_flag = -1

    def parse(self):
        #if 'UNIDENTIFIABLE' in self.ipstr:
         #   return -1
        while True:
            print("ip ptr is at [index]=", self.ipstr_ptr, "char @ ip ptr=", self.ipstr_ptr_char)
            print("stack is now:", self.parse_stack)
            print("actions so far:", self.actions, '\n')
            try:
                self.i = self.rows[self.parse_stack[-1]]
                self.j = self.cols.index(self.ipstr_ptr_char)
                cell = self.Table[self.i][self.j][0]
                print("haha gotta check i=", self.i, "j=", self.j)
            except:
                print("rejected because cannot find i or j/ cell is empty")
                self.reject()
                return -1
            if self.exit_flag != 0:
                return 1
            if  cell == 'S':
                print("shift op")
                self.shift()
            elif cell == 'R':
                print("reduce op")
                self.reduce()
            elif cell == 'A':
                print("accept op")
                self.accept()


"""
parse_stack.push(0)
input_string = "aabb"
actions = [] #what operations were chosen
input_ptr = 0
ptr_char = input_string[input_ptr]
loop:
check Iparse_stack.top() and ptr_char in the Table, and call operation according to what you find:
1) empty - reject
2) accepted - accept
3) Snum - shift operation
def accept:
    actions.push("accept")
def shift:
    input_ptr++
    ptr_char = input_string[input_ptr]
    parse_stack.push(ptr_char)
    parse_stack.push(num) #Snum in table
    actions.push("shift")
4) Rnum - reduce operation
def reduce:
    prod = get prod num from rules #Rnum in table
    pop_length = len(RHSprod) * 2
    while(pop_length > 0):
        parse_stack.pop()
        pop_length -= 1
    old_state = parse_stack.top()
    parse_stack.push(LHSprod)
    new_state = check I-old_state- and LHSprod in table
    parse_stack.push(new_state)
    actions.push("reduce by -prod-")
"""