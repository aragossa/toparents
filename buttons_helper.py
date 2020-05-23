from telebot import types


class KeyboardHelper:
    @staticmethod
    def first_post_keyboard(user):
        keyboard = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text=user.select_message('GO'), callback_data='send_first_post')
        keyboard.add(btn1)
        btn2 = types.InlineKeyboardButton(text=user.select_message('CONTACT'), callback_data='call_back')
        keyboard.add(btn2)
        return keyboard

    @staticmethod
    def reply_call_back_button(user):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text=user.select_message('CONTACT'))
        keyboard.add(btn1)
        return keyboard

    @staticmethod
    def inline_call_back_button(user):
        keyboard = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text=user.select_message('CONTACT'), callback_data='call_back')
        keyboard.add(btn1)
        return keyboard

    @staticmethod
    def reply_tp_user_request_keyboard(user, request_id):
        keyboard = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text=user.select_message('REPLY_TO'),
                                          callback_data='reply_{}_{}'.format(user.uid, request_id))
        keyboard.add(btn1)
        return keyboard
