"""
Configuration constants for the data domain modules.
"""
from pathlib import Path

# Storage (MinIO: S3-compatible object storage)
MINIO_ENDPOINT: str = "localhost:9000"
MINIO_ACCESS_KEY: str = "minioadmin"
MINIO_SECRET_KEY: str = "minioadmin"
MINIO_BUCKET: str = "data-lake"
MINIO_SECURE: bool = False  # Use True if using HTTPS

# Vector DB
MILVUS_HOST: str = "localhost"
MILVUS_PORT: str = "19530"
COLLECTION_NAME: str = "property_embeddings"
POSTGRES_URI: str = "postgresql://user:pass@localhost:5432/realestate"

# NLP
HF_SENTIMENT_MODEL: str = "distilbert-base-uncased-finetuned-sst-2-english"

# Logging
LOG_FILE: Path = Path("./logs/data_domain.log")