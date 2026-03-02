from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"

def crawl_catalog():

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    all_assessments = []
    start = 0
    step = 12

    while True:
        url = f"{CATALOG_URL}?start={start}"
        print(f"Opening: {url}")
        driver.get(url)
        time.sleep(4)

        rows = driver.find_elements(By.XPATH, "//table//tr")
        page_count = 0

        for row in rows:
            try:
                link = row.find_element(By.TAG_NAME, "a")
                name = link.text.strip()
                product_url = link.get_attribute("href")

                # Extract test types from this row
                badges = row.find_elements(By.CLASS_NAME, "product-catalogue__key")
                test_types = ",".join([b.text.strip() for b in badges])

                if name and product_url:
                    all_assessments.append({
                        "name": name,
                        "url": product_url,
                        "test_type": test_types
                    })
                    page_count += 1

            except:
                continue

        print(f"Collected {page_count} from this page")

        if page_count == 0:
            break

        start += step

    driver.quit()

    df = pd.DataFrame(all_assessments).drop_duplicates()

    print(f"\nTotal collected: {len(df)}")

    df.to_csv("data/shl_catalogue_with_types.csv", index=False)
    print("Saved to data/shl_catalogue_with_types.csv")

if __name__ == "__main__":
    crawl_catalog()