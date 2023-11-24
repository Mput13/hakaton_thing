dialogs = {
    'intro': {
        'start': {
            'hello': 'Привет! Ты попал в чат бота для поиска команды на хакатон. '
                     'Прежде чем я покажу тебе других участников и покажу команду, не мог бы немного рассказать о себе?',

            'usage_statistic': 'Что бы ты не думал, что я бесполезный бот, вот тебе статистика:\n\n'
                               'На данный момент в активном поиске: {active_users}\n\nНеукоплектованных команд: {active_commands}',
            # лучше стараться избегать формулировок, где нужно склонение с числительными

            'articles_button': 'Статьи',
            'closest_point_button': 'Ближайшая точка раздельного сбора мусора'
        },
        'choose_article': 'Выберите статью',
        'about_info': 'Расскажи о себе:',
        'roles': '  Выберите роль',
        'target': 'Расскажите, какой проект вы хотите сделать',
        'complete': 'Спасибо, теперь вы можете подыскать себе команду или создать новую! Для этого нажмите на /teams',
        'profile_info': 'Вы ранее заполняли:\n\nО Себе: {about}, Роль: {role}\n\nЦель: {target}\n\n'
                        'Если хотите заново заполнить информацию о себе, можете нажать /start'
    }
}
