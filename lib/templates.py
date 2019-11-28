from bot_settings import templates_overrides


def is_override_available(template_name):
    return template_name in templates_overrides and templates_overrides[template_name] is not None


TITLE_TEMPLATE = templates_overrides['TITLE_TEMPLATE'] if is_override_available('TITLE_TEMPLATE') else \
    u'AB {date}'


PAGE_TEMPLATE = templates_overrides['PAGE_TEMPLATE'] if is_override_available('PAGE_TEMPLATE') else \
    u"""
    После заполнения своей ячейки отметьте чекбокс рядом со своей фамилией, иначе AB Reminder 
    расстроится и пойдет вас искать.
    <table>
        <thead>
            <tr>
                <th>Имя</th>
                <th>Что интересного произошло за неделю<br/>Что планируете делать на следующей</th>
                <th>Вопросы и ответы<br/>Указывайте имя, когда задаёте вопрос</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
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
    else u'Привет всем :wave:! {date} у вас будет АБ, я подготовил страницу, на которой вам нужно рассказать, ' + \
         u'чем занимались и чем планируете заниматься в ближайшее время: {url} .\nНайдите там себя, заполните ' + \
         u'ячейку и отметьте чекбокс напротив своей фамилии. Также, вы можете посмотреть, чем занимались другие, ' + \
         u'и оставить свои вопросы и коментарии в последней колонке.\nБлиже к АБ я просмотрю неотмеченные ' + \
         u'чекбоксы, и еще раз напомню об этом тем, кто забыл.'

SLACK_REMIND_MESSAGE_TEMPLATE = templates_overrides['SLACK_REMIND_MESSAGE_TEMPLATE'] \
    if is_override_available('SLACK_REMIND_MESSAGE_TEMPLATE') \
    else u'Привет всем :wave:! Совсем скоро у вас будет АБ и, насколько я вижу, вы заполнили страницу ' + \
         u'{remind_condition}\nВот ссылка на страницу: {url} .'

SLACK_REMIND_ALL_CHECKED_TEMPLATE = templates_overrides['SLACK_REMIND_ALL_CHECKED_TEMPLATE'] \
    if is_override_available('SLACK_REMIND_ALL_CHECKED_TEMPLATE') \
    else u'полностью :notbad:! На всякий случай напомню, что вы можете оставить вопросы и коментарии к тому, ' + \
         u'что написали другие, в последней колонке.'

SLACK_REMIND_HAS_UNCHECKED_TEMPLATE = templates_overrides['SLACK_REMIND_HAS_UNCHECKED_TEMPLATE'] \
    if is_override_available('SLACK_REMIND_HAS_UNCHECKED_TEMPLATE') \
    else u'не полностью :crycat:. Поэтому, как и писал до этого, напоминаю: {users} - вам нужно рассказать о том, ' + \
         u'чем вы занимались последнее время, и чем планируете заниматься. Также, все вы можете оставить вопросы ' + \
         u'и коментарии написанному другими, в последней колонке.'
