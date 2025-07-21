#===========================================================================================================================================
# Now we scrape each player statistic
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

df_player_info = pd.read_csv("C:/Users/daniel/Desktop/Serious Projects/web_scraping/new/datasets/premier_player_info.csv")

player_dict = df_player_info.to_dict(orient='list')


player_stats_dict = {
        "player_name": [],
        "preferred_foot": [],
        "date_of_birth": [],
        "appearances_sub": [],
        "goals": [],
        "assists": [],
        "xa": [],
        "xg": [],
        "touches_in_opposition_box": [],
        "crosses_completed": [],
        "pass_accuracy": [],
        "long_pass_accuracy": [],
        "minutes_played": [],
        "dribbles_completed": [],
        "duels_won": [],
        "aerial_duels_won": [],
        "total_tackles": [],
        "interceptions": [],
        "blocks": [],
        "red_cards": [],
        "yellow_cards": [],
        "fouls": [],
        "offsides": [],
        "all_stats_on_page": []
    }



for i, player_stat_link in enumerate(player_dict["player_stats_url"]):
    print(f"Processing player {i+1}/{len(player_dict['player_stats_url'])}: {player_dict['player_name'][i]}")
    all_stats_on_page = dict()
    
    # Assign player name
    player_stats_dict["player_name"].append(player_dict["player_name"][i])
    
    # Navigate to player page
    driver.get(player_stat_link)
    
    # Handle cookies
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept')]"))
        ).click()
    except:
        pass

    # RESET FILTER BEFORE APPLYING
    try:
        # Open dropdown
        filter_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Filter By: ']"))
        )
        driver.execute_script("arguments[0].click();", filter_btn)
        
        # RESET: Uncheck all seasons first
        try:
            reset_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Reset')]"))
            )
            driver.execute_script("arguments[0].click();", reset_btn)
            print("Reset filters")
            time.sleep(1)  # Allow reset to complete
        except:
            print("No reset button found")
        
        # Select 2024/25
        season_option = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//label[contains(., '2024/25')]"))
        )
        driver.execute_script("arguments[0].click();", season_option)
        
        # Save filter
        save_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Save')]"))
        )
        driver.execute_script("arguments[0].click();", save_btn)
        
        # Wait for stats to reload
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.profiles-stat-card"))
        )
        time.sleep(2)  # Additional buffer
        print("Applied 2024/25 filter")
        
    except Exception as e:
        print(f"Filter error: {str(e)[:100]}")

    # # Wait for page to load
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, "#main-content")))
    # Scrapping the preferred foot
    try:
        preferred_foot_element = driver.find_element(By.CSS_SELECTOR, "section.player-profile-bio ul:nth-child(1) li.player-profile-bio__item:nth-child(2) p.player-profile-bio__item-value")
        preferred_foot = preferred_foot_element.text
        player_stats_dict["preferred_foot"].append(preferred_foot)
    except Exception as e:
        print(f"issue with adding preferred Foot: {e}")
        player_stats_dict["preferred_foot"].append("n/a")


    # Scrapping the date of birth
    try:
        date_of_birth_element = driver.find_element(By.CSS_SELECTOR, "section.player-profile-bio ul:nth-child(1) li.player-profile-bio__item:nth-child(3) p.player-profile-bio__item-value")
        date_of_birth = date_of_birth_element.text
        player_stats_dict["date_of_birth"].append(date_of_birth)
    except Exception as e:
        print(f"issue with adding date of birth: {e}")
        player_stats_dict["date_of_birth"].append("n/a")

    # Scrapping the appearances
    try:
        appearances_element = driver.find_element(By.CSS_SELECTOR, "section.profile-stat-cards-container div.profiles-stat-card:nth-child(1) p.profiles-stat-card__stat")
        appearances = appearances_element.text
        player_stats_dict["appearances_sub"].append(appearances)
    except Exception as e:
        print(f"issue with adding appearance: {e}")
        player_stats_dict["appearances_sub"].append(0)

    # Scrapping the goals
    try:
        goals_element = driver.find_element(By.CSS_SELECTOR, "section.profile-stat-cards-container div.profiles-stat-card:nth-child(2) p.profiles-stat-card__stat")
        goals = goals_element.text
        player_stats_dict["goals"].append(goals)
    except Exception as e:
        print(f"issue with adding goals: {e}")
        player_stats_dict["goals"].append(0)
        

    # Scrapping the assists
    try:
        assists_element = driver.find_element(By.CSS_SELECTOR, "section.profile-stat-cards-container div.profiles-stat-card:nth-child(3) p.profiles-stat-card__stat")
        assists = assists_element.text
        player_stats_dict["assists"].append(assists)
    except Exception as e:
        print(f"issue with adding assists: {e}")
        player_stats_dict["assists"].append(0)

    # Scrapping the xg
    try:
        xg_element = driver.find_element(By.CSS_SELECTOR, "section.profile-stat-lists-container div.profiles-stats-list:nth-child(1) ul li.profiles-stats-list__stat:nth-child(2) p.profiles-stats-list__stat-value")
        xg = xg_element.text
        player_stats_dict["xg"].append(xg)
    except Exception as e:
        print(f"issue with adding xg: {e}")
        player_stats_dict["xg"].append(0)

    # Scrapping the xa
    try:
        xa_element = driver.find_element(By.CSS_SELECTOR, "section.profile-stat-lists-container div.profiles-stats-list:nth-child(1) ul li.profiles-stats-list__stat:nth-child(3) p.profiles-stats-list__stat-value")
        xa = xa_element.text
        player_stats_dict["xa"].append(xa)
    except Exception as e:
        print(f"issue with adding xa: {e}")
        player_stats_dict["xa"].append(0)

    # Scrapping the touches_in_opposition_box
    try:
        touches_in_opposition_box_element = driver.find_element(By.CSS_SELECTOR, "section.profile-stat-lists-container div.profiles-stats-list:nth-child(1) ul li.profiles-stats-list__stat:nth-child(4) p.profiles-stats-list__stat-value")
        touches_in_opposition_box = touches_in_opposition_box_element.text
        player_stats_dict["touches_in_opposition_box"].append(touches_in_opposition_box)
    except Exception as e:
        print(f"issue with adding touches_in_opposition_box: {e}")
        player_stats_dict["touches_in_opposition_box"].append(0)

    # Scrapping the crosses_completed
    try:
        crosses_completed_element = driver.find_element(By.CSS_SELECTOR, "section.profile-stat-lists-container div.profiles-stats-list:nth-child(1) ul li.profiles-stats-list__stat:nth-child(5) p.profiles-stats-list__stat-value")
        crosses_completed = crosses_completed_element.text
        player_stats_dict["crosses_completed"].append(crosses_completed)
    except Exception as e:
        print(f"issue with adding crosses_completed: {e}")
        player_stats_dict["crosses_completed"].append(0)

    # Scrapping the pass_accuracy
    try:
        pass_accuracy_element = driver.find_element(By.CSS_SELECTOR, "section.profile-stat-lists-container div.profiles-stats-list:nth-child(2) ul li.profiles-stats-list__stat:nth-child(1) p.profiles-stats-list__stat-value")
        pass_accuracy = pass_accuracy_element.text
        player_stats_dict["pass_accuracy"].append(pass_accuracy)
    except Exception as e:
        print(f"issue with adding pass_accuracy: {e}")
        player_stats_dict["pass_accuracy"].append(0)

    # Scrapping the long_pass_accuracy
    try:
        long_pass_accuracy_element = driver.find_element(By.CSS_SELECTOR, "section.profile-stat-lists-container div.profiles-stats-list:nth-child(2) ul li.profiles-stats-list__stat:nth-child(2) p.profiles-stats-list__stat-value")
        long_pass_accuracy = long_pass_accuracy_element.text
        player_stats_dict["long_pass_accuracy"].append(long_pass_accuracy)
    except Exception as e:
        print(f"issue with adding long_pass_accuracy: {e}")
        player_stats_dict["long_pass_accuracy"].append(0)

    # Scrapping the minutes_played
    try:
        minutes_played_element = driver.find_element(By.CSS_SELECTOR, "section.profile-stat-lists-container div.profiles-stats-list:nth-child(3) ul li.profiles-stats-list__stat:nth-child(1) p.profiles-stats-list__stat-value")
        minutes_played = minutes_played_element.text
        player_stats_dict["minutes_played"].append(minutes_played)
    except Exception as e:
        print(f"issue with adding minutes_played: {e}")
        player_stats_dict["minutes_played"].append(0)

    # Scrapping the dribbles_completed
    try:
        dribbles_completed_element = driver.find_element(By.CSS_SELECTOR, "section.profile-stat-lists-container div.profiles-stats-list:nth-child(3) ul li.profiles-stats-list__stat:nth-child(2) p.profiles-stats-list__stat-value")
        dribbles_completed = dribbles_completed_element.text
        player_stats_dict["dribbles_completed"].append(dribbles_completed)
    except Exception as e:
        print(f"issue with adding dribbles_completed: {e}")
        player_stats_dict["dribbles_completed"].append(0)

    # Scrapping the duels_won
    try:
        duels_won_element = driver.find_element(By.CSS_SELECTOR, "section.profile-stat-lists-container div.profiles-stats-list:nth-child(3) ul li.profiles-stats-list__stat:nth-child(3) p.profiles-stats-list__stat-value")
        duels_won = duels_won_element.text
        player_stats_dict["duels_won"].append(duels_won)
    except Exception as e:
        print(f"issue with adding duels_won: {e}")
        player_stats_dict["duels_won"].append(0)

    # Scrapping the aerial_duels_won
    try:
        aerial_duels_won_element = driver.find_element(By.CSS_SELECTOR, "section.profile-stat-lists-container div.profiles-stats-list:nth-child(3) ul li.profiles-stats-list__stat:nth-child(4) p.profiles-stats-list__stat-value")
        aerial_duels_won = aerial_duels_won_element.text
        player_stats_dict["aerial_duels_won"].append(aerial_duels_won)
    except Exception as e:
        print(f"issue with adding aerial_duels_won: {e}")
        player_stats_dict["aerial_duels_won"].append(0)

    # Scrapping the total_tackles
    try:
        total_tackles_element = driver.find_element(By.CSS_SELECTOR, "section.profile-stat-lists-container div.profiles-stats-list:nth-child(4) ul li.profiles-stats-list__stat:nth-child(1) p.profiles-stats-list__stat-value")
        total_tackles = total_tackles_element.text
        player_stats_dict["total_tackles"].append(total_tackles)
    except Exception as e:
        print(f"issue with adding total_tackles: {e}")
        player_stats_dict["total_tackles"].append(0)

    # Scrapping the interceptions
    try:
        interceptions_element = driver.find_element(By.CSS_SELECTOR, "section.profile-stat-lists-container div.profiles-stats-list:nth-child(4) ul li.profiles-stats-list__stat:nth-child(2) p.profiles-stats-list__stat-value")
        interceptions = interceptions_element.text
        player_stats_dict["interceptions"].append(interceptions)
    except Exception as e:
        print(f"issue with adding interceptions: {e}")
        player_stats_dict["interceptions"].append(0)

    # Scrapping the blocks
    try:
        blocks_element = driver.find_element(By.CSS_SELECTOR, "section.profile-stat-lists-container div.profiles-stats-list:nth-child(4) ul li.profiles-stats-list__stat:nth-child(3) p.profiles-stats-list__stat-value")
        blocks = blocks_element.text
        player_stats_dict["blocks"].append(blocks)
    except Exception as e:
        print(f"issue with adding blocks: {e}")
        player_stats_dict["blocks"].append(0)




    # Scrapping the red_cards
    try:
        red_cards_element = driver.find_element(By.CSS_SELECTOR, "section.profile-stat-lists-container div.profiles-stats-list:nth-child(5) ul li.profiles-stats-list__stat:nth-child(1) p.profiles-stats-list__stat-value")
        red_cards = red_cards_element.text
        player_stats_dict["red_cards"].append(red_cards)
    except Exception as e:
        print(f"issue with adding red_cards: {e}")
        player_stats_dict["red_cards"].append(0)

    # Scrapping the yellow_cards
    try:
        yellow_cards_element = driver.find_element(By.CSS_SELECTOR, "section.profile-stat-lists-container div.profiles-stats-list:nth-child(5) ul li.profiles-stats-list__stat:nth-child(2) p.profiles-stats-list__stat-value")
        yellow_cards = yellow_cards_element.text
        player_stats_dict["yellow_cards"].append(yellow_cards)
    except Exception as e:
        print(f"issue with adding yellow_cards: {e}")
        player_stats_dict["yellow_cards"].append(0)

    # Scrapping the fouls
    try:
        fouls_element = driver.find_element(By.CSS_SELECTOR, "section.profile-stat-lists-container div.profiles-stats-list:nth-child(5) ul li.profiles-stats-list__stat:nth-child(3) p.profiles-stats-list__stat-value")
        fouls = fouls_element.text
        player_stats_dict["fouls"].append(fouls)
    except Exception as e:
        print(f"issue with adding fouls: {e}")
        player_stats_dict["fouls"].append(0)

    # Scrapping the offsides
    try:
        offsides_element = driver.find_element(By.CSS_SELECTOR, "section.profile-stat-lists-container div.profiles-stats-list:nth-child(5) ul li.profiles-stats-list__stat:nth-child(4) p.profiles-stats-list__stat-value")
        offsides = offsides_element.text
        player_stats_dict["offsides"].append(offsides)
    except Exception as e:
        print(f"issue with adding offsides: {e}")
        player_stats_dict["offsides"].append(0)

    # Scraping all info just in case

    # Scraping player profile section
    try:
        all_stats_on_page_elements = driver.find_elements(By.CSS_SELECTOR, "section.player-profile-bio ul:nth-child(1) li.player-profile-bio__item")
        for stat in all_stats_on_page_elements:
            stat_header = stat.find_element(By.CSS_SELECTOR, "h3.player-profile-bio__item-label").text
            stat_value = stat.find_element(By.CSS_SELECTOR, ".player-profile-bio__item-value").text
            all_stats_on_page[stat_header] = stat_value


        
    except Exception as e:
        print(f"issue with getting info from player profile sectioin: {e}")
    

    # scraping section cards container 
    try:
        all_stats_on_page_elements = driver.find_elements(By.CSS_SELECTOR, "section.profile-stat-cards-container div.profiles-stat-card")
        for stat in all_stats_on_page_elements:
            stat_header = stat.find_element(By.CSS_SELECTOR, ".profiles-stat-card__label").text
            stat_value = stat.find_element(By.CSS_SELECTOR, ".profiles-stat-card__stat").text
            all_stats_on_page[stat_header] = stat_value

        

        
    except Exception as e:
        
        print(f"issue with getting info from player profile sectioin: {e}")

    # Scraping section cards lists
    try:
        all_stats_on_page_elements = driver.find_elements(By.CSS_SELECTOR, "section.profile-stat-lists-container div.profiles-stats-list")
        for stat in all_stats_on_page_elements:
            stat_items = stat.find_elements(By.CSS_SELECTOR, "ul.profiles-stats-list__stats li.profiles-stats-list__stat")
            for single_stat in stat_items:
                stat_header = single_stat.find_element(By.CSS_SELECTOR, ".profiles-stats-list__stat-label").text
                stat_value = single_stat.find_element(By.CSS_SELECTOR, ".profiles-stats-list__stat-value").text
                all_stats_on_page[stat_header] = stat_value


            
    
        

        
    except Exception as e:
        print(f"issue with getting info from player profile sectioin: {e}")
    player_stats_dict["all_stats_on_page"].append(all_stats_on_page)

    try:
        # Convert to DataFrame and save
        df_prem_player_stats = pd.DataFrame(player_stats_dict)
        df_prem_player_stats.to_csv("C:/Users/daniel/Desktop/Serious Projects/web_scraping/new/datasets/player_stats.csv", index=False)
        print("Data saved to datasets/player_stats_dict.csv")
        print(df_prem_player_stats)
    except:
        print("Error occured when trying to write to file")
    
driver.quit()
     
print(player_stats_dict)

    

# try:
#     # Convert to DataFrame and save
#     df_prem_player_stats = pd.DataFrame(player_stats_dict)
#     df_prem_player_stats.to_csv("C:/Users/daniel/Desktop/Serious Projects/web_scraping/new/datasets/player_stats.csv", index=False)
#     print("Data saved to datasets/player_stats_dict.csv")
#     print(df_prem_player_stats)
# except:
#     print("Error occured when trying to write to file")