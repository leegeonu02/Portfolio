class Stack:
	def __init__(self):
		self.items = []

	def push(self, val):
		self.items.append(val)

	def pop(self):
		try:
			return self.items.pop()
			
		except IndexError:
			print("INVALID_EXPRESSION")
			
	def top(self):
		try:
			return self.items[-1]
			
		except IndexError:
			print("INVALID_EXPRESSION")

	def __len__(self):
		return len(self.items)
	
	def isEmpty(self):
		return self.__len__() == 0

def search_Error(expr):
	possible = list('0123456789.()+-*/^')
	integers = list('0123456789')
	operators = list('+-*/^')
	opstack = Stack()

	open_parentheses = 0
	
	for i in range(len(expr)):
		if expr[i] not in possible:            
			return i
		
		elif i == 0 and expr[i] in operators:     
			return i
		
		elif expr[i] == '(':                        
			if i > 0 and expr[i - 1] in integers:  
				return i
			open_parentheses += 1
			opstack.push('(') 

		elif expr[i] in operators:
			if i + 1 == len(expr):               
				return i
			else:                                  
				if expr[i + 1] in operators:
					return i + 1
					
		elif expr[i] == ')':                    
			if opstack.isEmpty():                        
				return i          

			elif open_parentheses == 0:
				return i
            
			elif i != len(expr) - 1 and expr[i + 1] in integers:
				return i + 1                        
            
			else:
				open_parentheses -= 1
				opstack.push(')')   

	if open_parentheses != 0:
		return "INVALID_EXPRESSION"
	
	if not opstack.isEmpty():                             
		if opstack.pop() == '(':
			return len(expr)  
		
def get_token_list(expr):
	numbers = list('0123456789.')
	recognized = []

	i = 0

	while i < len(expr):
		j = 1
		if expr[i] in numbers:
			while i + j < len(expr):
				if expr[i + j] in numbers:
					j += 1
				
				else:
					break

			str(recognized.append(''.join(expr[i:i + j])))
			i += j

		else:
			str(recognized.append(expr[i]))
			i += 1

	return recognized

priority = {'(' : 1, ')' : 1, '+' : 2, '-' : 2, '*' : 3, '/' : 3, '^' : 4}
	
def infix_to_postfix(token_list):
	opstack = Stack()
	outstack = []
	
	for token in token_list:
		if token == '(':
			opstack.push(token)

		elif token == ')':
			while opstack.top() != '(':
				outstack.append(opstack.pop())
			opstack.pop()

		elif token in priority:
			while not opstack.isEmpty():
				if priority[opstack.top()] >= priority[token]:
					outstack.append(opstack.pop())

				else:
					break

			opstack.push(token)

		else:
			outstack.append(token)

	while not opstack.isEmpty():
		outstack.append(opstack.pop())

	return outstack
	
def compute_postfix(outstack):
	opstack = Stack()

	for token in outstack:
		if token in priority:
			num1 = float(opstack.pop())
			num2 = float(opstack.pop())

			if token == '+':
				opstack.push(num2 + num1)
			elif token == '-':
				opstack.push(num2 - num1)
			elif token == '*':
				opstack.push(num2 * num1)
			elif token == '/':
				if num1 != 0:
					opstack.push(num2 / num1)
				else:
					return print("ZERO_DIVISION_ERROR")
			elif token == '^':
				opstack.push(num2 ** num1)
		else:
			opstack.push(token)

	return opstack.pop()
	
# 입력받아 계산기 함수들 차례로 호출
expr = list(input().replace(" ", ""))

if search_Error(expr) != None:
	print("INVALID_EXPRESSION")

else:
	result = compute_postfix(infix_to_postfix(get_token_list(expr)))

	if str(type(result)) == "<class 'float'>":
		print(f"{result:.3f}")