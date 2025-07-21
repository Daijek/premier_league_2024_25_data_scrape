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

player_dict = {
    "player_image_url": [],
    "player_name": [],
    "player_country": [],
    "player_club": [],
    "player_position": [],
    "player_stats_url": []
}

try:
    driver.get("https://www.premierleague.com/en/players?competition=8&season=2024")
    print("Page loaded")
    
    # Accept cookies
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept')]"))
        ).click()
        print("Cookies accepted")
    except:
        print("No cookie banner found")
    
    page_count = 1
    
    while True:
        # Wait for player information to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tr.player-listings-row"))
        )
        
        # Extract information
        player_rows = driver.find_elements(By.CSS_SELECTOR, "tr.player-listings-row")

        for row in player_rows:
            try:
                # Exctract player stats link
                try:
                    player_stats_element = row.find_element(By.CSS_SELECTOR, "td a.player-listings-row__player")
                    player_stats_url = player_stats_element.get_attribute('href')

                    # Making the URL absolute
                    if player_stats_url.startswith("/"):
                        base_url = "https://www.premierleague.com"
                        player_stats_url = base_url + player_stats_url

                    # Change 'overview' to 'stats' in the URL
                    if player_stats_url.endswith("/overview"):
                        player_stats_url = player_stats_url.replace("/overview", "/stats")
                    elif "/overview" in player_stats_url:
                        player_stats_url = player_stats_url.replace("/overview", "/stats")
                    else:
                        # Handle cases where URL doesn't have overview
                        player_stats_url = player_stats_url.replace("/profile", "/stats")

                    player_dict["player_stats_url"].append(player_stats_url)
                except:
                    player_dict["player_stats_url"].append("n/a")
                    
    
                # Extract image URL
                try:
                    player_image_element = row.find_element(By.CSS_SELECTOR, ".player-headshot img")
                    player_image_url = player_image_element.get_attribute('src') or player_image_element.get_attribute('data-src')
                    player_dict["player_image_url"].append(player_image_url)
                except:
                    player_dict["player_image_url"].append("n/a")

                # Extract player name
                try:
                    player_name_element = row.find_element(By.CSS_SELECTOR, "p.player-listings-row__player-name")
                    player_name = player_name_element.text
                    player_dict["player_name"].append(player_name)
                except:
                    player_dict["player_name"].append('n/a')

                # Extract player country
                try:
                    player_country_element = row.find_element(By.CSS_SELECTOR, "td .player-listings-row__country")
                    player_country = player_country_element.text
                    player_dict["player_country"].append(player_country)
                except:
                    player_dict["player_country"].append("n/a")


                # Extract player club
                try:
                    player_club_element = row.find_element(By.CSS_SELECTOR, "td .player-listings-row__club")
                    player_club = player_club_element.text
                    player_dict["player_club"].append(player_club)
                except:
                    player_dict["player_club"].append("n/a")

                # Extract player position
                try:
                    player_position_element = row.find_element(By.CSS_SELECTOR, ".player-listings-row__data.player-listings-row__data--position")
                    player_position = player_position_element.text
                    player_dict["player_position"].append(player_position)
                except:
                    player_dict["player_position"].append("n/a")
            except:
                print('issue extracting player information')
        

        print(f"Page {page_count}: Collected {len(player_dict['player_name'])} players")
        
        # Find the correct next button with aria-label="Next"
        next_buttons = driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Next']")
        
        
        # If still no button found, exit
        if not next_buttons:
            print("No next button found - exiting")
            break
            
        next_button = next_buttons[0]

        # Check if button is disabled
        is_disabled = (
            next_button.get_attribute("disabled") is not None or 
            next_button.get_attribute("aria-disabled") == "true"
        )

        if is_disabled:
            print("Reached last page")
            break
        
            
        # Scroll to and click next button
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_button)
        time.sleep(0.5)  # Smooth scrolling animation
        
        # Click using JavaScript to avoid interception
        driver.execute_script("arguments[0].click();", next_button)
        print("Clicked next button")
        
        # Wait for page to update
        WebDriverWait(driver, 10).until(
            EC.staleness_of(player_rows[0])
        )
        
        page_count += 1
        time.sleep(1)  # Additional stability wait

    print(f"\nTOTAL PLAYERS COLLECTED: {len(player_dict['player_name'])}")
    print("=" * 50)

except Exception as e:
    print(f"Error occurred: {str(e)}")
    
finally:
    driver.quit()
    print("Browser closed")

    try:
        # Convert to DataFrame and save
        df_prem_player_info = pd.DataFrame(player_dict)
        df_prem_player_info.to_csv('datasets/premier_player_info.csv', index=False)
        print("Data saved to datasets/premier_league_players.csv")
        print(df_prem_player_info)
    except:
        print("Error occured when trying to write to file")




