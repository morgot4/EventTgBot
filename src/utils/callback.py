from aiogram.filters.callback_data import CallbackData 

class EventDetails(CallbackData, prefix='details'):
    id: int
    action: str
    listing: bool
