import copy

class Ptable:
    # perform grammar augmentation
    def grammarAugmentation(self, rules, nonterm_userdef, start_symbol):
        # newRules stores processed output rules
        newRules = []

        # create unique 'symbol' to
        # - represent new start symbol
        newChar = start_symbol + "'"
        while (newChar in nonterm_userdef):
            newChar += "'"

        # adding rule to bring start symbol to RHS
        newRules.append([newChar,
                         ['.', start_symbol]])

        # new format => [LHS,[.RHS]],
        # can't use dictionary since
        # - duplicate keys can be there
        for rule in rules:

            # split LHS from RHS
            k = rule.split("->")
            lhs = k[0].strip()
            rhs = k[1].strip()

            # split all rule at '|'
            # keep single derivation in one rule
            multirhs = rhs.split('|')
            for rhs1 in multirhs:
                rhs1 = rhs1.strip().split()

                # ADD dot pointer at start of RHS
                rhs1.insert(0, '.')
                newRules.append([lhs, rhs1])
        return newRules

    # find closure
    def findClosure(self, input_state, dotSymbol):
        #self.start_symbol, \
         #   self.separatedRulesList, \
          #  self.statesDict

        # closureSet stores processed output
        self.closureSet = []

        # if findClosure is called for
        # - 1st time i.e. for I0,
        # then LHS is received in "dotSymbol",
        # add all rules starting with
        # - LHS symbol to closureSet
        if dotSymbol == self.start_symbol:
            for rule in self.separatedRulesList:
                if rule[0] == dotSymbol:
                    self.closureSet.append(rule)
        else:
            # for any higher state than I0,
            # set initial state as
            # - received input_state
            self.closureSet = input_state

        # iterate till new states are
        # - getting added in closureSet
        prevLen = -1
        while prevLen != len(self.closureSet):
            prevLen = len(self.closureSet)

            # "tempClosureSet" - used to eliminate
            # concurrent modification error
            tempClosureSet = []

            # if dot pointing at new symbol,
            # add corresponding rules to tempClosure
            for rule in self.closureSet:
                indexOfDot = rule[1].index('.')
                if rule[1][-1] != '.':
                    dotPointsHere = rule[1][indexOfDot + 1]
                    for in_rule in self.separatedRulesList:
                        if dotPointsHere == in_rule[0] and \
                                in_rule not in tempClosureSet:
                            tempClosureSet.append(in_rule)

            # add new closure rules to closureSet
            for rule in tempClosureSet:
                if rule not in self.closureSet:
                    self.closureSet.append(rule)
        return self.closureSet

    def compute_GOTO(self, state):
        #self.statesDict, self.stateCount

        # find all symbols on which we need to
        # make function call - GOTO
        generateStatesFor = []
        for rule in self.statesDict[state]:
            # if rule is not "Handle"
            if rule[1][-1] != '.':
                indexOfDot = rule[1].index('.')
                dotPointsHere = rule[1][indexOfDot + 1]
                if dotPointsHere not in generateStatesFor:
                    generateStatesFor.append(dotPointsHere)

        # call GOTO iteratively on all symbols pointed by dot
        if len(generateStatesFor) != 0:
            for symbol in generateStatesFor:
                self.GOTO(state, symbol)
        return

    def GOTO(self, state, charNextToDot):
        #self.statesDict, self.stateCount, self.stateMap

        # newState - stores processed new state
        newState = []
        for rule in self.statesDict[state]:
            indexOfDot = rule[1].index('.')
            if rule[1][-1] != '.':
                if rule[1][indexOfDot + 1] == \
                        charNextToDot:
                    # swapping element with dot,
                    # to perform shift operation
                    shiftedRule = copy.deepcopy(rule)
                    shiftedRule[1][indexOfDot] = \
                        shiftedRule[1][indexOfDot + 1]
                    shiftedRule[1][indexOfDot + 1] = '.'
                    newState.append(shiftedRule)

        # add closure rules for newState
        # call findClosure function iteratively
        # - on all existing rules in newState

        # addClosureRules - is used to store
        # new rules temporarily,
        # to prevent concurrent modification error
        addClosureRules = []
        for rule in newState:
            indexDot = rule[1].index('.')
            # check that rule is not "Handle"
            if rule[1][-1] != '.':
                closureRes = \
                    self.findClosure(newState, rule[1][indexDot + 1])
                for rule in closureRes:
                    if rule not in addClosureRules \
                            and rule not in newState:
                        addClosureRules.append(rule)

        # add closure result to newState
        for rule in addClosureRules:
            newState.append(rule)

        # find if newState already present
        # in Dictionary
        stateExists = -1
        for state_num in self.statesDict:
            if self.statesDict[state_num] == newState:
                stateExists = state_num
                break

        # stateMap is a mapping of GOTO with
        # its output states
        if stateExists == -1:

            # if newState is not in dictionary,
            # then create new state
            self.stateCount += 1
            self.statesDict[self.stateCount] = newState
            self.stateMap[(state, charNextToDot)] = self.stateCount
        else:

            # if state repetition found,
            # assign that previous state number
            self.stateMap[(state, charNextToDot)] = stateExists
        return

    def generateStates(self, statesDict):
        prev_len = -1
        called_GOTO_on = []

        # run loop till new states are getting added
        while (len(statesDict) != prev_len):
            prev_len = len(statesDict)
            keys = list(statesDict.keys())

            # make compute_GOTO function call
            # on all states in dictionary
            for key in keys:
                if key not in called_GOTO_on:
                    called_GOTO_on.append(key)
                    self.compute_GOTO(key)
        return

    # calculation of first
    # epsilon is denoted by '#' (semi-colon)

    # pass rule in first function
    def first(self, rule):
        #global rules, nonterm_userdef, \
         #   term_userdef, diction, firsts

        # recursion base condition
        # (for terminal or epsilon)
        if len(rule) != 0 and (rule is not None):
            if rule[0] in self.term_userdef:
                return rule[0]
            elif rule[0] == '#':
                return '#'

        # condition for Non-Terminals
        if len(rule) != 0:
            if rule[0] in list(self.diction.keys()):

                # fres temporary list of result
                fres = []
                rhs_rules = self.diction[rule[0]]

                # call first on each rule of RHS
                # fetched (& take union)
                for itr in rhs_rules:
                    indivRes = self.first(itr)
                    if type(indivRes) is list:
                        for i in indivRes:
                            fres.append(i)
                    else:
                        fres.append(indivRes)

                # if no epsilon in result
                # - received return fres
                if '#' not in fres:
                    return fres
                else:

                    # apply epsilon
                    # rule => f(ABC)=f(A)-{e} U f(BC)
                    newList = []
                    fres.remove('#')
                    if len(rule) > 1:
                        ansNew = self.first(rule[1:])
                        if ansNew != None:
                            if type(ansNew) is list:
                                newList = fres + ansNew
                            else:
                                newList = fres + [ansNew]
                        else:
                            newList = fres
                        return newList

                    # if result is not already returned
                    # - control reaches here
                    # lastly if eplison still persists
                    # - keep it in result of first
                    fres.append('#')
                    return fres

    # calculation of follow
    def follow(self, nt):
        # start_symbol, rules, nonterm_userdef, \
            #term_userdef, firsts, follows, diction

        # for start symbol return $ (recursion base case)
        solset = set()
        if nt == self.start_symbol:
            # return '$'
            solset.add('$')

        # check all occurrences
        # solset - is result of computed 'follow' so far

        # For input, check in all rules
        for curNT in self.diction:
            rhs = self.diction[curNT]

            # go for all productions of NT
            for subrule in rhs:
                if nt in subrule:

                    # call for all occurrences on
                    # - non-terminal in subrule
                    while nt in subrule:
                        index_nt = subrule.index(nt)
                        subrule = subrule[index_nt + 1:]

                        # empty condition - call follow on LHS
                        if len(subrule) != 0:

                            # compute first if symbols on
                            # - RHS of target Non-Terminal exists
                            res = self.first(subrule)

                            # if epsilon in result apply rule
                            # - (A->aBX)- follow of -
                            # - follow(B)=(first(X)-{ep}) U follow(A)
                            if '#' in res:
                                newList = []
                                res.remove('#')
                                ansNew = self.follow(curNT)
                                if ansNew != None:
                                    if type(ansNew) is list:
                                        newList = res + ansNew
                                    else:
                                        newList = res + [ansNew]
                                else:
                                    newList = res
                                res = newList
                        else:

                            # when nothing in RHS, go circular
                            # - and take follow of LHS
                            # only if (NT in LHS)!=curNT
                            if nt != curNT:
                                res = self.follow(curNT)

                        # add follow result in set form
                        if res is not None:
                            if type(res) is list:
                                for g in res:
                                    solset.add(g)
                            else:
                                solset.add(res)
        return list(solset)

    def createParseTable(self, statesDict, stateMap, T, NT):
        #self.separatedRulesList, self.diction

        # create rows and cols
        self.rows = list(self.statesDict.keys())
        self.cols = T + ['$'] + NT

        # create empty table
        self.Table = []
        tempRow = []
        for y in range(len(self.cols)):
            tempRow.append('')
        for x in range(len(self.rows)):
            self.Table.append(copy.deepcopy(tempRow))

        # make shift and GOTO entries in table
        for entry in stateMap:
            state = entry[0]
            symbol = entry[1]
            # get index
            a = self.rows.index(state)
            b = self.cols.index(symbol)
            if symbol in NT:
                self.Table[a][b] = self.Table[a][b] \
                              + f"{stateMap[entry]} "
            elif symbol in T:
                self.Table[a][b] = self.Table[a][b] \
                              + f"S{stateMap[entry]} "

        # start REDUCE procedure

        # number the separated rules
        numbered = {}
        key_count = 0
        for rule in self.separatedRulesList:
            tempRule = copy.deepcopy(rule)
            tempRule[1].remove('.')
            numbered[key_count] = tempRule
            key_count += 1

        # start REDUCE procedure
        # format for follow computation
        addedR = f"{self.separatedRulesList[0][0]} -> " \
                 f"{self.separatedRulesList[0][1][1]}"
        self.rules.insert(0, addedR)
        for rule in self.rules:
            k = rule.split("->")

            # remove un-necessary spaces
            k[0] = k[0].strip()
            k[1] = k[1].strip()
            rhs = k[1]
            multirhs = rhs.split('|')

            # remove un-necessary spaces
            for i in range(len(multirhs)):
                multirhs[i] = multirhs[i].strip()
                multirhs[i] = multirhs[i].split()
            self.diction[k[0]] = multirhs

        # find 'handle' items and calculate follow.
        for stateno in statesDict:
            for rule in statesDict[stateno]:
                if rule[1][-1] == '.':

                    # match the item
                    temp2 = copy.deepcopy(rule)
                    temp2[1].remove('.')
                    for key in numbered:
                        if numbered[key] == temp2:

                            # put Rn in those ACTION symbol columns,
                            # who are in the follow of
                            # LHS of current Item.
                            follow_result = self.follow(rule[0])
                            for col in follow_result:
                                index = self.cols.index(col)
                                if key == 0:
                                    self.Table[stateno][index] = "Accept"
                                else:
                                    self.Table[stateno][index] = \
                                        self.Table[stateno][index] + f"R{key} "

        return self.rows, self.cols, self.Table

    def printResult(self, rules):
        for rule in rules:
            print(f"{rule[0]} ->"
                  f" {' '.join(rule[1])}")

    def printAllGOTO(self, diction):
        for itr in diction:
            print(f"GOTO ( I{itr[0]} ,"
                  f" {itr[1]} ) = I{self.stateMap[itr]}")

    def printTable(self):
        # printing table
        print("\nSLR(1) parsing table:\n")
        frmt = "{:>14}" * len(self.cols)
        print(" ", frmt.format(*self.cols), "\n")
        ptr = 0
        j = 0
        for y in self.Table:
            frmt1 = "{:>14}" * len(y)
            print(f"{{:>3}} {frmt1.format(*y)}"
                  .format('I' + str(j)))
            j += 1
        # print("rows:", rows)
        # print("cols:", cols)

        self.updated_rules = self.separatedRulesList
        for rule in self.separatedRulesList:
            del rule[1][0]
            # print(rule)

    def __init__(self):
        print("\nmade table!!!!")
        self.rules = ["stmnt-seq -> stmnt-seq statement | statement",
                      "statement -> if-stmnt | assign-stmnt",
                      "if-stmnt -> IF NUM THEN stmnt-seq END",
                      "assign-stmnt -> ID ASSIGN factor SEMICOLON",
                      "factor -> ID | NUM"]
        self.nonterm_userdef = ['stmnt-seq', 'statement', 'if-stmnt', 'assign-stmnt', 'factor']
        self.term_userdef = ['IF', 'THEN', 'END', 'ID', 'ASSIGN', 'SEMICOLON', 'NUM']
        self.start_symbol = self.nonterm_userdef[0]

        print("\ngrammar augmentation: \n")
        self.separatedRulesList = self.grammarAugmentation(self.rules,
                                self.nonterm_userdef,
                                self.start_symbol)
        self.printResult(self.separatedRulesList)

        # find closure
        self.start_symbol = self.separatedRulesList[0][0]
        print("\ncalculated closure: I0\n")
        I0 = self.findClosure(0, self.start_symbol)
        self.printResult(I0)

        # use statesDict to store the states
        # use stateMap to store GOTOs
        self.statesDict = {}
        self.stateMap = {}

        # add first state to statesDict
        # and maintain stateCount
        # - for newState generation
        self.statesDict[0] = I0
        self.stateCount = 0

        # computing states by GOTO
        self.generateStates(self.statesDict)

        # print goto states
        print("\ngenerated states: \n")
        for st in self.statesDict:
            print(f"State = I{st}")
            self.printResult(self.statesDict[st])
            print()

        print("result of GOTO computation:\n")
        self.printAllGOTO(self.stateMap)

        # "follow computation" for making REDUCE entries
        self.diction = {}

        # call createParseTable function
        self.rows, self.cols, self.Table = self.createParseTable(self.statesDict, self.stateMap,
                         self.term_userdef,
                         self.nonterm_userdef)

        self.printTable()