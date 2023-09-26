from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters



TYPE_WORK, FILLING_FORM, CONFIRMATION, ACTION, EDIT_VALUE, PROMO_CODE, CONTACT_INFO, RESET_PROMO_CODE, ESSAY, PRESENTATION, PROBLEM_SOLVING = range(11)


# слоаврь вопросов в анкете
questions = {
    'Диплом': {
        'Университет': 'Название университета:',
        'Факультет': 'Название факультета:',
        'Тема работы': 'Тема работы:',
        'Объем работы': 'Объем работы:',
        'Обязательный % уникальности': 'Оригинальность работы:',
        'Дополнительные требования': 'Дополнительные требования:',
        'Как с вами связаться': 'Контактные данные:'
    },
    'Курсовая': {
        'Университет': 'Название университета:',
        'Факультет': 'Название факультета:',
        'Тема работы': 'Тема работы:',
        'Объем работы': 'Объем работы:',
        'Обязательный % уникальности': 'Оригинальность работы:',
        'Дополнительные требования': 'Дополнительные требования:',
        'Как с вами связаться': 'Контактные данные:'
    },
    'Экзамен': {
        'Университет': 'Название университета:',
        'Факультет': 'Название факультета:',
        'Курс': 'Курс:',
        'Предмет': 'Предмет:',
        'Формат проведения': 'Формат проведения:',
        'Образец заданий': 'Образец заданий:',
        'Дополнительные требования': 'Дополнительные требования:',
        'Как с вами связаться': 'Контактные данные:'
    },
    'Пересдача': {
        'Университет': 'Название университета:',
        'Факультет': 'Название факультета:',
        'Курс': 'Курс:',
        'Предмет': 'Предмет:',
        'Формат проведения': 'Формат проведения:',
        'Образец заданий': 'Образец заданий:',
        'Дополнительные требования': 'Дополнительные требования:',
        'Как с вами связаться': 'Контактные данные:'
    },
    'Комиссия': {
        'Университет': 'Название университета:',
        'Факультет': 'Название факультета:',
        'Курс': 'Курс:',
        'Предмет': 'Предмет:',
        'Дополнительные требования': 'Дополнительные требования:',
        'Как с вами связаться': 'Контактные данные:'
    },
    'Домашнее задание': {
        'Тип домашнего задания': 'Тип домашнего задания:',
    },
    'Эссе': {
        'Университет': 'Название университета:',
        'Тема': 'Тема эссе:',
        'Количество символов': 'Количество символов:',
        'Дедлайн': 'Дедлайн:',
        'Дополнительные требования': 'Дополнительные требования:',
        'Как с вами связаться': 'Контактные данные:'
    },
    'Презентация': {
        'Университет': 'Название университета:',
        'Тема': 'Тема презентации:',
        'Количество слайдов': 'Количество слайдов:',
        'Дедлайн': 'Дедлайн:',
        'Дополнительные требования': 'Дополнительные требования:',
        'Как с вами связаться': 'Контактные данные:'
    },
    'Решение задач': {
        'Университет': 'Название университета:',
        'Срок выполнения Дедлайн': 'Дедлайн:',
        'Как с вами связаться': 'Контактные данные:'
    }
}

# команда старт
def start(update, context):
    update.message.reply_text(
        'Ответьте пожалуйста на некоторые вопросы, это поможет более корректно определить нашего специалиста на вашу работу.')

    keyboard = [
        [InlineKeyboardButton("Диплом", callback_data='Диплом')],
        [InlineKeyboardButton("Курсовая", callback_data='Курсовая')],
        [InlineKeyboardButton("Экзамен", callback_data='Экзамен')],
        [InlineKeyboardButton("Пересдача", callback_data='Пересдача')],
        [InlineKeyboardButton("Комиссия", callback_data='Комиссия')],
        [InlineKeyboardButton("Домашнее задание", callback_data='Домашнее задание')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Выберите тип работы:', reply_markup=reply_markup)
    return TYPE_WORK


#выбор типа работы
def choose_type(update, context):
    query = update.callback_query
    query.answer()

    type_work = query.data
    context.user_data['type'] = type_work

    if type_work == 'Домашнее задание':
        keyboard = [
            [InlineKeyboardButton("Эссе", callback_data='Эссе')],
            [InlineKeyboardButton("Презентация", callback_data='Презентация')],
            [InlineKeyboardButton("Решение задач", callback_data='Решение задач')],
            [InlineKeyboardButton("Назад", callback_data='back')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.effective_message.reply_text('Выберите тип домашнего задания:', reply_markup=reply_markup)
        return TYPE_WORK  # Изменено на TYPE_WORK, чтобы выбрать тип работы снова
    else:
        context.user_data['current_questions'] = questions[type_work]
        context.user_data['form'] = {}
        context.user_data['current_step'] = list(context.user_data['current_questions'].keys())[0]

        update.effective_message.reply_text('Тип работы: {}\n{}'.format(type_work, context.user_data['current_questions'][context.user_data['current_step']]))
        return FILLING_FORM

# вопросы из словаря
def ask_question(update, context):
    current_step = context.user_data['current_step']

    update.message.reply_text(context.user_data['current_questions'][current_step])
    return FILLING_FORM


# заполнение анкеты
def fill_form(update, context):
    user_data = context.user_data
    user_answer = update.message.text

    if 'edit_param' in user_data:
        edit_param = user_data.pop('edit_param')
        user_data['form'][edit_param] = user_answer
        return ask_question(update, context)

    current_step = user_data['current_step']
    user_data['form'][current_step] = user_answer

    if current_step == 'Тип домашнего задания':
        return show_confirmation(update, context)

    questions_list = list(user_data['current_questions'].keys())
    current_index = questions_list.index(current_step)

    if current_index + 1 < len(questions_list):
        user_data['current_step'] = questions_list[current_index + 1]
    else:
        return show_confirmation(update, context)

    return ask_question(update, context)

# подтверждение анкеты да или нет ресет работает только после выбора темы
def show_confirmation(update, context):
    form_text = "\n".join("{}: {}".format(key, value) for key, value in context.user_data['form'].items())

    keyboard = [
        [InlineKeyboardButton("Да", callback_data='confirm')],
        [InlineKeyboardButton("Нет", callback_data='edit')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Ваша анкета:\n{}\n\nПроверьте, все ли данные введены верно?'.format(form_text),
                              reply_markup=reply_markup)

    return CONFIRMATION


# подтвердить или изменить
def handle_confirmation(update, context):
    query = update.callback_query
    query.answer()

    if query.data == 'confirm':
        query.message.reply_text('Есть ли у вас промокод?', reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton('Да', callback_data='promo_code_yes')],
             [InlineKeyboardButton('Нет', callback_data='promo_code_no')]]))
        return ACTION
    elif query.data == 'edit':
        keyboard = [
            [InlineKeyboardButton("Изменить определенный параметр", callback_data='change')],
            [InlineKeyboardButton("Заполнить анкету заново", callback_data='reset')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.message.reply_text('Изменить анкету:', reply_markup=reply_markup)
        return ACTION



# обработка изменеить или подтвердить
def handle_action(update, context):
    query = update.callback_query
    query.answer()

    if query.data == 'cancel':
        query.message.reply_text('Сожалеем, что вы не заполнили анкету. До встречи!')
        return ConversationHandler.END
    elif query.data == 'reset':
        context.user_data['form'] = {}
        context.user_data['current_step'] = list(context.user_data['current_questions'].keys())[0]
        query.message.reply_text('Анкета полностью сброшена.\n{}'.format(
            context.user_data['current_questions'][context.user_data['current_step']]))
        return FILLING_FORM
    elif query.data == 'change':
        steps = list(context.user_data['current_questions'].keys())
        keyboard = [[InlineKeyboardButton(step, callback_data=step)] for step in steps]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.message.reply_text('Выберите параметр, который хотите изменить:', reply_markup=reply_markup)
        return ACTION
    elif query.data in context.user_data['current_questions'].keys():
        context.user_data['edit_param'] = query.data
        query.message.reply_text(
            'Введите новое значение для параметра "{}"'.format(context.user_data['current_questions'][query.data]))
        return EDIT_VALUE
    elif query.data == 'promo_code_yes':
        query.message.reply_text('Введите промокод:')
        return PROMO_CODE
    elif query.data == 'promo_code_no':
        reset_promo_code(update, context)
        query.message.reply_text('Как с вами связаться:')
        return CONTACT_INFO
    elif query.data == 'back':
        return start(update, context)  # Вернуться к выбору типа работы


#изменение конкретного параметра
def edit_value(update, context):
    user_answer = update.message.text
    current_step = context.user_data['edit_param']
    context.user_data['form'][current_step] = user_answer

    update.effective_message.reply_text(
        'Параметр "{}" успешно изменен!'.format(context.user_data['current_questions'][current_step]))
    return show_confirmation(update, context)


# удаление промокода
def reset_promo_code(update, context):
    if 'promo_code' in context.user_data:
        del context.user_data['promo_code']


# ввод промокода
def handle_promo_code(update, context):
    user_data = context.user_data
    user_data['promo_code'] = update.message.text

    update.effective_message.reply_text('Как с вами связаться:')
    return CONTACT_INFO


# информация контакт
def handle_contact_info(update, context):
    user_data = context.user_data
    user_data['contact_info'] = update.message.text

    return send_application(update, context)


# отправка админу
def send_application(update, context, admin_id=5696512274, admin_id1=652596926):
    form_text = "Пользователь: @{}\n".format(update.effective_user.username)
    form_text += "Тип работы: {}\n".format(context.user_data['type'])
    form_text += "\n".join("{}: {}".format(key, value) for key, value in context.user_data['form'].items())

    if 'promo_code' in context.user_data:
        form_text += "\nПромокод: {}".format(context.user_data['promo_code'])

    form_text += "\nКонтактные данные: {}".format(context.user_data['contact_info'])

    # отправка админу
    admin_message = form_text
    context.bot.send_message(admin_id, admin_message)
    context.bot.send_message(admin_id1, admin_message)
    update.message.reply_text(
        'Спасибо за обращение! Скоро с вами свяжется менеджер для обсуждения работы и обозначения цены.')

    return ConversationHandler.END


# отмена
def cancel(update, context):
    update.message.reply_text('Сожалеем, что вы не заполнили анкету. До встречи!')
    return ConversationHandler.END


# работа бота токен и номер админа
def main():
    # токены
    token = '6025991413:AAEXiQTsTsGt1w9tCSVPAXKu4Vp3d6NAJHg'
    admin_id = 5696512274
    admin_id1 = 652596926
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            TYPE_WORK: [CallbackQueryHandler(choose_type)],
            FILLING_FORM: [MessageHandler(Filters.text, fill_form)],
            CONFIRMATION: [CallbackQueryHandler(handle_confirmation)],
            ACTION: [CallbackQueryHandler(handle_action)],
            EDIT_VALUE: [MessageHandler(Filters.text, edit_value)],
            PROMO_CODE: [MessageHandler(Filters.text, handle_promo_code)],
            CONTACT_INFO: [MessageHandler(Filters.text, handle_contact_info)],
            ESSAY: [MessageHandler(Filters.text, fill_form)],
            PRESENTATION: [MessageHandler(Filters.text, fill_form)],
            PROBLEM_SOLVING: [MessageHandler(Filters.text, fill_form)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()