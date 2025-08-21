from web3 import Web3
import json
import os

class Web3Helper:
    def __init__(self, rpc_url="http://127.0.0.1:7545"):
        """Initialize Web3 connection to local blockchain"""
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.contract = None
        self.contract_address = None
        
        if not self.w3.is_connected():
            raise ConnectionError(f"Failed to connect to {rpc_url}")
        
        print(f"Connected to blockchain at {rpc_url}")
        print(f"Current block number: {self.w3.eth.block_number}")
    
    def deploy_contract(self, account_address, private_key, contract_path="contracts/EnergyTrading.sol"):
        """Deploy the EnergyTrading contract"""
        try:
            # Read contract source
            with open(contract_path, 'r') as f:
                contract_source = f.read()
            
            # Compile contract (this is a simplified approach)
            # In production, you'd use solc or hardhat
            print("Note: Contract compilation requires solc or hardhat")
            print("For now, assuming contract is already compiled")
            
            # For demo purposes, we'll use a placeholder
            # In real implementation, you'd compile and get ABI
            contract_abi = self._get_contract_abi()
            
            # Create contract instance
            contract = self.w3.eth.contract(abi=contract_abi, bytecode=self._get_contract_bytecode())
            
            # Estimate gas
            gas_estimate = contract.constructor().estimate_gas({'from': account_address})
            
            # Build transaction
            transaction = contract.constructor().build_transaction({
                'from': account_address,
                'gas': gas_estimate,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(account_address)
            })
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Wait for transaction receipt
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            self.contract_address = tx_receipt.contractAddress
            self.contract = self.w3.eth.contract(address=self.contract_address, abi=contract_abi)
            
            print(f"Contract deployed at: {self.contract_address}")
            return self.contract_address
            
        except Exception as e:
            print(f"Error deploying contract: {e}")
            return None
    
    def load_contract(self, contract_address, abi_path=None):
        """Load an existing contract"""
        if abi_path:
            with open(abi_path, 'r') as f:
                contract_abi = json.load(f)
        else:
            contract_abi = self._get_contract_abi()
        
        self.contract_address = contract_address
        self.contract = self.w3.eth.contract(address=contract_address, abi=contract_abi)
        print(f"Contract loaded at: {contract_address}")
    
    def place_order(self, account_address, private_key, energy_amount, price, is_buy_order):
        """Place a buy or sell order"""
        if not self.contract:
            raise ValueError("Contract not loaded")
        
        try:
            # Build transaction
            transaction = self.contract.functions.placeOrder(
                energy_amount,
                price,
                is_buy_order
            ).build_transaction({
                'from': account_address,
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(account_address)
            })
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Wait for transaction receipt
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            print(f"Order placed successfully! Transaction hash: {tx_hash.hex()}")
            return tx_hash.hex()
            
        except Exception as e:
            print(f"Error placing order: {e}")
            return None
    
    def get_order(self, order_id):
        """Get order details"""
        if not self.contract:
            raise ValueError("Contract not loaded")
        
        try:
            order = self.contract.functions.getOrder(order_id).call()
            return {
                'user': order[0],
                'energyAmount': order[1],
                'price': order[2],
                'isBuyOrder': order[3],
                'timestamp': order[4],
                'isActive': order[5]
            }
        except Exception as e:
            print(f"Error getting order: {e}")
            return None
    
    def get_trade(self, trade_id):
        """Get trade details"""
        if not self.contract:
            raise ValueError("Contract not loaded")
        
        try:
            trade = self.contract.functions.getTrade(trade_id).call()
            return {
                'buyer': trade[0],
                'seller': trade[1],
                'energyAmount': trade[2],
                'price': trade[3],
                'timestamp': trade[4],
                'isCompleted': trade[5],
                'isCancelled': trade[6]
            }
        except Exception as e:
            print(f"Error getting trade: {e}")
            return None
    
    def get_active_orders_count(self):
        """Get count of active orders"""
        if not self.contract:
            raise ValueError("Contract not loaded")
        
        try:
            return self.contract.functions.getActiveOrdersCount().call()
        except Exception as e:
            print(f"Error getting active orders count: {e}")
            return 0
    
    def _get_contract_abi(self):
        """Get contract ABI (placeholder for demo)"""
        # This is a simplified ABI for demonstration
        # In production, you'd get this from compilation
        return [
            {
                "inputs": [],
                "stateMutability": "nonpayable",
                "type": "constructor"
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "orderId",
                        "type": "uint256"
                    }
                ],
                "name": "OrderCancelled",
                "type": "event"
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "orderId",
                        "internalType": "address",
                        "name": "user",
                        "type": "address"
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "energyAmount",
                        "type": "uint256"
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "price",
                        "type": "uint256"
                    },
                    {
                        "indexed": False,
                        "internalType": "bool",
                        "name": "isBuyOrder",
                        "type": "bool"
                    }
                ],
                "name": "OrderPlaced",
                "type": "event"
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "tradeId",
                        "type": "uint256"
                    },
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "buyer",
                        "type": "address"
                    },
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "seller",
                        "type": "address"
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "energyAmount",
                        "type": "uint256"
                    },
                    {
                        "indexed False,
                        "internalType": "uint256",
                        "name": "price",
                        "type": "uint256"
                    }
                ],
                "name": "TradeExecuted",
                "type": "event"
            },
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "_orderId",
                        "type": "uint256"
                    }
                ],
                "name": "cancelOrder",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "getActiveOrdersCount",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "",
                        "type": "uint256"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "_orderId",
                        "type": "uint256"
                    }
                ],
                "name": "getOrder",
                "outputs": [
                    {
                        "internalType": "address",
                        "name": "user",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "energyAmount",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "price",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bool",
                        "name": "isBuyOrder",
                        "type": "bool"
                    },
                    {
                        "internalType": "uint256",
                        "name": "timestamp",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bool",
                        "name": "isActive",
                        "type": "bool"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "_tradeId",
                        "type": "uint256"
                    }
                ],
                "name": "getTrade",
                "outputs": [
                    {
                        "internalType": "address",
                        "name": "buyer",
                        "type": "address"
                    },
                    {
                        "internalType": "address",
                        "name": "seller",
                        "type": "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "energyAmount",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "price",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "timestamp",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bool",
                        "name": "isCompleted",
                        "type": "bool"
                    },
                    {
                        "internalType": "bool",
                        "name": "isCancelled",
                        "type": "bool"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "_energyAmount",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "_price",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bool",
                        "name": "_isBuyOrder",
                        "type": "bool"
                    }
                ],
                "name": "placeOrder",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "stateMutability": "payable",
                "type": "receive"
            }
        ]
    
    def _get_contract_bytecode(self):
        """Get contract bytecode (placeholder for demo)"""
        # This would be the actual compiled bytecode
        # For demo purposes, returning a placeholder
        return "0x608060405234801561001057600080fd5b50604051610..."
