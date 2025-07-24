#===========================================================================================================================================

#-------------------------------------------------------------------------------------------------------------------------------------------
# Scraping information about the club
#-------------------------------------------------------------------------------------------------------------------------------------------
#
# This script scrapes Premier League performance statistics from official premier league website.
# Data collection includes:
#
# 
# 1) Gameweek-by-gameweek league table statistics for all clubs (2016/2017 - 2024/2025)
# 2) Home league table statistics by gameweek for all clubs (2016/2017 - 2024/2025)
# 3) Away league table statistics by gameweek for all clubs (2016/2017 - 2024/2025)
#
#===========================================================================================================================================



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import os

# Configuring chrome as browser for scraping
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")
service = Service()  # UPDATE THIS PATH
driver = webdriver.Chrome(service=service, options=chrome_options)

# Setting the range for scraping all the game week data from the 2008/2009 season to the 2024/2025 season
for year in range(2024, 2025, 1):


    #========================================================================================================================================================
    # We start collecting the data for each home and away gameweek from the 2016/2017 season
    for matchweek in range(1, 39, 1):
        gameweek_club_dict = {
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
        driver.get(f"https://www.premierleague.com/en/tables?competition=8&season={year}&round=L_1&matchweek={matchweek}&ha=-1")
        print("Page loaded")
        
        # looking for and accepting cookies 
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept')]"))
            ).click()
            print("Cookies accepted")
        except:
            print("No cookie banner found")

        # collecting the gameweek data for every season, and storing it in a specified directory
        try:
            club_rows = driver.find_elements(By.CSS_SELECTOR, "tbody.standings-table__table-body td.standings-row__container")

            for club_row in club_rows:
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

                gameweek_club_dict["position"].append(position)
                gameweek_club_dict["badge_url"].append(badge_url)
                gameweek_club_dict["name"].append(name)
                gameweek_club_dict["games_played"].append(games_played)
                gameweek_club_dict["games_won"].append(games_won)
                gameweek_club_dict["games_drawn"].append(games_drawn)
                gameweek_club_dict["games_lost"].append(games_lost)
                gameweek_club_dict["goals_for"].append(goals_for)
                gameweek_club_dict["goals_against"].append(goals_against)
                gameweek_club_dict["goal_difference"].append(goal_difference)
                gameweek_club_dict["points"].append(points)


        except Exception as e:
            print(e)

        # Convert to DataFrame and save
        gameweek_info = pd.DataFrame(gameweek_club_dict)

        # Define the DIRECTORY path, not the file path
        directory_path = f"C:/Users/daniel/Desktop/Serious Projects/web_scraping/new/datasets/league_table/home_and_away/gameweek_{year}/"

        # Create the directory if it doesn't exist
        os.makedirs(directory_path, exist_ok=True)

        # Now define the full file path
        game_week_info_dir = f"{directory_path}/{year}_gameweek_{matchweek}.csv"


        gameweek_info.to_csv(game_week_info_dir, index=False)
        print("Data saved to datasets/df_club_info.csv")

    # Finished collecting the data for each home and away gameweek from the 2016/2017 season
    #======================================================================================================================================================



    #========================================================================================================================================================
    # We start collecting the data for each home gameweek from the 2016/2017 season
    for matchweek in range(1, 39, 1):
        gameweek_club_dict = {
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
        driver.get(f"https://www.premierleague.com/en/tables?competition=8&season={year}&round=L_1&matchweek={matchweek}&ha=h")
        print("Page loaded")
        
        # looking for and accepting cookies 
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept')]"))
            ).click()
            print("Cookies accepted")
        except:
            print("No cookie banner found")

        # collecting the gameweek data for every season, and storing it in a specified directory
        try:
            club_rows = driver.find_elements(By.CSS_SELECTOR, "tbody.standings-table__table-body td.standings-row__container")

            for club_row in club_rows:
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

                gameweek_club_dict["position"].append(position)
                gameweek_club_dict["badge_url"].append(badge_url)
                gameweek_club_dict["name"].append(name)
                gameweek_club_dict["games_played"].append(games_played)
                gameweek_club_dict["games_won"].append(games_won)
                gameweek_club_dict["games_drawn"].append(games_drawn)
                gameweek_club_dict["games_lost"].append(games_lost)
                gameweek_club_dict["goals_for"].append(goals_for)
                gameweek_club_dict["goals_against"].append(goals_against)
                gameweek_club_dict["goal_difference"].append(goal_difference)
                gameweek_club_dict["points"].append(points)


        except Exception as e:
            print(e)

        # Convert to DataFrame and save
        gameweek_info = pd.DataFrame(gameweek_club_dict)

        # Define the DIRECTORY path, not the file path
        directory_path = f"C:/Users/daniel/Desktop/Serious Projects/web_scraping/new/datasets/league_table/home/home_gameweek_{year}/"

        # Create the directory if it doesn't exist
        os.makedirs(directory_path, exist_ok=True)

        # Now define the full file path
        game_week_info_dir = f"{directory_path}/{year}_home_gameweek_{matchweek}.csv"


        gameweek_info.to_csv(game_week_info_dir, index=False)

    # Finished collecting the data for each home gameweek from the 2016/2017 season
    #======================================================================================================================================================

    #========================================================================================================================================================
    # We start collecting the data for each away gameweek from the 2016/2017 season
    for matchweek in range(1, 39, 1):
        gameweek_club_dict = {
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
        driver.get(f"https://www.premierleague.com/en/tables?competition=8&season={year}&round=L_1&matchweek={matchweek}&ha=a")
        print("Page loaded")
        
        # looking for and accepting cookies 
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept')]"))
            ).click()
            print("Cookies accepted")
        except:
            print("No cookie banner found")

        # collecting the gameweek data for every season, and storing it in a specified directory
        try:
            club_rows = driver.find_elements(By.CSS_SELECTOR, "tbody.standings-table__table-body td.standings-row__container")

            for club_row in club_rows:
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

                gameweek_club_dict["position"].append(position)
                gameweek_club_dict["badge_url"].append(badge_url)
                gameweek_club_dict["name"].append(name)
                gameweek_club_dict["games_played"].append(games_played)
                gameweek_club_dict["games_won"].append(games_won)
                gameweek_club_dict["games_drawn"].append(games_drawn)
                gameweek_club_dict["games_lost"].append(games_lost)
                gameweek_club_dict["goals_for"].append(goals_for)
                gameweek_club_dict["goals_against"].append(goals_against)
                gameweek_club_dict["goal_difference"].append(goal_difference)
                gameweek_club_dict["points"].append(points)


        except Exception as e:
            print(e)

        # Convert to DataFrame and save
        gameweek_info = pd.DataFrame(gameweek_club_dict)

        # Define the DIRECTORY path, not the file path
        directory_path = f"C:/Users/daniel/Desktop/Serious Projects/web_scraping/new/datasets/league_table/away/away_gameweek_{year}/"

        # Create the directory if it doesn't exist
        os.makedirs(directory_path, exist_ok=True)

        # Now define the full file path
        game_week_info_dir = f"{directory_path}/{year}_away_gameweek_{matchweek}.csv"


        gameweek_info.to_csv(game_week_info_dir, index=False)
        print("Data saved to datasets/df_club_info.csv")

    # Finished collecting the data for each home and away gameweek from the 2016/2017 season
    #======================================================================================================================================================

 
driver.quit()

    

