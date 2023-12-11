import csv
import os
from typing import Dict, List

from addresses import get_airdrop_addresses
from dateutil.parser import parse
from vesting import Vesting, VestingType
from web3 import Web3

CURRENT_DIRECTORY = os.path.dirname(__file__)


def read_vesting_file(
    vesting_file: str, chain_id: int, vesting_type: VestingType
) -> List[Vesting]:
    vestings: List[Vesting] = []
    airdrop_address = Web3.to_checksum_address(
        get_airdrop_addresses(chain_id)[vesting_type]
    )
    with open(vesting_file, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        print(80 * "-")
        print(f"Processing {vesting_type.name} vestings")

        for row in csv_reader:
            owner = Web3.to_checksum_address(row["owner"])
            duration_weeks: int
            start_date_timestamp: int

            if "duration" in row.keys():
                duration_weeks = int(row["duration"])
            else:
                duration_weeks = 416

            if "startDate" in row.keys():
                start_date_timestamp = int(parse(row["startDate"]).timestamp())
            else:
                start_date_timestamp = int(
                    parse("2023-07-07T00:00:00+00:00").timestamp()
                )

            amount = row["amount"]

            if "initialUnlock" in row.keys():
                initial_unlock = row["initialUnlock"]
            else:
                initial_unlock = "0"

            curve_type = 0

            vesting = Vesting(
                None,
                vesting_type,
                owner,
                airdrop_address,
                chain_id,
                curve_type,
                duration_weeks,
                start_date_timestamp,
                amount,
                initial_unlock,
                [],
            )
            vestings.append(vesting)

            calculated_vesting_id = vesting.calculateHash()

            if "vestingId" in row.keys():
                vesting_id = row["vestingId"]
                if vesting_id != calculated_vesting_id:
                    raise ValueError("provided and calculated vesting id do not match!")

        print(f"Processed {len(vestings)} {vesting_type} vestings.")
        print(80 * "-")
        return vestings


def parse_vestings_csv(chain_id: int) -> Dict[VestingType, List[Vesting]]:
    vesting_type_with_vestings = {}
    for vesting_type in VestingType:
        vesting_file = {
            VestingType.USER: os.path.join(
                CURRENT_DIRECTORY, f"assets/{chain_id}/user_airdrop.csv"
            ),
            VestingType.SPT_CONVERSION: os.path.join(
                CURRENT_DIRECTORY, f"assets/{chain_id}/sptconversion_airdrop.csv"
            ),
        }.get(vesting_type)
        if not vesting_file:
            raise ValueError(f"Not a valid vestings type: {vesting_type}")

        if not os.path.exists(vesting_file):
            print(vesting_file, "does not exist")

        vesting_type_with_vestings[vesting_type] = read_vesting_file(
            vesting_file, chain_id, vesting_type
        )
    return vesting_type_with_vestings
