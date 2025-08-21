# 🚀 VPP Energy Trading System - Advanced Upgrade

## 🌟 新增功能模块

### 🌦️ 模块 1：天气数据接入
- ✅ 地理位置输入（城市名或经纬度）
- ✅ OpenWeatherMap API 集成
- ✅ 24小时太阳辐照度数据获取
- ✅ 基于真实天气的动态光伏发电量计算
- ✅ 可视化柱状图展示

### ⚡ 模块 2：VPP优化后电价展示
- ✅ VPP Layer 模块
- ✅ Prosumer 净头寸计算
- ✅ VPP 统一对外交易电价
- ✅ 最终结算电价展示
- ✅ 优化前后对比分析

### 🔐 模块 3：MetaMask 钱包集成
- ✅ "Connect Wallet" 按钮
- ✅ @metamask/detect-provider 集成
- ✅ ethers.js 支持
- ✅ 钱包地址显示和账户切换
- ✅ 交易上链功能

## 🛠️ 安装依赖

### 1. 安装 Node.js 依赖
```bash
npm install
```

### 2. 安装 TypeScript 和构建工具
```bash
npm install -D typescript vite @types/node
```

### 3. 配置 API 密钥
在 `src/services/weatherService.ts` 中替换：
```typescript
const OPENWEATHER_API_KEY = 'YOUR_API_KEY_HERE';
```

## 🏗️ 项目结构

```
src/
├── components/          # React 组件
├── services/           # 服务层
│   ├── weatherService.ts    # 天气 API 服务
│   ├── vppService.ts        # VPP 优化服务
│   └── walletService.ts     # MetaMask 钱包服务
├── types/              # TypeScript 类型定义
├── utils/              # 工具函数
└── index.tsx           # 主入口文件
```

## 🚀 使用方法

### 1. 启动开发服务器
```bash
npm run dev
```

### 2. 构建生产版本
```bash
npm run build
```

### 3. 预览构建结果
```bash
npm run preview
```

## 🔧 配置说明

### 天气 API 配置
- 支持 OpenWeatherMap API
- 内置演示数据（纽约、伦敦、东京、悉尼、北京）
- 自动回退到演示数据

### VPP 配置
- 默认购电价格：$0.35/kWh
- 默认售电价格：$0.22/kWh
- 电池容量：5 kWh
- 电池效率：90%

### 钱包配置
- 支持 MetaMask 扩展
- 支持多链网络
- 自动检测网络切换

## 📱 功能特性

- **响应式设计**：支持桌面和移动设备
- **实时更新**：天气数据和交易状态实时刷新
- **可视化图表**：24小时发电预测图表
- **智能优化**：VPP 自动优化算法
- **区块链集成**：完整的交易上链流程

## 🌐 访问地址

开发环境：http://localhost:3000
生产环境：https://pengsihan867-lang.github.io/block-chain-energy/

## 📞 技术支持

如有问题，请查看：
1. 浏览器控制台错误信息
2. 网络请求状态
3. MetaMask 连接状态
4. API 密钥配置

## 🔄 更新日志

### v2.0.0 (2025-08-21)
- ✨ 新增天气数据接入
- ✨ 新增 VPP 优化电价
- ✨ 新增 MetaMask 钱包集成
- 🎨 使用 TypeScript 重构
- 🎨 集成 TailwindCSS
- 🚀 性能优化和代码重构
