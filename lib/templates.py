from bot_settings import templates_overrides


def is_override_available(template_name):
    return template_name in templates_overrides and templates_overrides[template_name] is not None


TITLE_TEMPLATE = templates_overrides['TITLE_TEMPLATE'] if is_override_available('TITLE_TEMPLATE') else \
    u'{date} Технологизация iOS'


PAGE_TEMPLATE = templates_overrides['PAGE_TEMPLATE'] if is_override_available('PAGE_TEMPLATE') else \
    u"""
    <div data-macro-name="details" class="plugin-tabmeta-details conf-macro output-block" data-hasbody="true">
        <table>
            <tbody>
                <tr>
                    <th>Дата</th>
                    <td> <span>&nbsp; <time datetime="{date}" class="date-past"> </time> &nbsp;</span> </td>
                </tr>
                <tr>
                    <th>Докладчики</th>
                    <td>Вся команда</td>
                </tr>
                <tr>
                    <th>Темы</th>
                    <td> <ul><li>Что нового</li></ul> </td>
                </tr>
            </tbody>
        </table>
    </div>
    <br/>
    <p>
    После заполнения своей ячейки отметьте чекбокс рядом со своей фамилией, иначе AB Reminder
    расстроится и пойдет вас искать.
    </p>
    <br/>
    <table>
        <thead>
            <tr>
                <th>Имя</th>
                <th>Что интересного произошло за эту неделю<br/>Что планируете делать следующую неделю</th>
                <th>Комментарии</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
    <p>
        <strong>Не забудьте добавить метку 'технологизация_ios' к странице!</strong>
    </p>
    """

TEAM_ROW_TEMPLATE = templates_overrides['TEAM_ROW_TEMPLATE'] if is_override_available('TEAM_ROW_TEMPLATE') else \
    u"""<tr><th colspan="3">{name}</th></tr>"""

USER_ROW_TEMPLATE = templates_overrides['USER_ROW_TEMPLATE'] if is_override_available('USER_ROW_TEMPLATE') else \
    u"""
    <tr>
        <td>
            <ac:task-list>
                <ac:task>
                    <ac:task-id>{task_id}</ac:task-id>
                    <ac:task-status>incomplete</ac:task-status>
                    <ac:task-body>
                        <ac:link><ri:user ri:userkey="{user_key}" /></ac:link>
                    </ac:task-body>
                </ac:task>
            </ac:task-list>
        </td>
        <td> </td>
        <td> </td>
    </tr>
    """

SLACK_PAGE_MESSAGE_TEMPLATE = templates_overrides['SLACK_PAGE_MESSAGE_TEMPLATE'] \
    if is_override_available('SLACK_PAGE_MESSAGE_TEMPLATE') \
    else u'Здоровеньки :wave:! Дедушка Джобс завещал делать технологизацию каждую пятницу, и, особеннов, в эту: {date}. ' + \
         u'Тут есть страничка, напиши плиз чем занимаешься, чем планируешь заниматься в ближайшее время: {url} .\nНайди там себя, заполни ' + \
         u'ячейку и отметь чекбокс напротив своей фамилии. Также, можно посмотреть, чем занимались другие, ' + \
         u'и оставить свои вопросы и коментарии в последней колонке.\nБлиже к технологизации дедушка Джобс ' + \
         u' проверит чекбоксы, и еще раз напомнит об этом тем, кто забыл.'

SLACK_REMIND_MESSAGE_TEMPLATE = templates_overrides['SLACK_REMIND_MESSAGE_TEMPLATE'] \
    if is_override_available('SLACK_REMIND_MESSAGE_TEMPLATE') \
    else u'Вечер в хату! Короче, разраб, скоро технологизация и я в благородство играть не буду: расскажешь чем занимался последнее время и чем планируешь заниматься – и мы в расчете. Заодно посмотрим, как быстро у тебя башка после проверок на CI прояснится. А по твоей теме постараюсь разузнать.' + \
         u'{remind_condition}\nВот ссылка на страницу: {url} .'

SLACK_REMIND_ALL_CHECKED_TEMPLATE = templates_overrides['SLACK_REMIND_ALL_CHECKED_TEMPLATE'] \
    if is_override_available('SLACK_REMIND_ALL_CHECKED_TEMPLATE') \
    else u'полностью :notbad:! На всякий случай напомню, что вы можете оставить вопросы и коментарии к тому, ' + \
         u'что написали другие, в последней колонке.'

SLACK_REMIND_HAS_UNCHECKED_TEMPLATE = templates_overrides['SLACK_REMIND_HAS_UNCHECKED_TEMPLATE'] \
    if is_override_available('SLACK_REMIND_HAS_UNCHECKED_TEMPLATE') \
    else u'Короч, напоминаю: {users} - вам нужно рассказать о том, ' + \
         u'чем вы занимались последнее время, и чем планируете заниматься. Также, все вы можете оставить вопросы ' + \
         u'и комментарии написанному другими, в последней колонке.'
