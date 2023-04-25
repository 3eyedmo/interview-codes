from from_last_dkp import scrape_data
from jdatetime import date as jd
from pathlib import Path

detail_url = "https://api.digikala.com/v1/product"

total_data = [
    {
        "name": "Lens",
        "last_dkp": 10539299,
        "main_url": "https://api.digikala.com/v1/categories/mobile-lens-screen-protector/search/?sort=1"
    },
    {
        "name": "Glass-Phone",
        "last_dkp": 10551433,
        "main_url": "https://api.digikala.com/v1/categories/cell-phone-screen-guard/search/?sort=1"
    },
    {
        "name": "Glass-Watch",
        "last_dkp": 10551825,
        "main_url": "https://api.digikala.com/v1/categories/watch-accessorie/search/?sort=1"
    },
    {
        "name": "Glass-Tablet",
        "last_dkp": 10533084,
        "main_url": "https://api.digikala.com/v1/categories/tablet-screen-guard/search/?sort=1"
    },
    {
        "name": "Cover",
        "last_dkp": 10556607,
        "main_url": "https://api.digikala.com/v1/categories/cell-phone-pouch-cover/search/?sort=1"
    },
]
today = str(jd.today())
today_path = Path(f"data/{today}")
if not today_path.exists():
    today_path.mkdir()

for item in total_data:
    
    name = item.get("name")
    last_dkp = item.get("last_dkp")
    main_url = item.get("main_url")
    final_path = today_path / f"{name}-{last_dkp}.json"
    scrape_data(main_url=main_url, detail_url=detail_url, final_dkp=last_dkp, filename=final_path)


