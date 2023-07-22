import json
import jinja2
import pdfkit


class Template:

    def __init__(self, log_path ,template_path="./templates") -> None:
        self.log_path = log_path
        self.data_file_name = self.log_path + "/" + self.log_path.split("/")[-1] + ".json"
        
        with open(self.data_file_name, "r", encoding="utf8") as f:
            self.data = json.loads(f.read())

        # Format volume cible
        vol = str(self.data["volume_cible"])
        vol_heure = vol.split(".")
        
        vol_cible = str(vol_heure[0])

        try:
            vol_min = vol_heure[1]
            vol_cible += ":30:00"
        except:
            vol_cible += ":00:00"

        self.template_path = template_path
        self.context = {
            "periode" : self.data["periode"],
            "volume_cible" : vol_cible,
            "volume_reel" : self.data["info_pourcentage_repetition_temps_data"]["TOTAL"]["temps_total"],
            "path_graph_pourcentage_discipline" : "C:/Users/natha/Documents/notionApi/logs/" + self.log_path.split("/")[-1] + "\graphes\graphe_pourcentage.png",
            
            "temps_passe_natation" : self.data["info_pourcentage_repetition_temps_data"]["NATATION"]["temps_total"],
            "nombre_seances_natation" : self.data["info_pourcentage_repetition_temps_data"]["NATATION"]["nombre_seance"],

            "temps_passe_velo" : self.data["info_pourcentage_repetition_temps_data"]["VELO"]["temps_total"],
            "nombre_seances_velo" : self.data["info_pourcentage_repetition_temps_data"]["VELO"]["nombre_seance"],

            "temps_passe_cap" : self.data["info_pourcentage_repetition_temps_data"]["COURSE A PIED"]["temps_total"],
            "nombre_seances_cap" : self.data["info_pourcentage_repetition_temps_data"]["COURSE A PIED"]["nombre_seance"],

            "temps_passe_total" : self.data["info_pourcentage_repetition_temps_data"]["TOTAL"]["temps_total"],
            "nombre_seances_total" : self.data["info_pourcentage_repetition_temps_data"]["TOTAL"]["nombre_seance"],
            }

    def build(self):
        template_loader = jinja2.FileSystemLoader("./")
        template_env = jinja2.Environment(loader=template_loader)

        template = template_env.get_template(self.template_path + "/template_report.html")
        output_text = template.render(self.context)

        config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
        pdfkit.from_string(output_text, self.log_path + "/" + self.log_path.split("/")[-1] + ".pdf", configuration=config, css=self.template_path + "/template_report.css", options={"enable-local-file-access": ""})

        return output_text, self.log_path + "/" + self.log_path.split("/")[-1] + ".pdf"

