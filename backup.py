import datetime
import logging
import subprocess
from os import path

import click
from dotenv import load_dotenv
from google.cloud import storage
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


@click.command()
@click.option("-M", "--mongo-uri", required=True, help="MongoDB connection string.")
@click.option(
    "-B", "--gcs-bucket-name", required=True, help="Google Cloud Storage bucket name."
)
@click.option(
    "-C",
    "--gcs-credentials",
    required=True,
    type=click.Path(exists=True),
    help="Path to the GCP service account JSON file.",
)
@click.option("--database-alias", "-A", type=str, required=True)
def backup_mongo_to_gcs(mongo_uri, gcs_bucket_name, gcs_credentials, database_alias):
    """
    Backs up a MongoDB database to a Google Cloud Storage bucket.
    """
    try:
        # 1. Connect to MongoDB
        click.echo("Connecting to MongoDB...")
        client = MongoClient(mongo_uri)
        # The ismaster command is cheap and does not require auth.
        client.admin.command("ismaster")
        click.echo("Successfully connected to MongoDB.")

        # 2. Create a database backup
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")
        backup_name = f"mongo_backup_{database_alias}_{timestamp}"
        backup_archive_name = f"{backup_name}.gz"

        click.echo(f"Creating MongoDB backup: {backup_archive_name}...")

        # Using mongodump to create a gzipped archive of the entire database
        mongodump_command = [
            "mongodump",
            f"--uri={mongo_uri}",
            f"--archive={backup_archive_name}",
            "--gzip",
        ]

        process = subprocess.Popen(
            mongodump_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            click.echo(f"Error during mongodump: {stderr.decode('utf-8')}", err=True)
            return

        click.echo("Backup created successfully.")

        # 3. Upload to Google Cloud Storage
        click.echo(f"Uploading backup to GCS bucket: {gcs_bucket_name}...")
        storage_client = storage.Client.from_service_account_json(gcs_credentials)
        bucket = storage_client.bucket(gcs_bucket_name)
        blob = bucket.blob(backup_archive_name)

        blob.upload_from_filename(backup_archive_name)
        click.echo(f"Backup {backup_archive_name} uploaded to {gcs_bucket_name}.")

    except ConnectionFailure as e:
        click.echo(f"MongoDB connection failed: {e}", err=True)
    except Exception as e:
        click.echo(f"An error occurred: {e}", err=True)


if __name__ == "__main__":
    fn = ".env"
    if path.isfile(fn):
        logging.warning(f"loading `{fn}`")
        load_dotenv(dotenv_path=fn)

    backup_mongo_to_gcs()
