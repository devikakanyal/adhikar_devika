from web3 import Web3
import json

# Local blockchain
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Load contract ABI
with open('adhikar/backend/fir/contract_abi.json') as f:
    abi = json.load(f)

# Use deployed contract address from local deployment
CONTRACT_ADDRESS = '0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512'
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

# Use one of the Hardhat unlocked accounts
PRIVATE_KEY = '0xdf57089febbacf7ba0bc227dafbffa9fc08a93fdc68e1e42411a14efcf23656e'
PUBLIC_ADDRESS = w3.eth.account.from_key(PRIVATE_KEY).address

def file_fir(name, description, ipfs_hash):
    nonce = w3.eth.get_transaction_count(PUBLIC_ADDRESS)

    tx = contract.functions.fileFIR(name, description, ipfs_hash).build_transaction({
        'from': PUBLIC_ADDRESS,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': w3.to_wei('10', 'gwei'),
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return w3.to_hex(tx_hash)
