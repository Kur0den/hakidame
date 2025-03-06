import boto3
import os
from dotenv import load_dotenv
import subprocess
import logging
import datetime

# .envファイルの読み込み
load_dotenv()

logging.basicConfig(level=logging.INFO)

def upload_to_s3(file_path, object_name):

    # 環境変数の取得
    S3_ENDPOINT = os.getenv('S3_ENDPOINT')
    S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
    S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
    S3_BUCKET = os.getenv('S3_BUCKET')

    # 未定義の環境変数がある場合はエラー
    if None in (S3_ENDPOINT, S3_ACCESS_KEY, S3_SECRET_KEY, S3_BUCKET):
        logging.error("Environment variables not set")
        raise ValueError("Environment variables not set")

    # boto3クライアントの作成
    s3_client = boto3.client('s3',
                            endpoint_url=S3_ENDPOINT,
                            aws_access_key_id=S3_ACCESS_KEY,
                            aws_secret_access_key=S3_SECRET_KEY)

    # ファイルのアップロード
    try:
        s3_client.upload_file(file_path, S3_BUCKET, object_name)
        logging.info(f"File {file_path} uploaded to {S3_BUCKET}/{object_name}")
        return
    except Exception as e:
        logging.error(f"Error uploading file: {e}")
        raise e

def dump_db(BACKUP_DIR):
    # 環境変数の取得
    DB_HOST = os.getenv('MARIADB_HOST')
    DB_PORT = os.getenv('MARIADB_PORT')
    DB_USER = os.getenv('MARIADB_USER')
    DB_PASS = os.getenv('MARIADB_PASS')
    DB_NAME = os.getenv('MARIADB_DATABASE')

    # 未定義の環境変数がある場合はエラー
    if None in (DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME):
        logging.error("Environment variables not set")
        raise ValueError("Environment variables not set")



    # バックアップファイルのパス
    backup_file = os.path.join(BACKUP_DIR, "mariadb_backup",  f"{DB_NAME}.sql")

    # mysqldumpコマンドの実行
    try:
        subprocess.run([
            'mysqldump',
            f'--host={DB_HOST}',
            f'--port={DB_PORT}',
            f'--user={DB_USER}',
            f'--password={DB_PASS}',
            DB_NAME,
            f'--result-file={backup_file}'
        ], check=True)
        logging.info(f"Database backup saved to {backup_file}")
        return backup_file
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during database backup: {e}")
        raise e

def main():
    # バックアップファイルの保存先
    # $XDG_CACHE_HOMEが設定されていない場合は$HOME/.cacheに保存
    BACKUP_DIR = os.getenv('XDG_CACHE_HOME', os.getenv('HOME', "~") + '/.cache')
    backup_file = dump_db(BACKUP_DIR)


    date = datetime.datetime.now().strftime("%Y-%m-%d")
    upload_to_s3(backup_file, f"mariadb_backup/{date}.sql")
