#!/usr/bin/env python

import paramiko
import time

import serverlogging 

def connect_and_pull(path_to_ssh_key_private_key, server_address):
    """
    :param path_to_ssh_key_private_key: path to ssh private key
    :param server_address: location of ec2 instance
    :return: ssh connection object
    """
    print "Connecting to box"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    pk = paramiko.RSAKey.from_private_key_file(path_to_ssh_key_private_key)
    ssh.connect(server_address, username='testtest', pkey=pk)
    ssh.exec_command("rm -rf sprintSquad; git clone https://github.com/tjpell/sprintSquad.git")  # update the git repo
    print "Pull from Github successful"

    return ssh  # we want to use the same connection later


def write_cron(ssh, prefix):
    """
    Writes a cron file to schedule processing of Raw.txt
    :param ssh: the connection initialized in connect_and_pull
    :param prefix: subdir inside /srv/runme/ to work in
    :return: None
    """
    print "Lets crontab some shit"
    ssh.exec_command('crontab - r')  # write out current crontab. we should remove this "mycron" part
    ssh.exec_command('(crontab - l 2>/dev/null; echo "*/2 * * * * python sprintSquad/procData.py {}") | crontab - '.format(prefix))  # every 5 mins
    print "Script fully executed ... exciting!"


def deploy(path_to_ssh_key_private_key, server_address, prefix):
    """
    Connects to ec2 instance, clones git repo, launches server, schedules JSON processing

    :param path_to_ssh_key_private_key: where the key file lives on local machine
    :param server_address: ec2 address
    :param prefix: The prefix for files to be processed
    :return: None
    """

    ssh = connect_and_pull(path_to_ssh_key_private_key, server_address)
    #write_cron(ssh, prefix)
    # ssh.exec_command('export FLASK_APP=serverlogging.py')
    # ssh.exec_command('flask run')
    print "Launching server at " + server_address + ':8080'
    ssh.exec_command('gunicorn -D --threads 4 -b {}:8080 --access-logfile \
                         server.log --timeout 360 serverlogging:app {}'.format(server_address,prefix))

    # ssh.exec_command('python sprintSquad/procData.py ' + prefix)
    ssh.close()


def main():
    """
    Put your deploy command here!
    """
    # key_path = '/Users/taylorjames/keys_2_the_city/sprintSquad.pem'
    key_path = '/Users/kaya/licenses/sprintSquad.pem'
    server_address = 'ec2-34-217-50-169.us-west-2.compute.amazonaws.com'
    prefix = 'prefix'

    deploy(key_path, server_address, prefix)


if __name__ == "__main__":
    main()