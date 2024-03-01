currently there is an issue with adding jinja templating to code.
It takes a while to add it ~ 10 minutes. I want to at least semi automate the process.

Reqs:
- It needs to add jinja templating only to parts where it is required
- it should not add jinja templating to areas where it is not relevant
- If a key is missing, alert user of the missing key(s)
- It is better for it to be atomic ie if there is an error, nothing happens
- It needs to take in a specified params file
- It should be able to be run on a folder path recursively or on individual files
- It needs to handle Variables from airflow
- It needs to be idempotent

Components:

File Retriever - it needs to scan for sql files given a path. It should only read files inside of path
Parser - it should take in the path to the file that is retrieved and add jinja templating



Parser Notes:

- Loop through all regex matches (comments are an issue)
- Best to pass through a series of filters:

1. replace project
2. check pre-existing jinja templating
3. check value in config file


obtain matches: make dict containing before and after -> modify after according to filters -> replace project.dataset.table in sql string using before for after




FOR NEXT TIME: file Retriever functions into sql_parser

only obtain args from main.py then pass them onto sql_parser init

we want to have it so that every init is one attempt to change the sql files provided