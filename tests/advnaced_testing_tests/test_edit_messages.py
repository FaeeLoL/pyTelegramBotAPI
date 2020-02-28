import sys

sys.path.append('../../../')

import pytest
import os
from pyTelegramBotAPI import telebot
from pyTelegramBotAPI.telebot import apihelper
from pyTelegramBotAPI.telebot import types


should_skip = 'TOKEN' and 'CHAT_ID' not in os.environ

if not should_skip:
    TOKEN = os.environ['TOKEN']
    CHAT_ID = os.environ['CHAT_ID']


# creates bot instance
@pytest.fixture()
def bot():
    if should_skip:
        print("Failed to read env variables: TOKEN, CHAT_ID")
        exit(1)

    tb = telebot.TeleBot(TOKEN)

    yield tb


@pytest.fixture()
def message(bot):
    msg = bot.send_message(CHAT_ID, "test_message")
    assert msg.message_id
    yield msg


def test_edit_message_text(bot, message):
    new_message = "edited_message"
    msg = bot.edit_message_text(new_message, chat_id=CHAT_ID,
                                message_id=message.message_id)
    assert msg.message_id == message.message_id
    assert msg.text == new_message


"""
edit_message parameters values:
text = {1; 4096} //boundary value analysis
message_id=None -- {1, current number of messages in chat} // 
parse_mode=None,  {markdown, html, None} // combination with message
disable_web_page_preview=None, {True, None} //if send message with url, 
                                              make web_page preview or not.
reply_markup={any keyboard, inline_keyboard, None} //equivalence class tests: 
no need to make different keyboards, that's why test with keyboards of 
different types
"""


def test_edit_message_empty_text(bot, message):
    new_message = ""
    with pytest.raises(apihelper.ApiException):
        bot.edit_message_text(new_message, chat_id=CHAT_ID,
                              message_id=message.message_id)


def test_edit_message_max_text(bot, message):
    new_message = "a" * 4096
    msg = bot.edit_message_text(new_message, chat_id=CHAT_ID,
                                message_id=message.message_id)
    assert msg.message_id == message.message_id


def test_edit_message_max_plus_one_text(bot, message):
    new_message = "a" * 4097
    with pytest.raises(apihelper.ApiException):
        bot.edit_message_text(new_message, chat_id=CHAT_ID,
                              message_id=message.message_id)


def test_edit_message_unknown_message(bot):
    new_message = "edit_message"
    with pytest.raises(apihelper.ApiException):
        bot.edit_message_text(new_message, chat_id=CHAT_ID,
                              message_id=999999)


def test_edit_message_unknown_chat(bot, message):
    new_message = "edit_message"
    with pytest.raises(apihelper.ApiException):
        bot.edit_message_text(new_message, chat_id=0,
                              message_id=message.message_id)


inline_markup = types.InlineKeyboardMarkup(row_width=1)
itembtn1 = types.InlineKeyboardButton('test', callback_data="test")
inline_markup.add(itembtn1)


def test_edit_message_with_inline_markup(bot, message):
    new_message = "edit_message"
    msg = bot.edit_message_text(new_message, chat_id=CHAT_ID,
                                message_id=message.message_id,
                                reply_markup=inline_markup)
    assert msg.message_id == message.message_id


markup = types.ReplyKeyboardMarkup(row_width=1)
itembtn1 = types.KeyboardButton('test')
markup.add(itembtn1)


def test_edit_message_with_common_markup(bot, message):
    new_message = "edit_message"
    with pytest.raises(telebot.apihelper.ApiException):
        bot.edit_message_text(new_message, chat_id=CHAT_ID,
                              message_id=message.message_id,
                              reply_markup=markup)


def test_edit_message_with_html_text(bot, message):
    new_message = "<b>edit_message</b>"
    msg = bot.edit_message_text(new_message, chat_id=CHAT_ID,
                                message_id=message.message_id,
                                parse_mode="html")
    assert msg.message_id == message.message_id


def test_edit_message_with_markdown_text(bot, message):
    new_message = "*edit_message*"
    msg = bot.edit_message_text(new_message, chat_id=CHAT_ID,
                                message_id=message.message_id,
                                parse_mode="Markdown")
    assert msg.message_id == message.message_id
