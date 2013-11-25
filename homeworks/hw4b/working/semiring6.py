#!/usr/bin/env python
import sys
from parser import *

rules = [ line.strip() for line in open(sys.argv[1]) ]

# You can omit declaring this function except in Section 1
def agendaComparator(item1, item2):
  (startPos1, endPos1, lhs1, value1) = item1
  (startPos2, endPos2, lhs2, value2) = item2
  span1 = endPos1 - startPos1
  span2 = endPos2 - startPos2
  spanDiff = span2 - span1
  if spanDiff != 0: # sort by span length first
    return 1 if spanDiff > 0 else -1
  else:
    posDiff = startPos2 - startPos1
    if posDiff != 0: # then start position
      return 1 if posDiff > 0 else -1
    else: # then the semiring value of the update to the chart
      valDiff = value2 - value1
      return 1 if valDiff < 0 else -1      

# Viterbi
# You can omit declaring the semiring except in Sections 2-3
semiZero = [(0,(), '')]
semiOne = [(1,(), '')]
def semiPlus(a, b): 
  c = a + b
  d = list(set(c))
  if len(d) > 10:
    d.sort(key=lambda tup:tup[0], reverse=True)
    return d[0:10]
  else:
    return d
def semiTimes(a, b):
  x = [];
  for e in a:
    (l1,t1,s1) = e
    for f in b:
      (l2,t2,s2) = f
      if len(t1) == 2:
        x.append((l1*l2, (t1[1]), s1 + ' ' + s2))
      else:
        if not s2:
          x.append((l1*l2, (), '(' + s1 + s2 + ')'))
        else:
          x.append((l1*l2, (), '(' + s1 + ' ' + s2 + ')'))
  y = list(set(x))
  if len(y) > 10:
    y.sort(key=lambda tup:tup[0], reverse=True)
    return y[0:10]
  return y
  
def A(word, startPos, endPos, sOne): return [(1, (), word)]
def R(ruleLhs, ruleRhs, ruleWeight):
  if len(ruleRhs) > 1:
    return [(ruleWeight, ruleRhs, ruleLhs)]
  else:
    s1 = ruleLhs + ' ' + ruleRhs[0]
    return [(ruleWeight, (), s1)]

# You can omit declaring prune() except in Section 5
def prune(item):
  return False

for (i, sent) in enumerate(sys.stdin):
    sent = sent.strip().split()
    # You should omit unused keyword arguments
    # (e.g. leave out agendaCmp except in Section 1)
    # (e.g. always omit the logging options such as dump in your solutions)
    (goalValue, chart, stats) = parse(sent, rules,
                                      #agendaCmp=agendaComparator,
                                      sZero=semiZero, sOne=semiOne, sPlus=semiPlus, sTimes=semiTimes, R=R,
                                      pruner=prune,
                                      dumpAgenda=False, dumpChart=False, logConsidering=False)
    print "SENT {0} AGENDA ADDS: {1}".format(i, stats['agendaAdds'])
    index = min(10,len(goalValue))
    for j in range(index):
      if goalValue[j][0] > 0:
        print "SENT {0} GOAL SCORE K={1}: {2}".format(i, j, goalValue[j][0])
        print "SENT {0} GOAL DERIVATION K={1}: {2}".format(i, j, goalValue[j][2])
