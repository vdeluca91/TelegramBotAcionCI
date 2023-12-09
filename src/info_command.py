from src.lib.lib import *

## Funzione di gestione del comando /info
# Mostra le informazioni generali del ristorante, quali numero, orari e mappa(utilizzando google maps)
async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone_number = "+391234567890"
    map_url = "https://www.google.com/maps?q=Latitudine,Longitudine"
    orari = "Lun: Chiuso\nMar: 19:30-02:00 (Special Nights Events)\nMer: 19:30-24:00\nGio: 19:30-02:00 (Special Nights Events)\nVen: 19:30-24:00\nSab: 19:30-02:00 (Special Nights Events)\nDom: 19:30-02:00"

    await update.message.reply_text(
        f"Orari di apertura:\n{orari}\n"
        f"Per chiamarci, clicca qui: tel:{phone_number}\n"
        f"Ci troviamo in Via del Ristorante, 12345, Città, clicca qui per raggiungerci: {map_url}"
    )
