# from ninja import Schema
#
#
# class UserIdSchema(Schema):
#     id: int



import requests
import json

# Inline keyboardni JSON formatida yaratish
inline_keyboard = {
    "inline_keyboard": [
        [
            {"text": "O'qidim", "callback_data": "show"}
        ]
    ]
}

# Xabarni yuborish uchun URL va ma'lumotlar
url = "https://api.telegram.org/bot6819252648:AAG4LhWqnO3RDECzSqmPTCJa3H_UY2tXYto/sendMessage"
params = {
    "chat_id": 834562449,
    "text": "🎉 Hamyonni to'ldirildi\n💲 1.000 UZS\n💳 Smart-market hamyoni\n🕒 13.02.2024 - 17:40\n🛠 To'landi.",
    "reply_markup": json.dumps(inline_keyboard)  # Inline keyboardni JSON ko'rinishida yuborish
}

# So'rovni amalga oshirish
response = requests.get(url, params=params)

# Javobni tekshirish
if response.status_code == 200:
    print("Xabar muvaffaqiyatli yuborildi!")
else:
    print(f"Xatolik yuz berdi: {response.status_code}")