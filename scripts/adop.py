import csv
import os
import sys

from datetime import datetime, timedelta
from sets import Set
from terminaltables import AsciiTable
from textwrap import TextWrapper

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

empty_holder = '------'
empty_date = '----------'
offices = {}
reporting_needs = {}
abrev_num = 3
event_log = []

def new_agency(name):
  return {
    'name': name,
    'elected': empty_date,
    'since': empty_date,
    'holder': empty_holder,
    'PR': '2',
    'RR' : '2',
  }

def new_reporting_need(name):
  return {
    'name': name,
    'monthly': None,
    'monthly_date' : empty_date,
    'weekly' : None,
    'weekly_date' : empty_date,
  }

def get_office(name):
  if name not in offices:
    offices[name] = new_agency(name)
  return offices[name]

def populate_events():
  with open(os.path.join(__location__, 'events.csv')) as csvfile:
    event_reader = csv.reader(csvfile)
    for row in event_reader:

      date = row[0]
      name = row[1]
      event = row[2]
      actor = row[3]
      office = get_office(name)
      if event.lower() == 'e':
        office['elected'] = date
        if office['holder'] != actor:
          office['since'] = date
        office['holder'] = actor
        if not actor in ['UNKNOWN', empty_holder]:
          event_log.append('{0} {1} elected to {2}'.format(date, actor, name))

      elif event.lower() in ['d', 'i']:
        office['since'] = date
        office['holder'] = actor
        if not actor in ['UNKNOWN', empty_holder]:
          event_log.append('{0} {1} deputizes to become {2}'.format(date, sh_n(actor, False), sh_a(name, False)))
      elif event.lower() == 'r':
        office['since'] = empty_date
        office['holder'] = empty_holder
        event_log.append('{0} {1} resigns from {2}'.format(date, sh_n(actor, False), sh_a(name, False)))
      elif event.lower() == 'w':
        report_info = get_report_need(name)
        report_info['weekly_date'] = date
        event_log.append('{0} {1} publishes weekly {2} report'.format(date, sh_n(actor, False), sh_a(name, False)))
      elif event.lower() == 'm':
        report_info = get_report_need(name)
        report_info['monthly_date'] = date
        event_log.append('{0} {1} publishes monthly {2} report'.format(date, sh_n(actor, False), sh_a(name, False)))

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

abrevs = {}
def sh_a(name, add_num=True):
  return shorten(name, 14, add_num)

def sh_n(name, add_num=True):
  return shorten(name, 8, add_num)

def shorten(name, amount, add_num=True):
  if (len(name) > amount):
    abrev = "".join(word[0] for word in name.split())
    if abrev not in abrevs:
      if add_num:
        global abrev_num
        abrevs[abrev] = {'name': name, 'text': abrev + "[{0}]".format(abrev_num)}
        abrev_num += 1
      else:
        abrevs[abrev] = {'name': name, 'text': abrev}

    return abrevs[abrev]['text']
  return name

def clear_abrevs():
  abrevs.clear()
  global abrev_num
  abrev_num = 3

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

def weeks_between(d1, d2):
  monday1 = (d1 - timedelta(days=d1.weekday()))
  monday2 = (d2 - timedelta(days=d2.weekday()))

  return abs((monday2 - monday1).days) / 7

def months_between(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def week_late(date):
  if date != '----------':
    today = datetime.now()
    d1 = datetime.strptime(date, "%Y-%m-%d")
    return "!"*max(0,min(3,weeks_between(today, d1) - 1 ))
  return '!!!'


def month_late(date):
  if date != '----------':
    today = datetime.now()
    d1 = datetime.strptime(date, "%Y-%m-%d")
    return "!"*max(0,min(3,months_between(today, d1) -1))
  return '!!!'

def print_table(data):
  table = AsciiTable(data)
  table.outer_border =False
  table.inner_column_border= False
  table.padding_left = 0
  table.padding_right =2

  output = table.table
  print
  print
  print output
  print output.split('\n')[1]

def print_offices():
  print """NB: The "PR|RR" and "Holder" columns of this report are
self-ratifying."""

  a_for_table = [['Office', 'PR|RR[1]', 'Holder', 'Since', 'Last Election', 'Can Elect[2]']]
  for agency in sorted(offices.keys()):
    info = offices[agency]
    to_insert = [sh_a(info['name']),
                        "{0:>2}|{1:<2}".format(info['PR'], info['RR']),
                        sh_n(info['holder']),
                        info['since'],
                        info['elected'],
                        can_elect(info['name'], info['elected'])]
    a_for_table.append(to_insert)

  print_table(a_for_table)
  print """[1] Payrate and Report Rate
[2] Whether an election for this position can be initiated by
announcement, as per R2154(1). Note any player can initiate an
election for any office with 4 Support per R2154(2)."""
  print_abrev(3)

def print_reporting_info():
  r_for_table = [['Office', 'M[1]','Report','Last Published','Late[2]']]
  for report in sorted(reporting_needs.keys()):
    info = reporting_needs[report]
    if info['weekly']:
      r_for_table.append([sh_a(info['name']),
                          '',
                          shorten(info['weekly'], 22),
                          info['weekly_date'],
                          week_late(info['weekly_date'])])
    if info['monthly']:
      r_for_table.append([sh_a(info['name']),
                          'Y',
                          shorten(info['monthly'], 22),
                          info['monthly_date'],
                          month_late(info['monthly_date'])])
  print_table(r_for_table)
  print """[1] Monthly
[2] ! = 1 period missed. !! = 2 periods missed. !!! = 3+ periods missed."""
  print_abrev(3)

def print_abrev(start_idx):
  for abrev in abrevs:
    print "[{0}] {1}".format(start_idx, abrevs[abrev]['name'])
    start_idx += 1
  clear_abrevs()

def print_header():
  print """See https://agoranomic.github.io/ADoP/ for past, current, and future
reports.

<---------------------------------------------------------------------->

Offices and Reports
Date of this report: {0}
Date of last report: {1}

Informal measures
-----------------""".format(datetime.now().date().isoformat(),reporting_needs['Associate Director of Personnel']['weekly_date'])

def consolidation_num():
  names = Set()
  valid_offices = 0
  for agency in offices:
    name = offices[agency]['holder']
    if name is not empty_holder:
      names.add(name)
      valid_offices += 1
  return valid_offices/float(len(names))

def health_val():
  completed = 0
  availible = 0

  for agency in offices:
    name = offices[agency]['holder']
    availible += 1
    if name is not empty_holder:
      completed += 1

  for report in reporting_needs.keys():
    info = reporting_needs[report]
    if info['weekly']:
      availible += 1
      if not week_late(info['weekly_date']):
        completed += 1
    if info['monthly']:
      availible += 1
      if not week_late(info['monthly_date']):
        completed += 1

  return round((float(completed)/availible) * 100,2)


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
""".format(health_val(), round(consolidation_num(),2))

def print_events():
  print """
EVENTS
------"""
  for event in event_log:
    print event


populate_reporting_needs()
populate_events()

print_header()
print_health()
print_offices()
print_reporting_info()
print_events()
print('\n<---------------------------------------------------------------------->')