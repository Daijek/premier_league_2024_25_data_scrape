# ⚽ Premier League Data Scraper

A comprehensive web scraping solution that collects rich Premier League statistics from the official website using Selenium and ChromeDriver. This project gathers club performance data, player profiles, and detailed match statistics from the 2016/2017 to 2024/2025 seasons.

![Premier League](https://upload.wikimedia.org/wikipedia/en/f/f2/Premier_League_Logo.svg)

## 🧰 Project Components

### 📊 Data Collection Scripts

| Script                    | Description                                                                             | Output Example            |
| ------------------------- | --------------------------------------------------------------------------------------- | ------------------------- |
| `club_scraper.py`         | Scrapes league tables for all game weeks (1-38) from 2016/2017 to 2024/2025 seasons     | `2024_gameweek_38.csv`    |
| `club_stats_scraper.py`   | Collects detailed club statistics per season (games played, goals, xG, shots, etc.)     | `2024_club_stats.csv`     |
| `player_info_scraper.py`  | Gathers player profiles (name, nationality, club, position, image) for 2024/2025 season | `premier_player_info.csv` |
| `player_stats_scraper.py` | Extends player profiles with detailed performance statistics                            | `player_stats.csv`        |

### 📂 Data Structure

datasets/
├── club_stats/
│ ├── 2016_club_stats.csv
│ ├── 2017_club_stats.csv
│ └── ...
├── league_table/
│ ├── away/
│ ├── home/
│ └── home_and_away/
├── player_stats.csv
└── premier_player_info.csv

## ⚙️ Technical Implementation

### 🧩 Key Technologies

- **Selenium**: For handling dynamic JavaScript content
- **ChromeDriver**: Headless browser automation
- **Pandas**: Data processing and CSV export
- **Explicit Waits**: Robust element detection
- **Anti-Scraping Evasion**:
  ```python
  chrome_options.add_argument("--disable-blink-features=AutomationControlled")
  chrome_options.add_argument("user-agent=Mozilla/5.0...")
  ```

### 🚀 Key Features

1. **Multi-Season Support**: 2016/2017 to 2024/2025 seasons

1. **Pagination Handling**: Automatic detection and navigation

1. **Dynamic Content Processing**: Waits for AJAX-loaded elements

1. **Error Resilience**: Comprehensive exception handling

1. **Data Validation**: Automatic fallback values for missing data

### 🛠️ Setup Instructions

Prerequisites

- **Python 3.8+**
- **Chrome browser**
- **ChromeDriver**
- **bash**

```
# Install dependencies
pip install selenium pandas webdriver-manager

# Run club scraper
python club_scraper.py

# Run player info scraper
python player_info_scraper.py
```

## 🧩 Data Points Collected

### Club Statistics

** Example **
| position | name | games_played | wins | draws | losses | goals_for | goals_against | points |
|----------|-----------------|--------------|------|-------|--------|-----------|---------------|--------|
| 1 | Arsenal | 38 | 28 | 5 | 5 | 91 | 29 | 89 |
| 2 | Manchester City | 38 | 27 | 7 | 4 | 93 | 33 | 88 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |
...

### Player Profiles

** Example **
| player_image_url | player_name | player_country | player_club | player_position | player_stats_url |
|-------------------------------------------------------|--------------|----------------|-------------|------------------|-------------------------------------------------------|
| ![Bukayo Saka](https://.../p165153.png) | Bukayo Saka | England | Arsenal | Midfielder | [Stats](https://www.premierleague.com/players/165153/Bukayo-Saka/stats) |
| ... | ... | ... | ... | ... | ... |

### Player Statistics

| player_name | appearances | goals | assists |  xG |  xA | pass_accuracy | tackles | interceptions |
| ----------- | ----------: | ----: | ------: | --: | --: | ------------: | ------: | ------------: |
| Declan Rice |          37 |     7 |       8 | 4.2 | 5.7 |           91% |      42 |            28 |
| ...         |         ... |   ... |     ... | ... | ... |           ... |     ... |           ... |

## 🚧 Challenges Overcome

1. **Dynamic Content: Implemented explicit waits for AJAX-loaded elements**

```
WebDriverWait(driver, 15).until(
EC.presence_of_element_located((By.CSS_SELECTOR, "tr.player-listings-row"))
)

```

1. **Pagination: Autohmatic "Next" button detection and handling**

1. **Season Filtering: Dynamic dropdown interaction**

```
season_option = WebDriverWait(driver, 5).until(
EC.element_to_be_clickable((By.XPATH, "//label[contains(., '2024/25')]"))
)
driver.execute_script("arguments[0].click();", season_option)
```

1. **Anti-Scraping Measures: Custom Chrome configuration and headers**

1. **Data Consistency: Automatic path creation and validation**

```
os.makedirs(directory_path, exist_ok=True)
```

## 📈 Future works

- **Add historical player statistics (2016-2023)**

- **Implement cloud storage integration (AWS S3)**

- **Create automated data validation checks**

- **Build dashboard visualization (Streamlit/Power BI)**

- **Add fixture and results scraping module**

## ⚠️ Ethical Note

**This project complies with Premier League website's robots.txt and**:

- Uses 3-second delays between requests
- Limits scraping to off-peak hours
- Stores data only for educational purposes
- Credits all data to Premier League Official Website
