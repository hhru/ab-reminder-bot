# -*- coding: utf-8 -*-

TITLE_TEMPLATE = u'{date} Технологизация Android'

PAGE_TEMPLATE = u"""
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
    <strong>Не забудьте добавить метку 'технологизация_android' к странице!</strong>
</p>
"""

TEAM_ROW_TEMPLATE = u"""<tr><th colspan="3">{name}</th></tr>"""

USER_ROW_TEMPLATE = u"""
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

SLACK_PAGE_MESSAGE_TEMPLATE = u"""
Привет всем :wave:! {date} у вас будет технологизация, я подготовил страницу, на которой вам нужно рассказать, чем занимались и чем
планируете заниматься в ближайшее время: {url} .\n
Найдите там себя, заполните ячейку и отметьте чекбокс напротив своей фамилии. Также, вы можете посмотреть, 
чем занимались другие, и оставить свои вопросы и коментарии в последней колонке.\n
Ближе к технологизации я просмотрю неотмеченные чекбоксы, и еще раз напомню об этом тем, кто забыл.
"""

SLACK_REMIND_MESSAGE_TEMPLATE = u"""
Привет всем :wave:! Совсем скоро у вас будет технологизация и, насколько я вижу, вы заполнили страницу {remind_condition}\n
Вот ссылка на страницу: {url} .
"""

SLACK_REMIND_ALL_CHECKED_TEMPLATE = u"""полностью :notbad:!
На всякий случай напомню, что вы можете оставить вопросы и коментарии к тому, что написали другие, в последней колонке.
"""

SLACK_REMIND_HAS_UNCHECKED_TEMPLATE = u'не полностью :crycat:. Поэтому, как и писал до этого, напоминаю: {users} - ' + \
    u'вам нужно рассказать о том, чем вы занимались последнее время, и чем планируете заниматься. Также, все вы ' + \
    u'можете оставить вопросы и комментарии написанному другими, в последней колонке.'

