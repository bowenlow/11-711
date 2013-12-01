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

# Viterbii
# You can omit declaring the semiring except in Sections 2-3
semiZero = (0, ('',sys.maxint,0), [])
semiOne = (1, ('',sys.maxint,0), [])
def semiPlus(a, b):
  (rw1, lhs1, bp1) = a
  (rw2, lhs2, bp2) = b
  rw3 = max(rw1,rw2)
  if (rw1 < rw2):
    return (rw3, lhs2, bp2)
  else:
    return (rw3, lhs1, bp1)
def semiTimes(a, b):
  (rw1, lhs1, bp1) = a
  (rw2, lhs2, bp2) = b
  (w1, sp1, ep1) = lhs1
  (w2, sp2, ep2) = lhs2
  rw3 = rw1 * rw2
  lhs3 = (w1, min(sp1,sp2), max(ep1,ep2))
  bp3 = bp1 + [lhs2]
  return (rw3, lhs3, bp3)
def A(word, startPos, endPos, sOne): 
  return (1, (word, startPos, endPos) , [])
def R(ruleLhs, ruleRhs, ruleWeight): 
  return (ruleWeight, (ruleLhs, sys.maxint, 0), [])

def backtrace(chart, goalValue):
  (rw, lhs, bplist) = goalValue
  (w, sp, ep) = lhs
  if len(bplist) >= 1:
    sys.stdout.write('(' + w + ' ')
    for bp in range(len(bplist)):
      (bpw, bpsp, bpep) = bplist[bp]
      child_goalValue = chart[bpw][(bpsp, bpep)]
      backtrace(chart, child_goalValue)
    sys.stdout.write(')') 
  else:
    sys.stdout.write(w)
    return


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
                                      sZero=semiZero, sOne=semiOne, sPlus=semiPlus, sTimes=semiTimes, R=R,A=A,
                                      pruner=prune,
                                      dumpAgenda=False, dumpChart=False, logConsidering=False)
    print "SENT {0} AGENDA ADDS: {1}".format(i, stats['agendaAdds'])
    print "SENT {0} GOAL SCORE: {1}".format(i, goalValue[0])
    print "SENT {0} GOAL BACKPOINTERS: {1}".format(i, goalValue[2])
    sys.stdout.write('SENT ' + str(i) + ' GOAL DERIVATIONS: ');
    backtrace(chart, goalValue); print;
