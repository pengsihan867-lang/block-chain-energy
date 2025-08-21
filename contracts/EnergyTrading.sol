// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract EnergyTrading {
    struct Trade {
        address buyer;
        address seller;
        uint256 energyAmount; // in kWh
        uint256 price; // in wei per kWh
        uint256 timestamp;
        bool isCompleted;
        bool isCancelled;
    }
    
    struct Order {
        address user;
        uint256 energyAmount; // in kWh
        uint256 price; // in wei per kWh
        bool isBuyOrder;
        uint256 timestamp;
        bool isActive;
    }
    
    mapping(uint256 => Trade) public trades;
    mapping(uint256 => Order) public orders;
    uint256 public tradeCounter;
    uint256 public orderCounter;
    
    event OrderPlaced(uint256 orderId, address user, uint256 energyAmount, uint256 price, bool isBuyOrder);
    event TradeExecuted(uint256 tradeId, address buyer, address seller, uint256 energyAmount, uint256 price);
    event OrderCancelled(uint256 orderId);
    
    // Place a buy or sell order
    function placeOrder(uint256 _energyAmount, uint256 _price, bool _isBuyOrder) public {
        require(_energyAmount > 0, "Energy amount must be greater than 0");
        require(_price > 0, "Price must be greater than 0");
        
        orderCounter++;
        orders[orderCounter] = Order({
            user: msg.sender,
            energyAmount: _energyAmount,
            price: _price,
            isBuyOrder: _isBuyOrder,
            timestamp: block.timestamp,
            isActive: true
        });
        
        emit OrderPlaced(orderCounter, msg.sender, _energyAmount, _price, _isBuyOrder);
        
        // Try to match orders
        _matchOrders();
    }
    
    // Match buy and sell orders
    function _matchOrders() internal {
        for (uint256 i = 1; i <= orderCounter; i++) {
            if (!orders[i].isActive) continue;
            
            for (uint256 j = i + 1; j <= orderCounter; j++) {
                if (!orders[j].isActive) continue;
                
                // Check if orders can be matched (one buy, one sell)
                if (orders[i].isBuyOrder != orders[j].isBuyOrder) {
                    Order storage buyOrder = orders[i].isBuyOrder ? orders[i] : orders[j];
                    Order storage sellOrder = orders[i].isBuyOrder ? orders[j] : orders[i];
                    
                    // Check if buy price >= sell price
                    if (buyOrder.price >= sellOrder.price) {
                        uint256 tradeAmount = _min(buyOrder.energyAmount, sellOrder.energyAmount);
                        
                        // Execute trade
                        tradeCounter++;
                        trades[tradeCounter] = Trade({
                            buyer: buyOrder.user,
                            seller: sellOrder.user,
                            energyAmount: tradeAmount,
                            price: sellOrder.price, // Use seller's price
                            timestamp: block.timestamp,
                            isCompleted: true,
                            isCancelled: false
                        });
                        
                        emit TradeExecuted(tradeCounter, buyOrder.user, sellOrder.user, tradeAmount, sellOrder.price);
                        
                        // Update order amounts
                        if (buyOrder.energyAmount == tradeAmount) {
                            orders[i].isActive = false;
                        } else {
                            orders[i].energyAmount -= tradeAmount;
                        }
                        
                        if (sellOrder.energyAmount == tradeAmount) {
                            orders[j].isActive = false;
                        } else {
                            orders[j].energyAmount -= tradeAmount;
                        }
                        
                        // Transfer ETH from buyer to seller
                        uint256 totalPrice = tradeAmount * sellOrder.price;
                        payable(sellOrder.user).transfer(totalPrice);
                    }
                }
            }
        }
    }
    
    // Cancel an order
    function cancelOrder(uint256 _orderId) public {
        require(orders[_orderId].user == msg.sender, "Only order owner can cancel");
        require(orders[_orderId].isActive, "Order is not active");
        
        orders[_orderId].isActive = false;
        emit OrderCancelled(_orderId);
    }
    
    // Get order details
    function getOrder(uint256 _orderId) public view returns (
        address user,
        uint256 energyAmount,
        uint256 price,
        bool isBuyOrder,
        uint256 timestamp,
        bool isActive
    ) {
        Order storage order = orders[_orderId];
        return (
            order.user,
            order.energyAmount,
            order.price,
            order.isBuyOrder,
            order.timestamp,
            order.isActive
        );
    }
    
    // Get trade details
    function getTrade(uint256 _tradeId) public view returns (
        address buyer,
        address seller,
        uint256 energyAmount,
        uint256 price,
        uint256 timestamp,
        bool isCompleted,
        bool isCancelled
    ) {
        Trade storage trade = trades[_tradeId];
        return (
            trade.buyer,
            trade.seller,
            trade.energyAmount,
            trade.price,
            trade.timestamp,
            trade.isCompleted,
            trade.isCancelled
        );
    }
    
    // Get active orders count
    function getActiveOrdersCount() public view returns (uint256) {
        uint256 count = 0;
        for (uint256 i = 1; i <= orderCounter; i++) {
            if (orders[i].isActive) {
                count++;
            }
        }
        return count;
    }
    
    // Helper function to find minimum
    function _min(uint256 a, uint256 b) internal pure returns (uint256) {
        return a < b ? a : b;
    }
    
    // Fallback function to receive ETH
    receive() external payable {}
}
