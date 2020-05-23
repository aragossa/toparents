import time

from bot_user import Botuser
from buttons_helper import KeyboardHelper
from dbconnector import Dbconnetor


class Notificator ():

    def __init__(self, bot):
        self.bot = bot

    def get_active_notifications(self):
        while True:
            Dbconnetor.execute_insert_query("SET TIME ZONE 'Europe/Moscow';")
            notifications = Dbconnetor.execute_select_many_query(
                """SELECT request_id, sender_user_id, message_text
                   FROM toparents_bot.user_requests
                   WHERE request_status = 'NEW'""")
            for notification in notifications:
                admin_list = Botuser.get_admins()
                request_text = notification[2]
                sender_id = notification[1]
                request_id = notification[0]
                sender_username = Botuser.get_username(sender_id)
                send_text = ('#request\nОТ: {}\n\n{}'.format(sender_username, request_text))
                for admin in admin_list:
                    user = Botuser(uid=admin, bot=self.bot)
                    keyboard = KeyboardHelper.reply_to_user_request_keyboard(user=user, sender_id=sender_id, request_id=request_id)
                    sent_message = user.send_message(chat_id=user.uid, text=send_text, keyboard=keyboard)
                    user.save_request_message(request_id=request_id, admin_id=user.uid, message_id=sent_message.message_id)
                    time.sleep(1)
                Dbconnetor.execute_insert_query("UPDATE toparents_bot.user_requests SET request_status = 'SENT' WHERE request_id = '{}' ".format(request_id))
            time.sleep(5)

