from typing import List, Union
import cv2
from dotenv.main import dotenv_values
from pinata import pinata_upload
from fbdb import get_position, add_position, get_id, add_id
from jpeg_creator import generate_board, place_icons
from test1 import sample_input
from contract_methods import hsign
from compression import compress_image
import json
import os
from web3 import Web3

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

delete_que = []
latest_position = [] # position value user_address

env = dotenv_values(".env")


def check_position(position):
    """
        Checks if a position is already minted
        if not returns an empty string and if it is
        return the public address of the person owning it
        # should be used to advertise from buying and selling
        # from other customers, we could ask users to log in
        # to be notified when some one is interested in buying
        # there positions
    """
    val = get_position(position)
    if (not val):
        return ""
    else:
        return val["Address"]
    
def generate_transaction(position, json_string, buyer_address): 
    
    global latest_position
    # check if this position have already been added
    pos_hash = str(hash(str(position)))
    address = check_position(pos_hash)
    if address:
        msg = f"""{address} already owns this position
        You can but it from the owner, do you want us
        to broker the transaction"""
        return msg
    
    latest_position = [pos_hash, buyer_address]
    # Generate positoin image
    board = generate_board()
    board = place_icons(board, position)
    
    image_name = f"generated_img{pos_hash}.png"
    if not cv2.imwrite(image_name, board):
        msg = "Couln't create image imwrite faild"
        return msg
    compressed = compress_image(image_name)
    if compressed:
        os.remove(image_name)
        image_name = compressed
    delete_que.append(image_name)
    
    # upload to pinata
    #upload_details = {'IpfsHash': 'QmZabpqTZQcWmTpx7urmYjCeVXVVNZNm3fH7QdijBipnai', 'PinSize': 677763, 'Timestamp': '2022-01-02T15:55:11.128Z'}
    upload_details = pinata_upload(image_name)
    if (not upload_details):
        return "Token generation faild: couldn't upload image"
    
    #get id to be used for token
    id = add_id()
    
    # generate token
    ipfs_address = "https://gateway.pinata.cloud/ipfs/"+upload_details['IpfsHash']
    time_stamp = upload_details['Timestamp']
    
    dic_left = "{"
    token = f"""{dic_left}
    \"id\":{id},
    \"position_hash\":{pos_hash},
    \"image\":\"{ipfs_address}\",
    \"time_stamp\":\"{time_stamp}\", 
    {json_string[1:]}"""
    # assert(type(json.loads(token)) == dict)
    
    # Upload token
    json_filename = f"generated_json{pos_hash}.json"
    with open(json_filename, 'w') as outfile:
        json.dump(token, outfile)
    # UNTESTED
    upload_details = pinata_upload(json_filename)
    delete_que.append(json_filename)
    
   
    tokenURI = "https://gateway.pinata.cloud/ipfs/"+upload_details['IpfsHash']
    
    # Pepare_signature
    contract_address = Web3.toChecksumAddress(env['CONTRACT_ADDRESS'])
    msghash, v, r, s = hsign(['uint256', 'string', 'string', 'address', 'address'],
                             [id, token, tokenURI, buyer_address, contract_address], 
                             env['OWNER_PRIVATE_KEY'])
    
    
    # tx = Chess_Byte[0].buy_token(token_id,token, tokenURI,msghash, v, r, s,{'from':accounts[0], 'value': Chess_Byte[0].cprice()})
    # Front end code
    # contractAddress = address of the contract
    # window.contract = await new web3.eth.Contract(contractABI, contractAddress);
    # const transactionParameters = {
    #     to: contractAddress, // Required except during contract publications.
    #     from: window.ethereum.selectedAddress, // must match user's active address.
    #     'data': window.contract.methods.buy_token(tokenid, token, tokenURI, msghash, v, r, s).encodeABI()//make call to NFT smart contract 
    # };
    
    print({'buyer_address':buyer_address,
            'token_id':id,
            'token': token,
            'tokenURI': tokenURI,
            'msghash':msghash,
            'v':v,
            'r':r,
            's':s,
            'pos_has': pos_hash
            })

# make sure to recive from the frontend if transaction was
# sent succesfully and if so add the position has to the database


# Example token ur
tokenURI = """{"name" : "The queen gambit",
    "group_id": 1,
    "time": "1890",
    "player1": "Winner",
    "player3": "Winner",
    "winner" : "Mocha",
    "description" : "The world's most adorable and sensitive game."
}
"""

def save_position():
    global latest_position
    add_position(latest_position[0], latest_position[1])
    
generate_transaction(sample_input, tokenURI, env['OWNER_PUBLIC_KEY'])
# {'IpfsHash': 'QmZabpqTZQcWmTpx7urmYjCeVXVVNZNm3fH7QdijBipnai', 'PinSize': 677763, 'Timestamp': '2022-01-02T15:55:11.128Z'}
# dic = {"image"}
# # r = upload_image("generated_img.png")
# # if (r.ok):
    
    