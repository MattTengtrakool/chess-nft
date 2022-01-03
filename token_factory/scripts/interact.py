from dotenv.main import dotenv_values
from brownie import Chess_Byte, accounts
from eth_account.messages import encode_defunct
from web3 import Web3
from web3.auto import w3

env_config = dotenv_values("../.env")


def to_32byte_hex(val):
   return Web3.toHex(Web3.toBytes(val).rjust(32, b'\0'))

def hsign (params, values, sk):
    """
        signs a hashed version of the values inside values
        The hashing algorithm is equivalent to solidity 0.7's
        Keccak256(abi.encodePacked())
        
        params - a list of the types of the equivlanet values inside values
        values - values to be merged hashed and signed
        sk - private key to signe them with
    """
    msg = encode_defunct(primitive=Web3.solidityKeccak(params,values))
    # print(msg)
    signed_message = w3.eth.account.sign_message(msg, private_key=sk)
    ec_recover_args = (msghash, v, r, s) = (
      Web3.toHex(signed_message.messageHash),
      signed_message.v,
      to_32byte_hex(signed_message.r),
      to_32byte_hex(signed_message.s),
    )
    return ec_recover_args

def main():
    # This part is for test in the real program the smart
    # contract would alredy be deployed
    deployer = accounts.add()
    Contract = Chess_Byte.deploy({
        'from':deployer
    })
    
    token_id = 1
    token = """
        {
        "name" : "The queen gambit"
        "id" :1,
        "group_id": 1,
        "time": "1890",
        "player1": "Winner",
        "player3": "Winner",
        "winner" : "Mocha"
        "description" : "The world's most adorable and sensitive game.",
        "image" : "https://gateway.pinata.cloud/ipfs/Qmck4myhw8wMnXdJ3E7LVWQqabACUxhFEPxjiaSWXoe1t4",
        }
    """
    tokenURI = "https://gateway.pinata.cloud/ipfs/Qmck4myhw8wMnXdJ3E7LVWQqabACUxhFEPxjiaSWXoe1t4"
    Buyer = accounts[0]

    # Buyer address is to make sure on buyer won't buy using other people's hash
    msghash, v, r, s = hsign(['uint256', 'string', 'string', 'address', 'address'],[token_id, token, tokenURI, Buyer.address, Contract.address], deployer.private_key)
    tx = Chess_Byte[0].buy_token(token_id,token, tokenURI,msghash, v, r, s,{'from':accounts[0], 'value': Chess_Byte[0].cprice()})
    Chess_Byte[0].withdraw({'from':deployer})
    print(tx.events)






