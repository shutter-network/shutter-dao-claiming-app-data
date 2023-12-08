from typing import Dict

from constants import (
    GOERLI_USER_AIRDROP_ADDRESS,
    MAINNET_USER_AIRDROP_ADDRESS,
    GOERLI_SPT_CONVERSION_ADDRESS,
    MAINNET_SPT_CONVERSION_ADDRESS,
)
from hexbytes import HexBytes
from vesting import VestingType


def get_airdrop_addresses(chain_id: int) -> Dict[str, Dict[int, HexBytes]]:
    return {
        VestingType.USER: {
            1: MAINNET_USER_AIRDROP_ADDRESS,
            5: GOERLI_USER_AIRDROP_ADDRESS,
        }[chain_id],
        VestingType.SPT_CONVERSION: {
            1: MAINNET_SPT_CONVERSION_ADDRESS,
            5: GOERLI_SPT_CONVERSION_ADDRESS,
        }[chain_id],
    }
