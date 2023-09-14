# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 12:57:32 2023

@author: Alex.Stephenson
"""

# import the installed Jira library
from jira import JIRA
import pandas as pd

# Specify a server key. It should be your
# domain name link. yourdomainname.atlassian.net
jiraOptions = {'server': "https://YOUR_DOMAIN.atlassian.net"}



# Get a JIRA client instance, pass,
# Authentication parameters
# and the Server name.
emailID = #your emailID
token = #token you receive after registration
jira = JIRA(options=jiraOptions, basic_auth=(emailID, token)

## create variable for correct custom field


custom_field_id = "customfield_XXXXX[0]" ### INSERT CUSTOMFIELD NUMBER HERE E.G. CUSTOMFIELD_10050[0]


sprint_str = "issue.fields.f" + custom_field_id + ".name"
state_str =  "issue.fields.f" + custom_field_id + ".state"
start_date_str = "issue.fields.f" + custom_field_id + ".startDate"
end_date_str = "issue.fields.f" + custom_field_id + ".endDate"



all_tickets = jira.search_issues('project = "DG Programme" AND sprint is not empty',  maxResults=False, expand='changelog')

data = []
for issue in all_tickets:
    summary = issue.fields.summary
    key = issue.key
    status = issue.fields.status.name
    date_done = issue.fields.resolutiondate
    assignee = None
    if hasattr(issue.fields.assignee, 'displayName'):
        assignee = issue.fields.assignee.displayName
    sprint = sprint_str
    state = state_str
    start_date = start_date_str
    end_date = end_date_str
    try:
        epic = issue.fields.parent.fields.summary
    except:
        epic = None
    data.append([key, summary, status, date_done, assignee, sprint, state, start_date, end_date, epic])

all_tickets_df = pd.DataFrame(data=data, columns=['Key', 'Summary', 'Status', 'Date Resolved', 'Assignee', 'Sprint', 'State', 'Start Date', 'End Date', 'Epic'])

##################


### query to return only tickets in current sprint

open_sprints = jira.search_issues('project = "DG Programme" AND sprint in openSprints() ',  maxResults=False, expand='changelog')

data = []
for issue in open_sprints:
    summary = issue.fields.summary
    key = issue.key
    status = issue.fields.status.name
    assignee = None
    if hasattr(issue.fields.assignee, 'displayName'):
        assignee = issue.fields.assignee.displayName
    sprint = sprint_str
    state = state_str
    start_date = start_date_str
    end_date = end_date_str
    try:
        epic = issue.fields.parent.fields.summary
    except:
        epic = None
    data.append([key, summary, status, assignee, sprint, state, start_date, end_date, epic])

open_sprint_df = pd.DataFrame(data=data, columns=['Key', 'Summary', 'Status', 'Assignee', 'Sprint', 'State', 'Start Date', 'End Date', 'Epic'])

### Query to return backlog items

backlog_items = jira.search_issues('project = "DG Programme" AND sprint not in openSprints()',  maxResults=False, expand='changelog')

data = []
for issue in backlog_items:
    summary = issue.fields.summary
    key = issue.key
    status = issue.fields.status.name
    date_done = issue.fields.resolutiondate
    assignee = None
    if hasattr(issue.fields.assignee, 'displayName'):
        assignee = issue.fields.assignee.displayName
    try:
        sprint = sprint = sprint_str
    except:
        sprint = None        
    try:
        epic = issue.fields.parent.fields.summary
    except:
        epic = None
    data.append([key, summary, status, sprint, date_done, assignee, epic])

backlog_items_df = pd.DataFrame(data=data, columns=['Key', 'Summary', 'Status', 'Sprint', 'Date Resolved', 'Assignee', 'Epic'])

backlog_items_empty = backlog_items_df[backlog_items_df['Sprint'].isna()]
backlog_items_not_done = backlog_items_empty[backlog_items_empty['Status'] != 'Done']

##########################



###  change date type from strings to dates


all_tickets_df['Date Resolved'] = pd.to_datetime(all_tickets_df['Date Resolved'])
all_tickets_df['Start Date'] = pd.to_datetime(all_tickets_df['Start Date'])
all_tickets_df['End Date'] = pd.to_datetime(all_tickets_df['End Date'])

    
###  generate dataframe with distinct sprints and corresponding dates

sprint_dates = pd.DataFrame()      
sprint_dates['Sprint'] = all_tickets_df['Sprint'].drop_duplicates()
sprint_dates['Start'] = all_tickets_df['Start Date'].drop_duplicates()
sprint_dates['End'] = all_tickets_df['End Date'].drop_duplicates()


### adjust sprint end dates so there are no gaps between ending the previous sprint and starting the next one

sprint_dates = sprint_dates.sort_values('Start', ascending = False)
sprint_dates['Adjusted End Dates'] = sprint_dates['Start'].shift(periods=1)

new_end_date = []
for index, row in sprint_dates.iterrows():
    if pd.isnull(row['Adjusted End Dates']) == True:
        new_end_date.append(row['End'])
    else:
        new_end_date.append(row['Adjusted End Dates'])

sprint_dates = pd.DataFrame(
    data = {'Sprint':sprint_dates['Sprint'],'Start':sprint_dates['Start'],'End':new_end_date})
        

### determining what sprint a ticket was resolved in - adding column to dataframe

sprint_closed = []
for res_date in all_tickets_df['Date Resolved']:
    if pd.isnull(res_date) == True :
        sprint_closed.append('Open')
    else:
        for index, row in sprint_dates.iterrows():
            if res_date > row['Start'] and res_date < row['End']:
                sprint_closed.append(row['Sprint'])
            else:
                pass

all_tickets_df['Closing Sprint'] = sprint_closed

### adding column to tell if ticket is in the current active sprint

all_tickets_df['In Active Sprint?'] = all_tickets_df['Key'].isin(open_sprint_df['Key'])

