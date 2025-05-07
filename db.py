import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

conn_no_db = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    charset="utf8mb4",
    autocommit=True
)

def create_database_if_not_exists():
    with conn_no_db.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    print(f"已確認資料庫 `{DB_NAME}` 存在")

create_database_if_not_exists()

conn = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    db=DB_NAME,
    charset="utf8mb4"
)

def create_table():
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                description TEXT NOT NULL,
                image_url TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    conn.commit()
    print("✅ 已建立 `posts` 資料表（如尚未存在）")

def insert_post(description: str, image_url: str):
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO posts (description, image_url) VALUES (%s, %s)",
            (description, image_url)
        )
    conn.commit()

def get_all_posts():
    with conn.cursor() as cursor:
        cursor.execute("SELECT description, image_url, created_at FROM posts ORDER BY created_at DESC LIMIT 10")
        return cursor.fetchall()
