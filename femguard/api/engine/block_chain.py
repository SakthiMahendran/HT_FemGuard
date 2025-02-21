import json
import hashlib
import logging
import os
from dotenv import load_dotenv
from web3 import Web3
from eth_account import Account

# Load API keys from .env
load_dotenv()
PROVIDER_URL = os.getenv("DAPP_KEY")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

class BlockchainConnector:
    def __init__(self, provider_url, private_key):
        """Initialize the connection to Ethereum blockchain."""
        self.provider_url = provider_url
        self.private_key = private_key
        self.web3 = Web3(Web3.HTTPProvider(self.provider_url))
        self.account = Account.from_key(self.private_key)
        self.connected = self.web3.is_connected()

        if self.connected:
            logging.info(f"✅ Connected to blockchain. Wallet: {self.account.address}")
        else:
            logging.error("❌ Connection failed.")

    def hash_data(self, data):
        """Hash JSON data using SHA-256."""
        json_string = json.dumps(data, sort_keys=True)
        return hashlib.sha256(json_string.encode()).hexdigest()

    def send_to_blockchain(self, data):
        """Hash JSON and send it as a transaction."""
        if not self.connected:
            logging.error("Not connected to blockchain.")
            return None

        data_hash = self.hash_data(data)
        nonce = self.web3.eth.get_transaction_count(self.account.address)

        txn = {
            "to": self.account.address,
            "value": 0,
            "gas": 21000,
            "gasPrice": self.web3.to_wei("10", "gwei"),
            "nonce": nonce,
            "data": self.web3.to_bytes(hexstr=data_hash),
            "chainId": 11155111,  # Sepolia Testnet Chain ID
        }

        signed_txn = self.web3.eth.account.sign_transaction(txn, private_key=self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        logging.info(f"✅ Transaction Sent! TX Hash: {tx_hash.hex()}")
        return tx_hash.hex()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    blockchain = BlockchainConnector(PROVIDER_URL, PRIVATE_KEY)
    sample_data = {"name": "Alice", "balance": 1000, "type": "deposit"}
    
    tx_hash = blockchain.send_to_blockchain(sample_data)
    if tx_hash:
        logging.info(f"✅ Transaction successful! Hash: {tx_hash}")
    
