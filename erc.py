import os
from web3 import Web3
import json
import asyncio
import websockets
from dotenv import load_dotenv

# environment variables
load_dotenv()

ws_provider = os.getenv('WEB3_PROVIDER_URI')
web3 = Web3(Web3.WebsocketProvider(ws_provider))

print(web3.is_connected())  # should print True if connected

erc20_abi = [
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "payable": False,
        "type": "function"
    }
]

async def subscribe_to_blocks():
    async with websockets.connect(ws_provider) as ws:
        await ws.send(json.dumps({
            "jsonrpc": "2.0",
            "method": "eth_subscribe",
            "params": ["newHeads"],
            "id": 1
        }))
        
        subscription_response = await ws.recv()
        print("Subscribed:", subscription_response)

        while True:
            message = await ws.recv()
            block_header = json.loads(message)
            print(f"New block received: {block_header['params']['result']['number']}")
            block_number = int(block_header['params']['result']['number'], 16)
            await process_block(block_number)

async def process_block(block_number):
    try:
        block = web3.eth.get_block(block_number, full_transactions=True)
        print(f"Processing block: {block_number}, transactions: {len(block['transactions'])}")
        for tx in block['transactions']:
            if tx['to'] is None:  # potential contract creation
                print(f"Found contract creation tx: {tx['hash'].hex()}")
                await check_for_erc20(tx)
    except Exception as e:
        print(f"Error processing block {block_number}: {e}")

async def check_for_erc20(tx):
    try:
        receipt = web3.eth.get_transaction_receipt(tx['hash'])
        if receipt and receipt['contractAddress']:
            print(f"Contract created at: {receipt['contractAddress']}")
            is_erc20 = await check_if_erc20(receipt['contractAddress'])
            print(f"Is it ERC20? {is_erc20}")
            if is_erc20:
                print(f"ERC20 contract deployed at: {receipt['contractAddress']}")
    except Exception as e:
        print(f"Error checking transaction {tx['hash'].hex()}: {e}")

async def check_if_erc20(contract_address):
    try:
        contract = web3.eth.contract(address=contract_address, abi=erc20_abi)
        contract.functions.totalSupply().call()
        contract.functions.balanceOf('0x0000000000000000000000000000000000000000').call()
        return True
    except Exception as e:
        print(f"Error checking ERC20 at {contract_address}: {e}")
        return False

if __name__ == "__main__":
    from web3.middleware import geth_poa_middleware
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    if web3.is_connected():
        print("WebSocket Connected")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(subscribe_to_blocks())
    else:
        print("Failed to connect to WebSocket")
