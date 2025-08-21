import { WalletInfo } from '../types';

// Wallet connection service using MetaMask
export class WalletService {
  private walletInfo: WalletInfo = {
    address: '',
    chainId: 0,
    isConnected: false,
    balance: '0'
  };
  
  private listeners: ((walletInfo: WalletInfo) => void)[] = [];
  
  constructor() {
    this.initializeWallet();
  }
  
  // Initialize wallet connection
  private async initializeWallet() {
    if (typeof window !== 'undefined' && (window as any).ethereum) {
      const ethereum = (window as any).ethereum;
      
      // Listen for account changes
      ethereum.on('accountsChanged', (accounts: string[]) => {
        if (accounts.length > 0) {
          this.updateWalletInfo(accounts[0]);
        } else {
          this.disconnectWallet();
        }
      });
      
      // Listen for chain changes
      ethereum.on('chainChanged', (chainId: string) => {
        this.updateChainId(parseInt(chainId, 16));
      });
      
      // Check if already connected
      const accounts = await ethereum.request({ method: 'eth_accounts' });
      if (accounts.length > 0) {
        this.updateWalletInfo(accounts[0]);
      }
    }
  }
  
  // Connect to MetaMask
  async connectWallet(): Promise<WalletInfo> {
    try {
      if (typeof window === 'undefined' || !(window as any).ethereum) {
        throw new Error('MetaMask not found. Please install MetaMask extension.');
      }
      
      const ethereum = (window as any).ethereum;
      
      // Request account access
      const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
      
      if (accounts.length > 0) {
        await this.updateWalletInfo(accounts[0]);
        return this.walletInfo;
      } else {
        throw new Error('No accounts found');
      }
    } catch (error) {
      console.error('Error connecting wallet:', error);
      throw error;
    }
  }
  
  // Disconnect wallet
  disconnectWallet(): void {
    this.walletInfo = {
      address: '',
      chainId: 0,
      isConnected: false,
      balance: '0'
    };
    this.notifyListeners();
  }
  
  // Switch account
  async switchAccount(): Promise<WalletInfo> {
    try {
      if (typeof window === 'undefined' || !(window as any).ethereum) {
        throw new Error('MetaMask not found');
      }
      
      const ethereum = (window as any).ethereum;
      
      // Request account switching
      await ethereum.request({ method: 'wallet_requestPermissions' });
      
      // Get current accounts
      const accounts = await ethereum.request({ method: 'eth_accounts' });
      
      if (accounts.length > 0) {
        await this.updateWalletInfo(accounts[0]);
        return this.walletInfo;
      } else {
        throw new Error('No accounts available');
      }
    } catch (error) {
      console.error('Error switching account:', error);
      throw error;
    }
  }
  
  // Get current wallet info
  getWalletInfo(): WalletInfo {
    return { ...this.walletInfo };
  }
  
  // Update wallet information
  private async updateWalletInfo(address: string): Promise<void> {
    if (typeof window === 'undefined' || !(window as any).ethereum) return;
    
    const ethereum = (window as any).ethereum;
    
    try {
      // Get chain ID
      const chainId = await ethereum.request({ method: 'eth_chainId' });
      
      // Get balance
      const balance = await ethereum.request({
        method: 'eth_getBalance',
        params: [address, 'latest']
      });
      
      this.walletInfo = {
        address,
        chainId: parseInt(chainId, 16),
        isConnected: true,
        balance: this.formatBalance(balance)
      };
      
      this.notifyListeners();
    } catch (error) {
      console.error('Error updating wallet info:', error);
    }
  }
  
  // Update chain ID
  private updateChainId(chainId: number): void {
    this.walletInfo.chainId = chainId;
    this.notifyListeners();
  }
  
  // Format balance from wei to ETH
  private formatBalance(balanceWei: string): string {
    const balanceEth = parseInt(balanceWei, 16) / Math.pow(10, 18);
    return balanceEth.toFixed(4);
  }
  
  // Add listener for wallet changes
  addListener(listener: (walletInfo: WalletInfo) => void): void {
    this.listeners.push(listener);
  }
  
  // Remove listener
  removeListener(listener: (walletInfo: WalletInfo) => void): void {
    const index = this.listeners.indexOf(listener);
    if (index > -1) {
      this.listeners.splice(index, 1);
    }
  }
  
  // Notify all listeners
  private notifyListeners(): void {
    this.listeners.forEach(listener => listener(this.walletInfo));
  }
  
  // Check if MetaMask is available
  isMetaMaskAvailable(): boolean {
    return typeof window !== 'undefined' && !!(window as any).ethereum;
  }
  
  // Get network name from chain ID
  getNetworkName(chainId: number): string {
    const networks: Record<number, string> = {
      1: 'Ethereum Mainnet',
      3: 'Ropsten Testnet',
      4: 'Rinkeby Testnet',
      5: 'Goerli Testnet',
      42: 'Kovan Testnet',
      56: 'BSC Mainnet',
      97: 'BSC Testnet',
      137: 'Polygon Mainnet',
      80001: 'Polygon Mumbai Testnet'
    };
    
    return networks[chainId] || `Chain ID ${chainId}`;
  }
  
  // Sign a message
  async signMessage(message: string): Promise<string> {
    if (!this.walletInfo.isConnected) {
      throw new Error('Wallet not connected');
    }
    
    if (typeof window === 'undefined' || !(window as any).ethereum) {
      throw new Error('MetaMask not available');
    }
    
    const ethereum = (window as any).ethereum;
    
    try {
      const signature = await ethereum.request({
        method: 'personal_sign',
        params: [message, this.walletInfo.address]
      });
      
      return signature;
    } catch (error) {
      console.error('Error signing message:', error);
      throw error;
    }
  }
  
  // Send transaction
  async sendTransaction(transaction: {
    to: string;
    value: string;
    data?: string;
  }): Promise<string> {
    if (!this.walletInfo.isConnected) {
      throw new Error('Wallet not connected');
    }
    
    if (typeof window === 'undefined' || !(window as any).ethereum) {
      throw new Error('MetaMask not available');
    }
    
    const ethereum = (window as any).ethereum;
    
    try {
      const txHash = await ethereum.request({
        method: 'eth_sendTransaction',
        params: [{
          from: this.walletInfo.address,
          to: transaction.to,
          value: transaction.value,
          data: transaction.data || '0x'
        }]
      });
      
      return txHash;
    } catch (error) {
      console.error('Error sending transaction:', error);
      throw error;
    }
  }
}

// Export singleton instance
export const walletService = new WalletService();
