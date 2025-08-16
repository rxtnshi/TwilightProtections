import json
import os

def add_ban(userid, reason, guildid):
    json_path = os.path.join(os.path.dirname(__file__), "..", "data", "ban_configs.json")
    if not os.path.exists(json_path):
        bans = []
    else:
        with open(json_path, "r") as f:
            try:
                bans = json.load(f)
            except json.JSONDecodeError:
                bans = []
                
    ban_entry = {
        "user_id": str(userid),
        "reason": reason,
        "guild_id": str(guildid)
    }
    bans.append(ban_entry)
    with open(json_path, "w") as f:
        json.dump(bans, f, indent=2)

def remove_ban(userid):
    json_path = os.path.join(os.path.dirname(__file__), "..", "data", "ban_configs.json")
