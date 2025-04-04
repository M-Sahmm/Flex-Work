#!/bin/bash

echo "Setting up Flex-CRM..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is required but not installed. Please install pip3 and try again."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env 2>/dev/null || echo "SECRET_KEY=demo-key-please-change-in-production" > .env
fi

# Initialize database
echo "Initializing database..."
python database/create_db.py

echo "Setup complete! You can now run the application with:"
echo "source venv/bin/activate"
echo "python main.py"
echo ""
echo "The application will be available at http://localhost:8000"
