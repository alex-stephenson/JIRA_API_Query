# Accessing JIRA data via the API

### This is a guide on how to query your JIRA board using the Python API. The focus is on extracting the core data from your board in a normalised form to then be able to visualise and run analytics.

The readthedocs is accessible here and provides some insight, but is not super helpful: https://jira.readthedocs.io/api.html#jira.client.JIRA.search_issues

## Step 1

Create an API token at the following link. Follow the instructions under 'Create an API token'. Save your API token to the clipboard and if you're not going to use it immediately, store it somewhere safe. 
https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/


## Step 2

Clone this repo to your machine (how to guide here: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository )

## Step 3

This is where it gets a bit hacky. The data returned through the `search_issues` function is complex. To make it more complicated, the name of variables within the data depend on your specific corporate instance of JIRA. I.e. one person's `'customfield_10450'` is different to another person's. 

We are going to extract all the information about tickets in the JIRA board and then find the data we're interested in for these tickets, like `sprint`, `epic`, `start_date`, `end_date`.

### Step 3.1 

1. Pip install the `JIRA` package
3. In line 14 include the name of your JIRA url, e.g.    `https://COMPANYNAME.atlassian.net`
3. In line 21 and 22 put your email, and the API token we extracted in Step 1.

### Step 3.2 - identify what the 'customfield' number is in your jira instance. 

1. Go to your JIRA board
2. Click on the search bar and hit enter
3. Change the view type to list (shortcut type 't')
4. Click columns and add the column 'sprint'
5. Click sprint to order by sprint
6. The JQL query at the top should now show have changed, to show something like ORDER BY cf[XXXX]. The number here is your custom field

![image](https://github.com/alex-stephenson/JIRA_API_Query/assets/49374679/fcb09363-5732-4d29-9525-3b25701e5c1b)


### Step 3.3 - Update code with Customfield number

1. Update line 29 in the  `JIRA_query.py` file.  Your code should now read like:
   `customfield_number = "12529"`
   We are doing this so when we query the JIRA data it returns information specific to your unique server details. 

When run, the code outputs 3 different dataframes:
1. All tickets
2. All tickets from the current sprint
3. Tickets from your backlog

The remainder of the code cleans the output and calculates which sprint a ticket was comppleted in. 

## Step 4 (Optional)

The output can be used to produce weekly reports based on your JIRA data. For example, you could create a view of your open sprint data:

![Active Sprint](https://github.com/alex-stephenson/JIRA_API_Query/assets/49374679/44a7afec-2394-4844-a5ed-19dd6517e0b7)



You could also produce a view that allows users to see previous tickets, either filtering by date range or by sprint. 
![past sprint](https://github.com/alex-stephenson/JIRA_API_Query/assets/49374679/a508318b-2a57-4e1d-b08c-8fbf752a202c)


