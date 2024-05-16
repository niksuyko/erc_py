# Ethereum ERC20 Contract Scraper + Solidity Sample

This project is a Python script that connects to the Ethereum blockchain via WebSocket, listens for new blocks, and checks for new ERC20 contracts deployed. The script uses the `web3.py` library to interact with the Ethereum blockchain and the `websocket-client` library to handle WebSocket connections.

## Features

- Connects to the Ethereum blockchain using a WebSocket provider.
- Listens for new block headers.
- Processes transactions in each block to identify potential contract creation transactions.
- Checks if the created contracts are ERC20 tokens.

## Prerequisites

- Python 3.6 or above
- `web3.py` library
- `websocket-client` library
- `python-dotenv` library

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/erc20-scraper.git
    cd erc20-scraper
    ```

2. **Create a virtual environment** (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required libraries**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file** in the project directory and add your WebSocket provider URL:

    ```plaintext
    WEB3_PROVIDER_URI=wss://eth-mainnet.g.alchemy.com/v2/your-api-key
    ```

## Usage

1. **Run the script**:

    ```bash
    python erc.py
    ```

2. **Output**:
    - The script will print `True` if it successfully connects to the WebSocket.
    - It will print "WebSocket Connected" once the connection is established.
    - The script will then listen for new blocks and print details of transactions that potentially create new contracts.
    - If a new contract is created, it will check if the contract is an ERC20 token and print the results.
