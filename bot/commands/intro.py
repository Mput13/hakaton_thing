import enum

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.core.constants import UserRoleTranslation
from bot.core.simple_dialog_handler import DialogContextStep, RetryError, ExitHandler, SimpleDialog
from bot.core.text import dialogs
from bot.models import db_session
from bot.services.account_service import account_service

intro_router = Router(name='intro')
intro_dialogs = dialogs['intro']


class FillAboutForm(StatesGroup):
    about = State()
    role = State()
    target = State()


class IntroActionKinds(str, enum.Enum):
    confirm = 'confirm'


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
        builder.button(text=intro_dialogs['start']['confirm_button'], callback_data=IntroAction(action='confirm'))
        await message.answer(
            intro_dialogs['start']['usage_statistic'],

            reply_markup=builder.as_markup()

        )


@intro_router.callback_query(IntroAction.filter(F.action == IntroActionKinds.confirm))
async def about_info(query: CallbackQuery, state: FSMContext, bot: Bot):
    await about_info_dialog.start_dialog(query, state, bot)


class CollectRole(DialogContextStep):
    reversed_translations = {v: k for k, v in UserRoleTranslation.items()}

    async def validate_user_data(self, message: Message, state: FSMContext):
        possible_values = set(UserRoleTranslation.values())

        if message.text not in possible_values:
            raise RetryError(f'Недопустимое значение: {message.text}')
        return self.reversed_translations[message.text]


class ExitAbout(ExitHandler):
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
        await message.answer(intro_dialogs['complete'])


about_info_dialog = SimpleDialog(
    name='about_collect', router=intro_router, steps=[
        DialogContextStep(
            state=FillAboutForm.about,
            text=intro_dialogs['about_info'],
            buttons=list(UserRoleTranslation.values())
        ),
        CollectRole(
            state=FillAboutForm.role,
            text=intro_dialogs['roles'],
            buttons=list(UserRoleTranslation.values())
        ),
        DialogContextStep(
            state=FillAboutForm.target,
            text=intro_dialogs['target'],
            buttons=list(UserRoleTranslation.values())
        ),
    ],
    on_exit=ExitAbout()
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
