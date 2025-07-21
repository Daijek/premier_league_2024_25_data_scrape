#===========================================================================================================================================
# Now we scrape each club information
#===========================================================================================================================================
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

# Configure Chrome
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")
service = Service()  # UPDATE THIS PATH
driver = webdriver.Chrome(service=service, options=chrome_options)

# Scraper for every year from 2008 to 2025
for year in range(2008, 2025, 1):
    club_dict = {
        "position": [],
        "badge_url": [],
        "name": [],
        "games_played": [],
        "games_won": [],
        "games_drawn": [],
        "games_lost": [],
        "goals_for": [],
        "goals_against": [],
        "goal_difference": [],
        "points": []
    }
    try:
        driver.get(f"https://www.premierleague.com/en/tables?competition=8&season={year}&round=L_1&matchweek=38&ha=-1")
        print("Page loaded")
        
        # Accept cookies
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept')]"))
            ).click()
            print("Cookies accepted")
        except:
            print("No cookie banner found")
    except:
        pass

    try:
        club_rows = driver.find_elements(By.CSS_SELECTOR, "tbody.standings-table__table-body td.standings-row__container")

        for club_row in club_rows:
            print("here")
            position = club_row.find_element(By.CSS_SELECTOR, ".standings-row__position").text
            badge_url = club_row.find_element(By.CSS_SELECTOR, "img.club-badge__img").get_attribute("src")
            name = club_row.find_element(By.CSS_SELECTOR, "span.standings-row__team-name-long").text
            games_played = club_row.find_element(By.CSS_SELECTOR, ".standings-row__stat--played").text
            games_won = club_row.find_element(By.CSS_SELECTOR, ".standings-row__stat--won").text
            games_drawn = club_row.find_element(By.CSS_SELECTOR, ".standings-row__stat--drawn").text
            games_lost = club_row.find_element(By.CSS_SELECTOR, ".standings-row__stat--lost").text
            goals_for = club_row.find_element(By.CSS_SELECTOR, ".standings-row__stat--goals-for").text
            goals_against = club_row.find_element(By.CSS_SELECTOR, ".standings-row__stat--goals-against").text
            goal_difference = club_row.find_element(By.CSS_SELECTOR, ".standings-row__stat--goals-difference").text
            points = club_row.find_element(By.CSS_SELECTOR, ".standings-row__stat--points").text

            club_dict["position"].append(position)
            club_dict["badge_url"].append(badge_url)
            club_dict["name"].append(name)
            club_dict["games_played"].append(games_played)
            club_dict["games_won"].append(games_won)
            club_dict["games_drawn"].append(games_drawn)
            club_dict["games_lost"].append(games_lost)
            club_dict["goals_for"].append(goals_for)
            club_dict["goals_against"].append(goals_against)
            club_dict["goal_difference"].append(goal_difference)
            club_dict["points"].append(points)

            # print(club_dict)
            # print(sdfsd)

    except Exception as e:
        print(e)

    # Convert to DataFrame and save
    df_club_info = pd.DataFrame(club_dict)
    df_club_info.to_csv(f"C:/Users/daniel/Desktop/Serious Projects/web_scraping/new/datasets/club_info_{year}.csv", index=False)
    print("Data saved to datasets/df_club_info.csv")
    print(df_club_info)

driver.quit()

    

