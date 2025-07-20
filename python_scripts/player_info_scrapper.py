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



#===========================================================================================================================================
# Now we scrape each player statistic
#===========================================================================================================================================

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
        "offsides": []
    }

    

for stats_page in player_dict["player_stats_url"]:

    driver.get(stats_page)

    # Accept cookies
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept')]"))
        ).click()
        print("Cookies accepted")
    except:
        print("No cookie banner found")
    # Find the correct next button with aria-label="Next"
    try:
        year_filter_dropdown = driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Filter By: ']")
        year_filter_save_button = driver.find_elements(By.CSS_SELECTOR, "button.button__icon-right button--medium.button--filled ")

        # Click drop down
        driver.execute_script("arguments[0].click();", year_filter_dropdown)
        print("Clicked year filter down")

        # selecting the 24/25 season
        season_option = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//label[contains(., '2024/25')]")))

        
        driver.execute_script("arguments[0].click();", season_option)
        print("selected 2024/25 season")
    

        # Save before we scrape
        driver.execute_script("arguments[0].click();", year_filter_save_button)
        print("Clicked save year filter button")

    except:
        print("issue selecting the data filter")



for i, player_stat_link in enumerate(player_dict["player_stats_url"]):
    # Assign player name for tracking
    player_stats_dict["player_name"].append(player_dict["player_name"][i])

    driver.get(player_stat_link)
    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept')]"))
        ).click()
        print("Cookies accepted")
    except:
        print("No cookie banner found")


    # # Wait for page to load
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, "div.statsContainer"))
    # )
    try:
        year_filter_dropdown = driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Filter By: ']")
        year_filter_dropdown = year_filter_dropdown[0]

        # Click drop down
        print("year_filter_dropdown")
        driver.execute_script("arguments[0].click();", year_filter_dropdown)
        
        print("Clicked year filter down")

        # selecting the 24/25 season
        season_option = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//label[contains(., '2024/25')]")))

        
        driver.execute_script("arguments[0].click();", season_option)
        print("selected 2024/25 season")


        # Save before we scrape
        year_filter_save_button = driver.find_elements(By.CSS_SELECTOR, "div.filters__button-container button.button")
        year_filter_save_button = year_filter_save_button[0]
        driver.execute_script("arguments[0].click();", year_filter_save_button)
        print("Clicked save year filter button")
    except Exception as e:
            print(f"issue: {e}")

    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#main-content")))
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
     
print(player_stats_dict)

    
driver.quit()
try:
    # Convert to DataFrame and save
    df_prem_player_stats = pd.DataFrame(player_stats_dict)
    df_prem_player_stats.to_csv('datasets/player_stats_dict.csv', index=False)
    print("Data saved to datasets/player_stats_dict.csv")
    print(df_prem_player_stats)
except:
    print("Error occured when trying to write to file")
