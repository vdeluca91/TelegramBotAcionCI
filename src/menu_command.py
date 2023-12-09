from src.lib.lib import *

## Funzione di gestione del comando /menu
# mostra il menu in formato .png / .pdf / link. abbiamo preferito il .png
async def menu_command(update: Update, context: CallbackContext) -> None:
    # Implementa la logica per visualizzare il menu
    await update.message.reply_text("Ecco il nostro menu:")
    # return context.bot.send_document(update.effective_chat.id, document=open('menu-completo.pdf', 'rb'))
    # return context.bot.send_document(update.effective_chat.id, "https://palermo.prezzemoloevitale.it/media/downloadable/menu/_menu_completo.pdf")
    return await context.bot.sendPhoto(update.effective_chat.id, photo=open('src\\media\\Menu.jpg', 'rb'))
