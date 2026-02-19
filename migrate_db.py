from sqlalchemy import text
from app.db import engine

def migrate():
    with engine.connect() as conn:
        print("Checking for missing columns in team1_users...")
        try:
            # Check if columns exist
            result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='team1_users'"))
            existing_columns = [row[0] for row in result]
            
            if 'linkedin_access_token' not in existing_columns:
                print("Adding linkedin_access_token column...")
                conn.execute(text("ALTER TABLE team1_users ADD COLUMN linkedin_access_token VARCHAR"))
                
            if 'linkedin_id' not in existing_columns:
                print("Adding linkedin_id column...")
                conn.execute(text("ALTER TABLE team1_users ADD COLUMN linkedin_id VARCHAR"))
            
            conn.execute(text("COMMIT"))
            print("Migration successful.")
        except Exception as e:
            print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate()
