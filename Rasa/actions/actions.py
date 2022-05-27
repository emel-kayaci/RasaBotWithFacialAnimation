# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.types import DomainDict
from db_sqlite import insert_data, get_data
from hastalik_tespit import kayıtlı_semptomlar, hastalık_tahmin_et
import re
from wikipedia.wikipedia import page
import wikipedia
import csv

class ValidateRandevuForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_randevu_form"

    def validate_number(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        if (not slot_value.replace(" ", "").isdigit()) or (len(slot_value.replace(" ", "")) != 10):
            dispatcher.utter_message("Numaranızı uygun bir formatta girmediniz. Lütfen yalnızca numaranızın 10 hanesini giriniz.")
            return {"number": None}
        else:
            return {"number": slot_value}

class GetNumber(Action):
    def name(self) -> Text:
        return "numara_sorgula"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot("number") == None:
            return [SlotSet("number", tracker.latest_message['text'])]
                
class Onay(Action):
    def name(self) -> Text:
        return "form_onay"

    def run(self, dispatcher: "CollectingDispather", tracker: "Tracker", domain: Dict[Text, Any]) -> List[Dict]:
        dispatcher.utter_message("""Girdiğiniz bilgiler bunlardır. Bilgilerin doğruluğunu onaylar mısınız?
        \nİsim: {0}, 
        \nTelefon: {1},
        \nRandevu tarihi ve zamanı: {2},
        \nRandevu notları: {3}""".format(tracker.get_slot("isim"),
        tracker.get_slot("number"),
        tracker.get_slot("date"),
        tracker.get_slot("randevu_not")))
        return []

class FormuKaydet(Action):
    def name(self) -> Text:
        return "formu_kaydet"
  
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        mesaj=insert_data(tracker.get_slot("isim"),
        tracker.get_slot("number"),
        tracker.get_slot("date"),
        tracker.get_slot("randevu_not"))
        dispatcher.utter_message(text=mesaj)

class RandevuBilgisiniGetir(Action):
    def name(self) -> Text:
        return "randevu_bilgisi_getir"
  
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        bilgi = get_data(tracker.get_slot("number"))
        dispatcher.utter_message(bilgi)
        return [SlotSet('number', None)]

class FormuSıfırla(Action):

    def name(self) -> Text:
        return "formu_sıfırla"

    async def run(self, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: "DomainDict") -> List[EventType]:
            return [SlotSet('isim', None), SlotSet('number', None), SlotSet('date', None), SlotSet('randevu_not', None)]

class TanıKoy(Action):

    def name(self) -> Text:
        return "tanı_koy"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot("semptom") == None:
            dispatcher.utter_message("Bana semptomlarınızı söyleyebilir misiniz?")
        else:
            gecerli_semptomlar = ""
            for semptom in tracker.get_slot("semptom"):
                if semptom in kayıtlı_semptomlar:
                    if gecerli_semptomlar == "":
                        gecerli_semptomlar += semptom
                    else:
                        gecerli_semptomlar = gecerli_semptomlar + "," + semptom
            tahmin_edilen_hastalik = hastalık_tahmin_et(gecerli_semptomlar)
            dispatcher.utter_message("Teşekkürler, demek ki yaşadığınız semptomlar şunlar: " + gecerli_semptomlar + " ")
            dispatcher.utter_message("Hastalığınızın " + str(tahmin_edilen_hastalik).replace('_', ' ') + " olduğunu düşünmekteyim.")
            dispatcher.utter_message(wikipediaAra(tahmin_edilen_hastalik))
        return [SlotSet("semptom", None)]

class HastalikAcikla(Action):

    def name(self) -> Text:
        return "hastalik_acikla"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot("hastalik") == None:
            dispatcher.utter_message("Merak ettiğiniz hastalığı söyleyebilir misiniz?")
        else:
            dispatcher.utter_message(wikipediaAra(tracker.get_slot("hastalik")))

def wikipediaAra(hastalik_ismi):
    wikipedia.set_lang("tr")
    try:
        # finding result for the search
        # sentences = 2 refers to numbers of line
        result = wikipedia.summary(hastalik_ismi, sentences=2)
        return f"Hastalık hakkında size şu bilgileri vermek istiyorum. {result}"
    except wikipedia.exceptions.PageError:
        return f"Detaylı bilgi için bana ulaşmanız gerekmektedir."
    except wikipedia.exceptions.DisambiguationError:
        return f"İsteğinizi farklı bir şekilde belirtebilir misiniz?"

class ActionDefaultAskAffirmation(Action):
    def name(self) -> Text:
        return "action_default_ask_affirmation"

    def __init__(self):
        self.intent_mappings = {}

        with open('./intent_mapping.csv', newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                self.intent_mappings[row[0]] = row[1]

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_intent_name = tracker.latest_message['intent']['name']
        intent_prompt = self.intent_mappings[last_intent_name]
        message = "Sizi tam anlayamadım. {}".format(intent_prompt)
        dispatcher.utter_message(message)

        return []