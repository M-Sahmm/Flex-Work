## Security Note

This is a demonstration project only!

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Flex-CRM.git
cd Flex-CRM
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - For demo purposes, you can use the default secret key or generate a new one

   OR

   - For quick demo setup, the app uses a hardcoded demo key (not recommended for production)

5. Initialize the database:
```bash
python database/create_db.py
```

6. Run the application:
```bash
python main.py
```

The application will be available at `http://localhost:8000`

## Project Structure

```
Flex-CRM/
├── app/
│   ├── __init__.py
│   ├── models/
│   └── routes/
├── database/
│   ├── create_db.py
│   └── database.db
├── static/
├── templates/
├── uploads/
├── .env.example
├── .gitignore
├── main.py
└── requirements.txt
```

## Dependencies

- Flask 3.0.2
- Werkzeug 3.0.1
- Flask-WTF 1.2.1
- python-dotenv 1.0.1
- Additional dependencies listed in requirements.txt

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

This is a demo project, but feel free to fork and modify for your own use.