"""
Object storage for the data lake using MinIO (S3-compatible).
"""
from typing import Union
from pathlib import Path
import pandas as pd
import io
from minio import Minio
from minio.error import S3Error
from ..utils import config

def get_minio_client() -> Minio:
    """
    Create and return a MinIO client using configuration variables.

    Returns:
        Configured Minio client.

    >>> isinstance(get_minio_client(), Minio)
    True
    """
    return Minio(
        endpoint=config.MINIO_ENDPOINT,
        access_key=config.MINIO_ACCESS_KEY,
        secret_key=config.MINIO_SECRET_KEY,
        secure=config.MINIO_SECURE
    )

def ensure_bucket_exists(client: Minio, bucket: str) -> None:
    """
    Ensure the specified bucket exists in MinIO, create if missing.

    Args:
        client: Minio client.
        bucket: Bucket name.

    >>> c = get_minio_client()
    >>> ensure_bucket_exists(c, config.MINIO_BUCKET)  # doctest: +SKIP
    """
    found = client.bucket_exists(bucket)
    if not found:
        client.make_bucket(bucket)

def save_parquet(df: pd.DataFrame, filename: Union[str, Path]) -> str:
    """
    Save a DataFrame as Parquet to MinIO.

    Args:
        df: DataFrame to save.
        filename: Object name (key) in the bucket.

    Returns:
        The object name.

    >>> import pandas as pd
    >>> df = pd.DataFrame({'a': [1, 2]})
    >>> save_parquet(df, 'test.parquet') == 'test.parquet'  # doctest: +SKIP
    True
    """
    client = get_minio_client()
    ensure_bucket_exists(client, config.MINIO_BUCKET)
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)
    client.put_object(
        config.MINIO_BUCKET,
        str(filename),
        buffer,
        length=buffer.getbuffer().nbytes,
        content_type="application/octet-stream"
    )
    return str(filename)

def load_parquet(filename: Union[str, Path]) -> pd.DataFrame:
    """
    Load a DataFrame from Parquet in MinIO.

    Args:
        filename: Object name in the bucket.

    Returns:
        Loaded DataFrame.

    >>> _ = save_parquet(pd.DataFrame({'a': [1]}), 'load_test.parquet')  # doctest: +SKIP
    >>> df = load_parquet('load_test.parquet')  # doctest: +SKIP
    >>> int(df.iloc[0,0]) == 1  # doctest: +SKIP
    True
    """
    client = get_minio_client()
    response = client.get_object(config.MINIO_BUCKET, str(filename))
    buffer = io.BytesIO(response.read())
    df = pd.read_parquet(buffer)
    response.close()
    response.release_conn()
    return df

def main() -> None:
    """
    CLI entrypoint for MinIO-based Parquet storage.

    Usage: python -m data_domain.lake.storage [save|load] filename

    >>> # Run main() in CLI, not as doctest.
    """
    import sys
    if len(sys.argv) < 3:
        print("Usage: python -m data_domain.lake.storage [save|load] filename")
        return
    cmd, filename = sys.argv[1], sys.argv[2]
    if cmd == "save":
        df = pd.DataFrame({'example': [1, 2, 3]})
        save_parquet(df, filename)
        print(f"Saved {filename} to MinIO.")
    elif cmd == "load":
        df = load_parquet(filename)
        print(df)
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()