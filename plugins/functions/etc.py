# SCP-079-AVATAR - Get newly joined member's profile photo
# Copyright (C) 2019-2020 SCP-079 <https://scp-079.org>
#
# This file is part of SCP-079-AVATAR.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from html import escape
from random import choice, uniform
from re import sub
from string import ascii_letters, digits
from threading import Thread, Timer
from time import localtime, sleep, time
from typing import Any, Callable, Optional, Union
from unicodedata import normalize

from cryptography.fernet import Fernet
from opencc import convert
from pyrogram import Message, User
from pyrogram.errors import FloodWait

from .. import glovar

# Enable logging
logger = logging.getLogger(__name__)


def code(text: Any) -> str:
    # Get a code text
    result = ""

    try:
        result = str(text).strip()

        if not result:
            return ""

        result = f"<code>{escape(result)}</code>"
    except Exception as e:
        logger.warning(f"Code error: {e}", exc_info=True)

    return result


def code_block(text: Any) -> str:
    # Get a code block text
    result = ""

    try:
        result = str(text).rstrip()

        if not result:
            return ""

        result = f"<pre>{escape(result)}</pre>"
    except Exception as e:
        logger.warning(f"Code block error: {e}", exc_info=True)

    return result


def crypt_str(operation: str, text: str, key: bytes) -> str:
    # Encrypt or decrypt a string
    result = ""

    try:
        f = Fernet(key)
        text = text.encode("utf-8")

        if operation == "decrypt":
            result = f.decrypt(text)
        else:
            result = f.encrypt(text)

        result = result.decode("utf-8")
    except Exception as e:
        logger.warning(f"Crypt str error: {e}", exc_info=True)

    return result


def delay(secs: int, target: Callable, args: list = None) -> bool:
    # Call a function with delay
    result = False

    try:
        t = Timer(secs, target, args)
        t.daemon = True
        result = t.start() or True
    except Exception as e:
        logger.warning(f"Delay error: {e}", exc_info=True)

    return result


def general_link(text: Union[int, str], link: str) -> str:
    # Get a general link
    result = ""

    try:
        text = str(text).strip()
        link = link.strip()

        if not (text and link):
            return ""

        result = f'<a href="{link}">{escape(text)}</a>'
    except Exception as e:
        logger.warning(f"General link error: {e}", exc_info=True)

    return result


def get_full_name(user: User, normal: bool = False, printable: bool = False, pure: bool = False) -> str:
    # Get user's full name
    result = ""

    try:
        if not user or user.is_deleted:
            return ""

        result = user.first_name

        if user.last_name:
            result += f" {user.last_name}"

        if result and normal:
            result = t2t(result, normal, printable, pure)
    except Exception as e:
        logger.warning(f"Get full name error: {e}", exc_info=True)

    return result


def get_hour() -> int:
    # Get hour
    result = 0

    try:
        result = localtime().tm_hour
    except Exception as e:
        logger.warning(f"Get hour error: {e}", exc_info=True)

    return result


def get_int(text: str) -> Optional[int]:
    # Get a int from a string
    result = None

    try:
        result = int(text)
    except Exception as e:
        logger.info(f"Get int error: {e}", exc_info=True)

    return result


def get_now() -> int:
    # Get time for now
    result = 0

    try:
        result = int(time())
    except Exception as e:
        logger.warning(f"Get now error: {e}", exc_info=True)

    return result


def get_text(message: Message, normal: bool = False, printable: bool = False, pure: bool = False) -> str:
    # Get message's text
    result = ""

    try:
        if not message:
            return ""

        message_text = message.text or message.caption

        if message_text:
            result += message_text

        if not result:
            return ""

        result = t2t(result, normal, printable, pure)
    except Exception as e:
        logger.warning(f"Get text error: {e}", exc_info=True)

    return result


def lang(text: str) -> str:
    # Get the text
    result = ""

    try:
        result = glovar.lang_dict.get(text, text)
    except Exception as e:
        logger.warning(f"Lang error: {e}", exc_info=True)

    return result


def mention_id(uid: int) -> str:
    # Get a ID mention string
    result = ""

    try:
        result = general_link(f"{uid}", f"tg://user?id={uid}")
    except Exception as e:
        logger.warning(f"Mention id error: {e}", exc_info=True)

    return result


def random_str(i: int) -> str:
    # Get a random string
    text = ""

    try:
        text = "".join(choice(ascii_letters + digits) for _ in range(i))
    except Exception as e:
        logger.warning(f"Random str error: {e}", exc_info=True)

    return text


def t2t(text: str, normal: bool, printable: bool, pure: bool = False) -> str:
    # Convert the string, text to text
    result = text

    try:
        if not result:
            return ""

        if glovar.normalize and normal:
            for special in ["spc", "spe"]:
                result = "".join(eval(f"glovar.{special}_dict").get(t, t) for t in result)

            result = normalize("NFKC", result)

        if glovar.normalize and normal and "Hans" in glovar.lang:
            result = convert(result, config="t2s.json")

        if printable:
            result = "".join(t for t in result if t.isprintable() or t in {"\n", "\r", "\t"})

        if pure:
            result = sub(r"""[^\da-zA-Z一-龥.,:'"?!~;()。，？！～@“”]""", "", result)
    except Exception as e:
        logger.warning(f"T2T error: {e}", exc_info=True)

    return result


def thread(target: Callable, args: tuple, kwargs: dict = None, daemon: bool = True) -> bool:
    # Call a function using thread
    result = False

    try:
        t = Thread(target=target, args=args, kwargs=kwargs, daemon=daemon)
        t.daemon = daemon
        result = t.start() or True
    except Exception as e:
        logger.warning(f"Thread error: {e}", exc_info=True)

    return result


def wait_flood(e: FloodWait) -> bool:
    # Wait flood secs
    result = False

    try:
        result = sleep(e.x + uniform(0.5, 1.0)) or True
    except Exception as e:
        logger.warning(f"Wait flood error: {e}", exc_info=True)

    return result
