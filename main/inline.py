from config import INDEX_USERNAME, SCHEDULE_ID, STATUS_ID, UPLOADS_USERNAME
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button1 = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="🌟Discussion Group", url= f"https://t.me/Anime_Chatterbox")
            ],
            [
                InlineKeyboardButton(text="Schedule [UTC]", url= f"https://t.me/Latest_Ongoing_Airing_Anime/15848"),
                InlineKeyboardButton(text="Schedule [IST]", url= f"https://t.me/Latest_Ongoing_Airing_Anime/15849")
            ]
        ]
    )

button2 = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="Check Queue", url= f"https://t.me/{UPLOADS_USERNAME}/{STATUS_ID}")
            ]
        ]
    )
