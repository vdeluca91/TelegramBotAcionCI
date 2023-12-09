
from typing import Final
from src.lib.config import *

#import command_functions
from src.start_command import *
from src.menu_command import *
from src.eventi_command import *
from src.info_command import *
from src.prenota_command import *
from src.le_mie_prenotazioni_command import *

from src.add_commands import add_commands

from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

TOKEN: Final = BOT_CONFIG['__TOKEN']

#Impostazione del ConversationHandler con i 6 stati: NAME, PHONE, RESERVED_SEATS, DAY, TIME_SLOT, CONFIRMATION, BUTTON_HANDLER
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('prenota', prenota_start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, prenota_name)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, prenota_phone)],
        RESERVED_SEATS: [MessageHandler(filters.TEXT & ~filters.COMMAND, prenota_reserved_seats)],
        DAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, prenota_day)],
        TIME_SLOT: [MessageHandler(filters.TEXT & ~filters.COMMAND, prenota_time_slot)],
        CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirmation)],
        BUTTON_HANDLER: [CallbackQueryHandler(button_click)],
    },
    fallbacks=[]
)


# Configurazione del bot con il ConversationHandler
# Inizializzazione dell'applicazione
app = Application.builder().token(TOKEN).build()
#updater = Updater(TOKEN, use_context=True)
print('🤙 EUREKA 🤙')
# Aggiunta del ConversationHandler



app.add_handler(CommandHandler("start", start_command))
app.add_handler(CommandHandler("le_mie_prenotazioni", le_mie_prenotazioni_command))
app.add_handler(CommandHandler("menu", menu_command))
app.add_handler(CommandHandler("eventi", eventi_command))
app.add_handler(CommandHandler("info", info_command))
app.add_handler(conv_handler)
app.add_handler(CallbackQueryHandler(edit_booking))


# Avvio dell'applicazione
app.run_polling()

#add_commands(app)
