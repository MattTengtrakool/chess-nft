from dotenv.main import dotenv_values
from brownie import Chess_Byte, accounts
# from brownie.network import priority_fee
from eth_account.messages import encode_intended_validator, encode_defunct
from web3 import Web3
from web3.auto import w3
from eth_abi import encode_single, encode_abi



env_config = dotenv_values("../.env")

def to_32byte_hex(val):
   return Web3.toHex(Web3.toBytes(val).rjust(32, b'\0'))


def hsign (params, values, validator, sk):
    # Web3.solidityKeccak(types, params).hex()
    # msg = encode_intended_validator(validator, text=msg)
    msg = encode_defunct(primitive=Web3.solidityKeccak(params,values))
    print(msg)
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
    tokenURI = """
        {
        "attributes" : [
        {
            "trait_type": "id",
            "value":1
        },
        {
            "trait_type": "group_id",
            "value":1
        },
        {
        "trait_type" : "Year",
        "value" : "1890"
        }, {
        "trait_type" : "Winner",
        "value" : "Mocha"
        } ],
        "description" : "The world's most adorable and sensitive game.",
        "image" : "https://gateway.pinata.cloud/ipfs/Qmck4myhw8wMnXdJ3E7LVWQqabACUxh
    FEPxjiaSWXoe1t4",
        "name" : "The queen gambit"
        }
    """
    Buyer = accounts[0]

    # msghash, v, r, s = hsign(str(token_id) + tokenURI + Buyer.address + Contract.address, deployer.address, deployer.private_key)
    # Buyer address is to make sure on buyer won't buy using other people's hash
    msghash, v, r, s = hsign(['uint256', 'string', 'address', 'address'],[token_id, tokenURI, Buyer.address, Contract.address], deployer.address, deployer.private_key)
    # print("Buyer balance before transacting ", Buyer.balance())
    tx = Chess_Byte[0].buy_token(token_id,tokenURI,msghash, v, r, s,{'from':accounts[0], 'value': Chess_Byte[0].cprice()})
    # print("Buyer balance after", Buyer.balance())
    Chess_Byte[0].withdraw({'from':deployer})
    # print("Deployer balance after withdrawing", deployer.balance())
    # print(tx.info, tx.events)
    # print("Token id", Chess_Byte[0].token_size({'from':deployer}))
    print(tx.events)






