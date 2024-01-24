import csv
import os
from datetime import date, datetime, time
from decimal import Decimal
from pathlib import Path
from typing import List

import pytz

from vesting import Vesting
from web3 import Web3

CURRENT_DIRECTORY = os.path.dirname(__file__)


def read_vesting_file(
    vesting_file: Path, chain_id: int
) -> List[Vesting]:
    vestings: List[Vesting] = []

    tz_cet = pytz.timezone("CET")

    with open(vesting_file, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        print(80 * "-")
        print(f"Processing {vesting_file.absolute()}")

        for row in csv_reader:
            owner = Web3.to_checksum_address(row["owner"])
            duration_weeks = int(float(row["duration"])*4.33)
            start_date_timestamp = int(
                tz_cet.localize(
                    datetime.combine(
                        date.fromisoformat(row["startDate"]),
                        time(0, 0, 0)
                    )
                ).timestamp()
            )
            amount = Decimal(row["amount"]) * Decimal("1e18")
            initial_unlock = amount * Decimal(row["initialUnlock"])
            requires_spt = row["requiresSPT"].lower() == "true"

            curve_type = 0

            vesting = Vesting(
                None,
                owner,
                chain_id,
                curve_type,
                duration_weeks,
                start_date_timestamp,
                str(int(amount)),
                str(int(initial_unlock)),
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

    files = list(sorted(Path(f"{CURRENT_DIRECTORY}/assets/{str(chain_id)}").glob("*.csv")))
    print(f"Found {len(files)} files")
    vesting_list = []
    for f in files:
        vesting_list.extend(read_vesting_file(f, chain_id))
    return vesting_list
