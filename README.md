# Python API Hands-on | Country Info Viewer (Tkinter + REST + Redis + Docker)

I developed this project to gain experience with APIs in Python.

This is a program that allows you to search for any country and view detailed information — including its flag, population, region, and more — using the [REST Countries API](https://restcountries.com/).

To improve performance (albeit only slightly), the app caches API results using a Redis server running in Docker.

---

## How to Run
1. Make sure Docker Desktop is running.
2. (First time only) Install Python requirements:
  - pip install -r requirements.txt
3. Double-click start.bat.

The Redis server will start automatically in Docker, and the program will launch.
After the application is closed, the Redis server will close as well.

---

## Features

- Search for any country by name
- View info: flag, population, region, capital, currency, etc.
- Caches results in Redis for faster repeated queries
  -  A message is sent in the terminal when an item is loaded from the cache
- Simple GUI for ease of use

---

## Requirements

- Python 3.8 or higher
- Docker Desktop installed and running
- Python dependencies:
  pip install -r requirements.txt





