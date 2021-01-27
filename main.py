import requests as r
import playsound as ps
import time as t
api_key = "Put your API Key Here" 
music = "put the name of your music.mp3"
steam_id = "Put your SteamID64 Here"

# Getting the game list

recently_played_link = f"http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={api_key}&steamid={steam_id}&format=json"
rp_request = r.get(recently_played_link).json()
total_games = rp_request["response"]["total_count"]  # Working only with recently played games
game_ids = [ rp_request["response"]["games"][i]["appid"] for i in range(total_games)]


# Let's obtain the already achieveds games

already_achieved = []
counter_first = 0

for i in range(len(game_ids)):

    game_achievements_start = r.get(f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={game_ids[i]}&key={api_key}&steamid={steam_id}").json()
    
    if game_achievements_start["playerstats"]["success"]:
        
        for i in range(len(game_achievements_start["playerstats"]["achievements"])):
            if game_achievements_start["playerstats"]["achievements"][i]["achieved"]:
                counter_first += 1
        
        
        already_achieved.append(counter_first)
        counter_first = 0


    else:
        already_achieved.append(0)

counter_now = 0    
print("Ok, waiting for achievements")

# Now, we're updating your achievement list to wait for a new achievement

while True:
    achieved_now = []
    for q in range(len(game_ids)):
        q_req = r.get(f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={game_ids[q]}&key={api_key}&steamid={steam_id}").json()

        if q_req["playerstats"]["success"]:
            
            for j in range(len(q_req["playerstats"]["achievements"])):
                if q_req["playerstats"]["achievements"][j]["achieved"]:
                    counter_now += 1
            
            
            achieved_now.append(counter_now)
            counter_now = 0


        else:
            achieved_now.append(0)

    
    
    if len(achieved_now) != total_games:
        print("The apllications is'n not running correctly, please restart.")

    elif achieved_now != already_achieved:
        ps.playsound(music)
        already_achieved = achieved_now
    
    t.sleep(2)
    


