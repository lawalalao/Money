from hashlib import sha256
from app.ussd import *
from app.settings import *


def gen_hash(strr: str):
    """
        This method just generate the hash of the given string on sha256
    """
    return sha256(strr.encode()).hexdigest()

def send_money(number: str, amount: str):
    """
        This method will send money to a given number with the 
        amount and the code in the configuration file
    """
    resp = send_ussd("#150*11*" + number + "*" + amount + "#")
    while "Entrez votre code secret" not in resp:
        print(".", end="")
        resp = send_ussd("#150*11*" + number + "*" + amount + "#")

    return exec_ussd(CODE, "respond")

def proceed(number: str, amount: str, mode=False):
    # Ok, let make somethings clear about this function
    # This is just a simulation function to simulate the process 
    # when you get in front of a kioske and want to get money
    #
    # ussd function is working as you can see in send_money function,
    # So this system can be easily replace by a kioske
    if mode == False:
        send_sms(number,
                "Vous allez faire un retrait de " + amount 
                + " FCFA. Veuillez entrer le #150# et suivre les instructions")
    else:
        final_amount = int(amount) + (int(amount)//100) 
        send_sms(number,
                "Retrait d argent reussi par le 698634178. Informations "
                + "detaillees : Montant: " + str(amount) + " FCFA, Frais: " + str(int(amount)//100) 
                + " FCFA, commission: 0 FCFA, "
                +"No de transaction CO200824.1542.B60550, montant net debite " + str(final_amount) 
                + " FCFA, Nouveau solde: 716.8 FCFA.")

def remove_from_list(number: str):
    """
        This method will rempve the number from the pending list
    """
    pass

def add_to_list(number: str):
    """
        This method will add a number to the pending list
    """
    pass
