from src.lib.lib import *

## Funzione di gestione del comando /eventi
# Mostra la locandina dei prossimi eventi in formato .png
async def eventi_command(update: Update, context: CallbackContext) -> None:
    # Implementa la logica per visualizzare il menu
    await update.message.reply_text("Ecco il nostri eventi settimanali:")
    return await context.bot.sendPhoto(update.effective_chat.id, photo=open('src\\media\\SpecialNightsEvents.jpeg', 'rb'))
