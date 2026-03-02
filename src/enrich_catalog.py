from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def enrich_catalog():
    df = pd.read_csv("data/shl_catalogue_cleaned.csv")

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    descriptions = []
    durations = []
    adaptive_support = []
    remote_support = []
    test_types = []

    for index, row in df.iterrows():
        print(f"Processing {index+1}/{len(df)}")

        driver.get(row["url"])
        time.sleep(3)

        # Default values
        description = ""
        duration = ""
        adaptive = "No"
        remote = "No"
        test_type = ""

        try:
            # Description
            desc_element = driver.find_element(By.XPATH, "//meta[@name='description']")
            description = desc_element.get_attribute("content")
        except:
            pass

        try:
            # Duration (may appear in page text)
            duration_element = driver.find_element(By.XPATH, "//*[contains(text(),'minutes')]")
            duration = duration_element.text
        except:
            pass

        try:
            # Adaptive indicator
            adaptive_icon = driver.find_element(By.XPATH, "//*[contains(text(),'Adaptive')]")
            adaptive = "Yes"
        except:
            adaptive = "No"

        try:
            # Remote indicator
            remote_icon = driver.find_element(By.XPATH, "//*[contains(text(),'Remote')]")
            remote = "Yes"
        except:
            remote = "No"

        try:
            # Test Type badges
            badges = driver.find_elements(By.XPATH, "//div[contains(@class,'test-type')]//span")
            test_type = ",".join([b.text for b in badges])
        except:
            pass

        descriptions.append(description)
        durations.append(duration)
        adaptive_support.append(adaptive)
        remote_support.append(remote)
        test_types.append(test_type)

    driver.quit()

    df["description"] = descriptions
    df["duration"] = durations
    df["adaptive_support"] = adaptive_support
    df["remote_support"] = remote_support
    df["test_type"] = test_types

    df.to_csv("data/shl_catalogue_final.csv", index=False)
    print("Saved enriched dataset.")

if __name__ == "__main__":
    enrich_catalog()