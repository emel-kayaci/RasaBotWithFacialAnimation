import pickle
import numpy as np
import pandas as pd 

veri_komb = pd.read_csv('veri_komb.csv', encoding='iso-8859-9', sep=",")

kayıtlı_semptomlar = veri_komb.columns.values[:-1]
       
hastalıklar = veri_komb.hastalik.unique()

semptom_numarası = {}
for index, value in enumerate(kayıtlı_semptomlar):
    semptom_numarası[value] = index

data_dict = {
    "semptom_numarası":semptom_numarası,
    "tahmin_sınıfları":hastalıklar
}

# Girdi: Virgüller ile ayrılmış semptomlar
# Çıktı: Tahmin edilen hastalığın ismi
def hastalık_tahmin_et(kayıtlı_semptomlar):

    filename = 'model.sav'
 
    # Eğitilmiş modelin yüklenmesi
    gs_NB = pickle.load(open(filename, 'rb'))

    kayıtlı_semptomlar = kayıtlı_semptomlar.split(",")
    print(kayıtlı_semptomlar)
    # Modele uygun girdi verisinin hazırlanması 
    input_data = [0] * len(data_dict["semptom_numarası"])
    for semptom in kayıtlı_semptomlar:
        index = data_dict["semptom_numarası"][semptom]
        input_data[index] = 1
        
    input_data = np.array(input_data).reshape(1,-1)
    
    tahmin = data_dict["tahmin_sınıfları"][gs_NB.predict(input_data)[0]]

    return f"{tahmin}"

