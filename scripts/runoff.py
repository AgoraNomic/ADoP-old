import csv
import os
import sys

from datetime import datetime, timedelta
from sets import Set
from terminaltables import AsciiTable
from textwrap import TextWrapper
import ast

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def new_ballot(voter, runoff, cast):
  return {
    'voter': voter,
    'runoff': runoff,
    'cast': cast,
    'final_vote': runoff[0] if len(runoff[0]) else "PRESENT",
  }

ballots = []
def populate_votes(office):
  with open(os.path.join(__location__, '../data/' + office.lower() + '.csv')) as csvfile:
    event_reader = csv.reader(csvfile)
    ballot_info = ''
    for row in event_reader:
      voter = row[0]
      votes = [s.strip() for s in row[1].split(',')]
      cast = row[2]
      ballots.append(new_ballot(voter, votes, cast))

def calculate_winner(office):

  towards_quorum = 0
  voters = 0
  for ballot in ballots:
      votes = ballot['runoff']
      towards_quorum += 1
      if len(votes[0]):
        voters += 1

  print("Full results for {0}:".format(office))
  print("  Towards Quorum: {0}, Cast Votes: {1}".format(towards_quorum, voters))

  for ballot in ballots:
    print("""{0}
  Vote   : {1}
  As Cast: {2}
""".format(ballot['voter'], ballot['final_vote'], ballot['cast']))



def election(office):
  global ballots
  ballots = []
  populate_votes(office)
  calculate_winner(office)
  print


print("<------------------->\n")
election("ADoP")
print("<------------------->\n")
election("Registrar")
print("<------------------->\n")
election("Referee")
