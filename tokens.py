import re

# example input
"""
if @mxf$ 0 then
y := 5 ;
else x := 5;
end;
ok1 := 50;
ok_2 := 3102.25;
ok_3:= -4.0 ;;
not_ok :=-4?
count-1;ok_4 := -2;
"""

class TokenStream:
    def __init__(self):
        print("\nmade Tok!!")
        self.call_input()

    def user_in(self):  #function to get multiline input from user, return a list (element = 1 line)
        contents = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            contents.append(line)
        return contents

    def prep_str(self, lis): #function to prepare string for tokenization
        my_string = ' '.join(lis) #join lines with spaces
        my_string = my_string.replace(";", " ; ") #any semicolon will have space before and after
        my_string = my_string.replace(":=", " := ") #any semicolon will have space before and after
        return my_string

    def tokenize(self, my_string): #function to return token stream
        my_pattern = re.compile(r"\S+") #matching any sequence of non-whitespaces
        matches = my_pattern.findall(my_string)
        #for match in matches:
        #    print(match)

        token_type_list = []
        for attr in matches:
            #match each attribute to its token type and output the token in angled brackets
            if attr == "if":
                print("<" + attr + ", "+ "IF>")
                token_type_list.append("IF")
                continue
            elif attr == "then":
                print("<" + attr + ", " + "THEN>")
                token_type_list.append("THEN")
                continue
            elif attr == "end":
                print("<" + attr + ", " + "END>")
                token_type_list.append("END")
                continue
            elif attr == ":=":
                print("<" + attr + ", " + "ASSIGN>")
                token_type_list.append("ASSIGN")
                continue
            elif attr == ";":
                print("<" + attr + ", " + "SEMICOLON>")
                token_type_list.append("SEMICOLON")
                continue
            elif re.fullmatch(r"[0-9]+", attr):
                print("<" + attr + ", " + "NUM>")
                token_type_list.append("NUM")
                continue
            elif re.fullmatch(r"[a-zA-Z][a-zA-Z0-9]*", attr):
                print("<" + attr + ", " + "ID>")
                token_type_list.append("ID")
            else: #unidentifiable token
                print("<"+ attr + ", " + "UNIDENTIFIABLE>")
                token_type_list.append("UNIDENTIFIABLE")
        #print("\n--done tokenization--")
        #print("\nTOKEN_LIST: ")
        #print("my tokens!!", token_type_list)
        return token_type_list

    def call_input(self):
        print("To terminate input, press Enter then Ctrl + D")
        lis = self.user_in()
        my_string = self.prep_str(lis)
        self.token_type_list = self.tokenize(my_string)  # function to output token stream