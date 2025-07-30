# Data Domain: Open Source Python Implementation

## 1. Data Lake (Raw Data)
- **Purpose:** Store ingested raw data from APIs, web scrapers, and file uploads.
- **Implementation:**  
  - Use [Apache Parquet](https://parquet.apache.org/) or [Arrow](https://arrow.apache.org/) formats.
  - Store files locally or in cloud-compatible storage (e.g., [MinIO](https://min.io/), which is S3-compatible and open-source).
  - Use [pandas](https://pandas.pydata.org/) and [pyarrow](https://arrow.apache.org/docs/python/) for reading/writing.

## 2. Data Cleaning & Transformation
- **Purpose:** Standardize, deduplicate, validate, and enrich raw data.
- **Implementation:**  
  - Use [pandas](https://pandas.pydata.org/) for tabular data cleaning.
  - Use [Great Expectations](https://greatexpectations.io/) for data validation and pipeline documentation.
  - Modular pipeline with [Apache Airflow](https://airflow.apache.org/) or [Prefect](https://www.prefect.io/) for orchestration.

## 3. Index Calculation (P2R, Cap Rate, etc.)
- **Purpose:** Compute real estate indices (e.g., Price-to-Rent, Cap Rate).
- **Implementation:**  
  - Pure Python modules with [pandas](https://pandas.pydata.org/) for calculation logic.
  - Each index calculation as a function with typed inputs/outputs.
  - Easily extensible for new indices.

## 4. Time Series Analysis
- **Purpose:** Analyze market trends, forecast prices, etc.
- **Implementation:**  
  - Use [statsmodels](https://www.statsmodels.org/), [scikit-learn](https://scikit-learn.org/), [Prophet](https://facebook.github.io/prophet/) (if license fits).
  - Focus on open, local-servable models.
  - Modular pipeline for feature extraction, training, and forecasting.

## 5. Review Text Processing
- **Purpose:** NLP on property reviews for sentiment, topic extraction, etc.
- **Implementation:**  
  - Use [spaCy](https://spacy.io/) or [NLTK](https://www.nltk.org/) for NLP tasks.
  - [scikit-learn](https://scikit-learn.org/) for classical ML models.
  - Optional: [Haystack](https://haystack.deepset.ai/) for QA over text corpus.

## 6. Property Photo Processing
- **Purpose:** Analyze property images for features/quality/scoring.
- **Implementation:**  
  - Use [OpenCV](https://opencv.org/) and [scikit-image](https://scikit-image.org/).
  - For deep learning (if needed): [torchvision](https://pytorch.org/vision/stable/index.html) with pre-trained, locally-runnable models.

## 7. Recommendation Services
- **Purpose:** Suggest properties based on user and market data.
- **Implementation:**  
  - [Surprise](http://surpriselib.com/) (collaborative filtering), [scikit-learn](https://scikit-learn.org/) for classic recommenders.
  - Modular recommendation pipeline.

## 8. Forecasting Algorithms
- **Purpose:** Predict rents, prices, trends.
- **Implementation:**  
  - [scikit-learn](https://scikit-learn.org/), [Prophet](https://facebook.github.io/prophet/), [statsmodels](https://www.statsmodels.org/).
  - Emphasize model transparency and auditability.

## 9. Data Warehouse (RDBMS)
- **Purpose:** Store cleaned, structured, and indexed data.
- **Implementation:**  
  - [PostgreSQL](https://www.postgresql.org/) with [SQLAlchemy](https://www.sqlalchemy.org/) ORM for Python.
  - Schema managed via [Alembic](https://alembic.sqlalchemy.org/).

## 10. NoSQL Databases
- **Purpose:** Store semi-structured data (documents, logs, time-series).
- **Implementation:**  
  - [MongoDB](https://www.mongodb.com/) (open-source edition) or [Apache Cassandra](https://cassandra.apache.org/) for scalability.
  - Access via [pymongo](https://pymongo.readthedocs.io/) or [cassandra-driver](https://docs.datastax.com/en/developer/python-driver/latest/).

---

## Directory Structure Proposal

```plaintext
data_domain/
  __init__.py
  config.py  # All constants, connection strings, etc.
  lake/
    ingest.py
    storage.py
  cleaning/
    pipeline.py
    validation.py
  indices/
    p2r.py
    cap_rate.py
  timeseries/
    analysis.py
    forecasting.py
  nlp/
    review_processing.py
  image/
    photo_processing.py
  recommend/
    recommender.py
  warehouse/
    models.py
    schema.py
    loader.py
  nosql/
    mongo.py
    cassandra.py
  utils/
    logging.py
    helpers.py
```

---

## Example: Index Calculation (P2R)

```python
from typing import Optional
import pandas as pd

def calculate_p2r(price: float, annual_rent: float) -> Optional[float]:
    """
    Calculate Price-to-Rent ratio.

    Args:
        price: Property price (numeric).
        annual_rent: Total annual rent (numeric).

    Returns:
        P2R ratio, or None if input is invalid.

    >>> calculate_p2r(1000000, 50000)
    20.0
    >>> calculate_p2r(0, 50000)
    0.0
    >>> calculate_p2r(1000000, 0) is None
    True
    """
    if annual_rent <= 0:
        return None
    return price / annual_rent
```

---

## Example: Data Cleaning Pipeline

```python
import pandas as pd
from typing import Callable, List

def clean_dataframe(df: pd.DataFrame, cleaning_steps: List[Callable[[pd.DataFrame], pd.DataFrame]]) -> pd.DataFrame:
    """
    Apply a list of cleaning functions to a DataFrame.

    Args:
        df: Input DataFrame.
        cleaning_steps: List of functions that accept and return a DataFrame.

    Returns:
        Cleaned DataFrame.

    >>> import pandas as pd
    >>> def drop_na(df): return df.dropna()
    >>> df = pd.DataFrame({'a': [1, None, 3]})
    >>> clean_dataframe(df, [drop_na])
       a
    0  1.0
    2  3.0
    """
    for step in cleaning_steps:
        df = step(df)
    return df
```

---

## References

- [Awesome Open Source Data Engineering](https://github.com/pditommaso/awesome-data-engineering)
- [pandas Documentation](https://pandas.pydata.org/docs/)
- [Great Expectations Docs](https://docs.greatexpectations.io/)
- [scikit-learn Examples](https://scikit-learn.org/stable/auto_examples/index.html)
- [spaCy Usage Examples](https://spacy.io/usage)
- [OpenCV Python Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)