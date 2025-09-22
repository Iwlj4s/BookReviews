import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def test_postgres_connection():
    try:
        import asyncpg
        
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT')
        db_name = os.getenv('DB_NAME')
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD') 
        
        print(f"Try connect to: {db_user}@{db_host}:{db_port}/{db_name}")
        
        # Try to connect to default postgres DB
        conn = await asyncpg.connect(
            host=db_host,
            port=db_port,
            database='postgres',  
            user=db_user,
            password=db_password
        )
        
        version = await conn.fetchval('SELECT version()')
        print(f"Successfully connected to PostgreSQL: {version.split(',')[0]}")
        
        # Is bookreviews DB already exist?
        db_exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", db_name
        )
        
        if db_exists:
            print(f"DB '{db_name}' exist")
            await conn.close()
            
            # Connecting to bookreviews DB
            conn = await asyncpg.connect(
                host=db_host,
                port=db_port,
                database=db_name,
                user=db_user,
                password=db_password
            )
            print(f"Successfully connected to '{db_name}'")
            
        else:
            print(f"DB '{db_name}' doesent exist, creating...")
            await conn.execute(f'CREATE DATABASE {db_name}')
            print(f"DB '{db_name}' Created!")
        
        await conn.close()
        return True
        
    except Exception as e:
        print(f"Connection Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing connection to PostgreSQL...")
    result = asyncio.run(test_postgres_connection())
    if result:
        print("Test passed! PostgresQL ready to use")
    else:
        print("Test failed. Check your config")