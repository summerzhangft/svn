import paramiko
#import pdb
import json
import time
from flask import Flask
app = Flask(__name__)

username='xxxxx'
password='xxxx'

def sshcon(IP):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=IP,username=username,password=password)
    while True:
        try:
            stdin,stdout,stderr = client.exec_command('cd /opt/www.com/dev_www;svn info;' )
            result = ''.join(stdout.readlines())
            return result
            break
        except:
            client.close()

def sshwww1(IP):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=IP,username=username,password=password)
    while True:
        try:
            stdin,stdout,stderr = client.exec_command('cd /opt/www1.com/dev_www;svn info;' )
            result = ''.join(stdout.readlines())
            return result
            break
        except:
            client.close()

def sshstatic(IP):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=IP,username=username,password=password)
    while True:
        try:
            stdin,stdout,stderr = client.exec_command('cd /opt/static.com/dev_www;svn info;' )
            result = ''.join(stdout.readlines())
            return result
            break
        except:
            client.close()

def str2json(s):
    clean_line = [line for line in s.split('\n') if line]
    test =  dict([line.split(': ') for line in clean_line])
    testresult = {
                'svn Revision':test.get('Revision'),
                'Last Changed Author' : test.get('Last Changed Author'),
                    } 
    return testresult

def runner():
    yield{
        'HK29 www' : str2json(sshcon('172.10.1.29')),
        'HK12 www'  : str2json(sshcon('172.10.1.12')),
        'HK11 www'  : str2json(sshcon('172.10.1.11')),
        'HK15 www1'  : str2json(sshwww1('172.10.1.15')),
        'HK15 static' : str2json(sshstatic('172.10.1.15')),
        'Tokyo148 www' : str2json(sshcon('172.10.1.148')),
        }

def format_(data):
     return json.dumps(data, indent=4, ensure_ascii=False)

@app.route('/')
def running():
    for items in runner():
        return format_(items)

#def main():
 #   print(running())


if __name__ == '__main__':
    app.run(debug=True)
