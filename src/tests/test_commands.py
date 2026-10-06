from unittest.mock import MagicMock

from kernelo.commands import build_commands


def test_build_commands():
    app = MagicMock()
    app.commands = {}
    cmds = build_commands(app)
    assert "/help" in cmds
    assert "/clear" in cmds
    assert "/exit" in cmds


def test_exit_command():
    app = MagicMock()
    cmds = build_commands(app)
    cmds["/exit"].handler("")
    assert app.running is False


def test_clear_command():
    app = MagicMock()
    app.messages = [{"role": "user", "content": "hi"}]
    cmds = build_commands(app)
    cmds["/clear"].handler("")
    assert len(app.messages) == 0
    app.console.clear.assert_called_once()
    app.print_banner.assert_called_once()
