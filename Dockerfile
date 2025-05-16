FROM python:3.11-slim

# Install all of the system dependencies
# python3-tk and libg11-... are for the gui
RUN apt-get update && \
    apt-get install -y python3-tk tk libgl1-mesa-glx && \
    apt-get-clean

# Set Working Directory
WORKDIR /app

# Copy the programs files
COPY . .

# Install Python Dependencies
RUN pip install --no-cache-dir -r requirments.txt

# Command to run the program
CMD ["python", "main.py"]