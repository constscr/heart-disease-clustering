from pathlib import Path

import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

from scripts.logger import setup_logger

# Initialization of the logger
logger = setup_logger(__name__)

# Configuration constants
DATASET_NAME = "redwankarimsony/heart-disease-data"
DATA_DIR = Path("./data/raw")
TARGET_FILE_NAME = "heart_disease_uci.csv"


def download_data(dataset: str, output_dir: Path, target_file: str) -> None:
    """
    Downloads the dataset from Kaggle and performs basic validation.
    """
    try:
        # API initialization and authentication
        api = KaggleApi()
        api.authenticate()

        # Create directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)

        # Download dataset
        logger.info(f"Starting download for dataset: {dataset}...")
        api.dataset_download_files(dataset, path=str(output_dir), unzip=True)

        # Validate and read the downloaded CSV file
        data_file_path = output_dir / target_file

        if data_file_path.exists():
            data = pd.read_csv(data_file_path)
            logger.info(f"Data successfully downloaded to {output_dir}!")
            logger.info(
                f"Dataset dimensions: {data.shape[0]} rows, {data.shape[1]} columns."
            )
        else:
            logger.error(f"File {target_file} not found after download completion.")

    except Exception:
        logger.exception("Download process interrupted due to an error:")


if __name__ == "__main__":
    download_data(DATASET_NAME, DATA_DIR, TARGET_FILE_NAME)
