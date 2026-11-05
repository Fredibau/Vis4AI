"""Download MASSIVE v1.1 (51 languages) into data/raw/.  Run once:  python src/download_data.py"""
import tarfile, urllib.request
from pathlib import Path

URL = "https://amazon-massive-nlu-dataset.s3.amazonaws.com/amazon-massive-dataset-1.1.tar.gz"
RAW = Path(__file__).resolve().parents[1] / "data" / "raw"

if __name__ == "__main__":
    archive = RAW / "massive-1.1.tar.gz"
    if not archive.exists():
        print("downloading", URL)
        urllib.request.urlretrieve(URL, archive)
    with tarfile.open(archive) as tar:
        tar.extractall(RAW, filter="data")
    print("done ->", RAW / "1.1" / "data")
