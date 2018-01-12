import paramiko
import json
#from flask import Flask
#app = Flask(__name__)



username = 'root'
password = 'xxxxxxxxxx'


#与host建立ssh连接
def ssh_connections(IP):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=IP,username=username,password=password)
    return ssh
#获取svn的信息
def exec_command(connection):
    try:
        stdin, stdout, stderr = connection.exec_command("cd /opt/www.com/dev_www;svn info;")
        result = ''.join(stdout.readlines())
        return result
    finally:
        connection.close()

def ssh_www1(IP):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=IP,username=username,password=password)
    try:
        stdin, stdout, stderr = ssh.exec_command("cd /opt/www1.com/dev_www;svn info;")
        result = ''.join(stdout.readlines())
        return result
    finally:
        ssh.close()

def ssh_static(IP):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=IP,username=username,password=password)
    try:
        stdin, stdout, stderr = ssh.exec_command("cd /opt/static.com/dev_www;svn info;")
        result = ''.join(stdout.readlines())
        return result
    finally:
        ssh.close()

#把输出的result转换为dict格式
def str2json(s):
    clean_line = [line for line in s.split('\n') if line]
    test = dict([line.split(": ") for line in clean_line])
    test_line = {
        'svn Revision':test.get('Revision'),
        'Last Changed Author' : test.get('Last Changed Author'),
    }
    return test_line


def runner():
    yield{
        'HK172.27.10.29 www' : str2json(exec_command(ssh_connections('172.27.10.29'))),
        'HK172.27.10.12 www'  : str2json(exec_command(ssh_connections('172.27.10.12'))),
        'HK172.27.10.11 www'  : str2json(exec_command(ssh_connections('172.27.10.11'))),
        'HK172.27.10.15 www1'  : str2json(ssh_www1('172.27.10.15')),
        'HK 172.27.10.15 static' : str2json(ssh_static('172.27.10.15')),
        'Tokyo148 10.148.10.11 www' : str2json(exec_command(ssh_connections('10.148.10.11'))),
        }
def format_(data):
    return json.dumps(data, indent=4, ensure_ascii=False)

#@app.route('/')
def running():
    for items in runner():
        return format_(items)

def main():
    print(running())

if __name__ == '__main__':
  #  app.run(debug=True)
    main()
