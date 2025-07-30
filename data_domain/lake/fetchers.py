"""
Data fetchers for competition, government and civic tech datasets.
Sources:
1. Kaggle Zillow Prize competition
2. Kaggle California Housing competition
3. Kaggle Ames Iowa competition
4. nadlan.gov.il (property transactions, maps, zoning, registration)
5. nadlan.taxes.gov.il (tax-related property data)
6. data.gov.il (permits, prices, construction)
7. cbs.gov.il (aggregate housing statistics)
8. opentaba (municipal zoning plan)
9. citizens4citizens (community engagement)
10. askdata (housing plans)
11. Hasadna projects (air, crime, environmental data)
"""
from pathlib import Path
from typing import Optional, Dict, Any, List, Union
import requests
import json
import subprocess

# Configuration
KAGGLE_USERNAME: str = "your_username"
KAGGLE_KEY: str = "your_key"
DATA_DIR: Path = Path("./data_raw")

def fetch_kaggle_dataset(dataset: str, dest: Optional[Path] = None) -> Path:
    """
    Download a dataset from Kaggle using the Kaggle API.

    Args:
        dataset: Kaggle dataset slug, e.g. "zillow/zecon"
        dest: Optional destination directory.

    Returns:
        Path to the downloaded zip file.

    >>> fetch_kaggle_dataset("zillow/zecon")  # doctest: +SKIP
    """
    dest = dest or DATA_DIR
    dest.mkdir(parents=True, exist_ok=True)
    kaggle_cmd = [
        "kaggle", "datasets", "download", "-d", dataset, "-p", str(dest)
    ]
    subprocess.run(kaggle_cmd, check=True)
    zip_files = list(dest.glob("*.zip"))
    if not zip_files:
        raise FileNotFoundError("No zip file found after Kaggle download.")
    return zip_files[0]

def fetch_kaggle_competition(competition: str, dest: Optional[Path] = None) -> Path:
    """
    Download files from a Kaggle competition.

    Args:
        competition: Kaggle competition slug, e.g. "house-prices-advanced-regression-techniques"
        dest: Optional destination directory.

    Returns:
        Path to the downloaded zip file.

    >>> fetch_kaggle_competition("house-prices-advanced-regression-techniques")  # doctest: +SKIP
    """
    dest = dest or DATA_DIR
    dest.mkdir(parents=True, exist_ok=True)
    kaggle_cmd = [
        "kaggle", "competitions", "download", "-c", competition, "-p", str(dest)
    ]
    subprocess.run(kaggle_cmd, check=True)
    zip_files = list(dest.glob("*.zip"))
    if not zip_files:
        raise FileNotFoundError("No zip file found after Kaggle download.")
    return zip_files[0]

def fetch_nadlan_gov_transactions(year: int, dest: Optional[Path] = None) -> Path:
    """
    Download property transactions data from nadlan.gov.il (data.gov.il resource).

    Args:
        year: The desired year (e.g. 2023).
        dest: Optional destination directory.

    Returns:
        Path to the downloaded JSON file with records.

    >>> fetch_nadlan_gov_transactions(2023)  # doctest: +SKIP
    """
    url = (f"https://data.gov.il/api/3/action/datastore_search"
           f"?resource_id=da54c6e7-6c2c-4e7b-9eae-32f7e7fb1317"
           f"&limit=100000&filters={{\"year\":{year}}}")
    dest = dest or DATA_DIR
    dest.mkdir(parents=True, exist_ok=True)
    r = requests.get(url)
    r.raise_for_status()
    file_path = dest / f"nadlan_transactions_{year}.json"
    file_path.write_text(r.text, encoding="utf-8")
    return file_path

def fetch_nadlan_taxes_transactions(page: int = 1, dest: Optional[Path] = None) -> Path:
    """
    Scrape tax-related property data from nadlan.taxes.gov.il.
    Note: This is a placeholder, as actual endpoints are not documented.

    Args:
        page: Page number.
        dest: Output directory.

    Returns:
        Path to the saved HTML.

    >>> fetch_nadlan_taxes_transactions(1)  # doctest: +SKIP
    """
    url = f"https://nadlan.taxes.gov.il/some_endpoint?page={page}"
    dest = dest or DATA_DIR
    dest.mkdir(parents=True, exist_ok=True)
    r = requests.get(url)
    r.raise_for_status()
    file_path = dest / f"nadlan_taxes_page_{page}.html"
    file_path.write_text(r.text, encoding="utf-8")
    return file_path

def fetch_datagov_resource(resource_id: str, dest: Optional[Path] = None) -> Path:
    """
    Download a resource from data.gov.il by resource_id.

    Args:
        resource_id: The resource ID as appears on data.gov.il.
        dest: Output directory.

    Returns:
        Path to the saved file (CSV, XLSX, etc).

    >>> fetch_datagov_resource("da54c6e7-6c2c-4e7b-9eae-32f7e7fb1317")  # doctest: +SKIP
    """
    info_url = f"https://data.gov.il/api/3/action/resource_show?id={resource_id}"
    r = requests.get(info_url)
    r.raise_for_status()
    info = r.json()
    url = info["result"]["url"]
    dest = dest or DATA_DIR
    dest.mkdir(parents=True, exist_ok=True)
    r2 = requests.get(url)
    r2.raise_for_status()
    file_name = url.split("/")[-1]
    file_path = dest / file_name
    file_path.write_bytes(r2.content)
    return file_path

def fetch_cbs_table(table_id: str, dest: Optional[Path] = None) -> Path:
    """
    Download a table (XLS, CSV) from cbs.gov.il open data.

    Args:
        table_id: Table ID as on CBS site.
        dest: Output directory.

    Returns:
        Path to the saved file.

    >>> fetch_cbs_table("shnaton/2023/06_01.xlsx")  # doctest: +SKIP
    """
    base_url = "https://www.cbs.gov.il/he/publications/doclib"
    url = f"{base_url}/{table_id}"
    dest = dest or DATA_DIR
    dest.mkdir(parents=True, exist_ok=True)
    r = requests.get(url)
    r.raise_for_status()
    file_name = url.split("/")[-1]
    file_path = dest / file_name
    file_path.write_bytes(r.content)
    return file_path

def fetch_opentaba_plan(plan_id: str, dest: Optional[Path] = None) -> Path:
    """
    Download zoning plan data (JSON) from opentaba.

    Args:
        plan_id: Opentaba plan id.
        dest: Output directory.

    Returns:
        Path to the saved JSON.

    >>> fetch_opentaba_plan("100-0136956")  # doctest: +SKIP
    """
    url = f"https://opentaba-server.herokuapp.com/api/plans/{plan_id}"
    dest = dest or DATA_DIR
    dest.mkdir(parents=True, exist_ok=True)
    r = requests.get(url)
    r.raise_for_status()
    file_path = dest / f"opentaba_plan_{plan_id}.json"
    file_path.write_text(r.text, encoding="utf-8")
    return file_path

def fetch_citizens4citizens_projects(dest: Optional[Path] = None) -> Path:
    """
    Scrape community engagement projects from citizens4citizens.
    This endpoint is not officially documented and may change.

    Args:
        dest: Output directory.

    Returns:
        Path to saved JSON.

    >>> fetch_citizens4citizens_projects()  # doctest: +SKIP
    """
    url = "https://c4c.org.il/api/projects"
    dest = dest or DATA_DIR
    dest.mkdir(parents=True, exist_ok=True)
    r = requests.get(url)
    if r.status_code != 200:
        raise RuntimeError("API endpoint not available or has changed.")
    file_path = dest / "c4c_projects.json"
    file_path.write_text(r.text, encoding="utf-8")
    return file_path

def fetch_askdata_housing_plans(dest: Optional[Path] = None) -> Path:
    """
    Download housing plans from askdata.
    This endpoint is not officially documented and may change.

    Args:
        dest: Output directory.

    Returns:
        Path to saved data.

    >>> fetch_askdata_housing_plans()  # doctest: +SKIP
    """
    url = "https://askdata.co.il/api/plans?limit=1000"
    dest = dest or DATA_DIR
    dest.mkdir(parents=True, exist_ok=True)
    r = requests.get(url)
    if r.status_code != 200:
        raise RuntimeError("API endpoint not available or has changed.")
    file_path = dest / "askdata_housing_plans.json"
    file_path.write_text(r.text, encoding="utf-8")
    return file_path

def fetch_hasadna_openpolice_crime(city: str, dest: Optional[Path] = None) -> Path:
    """
    Download crime data for a city from Hasadna OpenPolice API.

    Args:
        city: City name in Hebrew or English (as in the API).
        dest: Output directory.

    Returns:
        Path to saved JSON.

    >>> fetch_hasadna_openpolice_crime("תל אביב-יפו")  # doctest: +SKIP
    """
    # See https://openpolice.hasadna.org.il/api/
    url = f"https://openpolice.hasadna.org.il/api/events/?city={city}"
    dest = dest or DATA_DIR
    dest.mkdir(parents=True, exist_ok=True)
    r = requests.get(url)
    r.raise_for_status()
    file_path = dest / f"hasadna_openpolice_{city}.json"
    file_path.write_text(r.text, encoding="utf-8")
    return file_path

def fetch_hasadna_openmunicipality_air(city_code: int, dest: Optional[Path] = None) -> Path:
    """
    Download air/environmental data for a city from Hasadna OpenMunicipality API.

    Args:
        city_code: City code as per the API (e.g. 5000 for Tel Aviv).
        dest: Output directory.

    Returns:
        Path to saved JSON.

    >>> fetch_hasadna_openmunicipality_air(5000)  # doctest: +SKIP
    """
    # See https://municipaldata.hasadna.org.il/api/
    url = f"https://municipaldata.hasadna.org.il/api/air_quality/{city_code}"
    dest = dest or DATA_DIR
    dest.mkdir(parents=True, exist_ok=True)
    r = requests.get(url)
    r.raise_for_status()
    file_path = dest / f"hasadna_openmunicipality_air_{city_code}.json"
    file_path.write_text(r.text, encoding="utf-8")
    return file_path

def fetch_kaggle_zillow_prize(dest: Optional[Path] = None) -> Path:
    """Shortcut for the Kaggle Zillow Prize competition dataset."""
    return fetch_kaggle_competition("zillow-prize-1", dest)

def fetch_kaggle_california_housing(dest: Optional[Path] = None) -> Path:
    """Shortcut for the Kaggle California Housing competition dataset."""
    return fetch_kaggle_dataset("camnugent/california-housing-prices", dest)

def fetch_kaggle_ames_iowa(dest: Optional[Path] = None) -> Path:
    """Shortcut for the Kaggle Ames Iowa competition dataset."""
    return fetch_kaggle_competition("house-prices-advanced-regression-techniques", dest)

def main() -> None:
    """
    CLI entrypoint for fetchers.
    Usage: python -m data_domain.lake.fetchers <fetcher> [params...]

    >>> # Run from CLI
    """
    import sys
    import pprint
    fetchers = {
        "kaggle_zillow": fetch_kaggle_zillow_prize,
        "kaggle_california": fetch_kaggle_california_housing,
        "kaggle_ames": fetch_kaggle_ames_iowa,
        "nadlan_gov": fetch_nadlan_gov_transactions,
        "nadlan_taxes": fetch_nadlan_taxes_transactions,
        "datagov": fetch_datagov_resource,
        "cbs": fetch_cbs_table,
        "opentaba": fetch_opentaba_plan,
        "c4c": fetch_citizens4citizens_projects,
        "askdata": fetch_askdata_housing_plans,
        "hasadna_crime": fetch_hasadna_openpolice_crime,
        "hasadna_air": fetch_hasadna_openmunicipality_air,
    }
    if len(sys.argv) < 2:
        print("Available fetchers:", list(fetchers.keys()))
        return
    fn = fetchers.get(sys.argv[1])
    if not fn:
        print(f"Fetcher '{sys.argv[1]}' not found.")
        return
    args = sys.argv[2:]
    result = fn(*args)
    pprint.pprint(result)

if __name__ == "__main__":
    main()