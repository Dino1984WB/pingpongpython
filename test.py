#unit testing for the pong game

import unittest # Import the Python unit testing framework
from kivy.base import EventLoop
from kivy.tests.common import GraphicUnitTest
from main import PongGame


def did_it_start():
    EventLoop.ensure_window()
    return EventLoop.window
