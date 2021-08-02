#trying OOP
#programmer fraIoann i_ingar@mail.ru
#written 02/08/2021


#create a new class stack as child of 'list' class
class stack(list):
    
    #let's define a few new methods of class stack
    def isempty(self):
        if self == []:
            return True
        else:
            return False
    
    def push(self, num):
        self.append(num)   
      
    def top(self):
        return self[-1]
    
    # .pop() irreversibly extracts and returns a top element of stack
    def pop(self):   
        _ = self.top()
        del self[-1]
        return _
    
    #reload some methods parent's class as an example of polymorphism
    #we forbid to use some parant's methods and give error message
    def insert(self, *args):
        print('\033[31m \033[1m Error: \033[0m You could not insert an element. Try .push()')
        
    def remove(self, *args):
        print('\033[31m \033[1m Error: \033[0m You can not remove arbitrary, just top element. Try .pop().')
        
    def reverse(self):
        print('\033[31m \033[1m Error: \033[0m You could not reverse stack.')
        
    def sort(self):
        print('\033[31m \033[1m Error: \033[0m You could not sort stack.')

def rpn_calc():
    '''Function-calculator of expression written in reverse polish notation 
    or postfix notation. Function gets nothing, during excution user input a row
    of values and simbols using postfix notation and execut operations.
    Function returns an answer as a result of expression'''
    
    ops = ['+', '-', '*', '/', '^']
    print('Please, input a values list using reverse polish notation')
    print('\033[31m \033[1m Note: \033[0m using {} symbols for operations'.format(ops))
    row = input().split()
        
    answer = stack()
    
    for arg in row:
        
        if arg.isdigit():
            answer.push(arg)
        
        else:
            x_2 = float(answer.pop())
            x_1 = float(answer.pop())
           
            if arg == ops[0]:
               answer.push(x_1 + x_2)
        
            elif arg == ops[1]:
                answer.push(x_1 - x_2)

            elif arg == ops[2]:
                answer.push(x_1 * x_2)
        
            elif arg == ops[3]:
                answer.push(x_1 / x_2)
                
            elif arg == ops[4]:
                answer.push(x_1 ** x_2)
                    
    return answer.top()

x = rpn_calc()