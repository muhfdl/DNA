import paramiko
import time

devices = [
    {
        'ip_address' : '192.168.22.10',
        'vendor' : 'cisco',
        'username' : 'fadil',
        'password' : 'F4dil'
    },
    {
        'ip_address' : '192.168.22.20',
        'vendor' : 'cisco',
        'username' : 'fadil',
        'password' : 'F4dil'
    },
    {
        'ip_address' : '192.168.22.30',
        'vendor' : 'cisco',
        'username' : 'fadil',
        'password' : 'F4dil'
    },
    {
        'ip_address' : '192.168.22.40',
        'vendor' : 'cisco',
        'username' : 'fadil',
        'password' : 'F4dil'
    }
]

old_ios=input('Masukkan Versi IOS lama\n')
new_ios=input('Masukkan Versi IOS baru\n')

print("\n"+old_ios)
print(new_ios)

input=input('\npress enter')
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for device in devices:
    ssh_client.connect(hostname=device['ip_address'],username=device['username'], password=device['password'])
    print("\nResult on {}".format(device['ip_address']))

    if device['vendor'] == 'cisco':
        conn = ssh_client.invoke_shell()
        #backup ios
        conn.send("copy flash: tftp:\n")
        conn.send(old_ios+"\n")
        conn.send("192.168.22.1\n")
        conn.send(old_ios+"\n")
        time.sleep(150)
        output = conn.recv(65535)
        print(output.decode())
        
        #Hapus flash ios
        conn.send("delete flash:"+old_ios+"\n")
        conn.send(old_ios+"\n")
        conn.send("y\n")
        time.sleep(5)
        output = conn.recv(65535)
        print(output.decode())

        #input ios baru
        conn.send("copy tftp: flash:\n")
        conn.send("192.168.22.1\n")
        conn.send(new_ios+"\n")
        conn.send(new_ios+"\n")
        time.sleep(150)
        output = conn.recv(65535)
        print(output.decode())

        #verify md5
        conn.send("verify /md5 flash:"+new_ios+"\n")
        time.sleep(150)
        output = conn.recv(65535)
        print(output.decode())

        #setboot & menghapus boot lama dari running-config
        conn.send("conf t\n")
        conn.send("boot system flash:"+new_ios+"\n")
        conn.send("no boot system flash:"+old_ios+"\n")
        conn.send("exit\n")
        time.sleep(1)
        output = conn.recv(65535)
        print(output.decode())

        #reload
        conn.send("wr\n")
        conn.send("reload\n")
        conn.send("y\n")
        time.sleep(10)
        output = conn.recv(65535)
        print(output.decode())

    ssh_client.close()