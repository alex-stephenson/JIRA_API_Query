# Accessing JIRA data via the API

### This is a guide on how to query your JIRA board using the Python API. The focus is on extracting the core data from your board in a normalised form to then be able to visualise and run analytics.

The readthedocs is accessible here and provides some insight, but is not super helpful: https://jira.readthedocs.io/api.html#jira.client.JIRA.search_issues

## Step 1

Create an API token at the following link. Follow the instructions under 'Create an API token'. Save your API token to the clipboard and if you're not going to use it immediately, store it somewhere safe. 

## Step 2

Clone this repo to your machine. There are lots of ways to do this: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository

## Step 3

This is where it gets a bit hacky. The data returned through the `search_issues` function is very  unstructured. To make it more complicated, the name of variables within the data depend on your specific corporate instance of JIRA. I.e. one person's 'customfield_10450' is different to another person's. 

We are going to extract all the information about tickets in the JIRA board and then find the data we're interested in for these tickets, like `sprint`, `epic`, `start_date`, `end_date`.
