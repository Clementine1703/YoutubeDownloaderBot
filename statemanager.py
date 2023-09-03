from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class StateManager():
    def __init__(self) -> None:
        self.keyboards = {
            'choosing_a_file_type': ReplyKeyboardMarkup(keyboard=[
                                        [
                                            KeyboardButton(text="Скачать видео"),
                                            KeyboardButton(text="Скачать аудиодорожку")
                                        ]
                                    ], resize_keyboard=True
            ),
            'waiting_for_a_url': ReplyKeyboardMarkup(keyboard=[
                                        [
                                            KeyboardButton(text="Назад"),
                                        ]
                                    ], resize_keyboard=True
            )
        }
        self.__active_format = '.mp4'
        self.__active_keyboard = self.keyboards['choosing_a_file_type']
    
    def set_active_keyboard(self, stage):
        self.__active_keyboard = self.keyboards[stage]

    def set_active_format(self, format):
        self.__active_format = format

    def get_active_keyboard(self):
        return self.__active_keyboard
    
    def get_active_format(self):
        return self.__active_format
