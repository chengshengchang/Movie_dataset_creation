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
from unittest import result

from numpy import number

# regular expression pattern 
numbers = r'\d+(,\d{3})*\.*\d*'
amounts = r'thousand|million|billion'

value_re = rf'\${numbers}'
word_re = rf'\${numbers}(-|\sto\s)?({numbers})?\s({amounts})'

def parse_value_syntax(string):
    # strip ',' cuz need to convert strings to float
    value = float(re.search(numbers , string ).group().replace(',',''))
    return value

def parse_word_syntax(string):
    
    if 'thousand' in string:
        value = float(re.search(numbers , string).group())
        word = float(re.search(amounts , string,flags=re.I).group().replace('thousand', '1000'))

    elif 'million' in string:
        value = float(re.search(numbers, string).group())
        word = float(re.search(amounts , string,flags=re.I).group().replace('million', '1000000'))

    elif 'billion' in string:
        value = float(re.search(numbers , string).group())
     
        word = float(re.search(amounts , string,flags=re.I).group().replace('billion', '1000000000'))
     
  
    


    return value*word

def money_conversion(money):
    
    # Handle with money with type:List
    if isinstance(money , list):
        money = money[0]
     
    # booling value check if the syntax exist 
    word_syntax = re.search(word_re , money)
    value_syntax = re.search(value_re, money)

    if word_syntax:
       
        value = parse_word_syntax(money)
    elif value_syntax:
        value  = parse_value_syntax(money)
    return value 
         

# print(re.search(amounts,'$12.2-12.2 million').group())
print(money_conversion('$12.2 to 123.123 thousand'))