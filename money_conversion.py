'''
    TODO money conversion 

    1. money_conversion("$12.2 million") -> 12200000
    2. money_conversion("$790,000") -> 790000

    TODO 

    common work 
    1. strip('$')
    2. strip(',')
    3. strip('.')

    Individul Task
    for task 1 
    1. turn million to int(100000) * int(money) after strip(common work)

    for task 2 
    turn money that after strip into int(money )

    use import re -> regular expression

'''

import re 

# regular expression pattern 
numbers = r'\d+(,\d{3})*\.*\d*'

print(re.search(numbers , '188,000.2').group())

def money_conversion(money):
    pass