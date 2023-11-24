import enum

from aiogram import Router, F, Bot, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.core.simple_dialog_handler import DialogContextStep, RetryError, ExitHandler, SimpleDialog
from bot.core.text import dialogs
from bot.models import db_session

intro_router = Router(name='intro')
intro_dialogs = dialogs['intro']


class FillAboutForm(StatesGroup):
    about = State()
    role = State()
    target = State()


class IntroActionKinds(str, enum.Enum):
    articles = 'articles'


class IntroAction(CallbackData, prefix='intr'):
    action: IntroActionKinds


@intro_router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    # сессия к БД также должна проходить через DI и передаваться в параметры функции, но встроенный DI у aiogram также плох
    with db_session.create_session() as session:
        pass
        # await account_service.register_account(
        #     session, UserInit(
        #         chat_id=message.from_user.id,
        #         login=message.from_user.username,
        #         name=message.from_user.first_name,
        #         surname=message.from_user.last_name,
        #     )
        # )

        await message.answer(intro_dialogs['start']['hello'])
        builder = InlineKeyboardBuilder()
        builder.button(text=intro_dialogs['start']['articles_button'], callback_data=IntroAction(action='articles'))
        await message.answer(
            intro_dialogs['start']['usage_statistic'],

            reply_markup=builder.as_markup()

        )


@intro_router.callback_query(IntroAction.filter(F.action == IntroActionKinds.articles))
async def about_info(query: CallbackQuery, state: FSMContext, bot: Bot):
    await articles_dialog.start_dialog(query, state, bot)
    articles = [[types.KeyboardButton(text="Тут будет ваша статья 1")],
                [types.KeyboardButton(text="Тут будет ваша статья 2")],
                [types.KeyboardButton(text="Тут будет ваша статья 3")],
                [types.KeyboardButton(text="Тут будет ваша статья 4")]]
    jsoned_dict = {"Тут будет ваша статья 1": "aboba", "Тут будет ваша статья 2": "aboba",
                   "Тут будет ваша статья 3": "aboba",
                   "Тут будет ваша статья 4": "aboba"}
    keyboard = types.ReplyKeyboardMarkup(keyboard=articles)
    await query.message.answer("Выбирите статью", reply_markup=keyboard)

    async def validate_user_data(self, message: Message, state: FSMContext):
        if message.text not in articles:
            raise RetryError(f'Недопустимое значение: {message.text}')

        return jsoned_dict[message.text]


class CollectArticle(DialogContextStep):
    jsoned_dict = {"Тут будет ваша статья 1": "aboba", "Тут будет ваша статья 2": "aboba",
                   "Тут будет ваша статья 3": "aboba",
                   "Тут будет ваша статья 4": "aboba"}

    async def validate_user_data(self, message: Message, state: FSMContext):
        possible_values = ["Тут будет ваша статья 1",
                           "Тут будет ваша статья 2",
                           "Тут будет ваша статья 3",
                           "Тут будет ваша статья 4"]

        if message.text not in possible_values:
            raise RetryError(f'Недопустимое значение: {message.text}')
        await message.answer(self.jsoned_dict[message.text], reply_markup=types.ReplyKeyboardRemove())
        return self.jsoned_dict[message.text]


class ExitArticle(ExitHandler):
    async def handle(self, message: Message, state: FSMContext):
        collected_data = await self.dialog.collect_dialog_data(state)

        with db_session.create_session() as session:
            pass
            # await account_service.fill_about(
            #     session, message.from_user.id, UserAbout(
            #         **collected_data
            #     )
            # )

        await state.clear()


articles_dialog = SimpleDialog(
    name='article_collect', router=intro_router, steps=[
        DialogContextStep(
            state=FillAboutForm.about,
            text=intro_dialogs['choose_article'],
            buttons=None
        ),
        CollectArticle(
            state=FillAboutForm.role,
            text=intro_dialogs['roles'],
            buttons=[[types.KeyboardButton(text="Тут будет ваша статья 1")],
                     [types.KeyboardButton(text="Тут будет ваша статья 2")],
                     [types.KeyboardButton(text="Тут будет ваша статья 3")],
                     [types.KeyboardButton(text="Тут будет ваша статья 4")]]
        ),
        DialogContextStep(

            state=FillAboutForm.target,
            text=intro_dialogs['target'],
            buttons=None
        ),
    ],
    on_exit=ExitArticle()
)


@intro_router.message(Command('my-profile'))
async def my_profile(message: Message, state: FSMContext):
    # на чтение можно ходить и напрямую в репо
    with db_session.create_session() as session:
        pass
    #     user = await user_repository.get_user_by_chat_id(session, message.chat.id)
    # about_info = user.about

    await message.answer(
        intro_dialogs['profile_info'].format(about=about_info.about, role=about_info.role, target=about_info.target)
    )
