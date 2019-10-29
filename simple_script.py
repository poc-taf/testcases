import paramiko
import time
import slash
import re
import os

def test_C11369653():
    """ Script to execute case C11369653, more details at https://testrail.ford.com"""
    #directory = r'C:\Users\esilva\Documents\Diagrams'
    target = '192.168.85.131'
    user = 'eduardo'
    passw = 'root'
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(target, username=user,password=passw)
    print ('\n---Connected to: %s' %target +'-----------------\n')
    ecuShell = client.invoke_shell()
    ecuShell.send('ps\n')
    time.sleep(1)
    banner = (ecuShell.recv(4096)).decode('UTF-8') # Flush the receive buffer
    pattern =r'(\d{1,})(.+bash)'
    found_supervisor = re.findall(pattern, banner)
    for match in found_supervisor:
        print ('process =',match)
    pid = match[0]
    print ('pid = ',pid)
    #Kill Supervisor
    ecuShell.send('kill -2 %s' %pid)
    time.sleep(1)
    banner = (ecuShell.recv(4096)).decode('UTF-8') # Flush the receive buffer
    print ('new =', banner)
    client.close()