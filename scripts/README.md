# Setup Scripts

This directory contains scripts to help you set up the Flex-CRM application quickly.

## For Unix/Mac Users

```bash
./scripts/setup.sh
```

This will:
1. Check for Python and pip
2. Create a virtual environment
3. Install dependencies
4. Set up environment variables
5. Initialize the database

## For Windows Users

```cmd
scripts\setup.bat
```

This will perform the same setup steps as the Unix script.

## After Setup

Once setup is complete, you can start the application:

```bash
# Unix/Mac
source venv/bin/activate
python main.py

# Windows
venv\Scripts\activate
python main.py
```

The application will be available at `http://localhost:8000`

## Troubleshooting

If you encounter any issues:
1. Make sure Python 3.x is installed and in your PATH
2. Ensure you have write permissions in the project directory
3. Check that pip is installed and working
4. If the virtual environment fails, try creating it manually:
   ```bash
   python -m venv venv
   ```
