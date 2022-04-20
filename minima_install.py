import os
import subprocess
import time


def get_yml(count):
    if os.path.exists("docker-compose.yml"):
        os.truncate("docker-compose.yml", 0)
    with open('docker-compose.yml', 'a') as dc:
        dc.write(
            "---\n"
            "version: '3'\n"
            "services:\n"
        )
        if count == 0:
            count += 1
        for i in range(0, count):
            dc.write(str(
                "  " + f"m{i+1}\n"
                "    " + "image: nikosns/minima_amd:latest\n"
                "    " + f"container_name: alp_min{i+1}\n"
                "    " + "restart: always\n"
                "    " + "cpus: 0.4\n"
                "    " + "ports:\n"
                "    " + f'- "90{i}1:9001"\n'
                "    " + f'- "90{i}2:9002"\n'
            ))
        dc.write("\n...")
        dc.close()

        if os.path.exists("docker-compose.yml"):
            subprocess.run(["docker-compose", "up", "-d"])
            return 0


def counter():
    try:
        print("wait 60 sec")
        for i in range(0, 60):
            time.sleep(1)
            print(f"wait for {i+1} seconds")
    except KeyboardInterrupt:
        pass
    return 0


def get_uid(count):
    for i in range(0, count):
        uid = str(input("paste your uid "))
        subprocess.run(["docker", "exec", f"alp_min{i+1}", "curl", "127.0.0.1:9002/incentivecash+uid:"+uid])


def run_containers():
    if get_yml(count) == 0:
        print("file for docker-compose created\nand containers are started")
        if counter() == 0:
            print("time to start uid")
            get_uid(count)
        else:
            print("something was wrong")


try:
    try:
        upd = int(input("Do you want install it firstly or update recently? Type 1 or 2: "))
        count = int(input("How many nodes you need (print number)? "))
    except TypeError:
        print("Only numbers, try again")
        exit(0)
    if upd == 1:
        time.sleep(1)
        print("Ok, let's go!")
        subprocess.run(["pip", "install", "-r", "requirements.txt"])
        run_containers()
    elif upd == 2:
        subprocess.run(["docker-compose", "down"])
        subprocess.run(["docker", "pull", "nikosns/minima_amd:latest"])
        run_containers()
except KeyboardInterrupt:
    exit(1)

