from src.lib.lib import *



# Dizionario di traduzione dei giorni della settimana in italiano
italian_day = {
    'Monday': 'Lunedì',
    'Tuesday': 'Martedì',
    'Wednesday': 'Mercoledì',
    'Thursday': 'Giovedì',
    'Friday': 'Venerdì',
    'Saturday': 'Sabato',
    'Sunday': 'Domenica'
}

# Dizionario di traduzione dei mesi in italiano
italian_month = {
    'January': 'Gennaio',
    'February': 'Febbraio',
    'March': 'Marzo',
    'April': 'Aprile',
    'May': 'Maggio',
    'June': 'Giugno',
    'July': 'Luglio',
    'August': 'Agosto',
    'September': 'Settembre',
    'October': 'Ottobre',
    'November': 'Novembre',
    'December': 'Dicembre'
}


## Funzioni di gestione del comando /prenota
# Permettono di prenotare un tavolo attraverso una procedura di domande-risposte ottenute in input dall'utente.
#le informazioni richieste sono rispettivamente: 
#   -nome prenotazione
#   -numero di telefono
#   -posti da prenotare
#   -giorno
#   -fascia oraria
#si conclude con il recap delle informazioni ottenute e con la possibilità di confermare o annullare la prenotazione prima di essere memorizzata nel sistema(db) 
async def prenota_start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text('Per effettuare la prenotazione mi servono alcune informazioni. Inserisci il nome per la prenotazione:')
    return NAME

# Funzione chiamata quando il nome viene inviato
async def prenota_name(update: Update, context: CallbackContext) -> int:
    context.user_data['name'] = update.message.text
    await update.message.reply_text(f'Grazie, {context.user_data["name"]}! Qual è il tuo numero di telefono?')
    return PHONE

# Funzione chiamata quando il numero di telefono viene inviato
async def prenota_phone(update: Update, context: CallbackContext) -> int:
    context.user_data['phone'] = update.message.text
    await update.message.reply_text('Ottimo! Quanti posti desideri prenotare? Inserisci un numero compreso tra 1 e 10.')
    
    return RESERVED_SEATS

# Funzione chiamata quando il numero di posti viene inviato
async def prenota_reserved_seats(update: Update, context: CallbackContext) -> int:
    #context.user_data['reserved_seats'] = update.message.text
    user_input = update.message.text
    if not user_input.isdigit():
        await update.message.reply_text('Per favore, inserisci un numero non un carattere PAGLIACCIO.')
        return
    reserved_seats = int(user_input)
    #1 <= reserved_seats <= 10
    if reserved_seats < 1 or reserved_seats > 10: 
        await update.message.reply_text('Per favore, inserisci un numero valido di posti (da 1 a 10).')
        return
    
    context.user_data['reserved_seats'] = reserved_seats
    await update.message.reply_text(f'Bene! Il numero di posti selezionati è {context.user_data['reserved_seats']}. Rispondi con un qualsiasi carattere per continuare...')
    return DAY

# Funzione chiamata quando il giorno viene inviato
async def prenota_day(update: Update, context: CallbackContext) -> int:
    
    #Mostra i pulsanti per selezionare una data nel formato "giorno, mese, anno"
    current_date = datetime.now()
    keyboard = []
    giorni = []
    for i in range(7):
        date = current_date + timedelta(days=i)
        formatted_date = italian_day[date.strftime('%A')] + ', ' + date.strftime('%d') + ' ' + italian_month[date.strftime('%B')] + ' ' + date.strftime('%Y')
        date_in_iso = date.strftime('%Y-%m-%d')  # Converti la data nel formato "anno-mese-giorno"
        giorni.append(date_in_iso)
        date_in_iso1 = datetime.strptime(date_in_iso, '%Y-%m-%d').strftime('%d-%m-%Y')
        date_again = f"manageDate@{date_in_iso}"
        keyboard.append([InlineKeyboardButton(formatted_date, callback_data=date_again)])

    reply_markup = InlineKeyboardMarkup(keyboard)
    #reply_markup = ReplyKeyboardMarkup(keyboard)
    await update.message.reply_text("Per quale giorno desideri prenotare?\nSeleziona una data:", reply_markup=reply_markup)
    return BUTTON_HANDLER
    

async def prenota_time_slot(update: Update, context: CallbackContext) -> int:
    print(context.user_data)
    reserved_seats = context.user_data["reserved_seats"]
    reserved_data  = context.user_data["date"]
    try:
        db.connect()
        # selezione poi la spiego
        new_day = ("SELECT *,s2.id as id_time_slot FROM seats_occupation s1 JOIN max_seats_time_slot s2 on s1.time_slot = s2.id WHERE s1.day = %s and s1.free_seats >= %s")
        res = db.select_query(new_day, (reserved_data,reserved_seats))
        available_time_slots = [ f'{item["time_slot"]}#{item["id_time_slot"]}' for item in res ]
    except Exception as e:
        Logger.error(str(e))
        await update.callback_query.answer(text="Si è verificato un errore button_click valore1=1.")
    finally:
        # Chiudi la connessione al database
        db.disconnect()

    if ( len(available_time_slots) == 0 ) :
        text = f"Non ci sono slot disponibili per {reserved_data}.\nSeleziona un'altra data"
        await update.message.reply_text(text)
        return DAY

    #Simulazione di fasce orarie disponibili 
    keyboard = [[InlineKeyboardButton(slot.split('#')[0], callback_data=f"manageTime@{slot}")] for slot in available_time_slots]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Perfetto! A che ora preferisci?\nScegli una fascia oraria:', reply_markup=reply_markup)
    return BUTTON_HANDLER

async def confirmation(update: Update, context: CallbackContext) -> int:
    # Simulazione di conferma della prenotazione
    confirmation_message = (
        f'Questi sono i dettagli della tua prenotazione:\n'
        f'Nome: {context.user_data["name"]}\n'
        f'Telefono: {context.user_data["phone"]}\n'
        f'Posti prenotati: {context.user_data["reserved_seats"]}\n'
        f'Giorno: {context.user_data["date"]}\n'
        f'Ora: {context.user_data["time_slot"]}\n\n'
        'Confermi la prenotazione?'
    )
    
    keyboard = [[InlineKeyboardButton("Conferma", callback_data=f"confirmPren@confirm"),
                InlineKeyboardButton("Annulla", callback_data=f"declinePren@cancel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(confirmation_message, reply_markup = reply_markup)
    #query.edit_message_text(confirmation_message, reply_markup=reply_markup)
    
    return BUTTON_HANDLER

async def button_click(update: Update, context: CallbackContext) -> int:
    query= update.callback_query
    id_user = query.message.chat_id
    data = query.data
        
    # Assume che il campo 'data' abbia la forma 'valore1:valore2'
    parts = data.split('@')
    
    if len(parts) == 2:
        valore1 = parts[0]
        valore2 = parts[1]

        # gestisce la risposta in base al 'valore1'
        if valore1 == 'manageDate':
            context.user_data['date'] = valore2
            # Connessione al database
            try:
                db.connect()
                # selezione poi la spiego
                new_day = ("SELECT count(*) n_row FROM seats_occupation WHERE day = %s")
                value_to_compare = valore2
                res = db.select_query(new_day, (value_to_compare,))
                res = res[0]['n_row']
                if res != 3:

                    values = [(valore2,1), (valore2,2), (valore2,3)]
                    new_pren_day = ("INSERT INTO seats_occupation (day, time_slot) VALUES (%s, %s)")
                    db.execute_query(new_pren_day, values, multi=True)
            except Exception as e:
                Logger.error(str(e))
                await update.callback_query.answer(text="Si è verificato un errore button_click valore1=1.")
            finally:
                # Chiudi la connessione al database
                db.disconnect()
            # Rimuovi il messaggio contenente la tastiera inline
            await context.bot.delete_message(chat_id=id_user, message_id=query.message.message_id)
            ##devo convertire valore 2
            date_in_iso1 = datetime.strptime(valore2, '%Y-%m-%d').strftime('%d-%m-%Y')
            text= f"D'accordo! La data selezionata è {date_in_iso1} . Rispondi con un qualsiasi carattere per continuare..."
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)    

            return TIME_SLOT
        if valore1 == 'manageTime':
            context.user_data['time_slot'] = valore2.split('#')[0]
            context.user_data['id_time_slot'] = valore2.split('#')[1]  
            text= f'Perfetto! Ci vediamo alle {context.user_data['time_slot']}! Rispondi con un qualsiasi carattere per continuare...'
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text) 
            # Rimuovi il messaggio contenente la tastiera inline
            await context.bot.delete_message(chat_id=id_user, message_id=query.message.message_id)
            return CONFIRMATION
        if valore1 == 'confirmPren':
            #Logica per inserire la prenotazione nel database
            try:
                # Connessione al database
                db.connect()
                # Esempio di inserimento dei dati nel database
                insert_query3 = (
                    "INSERT INTO prenotazioni (id_user, name, phone, reserved_seats, day, time_slot) "
                    "VALUES (%s, %s, %s, %s, %s, %s)"
                )
                values = (
                    id_user,
                    context.user_data['name'],
                    context.user_data['phone'],
                    context.user_data['reserved_seats'],
                    context.user_data['date'],
                    context.user_data['id_time_slot']
                )

                db.execute_query(insert_query3, values,multi=False)
                await update.callback_query.answer(text="Prenotazione confermata! Grazie!")
                text= "Tutto pronto! Ti aspettiamo.\n\nE ADESSO?!\nHai dato un'occhiata ai nostri eventi? Clicca qui --> /eventi e preparati a divertirti con noi!"
                await context.bot.send_message(chat_id=update.effective_chat.id, text=text) 
            except Exception as e:
                Logger.error(str(e))
                await update.callback_query.answer(text="Si è verificato un errore durante la conferma della prenotazione.")
            finally:
                # Chiudi la connessione al database
                db.disconnect()

            
            await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
            return ConversationHandler.END
        if valore1 == 'declinePren':
            await update.callback_query.answer(text="Prenotazione annullata!")
            text= f"Oh no, hai annullato la procedura di prenotazione :'(\n\nQualcosa è andato storto?\nContattaci pure atttraverso i nostri contatti che troverai qui --> /info\nSaremo felici di accoglierti presto, magari in uno dei nostri /eventi ;)"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text) 
            await context.bot.delete_message(chat_id=id_user, message_id=query.message.message_id)
            return ConversationHandler.END
        
        # if valore1 == 'deleteSinglePren':
        #     text= f"Oh no, hai annullato la procedura di prenotazione :'(\n\nQualcosa è andato storto?\nContattaci pure atttraverso i nostri contatti che troverai qui --> /info\nSaremo felici di accoglierti presto, magari in uno dei nostri /eventi ;)"
        #     return ConversationHandler.END
        # if valore1 == 'deleteAllByUser':
        #     text= f"Oh no, hai annullato la procedura di prenotazione :'(\n\nQualcosa è andato storto?\nContattaci pure atttraverso i nostri contatti che troverai qui --> /info\nSaremo felici di accoglierti presto, magari in uno dei nostri /eventi ;)"
        #     return ConversationHandler.END
    else:
        await update.callback_query.answer("Formato non valido.")
    return BUTTON_HANDLER