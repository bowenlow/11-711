import sys
from parser import *


for line in sys.stdin:
  stack = [];
  state = 1;
  # 1 is for normal, 2 is for X bracket
  for c in line:
    if c == ' ':
      pass
    #print state
    if state == 1:
      if c == '(':
        state = 2
        pass
      elif c == ')':
        sym = stack.pop()
        if sym == 1:
          sys.stdout.write(')')
          pass
        elif sym == 2:
          pass
      else:
        sys.stdout.write(str(c))
        pass
    elif state == 2:
      if c == '[':
        state = 3
        pass
    elif state == 3:
      if c == 'X':
        state = 4
        stack.append(2);
        pass
      else:
        sys.stdout.write("([")
        sys.stdout.write(c)
        state = 5
        stack.append(1)
        pass
    elif state == 4:
      if c == ']':
        state = 1
        pass
      else:
        pass
    elif state == 5:
      sys.stdout.write(c)
      if c == ']':
        state = 1
        pass
      else:
        pass
