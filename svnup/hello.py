import paramiko
import json
import os
from flask import Flask, render_template,flash
from wtforms import StringField, SubmitField
from flask_wtf import Form
from flask_bootstrap import Bootstrap
from flask_script import Manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wuyu'
Bootstrap(app)

manager = Manager(app)


username = 'root'
password = 'xxxxxxxx'

class UpdateForm(Form):
    ip = StringField('Remote Hostname')
    update = SubmitField('update')

host_mapping = [

   {
       "alias" : "HK172.27.10.11 www",
       "hostname": "72.27.10.11",
       "command" : "cd /opt/www.com/dev_www;svn up;",
       "command1":"cd /opt/www.com/dev_www;svn info;",
   },

   {
       "alias" : "HK172.27.10.12",
       "hostname":"172.27.10.12",
       "command": "cd /opt/www.com/dev_www/;svn up;",
       "command1": "cd /opt/www.com/dev_www/;svn info;"
   },
 
  {
      "alias" : "HK172.27.10.29",
       "hostname":"172.27.10.29",
       "command":"cd /opt/www.com/dev_www/;svn up;",
       "command1":"cd /opt/www.com/dev_www/;svn info;"
  },

  {
       "alias" : "Tokyo148 172.27.10.148 www",
       "hostname":"172.27.10.148",
       "command":"cd /opt/www.com/dev_www/;svn up;",
       "command1":"cd /opt/www.com/dev_www/;svn info;"
  },


  {
       "alias" : "HK172.27.10.15 www1",
       "hostname":"172.27.10.15",
       "command":"cd /opt/www1.com/dev_www;svn up --username www --password 1q2w3e:leo123;",
       "command1":"cd /opt/www1.com/dev_www/;svn info;"
  },

 {
       "alias" : "HK172.27.10.19 static",
       "hostname":"172.27.10.19",
       "command":"cd /opt/static.com/dev_www;svn up --username static --password 1q2w3e:leo123;",
       "command1":"cd /opt/static.com/dev_www/;svn info;"
  },
]
def ssh_connections(IP):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=IP,username=username,password=password)
    return ssh
def exec_command(connection,command):
    try:
        stdin, stdout, stderr = connection.exec_command(command)
        result = ''.join(stdout.readlines())
        if result:
            return result
        raise Exception(stderr.read())
    finally:
        connection.close()

def find_command(IP):
    for host in host_mapping:
        if host['hostname'] == IP:
            return host['command']
def find_command1(IP):
    for host in host_mapping:
        if host['hostname'] == IP:
            return host['command1']

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
        'HK172.27.10.29 www' : str2json(exec_command(ssh_connections('172.27.10.29'),find_command1('172.27.10.29'))),
        'HK172.27.10.12 www'  : str2json(exec_command(ssh_connections('172.27.10.12'),find_command1('172.27.10.12'))),
        'HK172.27.10.11 www'  : str2json(exec_command(ssh_connections('172.27.10.11'),find_command1('172.27.10.11'))),
        'HK172.27.10.15 www1'  : str2json(exec_command(ssh_connections('172.27.10.15'),find_command1('172.27.10.15'))),
        'HK 172.27.10.15 static' : str2json(exec_command(ssh_connections('172.27.10.15'),find_command1('172.27.10.15'))),
        'Tokyo148 172.27.10.148 www' : str2json(exec_command(ssh_connections('172.27.10.148'),find_command1('172.27.10.148'))),
        }

def format_(data):
     return json.dumps(data, indent=4, ensure_ascii=False)

@app.route('/')
def running():
    for items in runner():
        return format_(items)

@app.route('/update',methods = ['GET', 'POST'])
def index():
    form = UpdateForm()
    if form.validate_on_submit():
        ip = form.ip.data
        ret = exec_command(ssh_connections(ip), find_command(ip))
        if ret:
            return ret
    return render_template('update.html', form=form)


if __name__ == "__main__":
    app.run(
            port = 7777,
            host = '172.27.10.129',
            debug=True)

