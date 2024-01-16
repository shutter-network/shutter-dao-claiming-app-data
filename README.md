# claiming-app-data
The code in this repository was originally copied from the [gnosis/safe-claiming-app-data](
https://github.com/safe-global/claiming-app-data/
) repo and then modified to suit the Shutter DAO requirements

Vesting data converter and proofs generator.


### Prerequisites

- Place csv files with vesting data under `vestings/assets/{chain_id}/*.csv`.

### Vesting CSVs
Vesting csv files contains following fields

 - `owner`: Must be an Ethereum address
 - `amount`: Token amount to be allocated
 - `duration`: Vesting duration in months
 - `startDate`: Vesting start date (ISO 8601 Format YYYY-MM-DD)
 - `initialUnlock`: Initial unlocked token share in decimal fraction (0...1)
 - `requiresSPT`: TRUE or FALSE if it is required to exchange SPT tokens upon claiming tokens (only true for SPT holders)

### Allocation file structure

#### Vesting file 
Contains all defined allocations for a specific address with proofs.
```
[
    {
        "tag": "[user | spt_conversion]",
        "account": "checksummed address",
        "chainId": chain id,
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

## Generating output files

Now exporter script can be used to parse vesting csv files, generate proofs, and export data for claiming. The aforementioned steps can be performed at once or separately.

Example:
```
cd vestings
python exporter.py --chain-id 1 --output-directory ../data/allocations
```

Exporter will place generated files under `{output_directory}/{chain_id}`

### Output files
For each address an allocation file is created `{address}.json`. These files contain the merkle proof and all relevant
data to redeem the tokens into the vesting pool contract at a later point in time.

Additionally, the file `root.txt` is created containing the merkle root. Take this value and configure the respective
parameter upon DAO deployment.

All files are located under `{output_directory}/{chain_id}`.

# Contribute
You can contribute to this repo by creating a Pull Request or an issue. Please follow the default template set for the Pull Requests.
