from ScrapData import ScrapData
from Graph import genGraph
from Template import Template
from EmailSender import send_mail
import time, datetime, json

with open("../infos.json", "r") as f:
    info = json.loads(f.read())
    email = info["EMAIL"]
    password = info["APP_PASSWORD_GMAIL"]

def script():
    s = ScrapData()
    data, path = s.build()
    
    genGraph(data, path)
    
    template = Template(path)
    html_text, pdf_path = template.build()
    print(html_text)

    send_mail(
        email,
        [email],
        "Récap Hebdomadaire 70.3",
        html_text,
        [pdf_path],
        username=email,
        password=password
    )

if __name__ == "__main__":
    # flag = True
    # while True:
    #     if datetime.today().strftime('%A') == "Sunday" and flag:
    script()
        #     flag = False

        # else:
        #     flag = True
        #     time.sleep(3600)




    