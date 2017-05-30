import csv
import os
import sys

from datetime import datetime
from sets import Set
from terminaltables import AsciiTable
from textwrap import TextWrapper

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

empty_holder = '------'

def new_agency(name):
  return {
    'name': name,
    'elected': '----------',
    'since': '----------',
    'holder': empty_holder,
    'PR': '2?',
    'RR' : '2?',
  }

agencies = {}
def get_agency(name):
  if name not in agencies:
    agencies[name] = new_agency(name)
  return agencies[name]

def populate_events():
  with open(os.path.join(__location__, 'events.csv')) as csvfile:
    event_reader = csv.reader(csvfile)
    for row in event_reader:

      date = row[0]
      name = row[1]
      event = row[2]
      actor = row[3]
      agency = get_agency(name)
      if event.lower() == 'e':
        agency['elected'] = date
        agency['holder'] = actor
      elif event.lower() in ['d', 'i']:
        agency['since'] = date
        agency['holder'] = actor

def new_reporting_need(name):
  return {
    'name': name,
    'monthly': None,
    'weekly' : None,
  }

reporting_needs = {}
def get_report_need(name):
  if name not in reporting_needs:
    reporting_needs[name] = new_reporting_need(name)
  return reporting_needs[name]

def populate_reporting_needs():
  with open(os.path.join(__location__, 'reports.csv')) as csvfile:
    event_reader = csv.reader(csvfile)
    for row in event_reader:
      office = row[0]
      report_type = row[1]
      report_name = row[2]
      report_info = get_report_need(office)
      if report_type.lower() == 'm':
        report_info['monthly'] = report_name
      elif report_type.lower() == 'w':
        report_info['weekly'] = report_name


def sh_a(name):
  return shorten(name, 14)

def sh_n(name):
  return shorten(name, 8)

def shorten(name, amount):
  if (len(name) > amount):
    return "".join(word[0] for word in name.split())
  return name

def can_elect(name, date):
  if name.lower() == 'speaker':
    return 'Never'
  if date != '----------':
    today = datetime.now()
    d1 = datetime.strptime(date, "%Y-%m-%d")
    if abs((today - d1).days) > 90:
      return 'Y'
    return ''
  return 'Y'


def print_agencies():
  print """NB: The "PR|RR" and "Holder" columns of this report are
self-ratifying.
"""

  a_for_table = [['Office', 'PR|RR[1]', 'Holder', 'Since', 'Last Election', 'Can Elect[2]']]
  for agency in sorted(agencies.keys()):
    info = agencies[agency]
    to_insert = [sh_a(info['name']),
                        info['PR'] + '|' + info['RR'],
                        sh_n(info['holder']),
                        info['since'],
                        info['elected'],
                        can_elect(info['name'], info['elected'])]
    a_for_table.append(to_insert)

  table = AsciiTable(a_for_table)
  table.outer_border =False
  table.inner_column_border= False

  print table.table

def print_reporting_info():
  r_for_table = [['Office', 'M[1]','Report','Last Published','Late[2]']]
  for report in sorted(reporting_needs.keys()):
    info = reporting_needs[report]
    if info['weekly']:
      r_for_table.append([sh_a(info['name']),
                          '',
                          shorten(info['weekly'], 22),
                          '????-??-??',
                          ''])
    if info['monthly']:
      r_for_table.append([sh_a(info['name']),
                          'Y',
                          shorten(info['monthly'], 22),
                          '????-??-??',
                          ''])
  table = AsciiTable(r_for_table)
  table.outer_border =False
  table.inner_column_border= False
  print
  print table.table

def print_header():
  print """See https://agoranomic.github.io/ADoP/ for past, current, and future
reports.

<---------------------------------------------------------------------->

Offices and Reports
Date of this report: {0}
Date of last report: {1}

Informal measures
-----------------
""".format(datetime.now().date().isoformat(),"???-??-??")

def consolidation_num():
  names = Set()
  for agency in agencies:
    name = agencies[agency]['holder']
    if name is not empty_holder:
      names.add(name)
  return len(agencies)/float(len(names))


def print_health():
  print """Administrative Health [1]: {0}%
Consolidation [2]: {1:.2f}

[1] Calculated by the weighted average of # of offices filled/total and
# of reports not late/total. A higher Administrative Health % indicates
a more active bureaucracy.

[2] Calculated by dividing the # of filled offices by the number of
unique officeholders. A higher consolidation rating is not necessarily
bad, but means Agora is putting more power & responsibility in a small
group's hands.
""".format("??", round(consolidation_num(),2))

populate_events()
print_header()
print_health()
print_agencies()

populate_reporting_needs()
print_reporting_info()
