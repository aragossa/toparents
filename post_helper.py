
def send_post(user, post_index):
    user.send_post_to_users(post_index)

def enter_post_index(user):
    user.send_message(message_index="SELECT_INDEX")
    user.change_user_state ("INPUT_INDEX")

def send_custom_post (user, post_index):
    user.send_custom_post (post_index=post_index)

def enter_custom_post_index(user):
    user.send_message(message_index="SELECT_INDEX")
    user.change_user_state ("INPUT_INDEX_CUSTOM")