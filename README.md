# abi-compare

Compares a target ABI to a base ABI of an ERC20 token contract.

## Installation

This project uses Python 3.7.4

In order to clone the project and install required third-party packages please execute:
```
git clone https://github.com/makerdao/abi-compare.git
cd abi-compare
pip3 install -r requirements.txt
```

## Run

From project directory, run the a script from the CLI, similiar to the following: 
```
./abi-compare --fileA-name 'weth.json' --fileB-name 'BAT.json' --contractA-address '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2' --contractB-address '0x0D8775F648430679A709E98d2b0Cb6250d2887EF'
```
