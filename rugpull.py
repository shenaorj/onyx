from web3 import Web3
import requests
import pandas as pd

# Connection to Ethereum or Binance Smart Chain
infura_url = "https://mainnet.infura.io/v3/YOUR_INFURA_API_KEY"  # Change if using another network
web3 = Web3(Web3.HTTPProvider(infura_url))

# Check connection
if web3.isConnected():
    print("✅ Connected to the blockchain")
else:
    print("❌ Failed to connect to the blockchain")

# Smart contract address to analyze
contract_address = "0xYourContractAddress"
ABI = "YOUR_CONTRACT_ABI"  # Obtain the ABI from Etherscan or similar
contract = web3.eth.contract(address=contract_address, abi=ABI)

# Etherscan API configuration to analyze transactions
ETHERSCAN_API_KEY = "YOUR_ETHERSCAN_API_KEY"

# Function to check liquidity
def check_liquidity(contract):
    try:
        # This assumes the contract has a getReserves() method
        reserves = contract.functions.getReserves().call()
        liquidity = reserves[0] + reserves[1]  # Sum the liquidity of both pools
        print(f"🔍 Detected liquidity: {liquidity}")
        return liquidity
    except Exception as e:
        print(f"❌ Error while fetching liquidity: {e}")
        return None

# Function to get token holders (simulation with Etherscan API)
def check_token_distribution(contract_address):
    try:
        url = f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={contract_address}&apikey={ETHERSCAN_API_KEY}"
        response = requests.get(url)
        data = response.json()

        if data["status"] == "1":
            # Process data to identify token concentration
            transfers = pd.DataFrame(data["result"])
            transfers["to"] = transfers["to"].str.lower()  # Normalize addresses
            holders = transfers["to"].value_counts(normalize=True)
            top_holder_percentage = holders.iloc[0]
            print(f"🔍 Top holder controls {top_holder_percentage * 100:.2f}% of the tokens")
            return top_holder_percentage
        else:
            print("❌ Error fetching token distribution")
            return None
    except Exception as e:
        print(f"❌ Error in token distribution: {e}")
        return None

# Function to get trading volume (simulation with Etherscan API)
def check_trading_volume(contract_address):
    try:
        url = f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={contract_address}&apikey={ETHERSCAN_API_KEY}"
        response = requests.get(url)
        data = response.json()

        if data["status"] == "1":
            transfers = pd.DataFrame(data["result"])
            transfers["value"] = transfers["value"].astype(float) / (10 ** 18)  # Convert to ETH or token equivalent
            trading_volume = transfers["value"].sum()
            print(f"🔍 Total detected trading volume: {trading_volume:.2f} tokens")
            return trading_volume
        else:
            print("❌ Error fetching trading volume")
            return None
    except Exception as e:
        print(f"❌ Error in trading volume: {e}")
        return None

# Evaluate the smart contract
def evaluate_rug_pull_risk(contract_address, contract):
    print("\n🚀 Starting risk evaluation for contract:", contract_address)

    # Check liquidity
    liquidity = check_liquidity(contract)
    if liquidity is not None and liquidity < 1000:
        print("⚠️ Low liquidity: potential rug pull risk")
    else:
        print("✅ Acceptable liquidity")

    # Check token distribution
    top_holder_percentage = check_token_distribution(contract_address)
    if top_holder_percentage is not None and top_holder_percentage > 0.5:
        print("⚠️ High token concentration in a single wallet")
    else:
        print("✅ Acceptable token distribution")

    # Check trading volume
    trading_volume = check_trading_volume(contract_address)
    if trading_volume is not None and trading_volume < 10000:
        print("⚠️ Low trading volume: potential lack of trust in the token")
    else:
        print("✅ Acceptable trading volume")

# Run the evaluation
evaluate_rug_pull_risk(contract_address, contract)