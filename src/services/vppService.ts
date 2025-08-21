import { VPPConfig, VPPResult, BatterySchedule, ExternalTrade, Prosumer } from '../types';

// Default VPP configuration
const DEFAULT_VPP_CONFIG: VPPConfig = {
  buyPrice: 0.35, // $/kWh from retailer
  sellPrice: 0.22, // $/kWh to retailer
  batteryCapacity: 5, // kWh
  batteryEfficiency: 0.9 // 90%
};

// VPP optimization service
export class VPPOptimizationService {
  private config: VPPConfig;
  
  constructor(config: Partial<VPPConfig> = {}) {
    this.config = { ...DEFAULT_VPP_CONFIG, ...config };
  }
  
  // Optimize VPP operations and calculate final prices
  optimizeVPP(
    prosumers: Prosumer[],
    netPositions: Record<string, number>
  ): VPPResult {
    // Calculate battery schedule
    const batterySchedule = this.calculateBatterySchedule(netPositions);
    
    // Calculate external trades
    const externalTrades = this.calculateExternalTrades(netPositions, batterySchedule);
    
    // Calculate final prices for each prosumer
    const prosumerFinalPrices = this.calculateFinalPrices(prosumers, netPositions, externalTrades);
    
    return {
      batterySchedule,
      externalTrades,
      totalExternalBuy: externalTrades.filter(t => t.type === 'buy').reduce((sum, t) => sum + t.amount, 0),
      totalExternalSell: externalTrades.filter(t => t.type === 'sell').reduce((sum, t) => sum + t.amount, 0),
      prosumerFinalPrices
    };
  }
  
  // Calculate optimal battery charging/discharging schedule
  private calculateBatterySchedule(netPositions: Record<string, number>): BatterySchedule[] {
    const schedule: BatterySchedule[] = [];
    let batteryLevel = this.config.batteryCapacity / 2; // Start at 50%
    
    // Aggregate net positions by hour (simplified - assuming 24-hour data)
    const hourlyNetPositions = this.aggregateHourlyPositions(netPositions);
    
    hourlyNetPositions.forEach((netPosition, hour) => {
      let action: 'charge' | 'discharge' | 'idle' = 'idle';
      let change = 0;
      
      if (netPosition > 0 && batteryLevel < this.config.batteryCapacity) {
        // Surplus energy - charge battery
        action = 'charge';
        change = Math.min(netPosition, this.config.batteryCapacity - batteryLevel);
        batteryLevel += change * this.config.batteryEfficiency;
      } else if (netPosition < 0 && batteryLevel > 0) {
        // Energy deficit - discharge battery
        action = 'discharge';
        change = Math.min(-netPosition, batteryLevel);
        batteryLevel -= change / this.config.batteryEfficiency;
      }
      
      schedule.push({
        hour,
        action,
        change,
        level: Math.max(0, Math.min(this.config.batteryCapacity, batteryLevel))
      });
    });
    
    return schedule;
  }
  
  // Calculate external trades with retailers
  private calculateExternalTrades(
    netPositions: Record<string, number>,
    batterySchedule: BatterySchedule[]
  ): ExternalTrade[] {
    const externalTrades: ExternalTrade[] = [];
    
    // Calculate total VPP net position after battery optimization
    const totalNetPosition = Object.values(netPositions).reduce((sum, pos) => sum + pos, 0);
    
    // Calculate battery contribution
    const batteryContribution = batterySchedule.reduce((sum, schedule) => {
      if (schedule.action === 'charge') return sum - schedule.change;
      if (schedule.action === 'discharge') return sum + schedule.change;
      return sum;
    }, 0);
    
    const finalNetPosition = totalNetPosition + batteryContribution;
    
    if (finalNetPosition > 0) {
      // VPP has surplus - sell to retailer
      externalTrades.push({
        type: 'sell',
        amount: finalNetPosition,
        price: this.config.sellPrice,
        total: finalNetPosition * this.config.sellPrice
      });
    } else if (finalNetPosition < 0) {
      // VPP has deficit - buy from retailer
      externalTrades.push({
        type: 'buy',
        amount: -finalNetPosition,
        price: this.config.buyPrice,
        total: -finalNetPosition * this.config.buyPrice
      });
    }
    
    return externalTrades;
  }
  
  // Calculate final settlement prices for each prosumer
  private calculateFinalPrices(
    prosumers: Prosumer[],
    netPositions: Record<string, number>,
    externalTrades: ExternalTrade[]
  ): Record<string, number> {
    const finalPrices: Record<string, number> = {};
    
    prosumers.forEach(prosumer => {
      const netPosition = netPositions[prosumer.id] || 0;
      
      if (netPosition === 0) {
        // No net position - use original price
        finalPrices[prosumer.id] = prosumer.price;
      } else if (netPosition > 0) {
        // Surplus - VPP sells to retailer at lower price
        finalPrices[prosumer.id] = this.config.sellPrice;
      } else {
        // Deficit - VPP buys from retailer at higher price
        finalPrices[prosumer.id] = this.config.buyPrice;
      }
    });
    
    return finalPrices;
  }
  
  // Aggregate net positions by hour (simplified implementation)
  private aggregateHourlyPositions(netPositions: Record<string, number>): number[] {
    // This is a simplified implementation
    // In a real system, you would have hourly net positions for each prosumer
    const hourly: number[] = [];
    
    for (let hour = 0; hour < 24; hour++) {
      // Simulate hourly variation based on total net position
      const totalNet = Object.values(netPositions).reduce((sum, pos) => sum + pos, 0);
      const hourlyVariation = Math.sin((hour - 6) * Math.PI / 12) * 0.3; // Peak at noon
      hourly.push(totalNet * (1 + hourlyVariation));
    }
    
    return hourly;
  }
  
  // Update VPP configuration
  updateConfig(newConfig: Partial<VPPConfig>): void {
    this.config = { ...this.config, ...newConfig };
  }
  
  // Get current VPP configuration
  getConfig(): VPPConfig {
    return { ...this.config };
  }
}

// Export singleton instance
export const vppService = new VPPOptimizationService();
