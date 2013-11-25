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
semiZero = (0, (), '')
semiOne = (1, (), '')
def semiPlus(a, b): 
  (l1, t1, s1) = a
  (l2, t2 ,s2) = b
  l3 = max(l1,l2)
  s3 = s1;
  if (l1 > l2):
    s3 = s1
    t3 = t1
  else:
    s3 = s2
    t3 = t2
  return (l3, t3, s3)
def semiTimes(a, b):
  (l1,t1,s1) = a
  (l2,t2,s2) = b
  if len(t1) == 2:
    return (l1 * l2, (t1[1]), s1 + ' '  + s2)
  else:
    if not s2:
      return (l1 * l2, (), '(' + s1  + s2 + ')')
    else:
      return (l1 * l2, (), '(' + s1 + ' ' + s2 + ')')
#def A(word, startPos, endPos, sOne): return (1, word)
def R(ruleLhs, ruleRhs, ruleWeight):
  if len(ruleRhs) > 1:
    return (ruleWeight, ruleRhs, ruleLhs)
  else:
    s1 = ruleLhs + ' ' + ruleRhs[0]
    return (ruleWeight, (), s1)

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
    print "SENT {0} GOAL SCORE: {1}".format(i, goalValue[0])
    print "SENT {0} GOAL DERIVATION: {1}".format(i, goalValue[2])
