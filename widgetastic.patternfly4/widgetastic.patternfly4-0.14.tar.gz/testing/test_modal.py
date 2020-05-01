import pytest

from widgetastic_patternfly4.button import Button
from widgetastic_patternfly4.modal import Modal
from widgetastic_patternfly4.modal import ModalItemNotFound


@pytest.fixture()
def modal(browser):
    show_modal = Button(browser, "Show Modal")
    show_modal.click()
    modal = Modal(browser)
    yield modal
    if modal.is_displayed:
        modal.close()


def test_title(modal):
    assert modal.title


def test_body(modal):
    body = modal.body
    assert body.text.startswith("Lorem")


def test_close(modal):
    modal.close()
    assert not modal.is_displayed


def test_footer_items(modal):
    items = modal.footer_items
    assert len(items) == 2
    assert "Cancel" in items
    assert "Confirm" in items


def test_footer_item(modal):
    item = modal.footer_item("Confirm")
    assert item.text == "Confirm"
    item.click()
    assert not modal.is_displayed


def test_footer_item_invalid(modal):
    try:
        modal.footer_item("INVALID")
    except ModalItemNotFound:
        assert True
    else:
        pytest.fail("ModalItemNotFound exception expected.")
