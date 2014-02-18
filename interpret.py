class Context(dict):
  def __init__(self, scope, parent=None):
    self.scope = scope
    self.parent = parent

  def get_context(self, identifier):
    if self.scope.get(identifier):
      return self.scope.get(identifier)
    elif self.parent:
      return self.parent.get_context(identifier)

library = {
  'car': lambda x: x[0],
  'cdr': lambda x: x[1:],
}

def spec_lambda(input, context):
  def anon(*args):
    lambda_arguments = args[0]
    lambda_scope = {}
    for index, val in enumerate(input[1]):
      lambda_scope[val['value']] = lambda_arguments[index]

    return interpret(input[2], Context(lambda_scope, context))

  return anon

special = {
  'lambda': spec_lambda
}

def interpretList(input, context):
  print input
  if isinstance(input[0], dict) and input[0]['value'] in special.keys():
    return special[input[0]['value']](input, context)
  else:
    l = map(lambda x: interpret(x, context), input)
    if hasattr(l[0], '__call__'):
      return l[0].__call__(l[1:])
    else:
      return l

def interpret(input, context=None):
  if context is None:
    return interpret(input, Context(library))
  elif isinstance(input, list):
    return interpretList(input, context)
  elif input['type'] == 'identifier':
    return context.get_context(input['value'])
  else:
    return input['value']

