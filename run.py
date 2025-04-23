import os
from dotenv import load_dotenv; load_dotenv()
from main import create_app, register_signal_handlers

app = create_app()

if __name__ == '__main__':
    register_signal_handlers()
    app.run(host=os.getenv('HOST', '0.0.0.0'), port=int(os.getenv('PORT', 5000)))
