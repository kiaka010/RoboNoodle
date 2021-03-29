from unittest import TestCase

import discord
import mock
from mock import PropertyMock, Mock
from discord import Message

from src.utils.message_utils import MessageUtils


class TestMessageUtils(TestCase):

    @mock.patch('discord.Message')
    def test_gather_no_mentions(self, mocked_message):
        message = discord.Message

        message.mentions = []

        actual = MessageUtils().gather_mentions(message)

        expected = ""
        self.assertEqual(expected, actual)

    def test_gather_single_mention(self):
        message = discord.Message
        user_one = Mock()
        user_one.id = 1234
        message.mentions = [user_one]

        actual = MessageUtils().gather_mentions(message)
        expected = "<@%s> " % 1234
        self.assertEqual(expected, actual)

    def test_gather_two_mention(self):
        message = discord.Message

        user_one = Mock()
        user_one.id = 1234

        user_two = Mock()
        user_two.id = 5678

        message.mentions = [user_one, user_two]

        actual = MessageUtils().gather_mentions(message)
        expected = "<@%s> <@%s> " % (1234, 5678)
        self.assertEqual(expected, actual)
