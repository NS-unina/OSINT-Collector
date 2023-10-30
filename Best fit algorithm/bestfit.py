import spacy

# Carico il modello NLP pre-addestrato
nlp = spacy.load("it_core_news_sm")

# Definisco un dizionario che mappa le parole chiave ai social network e ai relativi tool
keyword_to_social_network = {
    "Instagram": ["instagram", "foto", "immagini", "foto profilo", "post"],
    "Twitter": ["twitter", "tweets", "tweet", "feed", "menzioni"],
    "Telegram": ["telegram", "messaggi", "chat", "gruppi", "contatti"],
    "Dark Web": ["dark web", "darkweb", "contenuti illegali", "mercato nero"]
}

def suggest_tool(input_text):
    # Esecuzione dell'analisi NLP dell'input
    doc = nlp(input_text)

    # Inizializzo di un insieme per tenere traccia dei tool suggeriti
    suggested_tools = set()

    # Analizzo il testo per identificare le parole chiave e i tool corrispondenti
    input_text_lowercase = input_text.lower()
    for token in doc:
        for network, keywords in keyword_to_social_network.items():
            if token.text.lower() in keywords:
                tool = f"{network}_tool"
                suggested_tools.add(tool)

    # Se non è stato suggerito alcun tool, restituisce un messaggio di errore
    if not suggested_tools:
        return "Nessun tool suggerito per l'input fornito."

    # Altrimenti restituisce i tool suggeriti
    return "Suggerimenti per l'analisi: " + ", ".join(suggested_tools) #la join serve per eliminare la ridondanza

# Esempio di utilizzo
input_text = "Trova le foto di John Doe"
result = suggest_tool(input_text)
print(result)