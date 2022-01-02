from brownie import Chess_Byte, accounts

def main():
    accnt = accounts.load('ropsten')
    Contract = Chess_Byte.deploy({
        'from':accnt
    })
    print(accnt.address, accnt.public_key)