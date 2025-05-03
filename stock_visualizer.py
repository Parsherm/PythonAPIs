__author__ = "Parker Sherman"
__copyright__ = "Copyright 2025 Parker Sherman"
__license__ = "Public Domain"
__version__ = "1.0"

"""
Stock Visualizer Application

This application allows users to visualize stock price data for technology companies
from the S&P 500 index. It provides a simple interface to select stocks and view
their price history over different time periods.

It was made with the intent to practice communication with APIs in python (via yfinance).
"""

import sys
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
import threading

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def get_tech_companies():
    """
    Fetch technology companies from the S&P 500 index.
    
    This function scrapes the Wikipedia page for S&P 500 components and filters
    for companies in the Information Technology sector.
    
    Returns:
        tuple: A tuple containing:
            - list: A list of stock ticker symbols for technology companies
            - dict: A dictionary mapping tickers to company names
    """
    # Get S&P 500 components
    sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    
    # Filter for tech companies (using GICS sector)
    tech_df = sp500[sp500['GICS Sector'] == 'Information Technology']
    tech_companies = tech_df['Symbol'].tolist()
    company_names = dict(zip(tech_df['Symbol'], tech_df['Security']))
    
    return tech_companies, company_names


def get_stock_data(ticker: str, days: int = 30):
    """
    Fetch historical stock data for a given ticker symbol.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL' for Apple)
        days (int): Number of days of historical data to fetch (default: 30)
        
    Returns:
        pandas.DataFrame: Stock data with date as index and OHLCV columns
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)
    return data


class StockVisualizerApp:
    """
    Main application class for the Stock Visualizer.
    
    This class handles the GUI interface and stock data visualization.
    It provides methods for:
    - Setting up the user interface
    - Loading and displaying stock data
    - Handling user interactions
    """
    
    def __init__(self, root):
        """
        Initialize the Stock Visualizer application.
        
        Args:
            root (tk.Tk): The root window for the application
        """
        self.root = root
        self.root.title("Tech Stock Visualizer")
        self.root.geometry("1000x800")
        self.root.minsize(800, 600)
        
        # Configure root grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Set up the protocol for window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Initialize data storage
        self.current_data = None
        self.current_ticker = None
        self.company_names = {}
        
        # Set up the UI
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the user interface components."""
        # Create main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Configure main frame grid
        self.main_frame.grid_rowconfigure(1, weight=1)  # Chart area
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Create control frame at the top
        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        # Configure control frame grid
        self.control_frame.grid_columnconfigure(0, weight=1)
        self.control_frame.grid_columnconfigure(1, weight=1)
        
        # Set up stock selection
        self._setup_stock_selection()
        
        # Set up time period selection
        self._setup_time_period()
        
        # Set up load button and status
        self._setup_controls()
        
        # Set up chart
        self._setup_chart()
    
    def _setup_stock_selection(self):
        """Set up the stock selection dropdown."""
        # Create stock selection frame
        self.stock_frame = tk.Frame(self.control_frame)
        self.stock_frame.grid(row=0, column=0, sticky="ew", padx=(0, 20))
        
        # Configure stock frame grid
        self.stock_frame.grid_columnconfigure(1, weight=1)
        
        self.stock_label = tk.Label(self.stock_frame, text="Select Stock:", font=('Arial', 10))
        self.stock_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        # Get tech companies and their names
        tech_companies, self.company_names = get_tech_companies()
        
        # Create a list of formatted strings for the dropdown
        self.company_display = [f"{ticker} - {name}" for ticker, name in self.company_names.items()]
        
        self.ticker_var = tk.StringVar()
        self.ticker_dropdown = ttk.Combobox(self.stock_frame, 
                                          textvariable=self.ticker_var, 
                                          values=self.company_display,
                                          font=('Arial', 10))
        self.ticker_dropdown.grid(row=0, column=1, sticky="ew")
        self.ticker_dropdown.set("Select a Tech Company")
    
    def _setup_time_period(self):
        """Set up the time period selection buttons."""
        # Create time period frame
        self.time_frame = tk.Frame(self.control_frame)
        self.time_frame.grid(row=0, column=1, sticky="ew")
        
        # Configure time frame grid
        self.time_frame.grid_columnconfigure(1, weight=1)
        
        self.time_label = tk.Label(self.time_frame, text="Time Period:", font=('Arial', 10))
        self.time_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        # Create time period buttons
        self.time_buttons_frame = tk.Frame(self.time_frame)
        self.time_buttons_frame.grid(row=0, column=1, sticky="ew")
        
        self.time_periods = {
            "1W": 7,
            "1M": 30,
            "3M": 90,
            "6M": 180,
            "1Y": 365,
            "5Y": 1825
        }
        
        self.time_var = tk.IntVar(value=30)  # Default to 1 month
        self.time_buttons = {}
        
        # Configure time buttons frame grid
        for i in range(len(self.time_periods)):
            self.time_buttons_frame.grid_columnconfigure(i, weight=1)
        
        for i, (period, days) in enumerate(self.time_periods.items()):
            btn = tk.Radiobutton(
                self.time_buttons_frame,
                text=period,
                variable=self.time_var,
                value=days,
                font=('Arial', 10),
                indicatoron=0,
                command=self.on_time_period_change
            )
            btn.grid(row=0, column=i, sticky="ew", padx=5)
            self.time_buttons[period] = btn
    
    def _setup_controls(self):
        """Set up the load button and status label."""
        # Create load button frame
        self.button_frame = tk.Frame(self.control_frame)
        self.button_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=15)
        
        # Configure button frame grid
        self.button_frame.grid_columnconfigure(0, weight=1)
        
        self.load_button = tk.Button(self.button_frame, 
                                   text="Load Stock Data", 
                                   command=self.load_stock_data,
                                   font=('Arial', 10),
                                   height=2)
        self.load_button.grid(row=0, column=0, sticky="ew")
        
        # Create status label frame
        self.status_frame = tk.Frame(self.control_frame)
        self.status_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
        
        # Configure status frame grid
        self.status_frame.grid_columnconfigure(0, weight=1)
        
        self.status_label = tk.Label(self.status_frame, 
                                   text="Select a stock and time period to begin",
                                   font=('Arial', 10),
                                   wraplength=800)
        self.status_label.grid(row=0, column=0, sticky="ew")
    
    def _setup_chart(self):
        """Set up the matplotlib chart."""
        # Create chart frame
        self.chart_frame = tk.Frame(self.main_frame)
        self.chart_frame.grid(row=1, column=0, sticky="nsew")
        
        # Configure chart frame grid
        self.chart_frame.grid_rowconfigure(0, weight=1)
        self.chart_frame.grid_columnconfigure(0, weight=1)
        
        self.fig, self.ax = plt.subplots(figsize=(12, 7))
        self.canvas = None
    
    def on_time_period_change(self):
        """Handle time period button selection."""
        if self.current_ticker is not None:
            self.load_stock_data()
    
    def on_closing(self):
        """Handle window closing event."""
        plt.close('all')
        self.root.destroy()
        sys.exit(0)
    
    def load_stock_data(self):
        """
        Load and display stock data for the selected ticker and time period.
        """
        # Extract ticker from the dropdown selection
        selection = self.ticker_var.get()
        if " - " in selection:
            ticker = selection.split(" - ")[0]
        else:
            ticker = selection
            
        days = self.time_var.get()
        
        if ticker in self.company_names:
            self.status_label.config(text=f"Loading data for {self.company_names[ticker]}...")
            # Run in a separate thread to keep UI responsive
            threading.Thread(target=self._load_and_plot, args=(ticker, days), daemon=True).start()
        else:
            self.status_label.config(text="Please select a valid tech company")
    
    def _load_and_plot(self, ticker, days):
        """
        Load stock data and update the chart.
        
        Args:
            ticker (str): Stock ticker symbol
            days (int): Number of days of data to display
        """
        try:
            data = get_stock_data(ticker, days)
            self.current_data = data
            self.current_ticker = ticker
            
            company_name = self.company_names[ticker]
            self.status_label.config(text=f"Latest {company_name} price: ${data['Close'][-1]:.2f}")
            
            # Clear previous plot
            self.ax.clear()
            
            # Create new plot
            self.ax.plot(data.index, data['Close'], label='Closing Price', linewidth=2)
            self.ax.set_title(f'{company_name} ({ticker}) - Last {days} Days', fontsize=12, pad=20)
            self.ax.set_xlabel('Date', fontsize=10)
            self.ax.set_ylabel('Price (USD)', fontsize=10)
            self.ax.grid(True, linestyle='--', alpha=0.7)
            self.ax.legend(fontsize=10)
            
            # Format x-axis dates
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Update the canvas
            if self.canvas is None:
                self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
                self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
            else:
                self.canvas.draw()
                
        except Exception as e:
            self.status_label.config(text=f"Error loading data: {str(e)}")


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = StockVisualizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
