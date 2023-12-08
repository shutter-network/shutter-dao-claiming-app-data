from hexbytes import HexBytes
from web3 import Web3

DOMAIN_SEPARATOR_TYPEHASH = Web3.keccak(text="EIP712Domain(string name,string version)")
VESTING_TYPEHASH = Web3.keccak(
    text="Vesting(address owner,uint8 curveType,bool managed,uint16 durationWeeks,uint64 startDate,uint128 amount,uint128 initialUnlock)")

EMPTY_HASH = Web3.solidity_keccak(["bytes"], [bytes(HexBytes("0x"))])

MAINNET_USER_AIRDROP_ADDRESS = HexBytes("0xA0b937D5c8E32a80E3a8ed4227CD020221544ee6")
MAINNET_SPT_CONVERSION_ADDRESS = HexBytes("0xA0b937D5c8E32a80E3a8ed4227CD020221544ee6")

GOERLI_USER_AIRDROP_ADDRESS = HexBytes("0x07dA2049Fa8127eF6280631BCbc56881d764C8Ee")
GOERLI_SPT_CONVERSION_ADDRESS = HexBytes("0xB4baCF8271DFA468a013e63896057497Ee18c892")
