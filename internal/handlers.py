import uuid
from internal.api_client import BackendClient
from helper.utils import Utils
from telebot import types
from telebot.async_telebot import AsyncTeleBot

class BotHandler:
    def __init__(self, api_client: BackendClient, utils: Utils) -> None:
        self.api_client = api_client
        self.utils = utils
        self.result_memory_save = {}

    async def prompt(self, bot: AsyncTeleBot, message: types.Message) -> None:
        message_splitter = message.text.split(" ")
        results_uuid = uuid.uuid4()
        self.result_memory_save.update({str(results_uuid): {}})

        parsed_elements = self.utils.parse_elements(message_splitter)
        parsed_filter = self.utils.strict_query_filter(parsed_elements)
        values_query = dict(parsed_elements.get("plain", ""))

        results = self.api_client.search(
            query=values_query.get("value"),
            filter=parsed_filter,
            limit=3
        )

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(text="◀️", callback_data=f"pagination_previous_{results_uuid}_0"), 
            types.InlineKeyboardButton(text="▶️", callback_data=f"pagination_next_{results_uuid}_0"), 
            types.InlineKeyboardButton(text="⏪", callback_data=f"pagination_start_{results_uuid}_0"), 
            types.InlineKeyboardButton(text="⏩", callback_data=f"pagination_last_{results_uuid}_0")
        )
    
        for result in results:
            sritct_values = self.utils.get_strict_values(elements=message_splitter)
            if self.utils.check_strict_values(strict_elements=sritct_values, result=result) or len(sritct_values) == 0:
                lenght = len(self.result_memory_save[str(results_uuid)])
                self.result_memory_save[str(results_uuid)][lenght] = result

        new_page = str(self.result_memory_save[str(results_uuid)][0])
        message = str(new_page).replace("{page_current}", new_page)
        
        await bot.send_message(
            message.chat.id,
            str(self.result_memory_save[str(results_uuid)][0]),
            parse_mode="HTML",
            reply_markup=markup
        )

    async def update_message(self, bot: AsyncTeleBot, call: types.CallbackQuery) -> None:
        data_split = call.data.split("_")
        chat_id = call.from_user.id
        message_id = call.message.id

        uuid = data_split[2]
        current_page = int(data_split[3])
        markup = types.InlineKeyboardMarkup(row_width=2)
        memory_save = self.result_memory_save

        print("Current page", current_page)
        if data_split[1] == "start":
            if current_page == 0:
                await bot.answer_callback_query(call.id, text='🚫 Vous ne pouvez pas effectuer cette action.')
                return
            
            new_page = memory_save[uuid][current_page]
            message = str(new_page).replace("{page_current}", new_page)

            markup.add(
                types.InlineKeyboardButton(text="◀️", callback_data=f"pagination_previous_{uuid}_0"), 
                types.InlineKeyboardButton(text="▶️", callback_data=f"pagination_next_{uuid}_0"), 
                types.InlineKeyboardButton(text="⏪", callback_data=f"pagination_start_{uuid}_0"), 
                types.InlineKeyboardButton(text="⏩", callback_data=f"pagination_last_{uuid}_0")
            )

            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=message,
                parse_mode="HTML",
                reply_markup=markup
            )
        
        elif data_split[1] == "previous":
            if current_page == 0:
                await bot.answer_callback_query(call.id, text='🚫 Vous ne pouvez pas effectuer cette action.')
                return
            
            new_page = memory_save[uuid][current_page-1]
            message = str(new_page).replace("{page_current}", new_page)

            markup.add(
                types.InlineKeyboardButton(text="◀️", callback_data=f"pagination_previous_{uuid}_{current_page-1}"), 
                types.InlineKeyboardButton(text="▶️", callback_data=f"pagination_next_{uuid}_{current_page-1}"), 
                types.InlineKeyboardButton(text="⏪", callback_data=f"pagination_start_{uuid}_{current_page-1}"), 
                types.InlineKeyboardButton(text="⏩", callback_data=f"pagination_last_{uuid}_{current_page-1}")
            )

            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=message,
                parse_mode="HTML",
                reply_markup=markup
            )
        
        elif data_split[1] == "next":
            if len(memory_save[uuid]) > current_page+1:
                await bot.answer_callback_query(call.id, text='🚫 Vous ne pouvez pas effectuer cette action.')
                return
            
            new_page = memory_save[uuid][current_page+1]
            message = str(new_page).replace("{page_current}", new_page)

            markup.add(
                types.InlineKeyboardButton(text="◀️", callback_data=f"pagination_previous_{uuid}_{current_page+1}"), 
                types.InlineKeyboardButton(text="▶️", callback_data=f"pagination_next_{uuid}_{current_page+1}"),
                types.InlineKeyboardButton(text="⏪", callback_data=f"pagination_start_{uuid}_{current_page+1}"), 
                types.InlineKeyboardButton(text="⏩", callback_data=f"pagination_last_{uuid}_{current_page+1}")
            )

            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=message,
                parse_mode="HTML",
                reply_markup=markup
            )
        
        elif data_split[1] == "last":
            if len(memory_save[uuid]) == current_page:
                await bot.answer_callback_query(call.id, text='🚫 Vous ne pouvez pas effectuer cette action.')
                return

            new_page = memory_save[uuid][current_page+len(memory_save[uuid])]
            message = str(new_page).replace("{page_current}", new_page)

            markup.add(
                types.InlineKeyboardButton(text="◀️", callback_data=f"pagination_previous_{uuid}_{len(memory_save[uuid])}"), 
                types.InlineKeyboardButton(text="▶️", callback_data=f"pagination_next_{uuid}_{len(memory_save[uuid])}"),
                types.InlineKeyboardButton(text="⏪", callback_data=f"pagination_start_{uuid}_{len(memory_save[uuid])}"), 
                types.InlineKeyboardButton(text="⏩", callback_data=f"pagination_last_{uuid}_{len(memory_save[uuid])}")
            )

            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=message,
                parse_mode="HTML",
                reply_markup=markup
            )