//Contract based on https://docs.openzeppelin.com/contracts/3.x/erc721
// SPDX-License-Identifier: MIT
pragma solidity 0.7.0;

import "OpenZeppelin/openzeppelin-contracts@3.1.0-solc-0.7/contracts/token/ERC721/ERC721.sol";
import "OpenZeppelin/openzeppelin-contracts@3.1.0-solc-0.7/contracts/utils/Counters.sol";
import "OpenZeppelin/openzeppelin-contracts@3.1.0-solc-0.7/contracts//access/Ownable.sol";


contract Chess_Byte is ERC721, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    address public minter;
    uint256 public cprice;
    uint256 private pending_withdrawals;
   
    event here(string msg);
    event key(address public_key);
    event vrs(uint8 v, bytes32 r, bytes32 s);

    constructor() ERC721("ChessByte", "CHY") {
        minter = msg.sender;
        cprice = 6100000000000000; // ~20 usd
    }

    function mint(string memory tokenURI)
        private 
        returns (uint256)
    {
        // If you are sending to a wrong address
        // you will loose money for a gas fee and nothing
        // we can do about it, so becarefull wih your adress
        _tokenIds.increment();

        uint256 newItemId = _tokenIds.current();
        _mint(minter, newItemId);
        _setTokenURI(newItemId, tokenURI);

        return newItemId;
    }
    

    function buy_token(string memory tokenURI, 
                        bytes32 hash, uint8 v, bytes32 r, bytes32 s, 
                        uint256 tokenID, address contract) 
                        payable public
        {

        // Make sure this token uri is signed by the owner of the contract
        // to the recipient that is asking to buy 
        emit vrs(v, r, s);
        address signer_address = ecrecover(hash, v, r, s); 
        emit key(signer_address);
        // require(signer_address == minter, "NFT not authorized by this contract");

        // check id
        // check contract
        
        require(msg.value >= cprice, "Insufficient funds to buy");

        require(minter != msg.sender, "Cant sell to owner");

        uint256 mint_id = mint(tokenURI);
        
          // transfer the token to the buyer
        _transfer(minter, msg.sender, mint_id);
    }

    function recoverSigner(bytes32 message, bytes memory sig)
       public
       pure
       returns (address)
    {
       uint8 v;
       bytes32 r;
       bytes32 s;
       (v, r, s) = splitSignature(sig);
       return ecrecover(message, v, r, s);
   }
    function splitSignature(bytes memory sig)
        public
        pure
        returns (uint8, bytes32, bytes32)
    {
        require(sig.length == 65, 'Wrong byte lenght');
        
        bytes32 r;
        bytes32 s;
        uint8 v;
        assembly {
            // first 32 bytes, after the length prefix
            r := mload(add(sig, 32))
            // second 32 bytes
            s := mload(add(sig, 64))
            // final byte (first byte of the next 32 bytes)
            v := byte(0, mload(add(sig, 96)))
        }
        return (v, r, s);
    }

    function update_price(uint256 new_price) onlyOwner public {
        cprice = new_price;
    }

    function withdraw() onlyOwner public {

        require(address(this).balance > 0);
        address payable receiver = payable(minter);

        uint256 amount = address(this).balance;
        receiver.transfer(amount);
    }
}