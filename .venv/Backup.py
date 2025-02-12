import paramiko
import configparser
import datetime

def send_command(ip, login, password, command):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=login, password=password, timeout=10)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        client.close()
        return output
    except Exception as e:
        raise RuntimeError(f"Failed to connect to {ip}: {e}")

def main():
    config = configparser.ConfigParser()
    config.read('config.cfg')
    username = config["DEFAULT"]["login"]
    password = config["DEFAULT"]["password"]
    devices = config["DEFAULT"]["devices"].split(',')

    datetime_now = datetime.datetime.now()
    for ip in devices:
        ip = ip.strip()
        try:
            output = send_command(ip, username, password, "show run")
            time_now = datetime_now.strftime("%Y-%m-%d_%H-%M")
            file_name = f"{ip}_{time_now}.txt"
            with open(file_name, 'w') as file:
                file.write(output)
            print(f"Backup for {ip} saved to {file_name}")
        except Exception as e:
            print(f"Failed to backup {ip}: {e}")

if __name__ == "__main__":
    main()