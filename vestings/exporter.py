import argparse
import json
import os
import time
from typing import Dict, List

from csv_parser import parse_vestings_csv
from eth_typing import ChecksumAddress
from merkle_proof import extract_proofs, generate_vestings_tree
from vesting import EnhancedJSONEncoder, Vesting


def export_data(chain_id: int, output_dir: str) -> Dict[ChecksumAddress, List[Vesting]]:
    vestings = parse_vestings_csv(chain_id)
    account_with_vestings = {}
    vesting_ids = list()
    for vesting in vestings:

        # As we have to iterate vestings to get the ids, we also use that loop
        # to build a dictionary with vestings grouped by account

        vesting_ids.append(vesting.vestingId)
        account_with_vestings.setdefault(vesting.account, []).append(vesting)

    vesting_tree = generate_vestings_tree(vesting_ids)
    print("root", vesting_tree[-1][0])

    # Sort accounts dictionary
    account_with_vestings = dict(
        sorted(account_with_vestings.items(), key=lambda x: x[0].lower())
    )

    for account, account_vestings in account_with_vestings.items():
        for account_vesting in account_vestings:
            account_vesting.proof = extract_proofs(
                vesting_tree, account_vesting.vestingId
            )
        with open(f"{output_dir}/{account}.json", "w") as file:
            file.write(json.dumps(account_vestings, indent=4, cls=EnhancedJSONEncoder))

    with open(f"{output_dir}/merkle-drop-allocations-data.json", "w") as file:
        file.write(
            json.dumps(
                list(account_with_vestings.values()), indent=4, cls=EnhancedJSONEncoder
            )
        )

    with open(f"{output_dir}/root.txt", "w") as file:
        file.write(vesting_tree[-1][0])

    return account_with_vestings


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vesting data converter and exporter.")

    parser.add_argument(
        "--chain-id", dest="chain_id", help="chain id", required=True, type=int
    )

    parser.add_argument(
        "--output-directory",
        dest="output_dir",
        default="/tmp/",
        help="output directory",
        required=False,
    )

    args = parser.parse_args()

    start_time = time.time()
    chain_id = args.chain_id
    output_dir = f"{args.output_dir}/{chain_id}"
    os.makedirs(output_dir, exist_ok=True)
    export_data(chain_id, output_dir)
    print("Elapsed", time.time() - start_time, "seconds")
