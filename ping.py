# Ping servers in Python
# Ping script in Python
import subprocess
import platform
from time import sleep
from gpiozero import LED
from datetime import datetime

# Variables

# Default server
server = '1.1.1.1'
# Other servers
server1 = '8.8.8.8'
server2 = '9.9.9.9'
server3 = 'twitter.com'


# Timings

# Main delay in seconds
delay = 30
# Delay after restart
delayR = 600
# Number of retries before restart (~20s/try)
num = 15


# Pin for relay
# Uses GPIO number not board number
signal = LED(18)
signal.off()


# Returns true if host is reachable
def ping(host):
    # param = '-n' if platform.system().lower() == 'windows' else '-c'
    param = '-c'
    command = ['ping', param, '1', '-w 10', host]
    # command = ['ping', param, '1',  host]
    return subprocess.call(command) == 0


def logs(text):
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S - ")
    file = open("Logs.txt", "a")
    file.write(dt_string + text + '\n')
    file.close()
    print(dt_string + text + '\n')
    return 0


def relay10s():
    signal.on()
    sleep(10)
    signal.off()
    sleep(1)
    return 0


# Main loop
logs('Ping has started')
sleep(60)
logs('Monitoring \n')

while True:

    if not ping(server):
        logs("Request timed out - " + server)
        y = 0
        for x in range(num):
            if ping(server1):
                logs(server1 + ' - Replied')
                y = 1
                break
            elif ping(server2):
                logs(server2 + ' - Replied')
                y = 1
                break
            elif ping(server3):
                logs(server3 + ' - Replied')
                y = 1
                break
            else:
                logs(str(x+1) + '/' + str(num) + " - Request timed out for all servers: " + server1 + ', ' + server2 + ', ' + server3)

        if y == 0:
            relay10s()
            print('\nModem Restarted\n')
            logs('Modem Restarted\n')

            while True:
                if ping('1.1.1.1'):
                    logs('Connected - ' + server + '\n')
                    break
                sleep(5)

            sleep(delayR)

    sleep(delay)

