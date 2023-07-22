import json, requests, datetime, os
from pprint import pprint
from slugify import slugify

class ScrapData:

    def __init__(self, path_info="../infos.json") -> None:
        
        with open(path_info, "r") as f:
            infos = json.loads(f.read())
            self.DB_ID = infos["DB_ID"]
            self.TOKEN = infos["TOKEN"]

        self.temp_file_path = "./temp.json"
        self.props_data = []
        self.week_training_props = []
        self.info_pourcentage_repetition_temps_data = {}
        self.pourcentage_type_discipline = {"NATATION" : 11.71, "VELO" : 55.76, "COURSE A PIED" : 32.53}
        self.volume_periode = {
            "Reprise - S1" : 5, 
            "Reprise - S2" : 5, 
            "Fondamentale 1 - S1" : 7, 
            "Fondamentale 1 - S2" : 9.5, 
            "Fondamentale 1 - S3" : 11,
            "Fondamentale 1 - S4" : 7,
            "Fondamentale 2 - S1" : 8,
            "Fondamentale 2 - S2" : 10.5, 
            "Fondamentale 2 - S3" : 12,
            "Fondamentale 2 - S4" : 8.5,
            "Fondamentale 3 - S1" : 11,
            "Fondamentale 3 - S2" : 12.5,
            "Fondamentale 3 - S3" : 7,
            "Fondamentale 3 - S4" : 9,
            "Fondamentale 4 - S1" : 11.5,
            "Fondamentale 4 - S2" : 13,
            "Fondamentale 4 - S3" : 7,
            "Fondamentale 4 - S4" : 10.5,
            "Spécifque 1 - S1" : 11,
            "Spécifque 1 - S2" : 11,
            "Spécifque 1 - S3" : 7,
            "Spécifque 1 - S4" : 10.5,
            "Spécifque 2 - S1" : 10.5,
            "Spécifque 2 - S2" : 10.5,
            "Spécifque 2 - S3" : 7,
            "Spécifque 2 - S4" : 9,
            "Pré Compétition - S1" : 8,
            "Pré Compétition - S2" : 8,
            "Pré Compétition - S3" : 5,
            "Compétition" : 2}

        self.periode = ""
        self.volume_cible = 0

    def queryDB(self):
        readUrl = f"https://api.notion.com/v1/databases/{self.DB_ID}/query"
        headers = {
            "Authorization": "Bearer " + self.TOKEN,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

        res = requests.request("POST", readUrl, headers=headers)
        info = res.json()

        with open(self.temp_file_path, "w", encoding="utf8") as f:
            f.write(json.dumps(info))

        return info

    def readPropsFromFile(self):
        with open(self.temp_file_path, "r+", encoding="utf8") as f:
            data = json.loads(f.read())["results"]

            self.props_data = [d["properties"] for d in data]

        return self.props_data

    def convert_duree_to_seconde(self, str_duree):
        hh, mm, ss = str_duree.split(":")
        return int(hh) * 3600 + int(mm) * 60 + int(ss)

    def getWeekTrainingProps(self):
        now = datetime.datetime.now()
        days_week_date = [now - datetime.timedelta(days=i) for i in range(7)]
        days_week_str = [day.strftime("%Y-%m-%d") for day in days_week_date]

        date_data = []
        for id, data in enumerate(self.props_data):
            date_data.append((id, data["Date"]["date"]["start"]))

        week_training_id = []
        for date in date_data:
            if date[1] in days_week_str:
                week_training_id.append(date)

        for id, props in enumerate(self.props_data):
            for train in week_training_id:
                if(train[0] == id):
                    self.week_training_props.append(props)

        return self.week_training_props

    def get_Nb_Time_TrainingData(self):
        data = []
        for train in self.week_training_props:
            entrainement_label = "ENTRAINEMENT"
            
            categorie_infos = train["Catégorie"]["multi_select"]
            labels = [info["name"] for info in categorie_infos]

            if entrainement_label in labels:
                row = {"nom" : train["Nom"]["title"][0]["plain_text"]}

                try:
                    row["rpe"] = train["RPE | ENTRAINEMENT"]["select"]["name"]
                except:
                    pass
                
                try:
                    row["duree"] = train["Durée | ENTRAINEMENT"]["rich_text"][0]["plain_text"]
                except:
                    pass
                
                try:
                    discipline_label = []
                    for info in train["Discipline | ENTRAINEMENT"]["multi_select"]:
                        discipline_label.append(info["name"])
                    
                    row["discipline"] = discipline_label
                except:
                    pass

                data.append(row)

        info_temps = {
            "NATATION" : {
                "seconde" : 0,
                "pourcentage" : 0,
                "temps_total" : "",
                "nombre_seance" : 0
            },
            "VELO" : {
                "seconde" : 0,
                "pourcentage" : 0,
                "temps_total" : "",
                "nombre_seance" : 0
            },
            "COURSE A PIED" : {
                "seconde" : 0,
                "pourcentage" : 0,
                "temps_total" : "",
                "nombre_seance" : 0
            },
            "MUSCULATION" : {
                "seconde" : 0,
                "pourcentage" : 0,
                "temps_total" : "",
                "nombre_seance" : 0
            },
            "TOTAL" : {
                "seconde" : 0,
                "pourcentage" : 100,
                "temps_total" : "",
                "nombre_seance" : len(data)
            },
        }

        seconde_discipline_keys = list(info_temps.keys())

        for d in data:
            duree = self.convert_duree_to_seconde(d["duree"])
            info_temps["TOTAL"]["seconde"] += duree

            for discipline in d["discipline"]:
                if discipline in info_temps:
                    info_temps[discipline]["seconde"] += duree
                    info_temps[discipline]["nombre_seance"] += 1

        for key in seconde_discipline_keys:
            info_temps[key]["pourcentage"] = round((info_temps[key]["seconde"] * 100) / info_temps["TOTAL"]["seconde"], 2) 
            info_temps[key]["temps_total"] = str(datetime.timedelta(seconds=info_temps[key]["seconde"]))

        self.info_pourcentage_repetition_temps_data = info_temps

        return self.info_pourcentage_repetition_temps_data
    
    def scrap_periode(self):
        for props in self.props_data:
            periodes_select = props["Catégorie"]["multi_select"]
            for select in periodes_select:
                if select["name"] == "PERIODE":
                    end_date = props["Date"]["date"]["end"]
                    now = datetime.datetime.now().strftime("%Y-%m-%d")

                    if(end_date == now):
                        self.periode = props["Nom"]["title"][0]["plain_text"]

                        for key in list(self.volume_periode.keys()):
                            if key in self.periode:
                                self.volume_cible = self.volume_periode[key]
                                break
                        
                        return self.periode

    def merge_data(self):
        data = {
            "info_pourcentage_repetition_temps_data" : self.info_pourcentage_repetition_temps_data,
            "periode" : self.periode,
            "volume_cible" : self.volume_cible,
            "pourcentage_type_discipline" : self.pourcentage_type_discipline
        }

        self.data = data
        return self.data

    def createLog(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d")
        path = f"../logs/{slugify(self.periode)}_{now}"

        try:
            os.mkdir(path)
            os.mkdir(path + "/graphes")
        except:
            pass

        with open(path + f"/{slugify(self.periode)}_{now}.json", "w", encoding="utf8") as f:
            f.write(json.dumps(self.data))

        return path


    def build(self, flag_queryDB=False):
            if(flag_queryDB):
                self.queryDB()
            
            self.readPropsFromFile()
            self.getWeekTrainingProps()
            self.get_Nb_Time_TrainingData()
            self.scrap_periode()
            self.merge_data()
            path = self.createLog()

            return self.data, path    
