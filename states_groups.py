from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

class AdminInserTask(StatesGroup):
    name = State()
    describe = State()
    img = State()
    callback = State()
