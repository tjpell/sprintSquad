#!/usr/bin/env python

import paramiko
import time

def deploy(path_to_ssh_key_private_key, server_address, prefix):
    """
    :param path_to_ssh_key_private_key: where the key file lives on local machine
    :param server_address: ec2 address
    :param prefix: The prefix for files to be processed
    :return: None
    """

    print "Connecting to box"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    pk = paramiko.RSAKey.from_private_key_file(path_to_ssh_key_private_key)
    ssh.connect(server_address, username='testtest', pkey=pk)  # do we pass these in?

    ssh.exec_command("rm -rf sprintSquad; git clone https://github.com/tjpell/sprintSquad.git")  # update the git repo
    print "Pull from Github successful"
    time.sleep(1)

    print "Lets crontab some shit"
    ssh.exec_command('rm mycron')  # rm old cron

    ssh.exec_command('crontab - l > mycron')  # write out current crontab. we should remove this "mycron" part
    ssh.exec_command('echo "*/5 * * * * python sprintSquad/procData.py {}" >> mycron'.format(prefix))  # every 5 mins
    ssh.exec_command('crontab mycron')  # fire up new cron file
    print "Script fully executed ... exciting!"

    # ssh.exec_command('python sprintSquad/procData.py ' + prefix)
    ssh.close()

if __name__ == "__main__":

    key_path = '/Users/taylorjames/keys_2_the_city/sprintSquad.pem'
    server_address = 'ec2-34-217-50-169.us-west-2.compute.amazonaws.com'
    prefix = 'prefix'

    deploy(key_path, server_address, prefix)
