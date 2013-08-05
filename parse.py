def tokenize(expression):
    """
    >>> x ='(lambda (x) x)'
    >>> tokenize(x)
    ['(', 'lambda', '(', 'x', ')', 'x', ')']
    """
    index = 0
    parans = (')', '(')
    expression = expression.replace(',', '')
    while index < len(expression):
        if expression[index] in parans:
            elem = expression[index]
            expression = (expression[:index + parans.index(elem)]
                          + ' ' + expression[index + parans.index(elem):])
            index += 1
        index += 1
    return expression.split()

def parse(tokenized, parsed_list=None):
    """
    >>> x = '(+ 1 2)'
    >>> x = '((lambda (x, y) x + y) "hello" 1)'
    >>> parse(tokenize(x))
    [[{'identifier': 'lambda'}, [{'identifier': 'x'}, {'identifier': 'y'}], {'identifier': 'x'}, {'identifier': '+'}, {'identifier': 'y'}], {'literal': 'hello'}, {'literal': 1}]
    """
    if parsed_list is None:
        parsed_list = []
    if len(tokenized) > 0:
        first_char = tokenized[0]
        if first_char == '(':
            parsed_list = []
            tokenized.pop(0)
            while tokenized[0] != ')':
                parsed_list.append(parse(tokenized, parsed_list))
            tokenized.pop(0)
        elif first_char == ')':
            raise Exception("Syntax Error, unexpected paranthesis")
        elif first_char != ',':
            return categorize_token(tokenized.pop(0))
    return parsed_list

def categorize_token(token):
    """
    """
    if token[0] == token[-1] == '"':
        token = token[1:-1]
    else:
        try:
            token = int(token)
        except ValueError:
            try:
                token = float(token)
            except ValueError:
                return {'identifier': token}
    return {'literal': token}

import doctest
doctest.testmod()
#x ='(lambda (x, y) x y)'
#print tokenize(x)