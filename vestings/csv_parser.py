import csv
import os
from pathlib import Path
from typing import List

from dateutil.parser import parse
from vesting import Vesting
from web3 import Web3

CURRENT_DIRECTORY = os.path.dirname(__file__)


def read_vesting_file(
    vesting_file: Path, chain_id: int
) -> List[Vesting]:
    vestings: List[Vesting] = []

    with open(vesting_file, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        print(80 * "-")
        print(f"Processing {vesting_file.absolute()}")

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

            if "requiresSPT" in row.keys():
                requires_spt = bool(row["requiresSPT"])
            else:
                requires_spt = False

            curve_type = 0

            vesting = Vesting(
                None,
                owner,
                chain_id,
                curve_type,
                duration_weeks,
                start_date_timestamp,
                amount,
                initial_unlock,
                requires_spt,
                [],
            )
            vestings.append(vesting)

            calculated_vesting_id = vesting.calculateHash()

            if "vestingId" in row.keys():
                vesting_id = row["vestingId"]
                if vesting_id != calculated_vesting_id:
                    raise ValueError("provided and calculated vesting id do not match!")

        print(f"Processed {len(vestings)} vestings.")
        print(80 * "-")
        return vestings


def parse_vestings_csv(chain_id: int) -> List[Vesting]:

    files = [f for f in Path(f"{CURRENT_DIRECTORY}/assets/{str(chain_id)}").glob("*.csv")]
    print(f"Found {len(files)} files")
    vesting_list = []
    for f in files:
        vesting_list.extend(read_vesting_file(f, chain_id))
    return vesting_list
