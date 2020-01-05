# this file is a tokenizer.
from enum import Enum
import re
import sys


class tokenType(Enum):
    KEYWORD = 1
    SYMBOL = 2
    IDENTIFIER = 3
    INT_CONST = 4
    STRING_CONST = 5


# class keyWord(Enum):
#     CLASS = 1
#     METHOD = 2
#     FUNCTION = 3
#     CONSTRUCTOR = 4
#     INT = 5
#     BOOLEAN = 6
#     CHAR = 7
#     VOID = 8
#     VAR = 9
#     STATIC = 10
#     FIELD = 11
#     LET = 12
#     DO = 13
#     IF = 14
#     ELSE = 15
#     WHILE = 16
#     RETURN = 17
#     TRUE = 18
#     FALSE = 19
#     NULL = 20
#     THIS = 21


class JackTokenizer:
    def __init__(self, inputFile):
        self.file = inputFile  # a file after open. not a dir
        self.cur_token = None
        self.cur_line = ""
        self.cur_line_iterator = None
        self.stringRegex = '\"\w*\"'
        self.intRegex = "\d+"
        self.keyWordRegex = "class|method|function|constructor|int|boolean|char|" \
                            "void|var|static|field|let|do|if|else|while|return|true|false|null|this"
        self.symbolRegex = "{|}|\[|\]|\(|\)|\.|,|;|\+|-|\*|\/|&|\||<|>|=|~"
        self.identifierRegex = "\w+"
        self.ultimateRegex = self.stringRegex + "|" + self.intRegex + "|" + \
                             self.keyWordRegex + "|" + self.identifierRegex + "|" + self.symbolRegex
        self._hasMoreTokens = True
        self.curIndex = 0
        self.longComment = False

        # start working
        # self.file = open(inputFile, "r")
        self._advance_line()
        self.cur_line_iterator = self._slice_line(self.cur_line)

    def hasMoreTokens(self):
        return self._hasMoreTokens

    def _advance_line(self):
        '''
        :return: true if not EOF
        '''
        self.cur_line = self.file.readline()
        # isComment = False

        while self.cur_line.startswith(("//", "\n", "/*")):
            # isComment = True
            if self.cur_line.startswith(("/*")):
                self.longComment = True
                if self.cur_line.endswith('*/\n') or self.cur_line.endswith('*/\r'):
                    self.longComment = False
            self.cur_line = self.file.readline()
            print("line", self.cur_line)

        while self.longComment:
            if self.cur_line.endswith('*/'):
                self.longComment = False
            self.cur_line = self.file.readline()
            print("long comment, line", self.cur_line)
        # while self.cur_line.startswith(("//", "\n")):
        #     self.cur_line = self.file.readline()
        bool = not (self.cur_line == "")
        self.cur_line = self.cur_line.replace("\t", "")
        self.cur_line = self.cur_line.replace("\r", "")
        self.cur_line = self.cur_line.replace("\n", "")
        return bool

    def _slice_line(self, line):
        '''
        :return: list of tokens in line
        '''
        line = line.strip()
        if line == "":
            return ""
        # slice comments:
        # TODO complete the slicing of comments

        it = re.finditer(self.ultimateRegex, line)
        lst = [str(i.group().split())[2:-2] for i in it]
        return lst
        # return re.finditer(self.ultimateRegex, line)

    def advance(self):
        try:
            self.cur_token = self.cur_line_iterator[self.curIndex]
            self.curIndex += 1
        except IndexError:
            self.curIndex = 0
            self._hasMoreTokens = self._advance_line()
            if not self._hasMoreTokens:
                exit(0)
            self.cur_line_iterator = self._slice_line(self.cur_line)
            self.advance()

    def tokenType(self):
        # print(self.cur_token)
        stringMatch = re.compile(self.stringRegex)
        if re.compile(self.stringRegex).match(self.cur_token):
            return tokenType.STRING_CONST
        if re.compile(self.intRegex).match(self.cur_token):
            return tokenType.INT_CONST
        if re.compile(self.keyWordRegex).match(self.cur_token):
            return tokenType.KEYWORD
        if re.compile(self.symbolRegex).match(self.cur_token):
            return tokenType.SYMBOL
        if re.compile(self.identifierRegex).match(self.cur_token):
            return tokenType.IDENTIFIER

    def keyWord(self):
        return self.cur_token

    def symbol(self):
        return self.cur_token

    def identifier(self):
        return self.cur_token

    def intVal(self):
        return self.cur_token

    def stringVal(self):
        print("token:" + self.cur_token)
        return self.cur_token



if __name__ == '__main__':
    f = open(sys.argv[1], 'r')
    tokenizer = JackTokenizer(f)
    while tokenizer.hasMoreTokens():
        tokenizer.advance()
        print("<" + str(tokenizer.tokenType().name) + ">" + " " + tokenizer.cur_token)
