#!/usr/bin/env python
import sys
from parser import *

rules = [ line.strip() for line in open(sys.argv[1]) ]

# You can omit declaring this function except in Section 1
#def agendaComparator(item1, item2):
#  (startPos1, endPos1, lhs1, value1) = item1
#  (startPos2, endPos2, lhs2, value2) = item2
#  span1 = endPos1 - startPos1
#  span2 = endPos2 - startPos2
#  spanDiff = span2 - span1
#  if spanDiff != 0: # sort by span length first
#    return 1 if spanDiff > 0 else -1
#  else:
#    posDiff = startPos2 - startPos1
#    if posDiff != 0: # then start position
#      return 1 if posDiff > 0 else -1
#    else: # then the semiring value of the update to the chart
#      print value1
#      print value2
#      valDiff = value2 - value1
#      return 1 if valDiff < 0 else -1      

# Viterbi
# You can omit declaring the semiring except in Sections 2-3
semiZero = (0, set())
semiOne = (1, set())
def semiPlus(a, b): 
  (l1, s1) = a
  (l2, s2) = b
  c = s1 | s2
  return (1, c)
def semiTimes(a, b):
  (l1, s1) = a
  (l2, s2) = b
  c = s1 | s2 
  return (1, c)
#def A(word, startPos, endPos, sOne): return sOne
def R(ruleLhs, ruleRhs, ruleWeight):
  rule = list(ruleRhs);
  rule.insert(0, ruleLhs);
  rule = tuple(rule);
  return (1, set([rule]))

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
    (l1,s1) = goalValue
    for e in s1:
      liste = list(e);
      sys.stdout.write ("SENT "+str(i)+" RULE: "+liste[0]+" -> ")
      for j in range(1,len(liste)):
        sys.stdout.write (str(liste[j])+" ")
      sys.stdout.write('\n')
