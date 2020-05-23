# /usr/bin/python3

from buttons_helper import KeyboardHelper


def stating_handler(user, message):
    last_name = message.from_user.last_name
    first_name = message.from_user.first_name
    username = message.from_user.username
    user.join_aggrbot(last_name=last_name, first_name=first_name, username=username, ref_key='Notset', lang='rus')
    keyboard = KeyboardHelper.first_post_keyboard(user=user)
    user.send_message(message_index='HELLO_MESSAGE', keyboard=keyboard)


def text_message_handler(user, message, bot):
    user_state = user.getstate()
    if message.text == 'Написать администраторам':
        user.change_user_state ('REQUEST')
        user.send_message(message_index='ENTER_TEXT')

    elif user_state:
        if user_state == 'REQUEST':
            user.change_user_state('')
            user.save_request (message_text=message.text)

        elif 'RESPONSE' in user_state:
            sender_id = user_state.split('_')[1]
            request_id = user_state.split('_')[2]
            send_text = ('{}\n\n{}'.format(message.text, user.get_username(user.uid)))
            user.send_message(chat_id=sender_id, text=send_text)
            user.request_update_staus(request_id=request_id, new_staus='FIN', resposne_text=send_text)
            result_query = user.get_message_ids(request_id)
            user.change_user_state('')
            for row in result_query:
                bot.edit_message_text(chat_id=row[1], message_id=row[0], text='Обработано')




def reply_to_request_handler(call, user, bot):
    sender_user = call.data.split('_')[1]
    request_id = call.data.split('_')[2]
    user.change_user_state('RESPONSE_{}_{}'.format(sender_user, request_id))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text)
    send_text = ('{}\n\nВвежите ответ:'.format(call.message.text))
    bot.send_message(chat_id=call.message.chat.id, text=send_text)


def first_post_handler(call, user, bot):
    user.send_message(message_index='POST_1')