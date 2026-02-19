from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def add_column():
    with engine.begin() as conn:
        print("Checking team1_contents columns...")
        result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='team1_contents'"))
        columns = [row[0] for row in result]
        print(f"Current columns: {columns}")
        
        if 'image_url' not in columns:
            print("Adding image_url column to team1_contents...")
            conn.execute(text("ALTER TABLE team1_contents ADD COLUMN image_url VARCHAR"))
            print("Column added successfully.")
        else:
            print("image_url column already exists.")

if __name__ == "__main__":
    add_column()
