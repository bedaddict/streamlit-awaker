from unittest.mock import MagicMock, patch

from selenium.common.exceptions import TimeoutException

import main


def test_no_button_means_already_awake():
    with patch("main.WebDriverWait") as mock_wait_cls:
        mock_wait_cls.return_value.until.side_effect = TimeoutException()
        assert main.wake_app(MagicMock(), "http://example.com") is True


def test_button_clicked_and_disappears():
    button = MagicMock()
    with patch("main.WebDriverWait") as mock_wait_cls:
        mock_wait_cls.return_value.until.side_effect = [button, None]
        assert main.wake_app(MagicMock(), "http://example.com") is True
        button.click.assert_called_once()


def test_button_clicked_but_stuck():
    button = MagicMock()
    with patch("main.WebDriverWait") as mock_wait_cls:
        mock_wait_cls.return_value.until.side_effect = [button, TimeoutException()]
        assert main.wake_app(MagicMock(), "http://example.com") is False


if __name__ == "__main__":
    test_no_button_means_already_awake()
    test_button_clicked_and_disappears()
    test_button_clicked_but_stuck()
    print("All tests passed.")
