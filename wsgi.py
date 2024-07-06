from app import create_app
from config import Config
from dotenv import load_dotenv

load_dotenv()

app = create_app()
app.config.from_object(Config)

if __name__ == "__main__":
    app.run()
