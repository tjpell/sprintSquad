# sprintSquad

This repo contains all of the code required to launch a JSON ingestion engine.

Files:
deploy.py :
1) Will connect to ec2 instance, and pull up git repo
2) Launches JSON reciever flask app, sends it a 'prefix'
3) Instantiates logging and log file rotator

serverlogging.py
1) Flask app that recieves JSON blobs
2) Records raw JSON in srv/runme/<prefix>/Raw.txt
3) Rotates the above raw JSON file every 2 minutes to generic time stamped file
4) Processes and writes JSON to srv/runme/<prefix>/proc.txt

procData.py :
1) main(): For every file that starts with prefix, read it
2) main(): If line in file is porperly formed JSON blob, extract name and age and write to output file
3) Contains methods to do the above, imported by serverlogging.py

Directories :
sprint1 : Launches a scheduled JSON ingester, less complex version of the above processes

templates: basic HTML for a front end to the server's address if visited on chrome
