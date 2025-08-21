// Weather API Types
export interface WeatherData {
  location: string;
  latitude: number;
  longitude: number;
  hourly: HourlyWeather[];
}

export interface HourlyWeather {
  hour: number;
  solarIrradiance: number; // W/m²
  temperature: number; // °C
  humidity: number; // %
  cloudCover: number; // %
}

// Prosumer Types
export interface Prosumer {
  id: string;
  name: string;
  location: string;
  latitude?: number;
  longitude?: number;
  area: number; // m²
  efficiency: number; // %
  orientation: 'east' | 'southeast' | 'south' | 'southwest' | 'west';
  hasBattery: boolean;
  batteryCapacity: number; // kWh
  maxBuy: number; // kWh
  maxSell: number; // kWh
  price: number; // $/kWh
  role: 'prosumer' | 'retailer';
  netPosition?: number; // kWh, positive = surplus, negative = deficit
  finalPrice?: number; // $/kWh after VPP optimization
}

// Prediction Types
export interface GenerationPrediction {
  prosumerId: string;
  hourlyGeneration: number[]; // 24 hours
  totalDailyGeneration: number;
  weatherData?: WeatherData;
}

// Trading Types
export interface Trade {
  from: string;
  to: string;
  amount: number; // kWh
  price: number; // $/kWh
  cost: number; // $
}

export interface OptimizationResult {
  trades: Trade[];
  totalCost: number;
  totalRevenue: number;
  prosumerNetPositions: Record<string, number>;
}

// VPP Types
export interface VPPConfig {
  buyPrice: number; // $/kWh from retailer
  sellPrice: number; // $/kWh to retailer
  batteryCapacity: number; // kWh
  batteryEfficiency: number; // %
}

export interface VPPResult {
  batterySchedule: BatterySchedule[];
  externalTrades: ExternalTrade[];
  totalExternalBuy: number;
  totalExternalSell: number;
  prosumerFinalPrices: Record<string, number>;
}

export interface BatterySchedule {
  hour: number;
  action: 'charge' | 'discharge' | 'idle';
  change: number; // kWh
  level: number; // kWh
}

export interface ExternalTrade {
  type: 'buy' | 'sell';
  amount: number; // kWh
  price: number; // $/kWh
  total: number; // $
}

// Blockchain Types
export interface BlockchainTransaction {
  hash: string;
  from: string;
  to: string;
  amount: number;
  price: number;
  gasUsed: number;
  timestamp: string;
  status: 'pending' | 'confirmed' | 'failed';
}

// Wallet Types
export interface WalletInfo {
  address: string;
  chainId: number;
  isConnected: boolean;
  balance?: string;
}

// API Response Types
export interface WeatherAPIResponse {
  success: boolean;
  data?: WeatherData;
  error?: string;
}

export interface OptimizationAPIResponse {
  success: boolean;
  data?: OptimizationResult;
  error?: string;
}

export interface VPPAPIResponse {
  success: boolean;
  data?: VPPResult;
  error?: string;
}
