from conf import config
import paramiko
import time
import slash

#import re

''' L1 library for DAT20 '''

class DAT20():

    def __init__(self, folder_name = None):
        self.Hostname = config.root.credentials.hostname
        self.Username = config.root.credentials.username
        self.Password = config.root.credentials.password
        self.Banner = config.root.credentials.banner

    #class ssh_client():

    # Private
    _ssh_client = None #SSH Client

    def ssh_init(self):
        ''' Create a SSH cliente object '''
        try:
            self._ssh_client = paramiko.SSHClient()
            self._ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            return True
        except Exception as failure:
            self._ssh_client = None
            print("SSH ERROR:", failure)

    def ssh_is_alive(self):
        pass

    def ssh_connect_Treerunner(self):
        ret = False

        # Check SSH has been created
        if self._ssh_client == None:
            print("No SSH Object, create one")
            ret = self.ssh_init()
        else:
            print("SSH Object OK")
            ret = True

        if ret == True:
            try:
                self._ssh_client.connect(
                    hostname=self.Hostname, username=self.Username, password=self.Password)
                print("SSH Connected")
                ret = True
            except Exception as failure:
                print("SSH Connect ERROR:", failure)
                ret = False
            
        return ret

    def ssh_close(self):
        if self._ssh_client:
            print("Closing SSH client")
            self._ssh_client.close()
            self._ssh_client = None
        else:
            print("Nothing to close")

    def ssh_is_process_running(self, process = None):
        return False

    def ssh_reboot(self, timeout):
        return False


    def ssh_send_command(self, command = None, timeout = 10):
        # Check SSH has been created
        ret_cmd_clean = ''
        ret_cmd = None

        if self._ssh_client == None:
            print("No SSH Object, create one")
            if self.ssh_init():
                ret = self.ssh_connect_Treerunner()
        else:
            print("SSH Object OK")
            ret = True

        if ret == True:

            ecuShell = self._ssh_client.invoke_shell()
            ecuShell.send('\n')
            rx = ecuShell.recv(2048).decode('UTF-8')  # Flush the receive buffer
            while( (rx.find(self.Banner) < 0) and timeout > 0):
                print("Banner not found, wait 1 second")
                ecuShell.send('\n')
                rx = ecuShell.recv(2048).decode('UTF-8')  # Flush the receive buffer
                time.sleep(1)
                timeout = timeout - 1
            if rx.find(self.Banner):
                print("Banner Found, sending command")

                #Sending command
                ecuShell.send(command)
                ecuShell.send('\n')
                time.sleep(1)
                rx = ecuShell.recv(2048).decode('UTF-8')  # Flush the receive buffer
                ret_cmd = rx # Append substring to final response
                while( (rx.find(self.Banner) < 0) and timeout > 0):
                    print("Waiting for banner")
                    time.sleep(1)
                    timeout = timeout - 1
                    rx = ecuShell.recv(2048).decode('UTF-8')  # Flush the receive buffer
                    ret_cmd += rx # Append substring to final response
                
                if timeout > 0:
                    ret = True
                else:
                    print("Partial result, command timeout")
                    ret = False

                #Remove Banner and garbage from output
                for line in ret_cmd.splitlines():
                    if line.find(self.Banner) < 0:
                        ret_cmd_clean += line

            else:
                ret = False

        return (ret, ret_cmd_clean)

    class log_collector():

        def collect(self):
            pass

