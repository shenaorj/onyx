from web3 import Web3
import requests
import time

# Connection to Ethereum or Binance Smart Chain
infura_url = "https://mainnet.infura.io/v3/YOUR_INFURA_API_KEY"  # Replace with your endpoint
web3 = Web3(Web3.HTTPProvider(infura_url))

# Check connection
if web3.isConnected():
    print("✅ Connected to the blockchain")
else:
    print("❌ Failed to connect to the blockchain")

# Token and contract details
TOKEN_CONTRACT_ADDRESS = "0xYourTokenContractAddress"  # Replace with the token's contract address
TOKEN_DECIMALS = 18  # Replace with the token's decimals
TOKEN_SYMBOL = "YOUR_TOKEN_SYMBOL"  # Replace with the token symbol
ABI = "YOUR_CONTRACT_ABI"  # Token ABI

# Initialize contract
contract = web3.eth.contract(address=TOKEN_CONTRACT_ADDRESS, abi=ABI)

# API details
COINGECKO_API = "https://api.coingecko.com/api/v3/simple/token_price/ethereum"
ETHERSCAN_API_KEY = "YOUR_ETHERSCAN_API_KEY"

# Function to get token price
def get_token_price(contract_address):
    try:
        params = {
            "contract_addresses": contract_address,
            "vs_currencies": "usd"
        }
        response = requests.get(COINGECKO_API, params=params)
        data = response.json()
        price = data[contract_address.lower()]["usd"]
        print(f"🔍 Current price of {TOKEN_SYMBOL}: ${price}")
        return price
    except Exception as e:
        print(f"❌ Error fetching token price: {e}")
        return None

# Function to get trading volume
def get_trading_volume(contract_address):
    try:
        url = f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={contract_address}&apikey={ETHERSCAN_API_KEY}"
        response = requests.get(url)
        data = response.json()

        if data["status"] == "1":
            transactions = data["result"]
            volume = sum(float(tx["value"]) / (10 ** TOKEN_DECIMALS) for tx in transactions)
            print(f"🔍 Trading volume in the last transactions: {volume:.2f} {TOKEN_SYMBOL}")
            return volume
        else:
            print("❌ Error fetching trading volume")
            return None
    except Exception as e:
        print(f"❌ Error in trading volume: {e}")
        return None

# Function to track token in real time
def track_token(contract_address, price_threshold, volume_threshold):
    print(f"\n🚀 Starting token tracking for {TOKEN_SYMBOL}...")

    while True:
        try:
            # Fetch price
            price = get_token_price(contract_address)

            # Fetch trading volume
            volume = get_trading_volume(contract_address)

            # Check conditions and alerts
            if price is not None and price > price_threshold:
                print(f"⚠️ Price exceeded threshold: ${price} > ${price_threshold}")
            if volume is not None and volume > volume_threshold:
                print(f"⚠️ Trading volume exceeded threshold: {volume:.2f} > {volume_threshold:.2f} {TOKEN_SYMBOL}")

            # Pause for 60 seconds before the next check
            time.sleep(60)

        except KeyboardInterrupt:
            print("\n🛑 Token tracking stopped by the user.")
            break

# Start token tracking
PRICE_THRESHOLD = 100  # Replace with your desired price threshold
VOLUME_THRESHOLD = 1000  # Replace with your desired volume threshold
track_token(TOKEN_CONTRACT_ADDRESS, PRICE_THRESHOLD, VOLUME_THRESHOLD)
