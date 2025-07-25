#=====================================================================================================================================
#-------------------------------------------------------------------------------------------------------------------------------------
# Scraping statistical information about the premiere league clubs from 2016/2017 to 2024/2025 season
#-------------------------------------------------------------------------------------------------------------------------------------
#
#



#=====================================================================================================================================


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import os
import csv

# Configure Chrome
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")
service = Service()  # UPDATE THIS PATH
driver = webdriver.Chrome(service=service, options=chrome_options)


#====================================================================================================================================
# Scraping all time premier league clubs names and urls
driver.get("https://www.premierleague.com/en/clubs")

# looking for and accepting cookies 
try:
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept')]"))
    ).click()
    print("Cookies accepted")
except:
    print("No cookie banner found")

# Creating a dictionary to hold prem club names and urls
all_prem_clubs_dict = {
    "club_name": [],
    "club_url": []
}

all_prem_clubs = driver.find_elements(By.CSS_SELECTOR, ".club-listings-table__table-body .club-listings-row")
for prem_club in all_prem_clubs:
    


    club_url = prem_club.find_element(By.CSS_SELECTOR, "a.club-listings-row__team").get_attribute("href")
    club_name = prem_club.find_element(By.CSS_SELECTOR, "p.club-listings-row__team-name span").text

    # Adding the base url, and changing the URL from overview to stats
    base_url = "https://www.premierleague.com"

    

    # Making the URL absolute
    if club_url.startswith("/"):
        club_url = base_url + club_url
    

    # Replacing the overview url with stats url
    club_url = club_url.replace("/overview", "/stats")

    # add the name and url to the dictionary
    all_prem_clubs_dict["club_name"].append(club_name)
    all_prem_clubs_dict["club_url"].append(club_url)

#====================================================================================================================================



#====================================================================================================================================
# Using the club paths stored in dictionary to scrape club stats from 23016/2017 season to 2024/2025 season
for club_no, club_url in enumerate(all_prem_clubs_dict["club_url"]):
    driver.get(club_url)

    # -------------------------------------------------------------------------------------------------------------------------------
    # looking for cookies, and applying season filter for search
    # looking for and accepting cookies 
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept')]"))
        ).click()
        print("Cookies accepted")
    except:
        print("No cookie banner found")
    club_stats_dict = dict()
    for season in range(2016, 2025, 1):
        # Open dropdown
        filter_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Filter By: ']"))
        )
        driver.execute_script("arguments[0].click();", filter_btn)
        
        time.sleep(1) 
        
        print(f"selecting {season}/{season+1} season")
        print(f"//label[contains(., '{season}/{season + 1}')]")
        # Select current season
        try:
            season_option = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f"//input[@value='{season}']"))
            )
            driver.execute_script("arguments[0].click();", season_option)
        except:
            print(f"{all_prem_clubs_dict['club_name'][club_no]} did not play in prem for {season}/{season+1} season")
            continue
        
        # Save filter
        save_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Save')]"))
        )
        driver.execute_script("arguments[0].click();", save_btn)
        
        # Wait for stats to reload
        print(f"checking div for club: {all_prem_clubs_dict['club_name'][club_no]} and year {season}")
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "div.club-profile__stats"))
        # )
        time.sleep(2)  # Additional buffer
        print(f"Applied {season}/{season + 1} filter for {all_prem_clubs_dict['club_name'][club_no]}")
        # -------------------------------------------------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------------------------------------------------
        # Scraping the data for each season for each club and saving it
        club_info_dict = {
            "name": all_prem_clubs_dict["club_name"][club_no],
            "url": all_prem_clubs_dict["club_url"][club_no],
            "season": f"{season}/{season+1}",  # Track which season the stats belong to
            "stats": []
        }

        club_stats_dict = dict()
        overall_stats = driver.find_elements(By.CSS_SELECTOR, ".club-profile__stats .profile-stat-cards-container .profiles-stat-card")

        for stat in overall_stats:
            label = stat.find_element(By.CSS_SELECTOR, ".profiles-stat-card__label").text
            value = stat.find_element(By.CSS_SELECTOR, ".profiles-stat-card__stat").text

            club_stats_dict[label] = value

        profile_stats_list = driver.find_elements(By.CSS_SELECTOR, ".profile-stat-lists-container .profiles-stats-list")
        label_list = []
        value_list = []
        for stat in profile_stats_list:
            labels = stat.find_elements(By.CSS_SELECTOR, ".profiles-stats-list__stat-label")
            for label in labels:
                label_list.append(label.text)
            values = stat.find_elements(By.CSS_SELECTOR, ".profiles-stats-list__stat-value")
            for value in values:
                value_list.append(value.text)

            for i, label in enumerate(label_list):
                club_stats_dict[label]= value_list[i]

        print("==========================================================================================================================================================================================")
        club_info_dict["stats"].append(club_stats_dict)

        # Define the DIRECTORY path, not the file path
        directory_path = f"C:/Users/daniel/Desktop/Serious Projects/web_scraping/new/datasets/club_stats/"

        # Create the directory if it doesn't exist
        os.makedirs(directory_path, exist_ok=True)

        # Now define the full file path
        club_info_path = f"{directory_path}/{season}_club_stats.csv"

        with open(club_info_path, "a", newline="", encoding="utf-8") as csvfile:
            writer =csv.DictWriter(csvfile, fieldnames=list(club_info_dict.keys()))

            # Write header if file is empty
            if csvfile.tell() == 0:
                writer.writeheader()
            
            writer.writerow(club_info_dict)



    



        # -------------------------------------------------------------------------------------------------------------------------------



# file_path_list = []
# for year in range(2016, 2025, 1):
#     file_path_list.append(f"C:/Users/daniel/Desktop/Serious Projects/web_scraping/new/datasets/league_table/home_and_away/gameweek_{year}/{year}_gameweek_38.csv")
# # End of Storing the path to the league seasons end
# print("Finished saving paths to player information")
# print()
# #====================================================================================================================================


# #====================================================================================================================================
# print("Starting to store table information in pandas dataframe")



# # df_player_info = pd.read_csv("C:/Users/daniel/Desktop/Serious Projects/web_scraping/new/datasets/premier_player_info.csv")

# # player_dict = df_player_info.to_dict(orient='list')