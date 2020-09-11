from app.settings import *

from os import system as ss
from subprocess import Popen, PIPE, STDOUT

import argparse
import time

def exec(command: str):
    """
        This method will just execute a command and return the output
    """
    ss(command + " > out.txt")
    return open("out.txt", "r").read()

def enable_modem():
    """
        This method is to enablethe modem
    """
    exec(MODULE + " -m " + get_modem_id() + " -e")

def reset_ussd():
    """
        This method will reset the current ongoing ussd
    """
    exec(MODULE + " -m " + get_modem_id() + " --3gpp-ussd-cancel")

def get_status():
    """
        This method will get the status of the precedent ussd code
    """
    return exec(MODULE + " -m " + get_modem_id() + " --3gpp-ussd-status").split("status:")[1]


def get_modem_id():
    """
        This method will parse the output of listing modem to return the modem_id
    """
    return exec(MODULE + " -L").split("/")[-1].split(" ")[0]


def exec_ussd(to_execute, mode="send"):
    print("[>] USSD: ", to_execute)

    command = MODULE + " -m " + get_modem_id() + " --3gpp-ussd-"
    command += "initiate" if mode == "send" else "respond"
    command += "='" + to_execute + "'"

    out = exec(command).split(": '")[1].replace(".'", "")
    print("[<] OUT: ", out)

    return out

def refresh_and_send_ussd(code):
    """
        This method will just refresh the USSD remaining response
    """
    if "idle" not in get_status():
        reset_ussd()

    return exec_ussd(code)

def send_ussd(code: str):
    """
        This method will send the ussd-code
    """
    print("[+] Executing USSD code ::{}::".format(code))
    try:
        enable_modem()
        # We need to parse and check multiple asterix on the USSD code
        if code.count("*") > 1:
            to_execute, parts = "", [elt.replace("#", "") for elt in code.split("*")]
            for i, p in enumerate(parts):
                if (i == 0 or i == 1):
                    to_execute += '*' if p == '' else exec_ussd(to_execute + p + "#")
                else:
                    return exec_ussd(p, "respond")
        else:
            return refresh_and_send_ussd(code)
    except Exception as es:
        print("[x] Err: ", es)
        return refresh_and_send_ussd(code)


def send_sms(number: str, text: str):
    """
        This method will just send the message
    """
    resp = exec(MODULE + " -m " + get_modem_id() + " --messaging-create-sms=\"number='" + number + "',text='" + text + "'\"").replace("\n", "")
    sms_id = resp.split("/")[-1].replace(" ", "").replace("\n", "")
    cmd = MODULE + " -s " + sms_id + " --send"
    
    if "Successfully created" in resp:
        resp = exec(cmd)
        time.sleep(3)
        while "GDBus.Error" in resp:
            resp = exec(cmd)

    return resp


if __name__ == "__main__":
    print("[+] modem_id: ", get_modem_id())
    code = input("[-] code : ")
    send_ussd(code)
