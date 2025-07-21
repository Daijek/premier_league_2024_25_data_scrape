import pandas as pd

df = pd.read_csv("C:/Users/daniel/Desktop/Serious Projects/web_scraping/new/datasets/premier_player_info.csv")
df = df.iloc[387:].reset_index(drop=True)

print(df)
# player_dict = df.to_dict(orient='list')
# print(player_dict["all_stats_on_page"])