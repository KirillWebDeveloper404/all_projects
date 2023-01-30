from aiogram.utils.callback_data import CallbackData

del_media = CallbackData('del_media_af', 'pr')
delete_something = CallbackData('del_something_af', 'thing')
create_message_funnel = CallbackData('_create_message_af_', 'msg_type', 'funnel_id', 'save')
close_add_message_funnel = CallbackData('close_add_message_funnel', 'prefix')