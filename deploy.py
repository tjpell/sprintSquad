#!/usr/bin/env python

# team "comfortable walking pace"
# Taylor Pellerin
# Kaya Tollas
# Sara Mahar
# Ford Higgins
# John Rumple

import paramiko

def connect_and_pull(path_to_ssh_key_private_key, server_address):
    """
    Connect to the provided ec2 instance, clones team github repo

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


def deploy(path_to_ssh_key_private_key, server_address, prefix):
    """
    Connects to ec2 instance, clones git repo, launches server, schedules JSON processing

    :param path_to_ssh_key_private_key: where the key file lives on local machine
    :param server_address: ec2 address
    :param prefix: The prefix for files to be processed
    :return: None
    """

    ssh = connect_and_pull(path_to_ssh_key_private_key, server_address)
    ssh.exec_command('export FLASK_APP=serverlogging.py')
    ssh.exec_command('flask run')

    ssh.exec_command("python sprintSquad/serverlogging.py '{}'".format(prefix))  # launch the server

    print "Firing up JSON receiver!"
    # stdin, stdout, stderr = ssh.exec_command("gunicorn -D --threads 4 -b 0.0.0.0:8080 --log-level=debug \
    #                                             --access-logfile serveraccess.log --error-logfile servererror.log \
    #                                             --timeout 360 'serverlogging:app '{}')'".format(prefix))

    ssh.close()


def main():
    """
    Put your deploy command here
    """

    # deploy(key_path, server_address, prefix)



if __name__ == "__main__":
    main()