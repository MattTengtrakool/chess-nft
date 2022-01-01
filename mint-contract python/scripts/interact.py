from dotenv.main import dotenv_values
from brownie import Chess_Byte, accounts
from web3 import Web3
from web3.auto import w3
from eth_account.messages import encode_defunct
from eth_abi.packed import encode_abi_packed
from eth_keys.datatypes import PublicKey, PrivateKey, Signature
import binascii, hashlib
from eth_utils import keccak, to_bytes


env_config = dotenv_values("../.env")

def to_32byte_hex(val):
   return Web3.toHex(Web3.toBytes(val).rjust(32, b'\0'))


def hsign (msg, sk):
    # Web3.solidityKeccak(types, params).hex()
    msg = encode_defunct(text=msg)
    signed_message = w3.eth.account.sign_message(msg, private_key=sk)
    ec_recover_args = (msghash, v, r, s) = (
      Web3.toHex(signed_message.messageHash),
      signed_message.v,
      to_32byte_hex(signed_message.r),
      to_32byte_hex(signed_message.s),
    )
    return ec_recover_args

def join(types, params):
    merge = encode_abi_packed(types,params)
    return merge

def sign(data: bytes, private_key_seed_ascii: str, hash_function=keccak):
    """Sign data using Ethereum private key.
    :param private_key_seed_ascii: Private key seed as ASCII string
    """
    priv_key = PrivateKey(Web3.sha3(text=private_key_seed_ascii))
    #priv_key = PrivateKey(keccak(private_key_seed_ascii))
    print("privat key", type(priv_key), private_key_seed_ascii)
    msghash = hash_function(data)
    print("msg hash", msghash)
    signature = priv_key.sign_msg_hash(msghash)
    print("signature", signature)
    v, r, s = signature.vrs
    print("v r s", v, r, s)
    # # assuming chainID is 1 i.e the main net
    # # TODO: take in chainID as a param, so that v is set appropriately
    # # currently there's no good way to determine chainID
    # v = to_eth_v(v)
    # r_bytes = to_bytes(r)
    # s_bytes = to_bytes(s)

    # # Make sure we use bytes data and zero padding stays
    # # good across different systems
    # r_hex = binascii.hexlify(r_bytes).decode("ascii")
    # s_hex = binascii.hexlify(s_bytes).decode("ascii")

    # # Convert to Etheruem address format
    # pub_key = priv_key.public_key
    # addr = pub_key.to_checksum_address()
    # pub = pub_key.to_bytes()
    # #
    # # Return various bits about signing so it's easier to debug
    return {
        "signature": signature,
        "v": v,
        "r": r,
        "s": s,
        # "r_bytes": r_bytes,
        # "s_bytes": s_bytes,
        # "r_hex": "0x" + r_hex,
        # "s_hex": "0x" + s_hex,
        # "address_bitcoin": addr,
        # "address_ethereum": get_ethereum_address_from_private_key(private_key_seed_ascii),
        # "public_key": pub,
        # "hash": msghash,
        # "payload": binascii.hexlify(bytes([v] + list(r_bytes) + list(s_bytes,)))
    }


def main():
    # This part is for test in the real program the smart
    # contract would alredy be deployed
    deployer = accounts.add()
    Chess_Byte.deploy({
        'from':deployer
    })
    
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
    Contract = Chess_Byte[0]
    
    # hash = Web3.toHex(Web3.soliditySha3(['string', 'address'], [tokenURI, deployer.private_key]))
    # hash = keccak(encode_abi_packed(['string','address'],[tokenURI, accounts[0].address]))
    # message = encode_defunct(text=hash.hex())
    # # account 1 privat key to be substitued with DEPLOYER_PRIVATE_KEY
    # signed_message =  w3.eth.account.sign_message(message, private_key=deployer.private_key)
    
    # signed = str(signed_message.messageHash.hex())

    # signature = sign(join(['string','address', 'address'],[tokenURI, accounts[0].address, Chess_Byte[0].address]), deployer.private_key)
    msghash, v, r, s = hsign(tokenURI + Buyer.address + Contract.address, deployer.private_key)
    tx = Chess_Byte[0].buy_token(tokenURI,msghash, v, r, s, 1, Contract.address,{'from':accounts[0], 'value': Chess_Byte[0].cprice() + 10000000000})

    print(tx.info, tx.events)
    
    






