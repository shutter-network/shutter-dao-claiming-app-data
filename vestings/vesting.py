import dataclasses
import json
from enum import Enum
from functools import cache
from typing import List, Optional

from constants import DOMAIN_SEPARATOR_TYPEHASH, VESTING_TYPEHASH
from eth_abi import abi
from eth_abi.packed import encode_packed
from eth_typing import ChecksumAddress, HexStr
from hexbytes import HexBytes
from web3 import Web3


class VestingType(Enum):
    USER = 0


@cache
def calculate_domain_separator() -> bytes:
    return Web3.solidity_keccak(
        ["bytes"],
        [
            abi.encode(
                ("bytes32", "string", "string"),
                (DOMAIN_SEPARATOR_TYPEHASH, "VestingLibrary", "1.0"),
            )
        ],
    )


@dataclasses.dataclass
class Vesting:
    vestingId: Optional[HexStr]
    tag: VestingType
    account: ChecksumAddress
    chainId: int
    curve: int
    durationWeeks: int
    startDate: int
    amount: str
    initialUnlock: str
    requiresSPT: bool
    proof: List[HexStr]

    # TODO Calculate on init
    def calculateHash(self) -> HexStr:
        domain_separator = calculate_domain_separator()
        vesting_data_hash = Web3.solidity_keccak(
            ["bytes"],
            [
                abi.encode(
                    (
                        "bytes32",
                        "address",
                        "uint8",
                        "bool",
                        "uint16",
                        "uint64",
                        "uint128",
                        "uint128",
                        "bool"
                    ),
                    (
                        VESTING_TYPEHASH,
                        self.account,
                        self.curve,
                        False,
                        self.durationWeeks,
                        self.startDate,
                        int(self.amount),
                        int(self.initialUnlock),
                        bool(self.requiresSPT)
                    ),
                )
            ],
        )

        vesting_id = Web3.solidity_keccak(
            ["bytes"],
            [
                encode_packed(
                    ("bytes1", "bytes1", "bytes", "bytes"),
                    (
                        HexBytes(0x19),
                        HexBytes(0x01),
                        domain_separator,
                        vesting_data_hash,
                    ),
                )
            ],
        )

        self.vestingId = HexBytes(vesting_id).hex()
        return self.vestingId


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        elif isinstance(o, VestingType):
            return o.name.lower()
        return super().default(o)
