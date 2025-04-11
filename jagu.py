import re

class Stack:
    def __init__(self):
        self.items = []
        self.idx = -1
        
    def push(self, val):
        self.items.append(val)  
        self.idx += 1
        
    def pop(self):
        if not self.isEmpty(): 
            return self.items.pop()
        else:
            print("Stack is empty.")
            raise IndexError("pop from empty list") 

    def top(self):
        if not self.isEmpty():  
            return self.items[-1]
        else:
            print("Stack is empty.")
            return None

    def __len__(self):
        return len(self.items)
    
    def isEmpty(self):
        return len(self) == 0

    def get_token_list(self, expr):
        token = r'\d+\.\d+|\d+|[\+\-\*/\^\(\)]'  
        tokens = re.findall(token, expr.replace(" ", "")) 
        return tokens

    def infix_to_postfix(self, token_list):
        priority = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}    
        outstack = []                        
        opstack = []               

        for token in token_list:
            if re.match(r'\d+\.\d+|\d+', token):  
                outstack.append(token)
            elif token == '(':                     
                opstack.append(token)
            elif token == ')':                    
                while opstack and opstack[-1] != '(':
                    outstack.append(opstack.pop())
                opstack.pop()  
            elif token in priority:    
                while (opstack and opstack[-1] != '(' and
                       priority.get(opstack[-1], 0) >= priority[token]):
                    outstack.append(opstack.pop())
                opstack.append(token)
            else:
                print("INVALID_EXPRESSION")
                return

        while opstack:
            outstack.append(opstack.pop())

        return outstack

    def compute_postfix(self, token_list):
        stack = []
        try:
            for token in token_list:
                if re.match(r'\d+\.\d+|\d+', token):  
                    stack.append(float(token))
                else:  
                    num1 = stack.pop()  
                    num2 = stack.pop()

                    if token == '+':
                        stack.append(num2 + num1)
                    elif token == '-':
                        stack.append(num2 - num1)
                    elif token == '*':
                        stack.append(num2 * num1)
                    elif token == '/':
                        if num1 == 0:           
                            print("ZERO_DIVISION_ERROR")
                            return
                        stack.append(num2 / num1)
                    elif token == '^':
                        stack.append(num2 ** num1)
        except IndexError:
            print("INVALID_EXPRESSION")
            return

        if len(stack) == 1:
            result = stack.pop()
            print(f"{result:.3f}")
        else:
            print("INVALID_EXPRESSION")

expr = str(input())
stack = Stack()

stack.compute_postfix(stack.infix_to_postfix(stack.get_token_list(expr)))