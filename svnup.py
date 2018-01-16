import paramiko

hosts = [
    {
        'alias':'HK172.27.10.11',
        'hostname':'172.27.10.11',
        'username':'xxxxx',
        'password':'xxxxxxx',
     },
    {
       'alias':'HK172.27.10.12',
        'hostname':'172.27.10.12',
        'username':'xxxx',
        'password':'xxxxxxx',
    },
    {
        'alias':'HK172.27.10.29',
        'hostname':'172.27.10.29',
        'username':'xxxx',
        'password':'xxxxxxx',
    },
    {
        'alias':'Tokyo172.148.10.11',
        'hostname':'172.148.10.11',
        'username':'xxxx',
        'password':'xxxxxxx',
    },
  ]



def ssh_connection(host):
    kwargs = host
    kwargs.pop('alias')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(**kwargs)
    return client

def exec_command(connection, command):
    try:
        stdin, stdout, stderr = connection.exec_command(command)
        result = ''.join(stdout.readlines())
        if result:
            return result
        raise Exception(stderr.read())
    finally:
        connection.close()
        

def conversion(s):
    clean_line = [line for line in s.split('\n') if line]
    testline = {
        'Svn Version is ': clean_line[0],
    }
    return testline

def main():
    for host in hosts:
        print(conversion(exec_command(ssh_connection(host),"cd /opt/www.com/dev_www;svn info;")))
    
if __name__ == '__main__':
    main()
    
