import matplotlib.pyplot as plt

def genGraph(data, folder_path):
    pourcentage_type_discipline = data["pourcentage_type_discipline"]
    label_type = list(pourcentage_type_discipline.keys())
    data_type = [pourcentage_type_discipline[key] for key in (pourcentage_type_discipline.keys())]

    info_pourcentage_repetition_temps_data = data["info_pourcentage_repetition_temps_data"]
    data_reel = [info_pourcentage_repetition_temps_data[key]["pourcentage"] for key in list(info_pourcentage_repetition_temps_data.keys()) if key != "TOTAL"]
    label_reel = [key for key in list(info_pourcentage_repetition_temps_data.keys()) if key != "TOTAL"]

    fig, ax = plt.subplots(1, 2, figsize=(15, 7))

    explode_1 = [0.05 for i in range(len(data_reel))]
    explode_2 = [0.05 for i in range(len(data_type))]
    colors = ["#219ebc", "#fdf0d5", "#2ec4b6", "#e07a5f"]
    wedge_properties = {"edgecolor":"k",'linewidth': 2}

    ax[0].pie(data_reel, labels=label_reel, explode=explode_1, colors=colors, startangle=30, counterclock=False, shadow=True, wedgeprops=wedge_properties,autopct="%1.1f%%", pctdistance=0.7)
    ax[0].set_title("Part de chaque disciplines dans la semaine")

    ax[1].pie(data_type, labels=label_type, explode=explode_2, colors=colors, startangle=30, counterclock=False, shadow=True, wedgeprops=wedge_properties,autopct="%1.1f%%", pctdistance=0.7)
    ax[1].set_title("Part de chaque disciplines dans le 70.3")

    fig.savefig(folder_path + "/graphes/graphe_pourcentage.png")

    