from eth_account.messages import encode_defunct
from web3 import Web3
from web3.auto import w3
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

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
    signed_message = w3.eth.account.sign_message(msg, private_key=sk)
    ec_recover_args = (msghash, v, r, s) = (
      Web3.toHex(signed_message.messageHash),
      signed_message.v,
      to_32byte_hex(signed_message.r),
      to_32byte_hex(signed_message.s),
    )
    return ec_recover_args
