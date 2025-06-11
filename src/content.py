import requests

class Content():
    def __init__(self, Requests, log):
        self.Requests = Requests
        self.log = log
        self.content = {}

    def get_content(self):
        self.content = self.Requests.fetch("custom", f"https://shared.{self.Requests.region}.a.pvp.net/content-service/v3/content", "get")
        return self.content

    def get_latest_season_id(self, content):
        for season in content["Seasons"]:
            if season["IsActive"]:
                self.log(f"retrieved season id: {season['ID']}")
                return season["ID"]

    def get_all_agents(self):
        rAgents = requests.get("https://valorant-api.com/v1/agents?isPlayableCharacter=true").json()
        agent_dict = {}
        agent_dict.update({None: None})
        agent_dict.update({"": ""})
        for agent in rAgents["data"]:
            agent_dict.update({agent['uuid'].lower(): agent['displayName']})
        self.log(f"retrieved agent dict: {agent_dict}")
        return agent_dict

    def get_maps(self):
        rMaps = requests.get("https://valorant-api.com/v1/maps").json()
        map_dict = {}
        map_dict.update({None: None})
        for Vmap in rMaps["data"]:
            map_dict.update({Vmap['mapUrl'].lower(): Vmap['displayName']})
        self.log(f"retrieved map dict: {map_dict}")
        return map_dict
    
    def roman_to_int(self, roman):
        roman_dict = {
            'I':1, 'II':2, 'III':3
        }
        return roman_dict.get(roman.upper(),0)
    
    def get_act_episode_from_act_id(self, act_id):
        final = {
            "act": None,
            "episode": None
        }
        act_found = False
        for season in self.content["Seasons"]:
            if season["ID"].lower() == act_id.lower():
                #print(f"[DEBUG] Nombre del season: {season['Name']}")
                
                name_upper = season["Name"].upper()
                
                if "ACT" in name_upper:
                    act_part = name_upper.split("ACT")[-1].strip()
                    final["act"] = self.roman_to_int(act_part)
                
                act_found = True

            if act_found and season["Type"] == "episode":
                #print(f"[DEBUG] Episodio candidato encontrado: {season['Name']}")  # NUEVO
                name_upper = season["Name"].upper()
                
                if "EPISODE" in name_upper:
                    episode_part = name_upper.split("EPISODE")[-1].strip().split(" ")[0]
                    try: 
                        final["episode"] = int(episode_part)
                    except ValueError:
                        final["episode"] = 0
                break

        #print(f"[DEBUG] Resultado final para ID {act_id}: Act: {final['act']}, Episode: {final['episode']}")
        return final




