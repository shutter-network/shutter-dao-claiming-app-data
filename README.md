# claiming-app-data
The code in this repository was originally copied from the [gnosis/safe-claiming-app-data](
https://github.com/safe-global/claiming-app-data/
) repo and then modified to suit the Shutter DAO requirements

Vesting data converter and proofs generator.


### Prerequisites

- Place csv files with vesting data under `vestings/assets/{chain_id}/{type}_airdrop.csv`.
Naming should be `user_airdrop.csv`, `sptconversion_airdrop.csv`.

### Vesting csv
Vesting csv file contains following fields

 - Owner address
 - Vesting duration in weeks
 - Vesting start date (ISO 8601 Format)
 - Vesting amount in wei

### Allocation file structure

#### Vesting file 
Contains all defined allocations for a specific address with proofs.
```
[
    {
        "tag": "[user | spt_conversion]",
        "account": "checksummed address",
        "chainId": chain id,
        "contract": "checksummed airdrop contract addres",
        "vestingId": "vesting hash",
        "durationWeeks": integer,
        "startDate": timestamp,
        "amount": "amount in wei",
        "curve": integer,
        "proof": [
        ]
    },
    ...
 ]
```


# Setting up locally
Create python virtual environment
```
python -m venv venv
```
Activate a virtual environment
```
source venv/bin/activate
```
Install dependencies
```
pip install -r requirements.txt
pip install pre-commit
pre-commit install -f
```

## Vestings

Place vesting csv files for a network under `vestings/assets/{chain_id}`.
Naming should be `user_airdrop.csv` for user airdrop.

### Generating

Now exporter script can be used to parse vesting csv files, generate proofs, and export data for claiming. The aforementioned steps can be performed at once or separately.

Example:
```
cd vestings
python exporter.py --chain-id 1 --output-directory ../data/allocations
```

Exporter will place generated files under `{output_directory}/{chain_id}`


# Contribute
You can contribute to this repo by creating a Pull Request or an issue. Please follow the default template set for the Pull Requests.
