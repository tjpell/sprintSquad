# sprintSquad

All of the code required to launch a JSON ingestion engine.

Files:
deploy.py :
1) will connect to ec2 instance, and pull up git repo
2) write procData to cron file to be executed every 5 minutes. passes along a file name prefix

procData.py :
1) for every file that starts with prefix, read it
2) if line in file is porperly formed JSON blob, extract name and age and write to output file
