from hexbytes import HexBytes
from web3 import Web3

DOMAIN_SEPARATOR_TYPEHASH = Web3.keccak(text="EIP712Domain(string name,string version)")
VESTING_TYPEHASH = Web3.keccak(
    text="Vesting(address owner,uint8 curveType,bool managed,uint16 durationWeeks,uint64 startDate,uint128 amount,uint128 initialUnlock,bool requiresSPT)")

EMPTY_HASH = Web3.solidity_keccak(["bytes"], [bytes(HexBytes("0x"))])

