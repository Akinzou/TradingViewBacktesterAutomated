# TradingView Backtester Automated [![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC_BY--NC--SA_4.0-lightgrey.svg)] [![Python package](https://github.com/Akinzou/TradingViewBacktesterAutomated/actions/workflows/python-app.yml/badge.svg)]

## Overview
TradingView Backtester Automated is a Python-based tool designed to help traders evaluate and optimize their trading strategies using TradingView alerts. By combining trading signals with historical price data, this tool provides detailed performance analytics, enabling users to make data-driven decisions.

## Features
Backtesting with TradingView Alerts: Load datasets containing trade alerts (entry/exit points) and historical price data for comprehensive backtesting.
Key Performance Metrics:
Profit and loss calculations.
Win rates analysis.
Evaluation of take-profit (TP) and stop-loss (SL) success rates.
Real-Time Trade Simulation:
Tracks price changes during open trades.
Ensures accurate evaluation of SL/TP triggers based on real-time price movements.
## How It Works
Import two datasets:
Trade Alerts Dataset: Entry and exit signals from TradingView alerts.
Historical Price Dataset: Historical price data to simulate price changes during trades.
The tool combines these datasets to simulate trades over time, checking for open positions and tracking price movements.
SL and TP conditions are continuously evaluated during the trade, ensuring realistic backtesting results.
## Benefits
Data-Driven Insights: Gain a clear understanding of how your trading strategies perform under different market conditions.
Detailed Analytics: Evaluate the effectiveness of your stop-loss and take-profit levels.
Customizable: Easily adapt the tool to different datasets and strategies.
