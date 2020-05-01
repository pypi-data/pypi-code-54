from widgetastic.widget import Text
from widgetastic.widget import View

from widgetastic_patternfly4 import Tab


class TabsTestView(View):
    @View.nested
    class primary(View):
        ROOT = ".//div[@id='ws-react-c-tabs-basic']"

        @View.nested
        class tab1(Tab):
            TAB_NAME = "Tab item 1"
            content = Text(".")

        @View.nested
        class tab2(Tab):
            TAB_NAME = "Tab item 2"
            content = Text(".")

    @View.nested
    class secondary(View):
        ROOT = ".//div[@id='ws-react-c-tabs-secondary-buttons']"

        @View.nested
        class tab1(Tab):
            TAB_NAME = "Tab item 1"

            @View.nested
            class secondary1(Tab):
                TAB_NAME = "Secondary tab item 1"
                content = Text(".")

            @View.nested
            class secondary2(Tab):
                TAB_NAME = "Secondary tab item 2"
                content = Text(".")

    @View.nested
    class separate(View):
        ROOT = ".//div[@id='ws-react-c-tabs-separate-content']"

        @View.nested
        class tab1(Tab):
            TAB_NAME = "Tab item 1"
            content = Text(".")

        @View.nested
        class tab2(Tab):
            TAB_NAME = "Tab item 2"
            content = Text(".")

        @View.nested
        class tab3(Tab):
            TAB_NAME = "Tab item 3"
            content = Text(".")


def test_primary_tabs(browser):
    view = TabsTestView(browser)
    assert view.primary.tab1.is_displayed
    # selecting the tab just in case, as other tests could have selected smth different
    view.primary.tab1.select()
    assert view.primary.tab2.is_displayed
    assert view.primary.tab1.is_active()
    assert not view.primary.tab2.is_active()
    assert view.primary.tab1.content.text == "Tab 1 section"
    view.primary.tab2.select()
    assert not view.primary.tab1.is_active()
    assert view.primary.tab2.is_active()
    assert view.primary.tab2.content.text == "Tab 2 section"


def test_secondary_tabs(browser):
    view = TabsTestView(browser)
    assert view.secondary.tab1.is_displayed
    # selecting the tab just in case, as other tests could have selected smth different
    view.primary.tab1.select()
    assert view.secondary.tab1.is_active()
    assert view.secondary.tab1.secondary1.is_displayed
    assert view.secondary.tab1.secondary2.is_displayed
    assert view.secondary.tab1.secondary1.is_active()
    assert not view.secondary.tab1.secondary2.is_active()
    assert view.secondary.tab1.secondary1.content.text == "Secondary tab item 1 item section"
    view.secondary.tab1.secondary2.select()
    assert not view.secondary.tab1.secondary1.is_active()
    assert view.secondary.tab1.secondary2.is_active()
    assert view.secondary.tab1.secondary2.content.text == "Secondary tab item 2 section"


def test_auto_selected(browser):
    view = TabsTestView(browser)
    # selecting the tab just in case, as other tests could have selected smth different
    view.primary.tab1.select()
    assert not view.primary.tab2.is_active()
    view.primary.tab2.content.read()
    assert view.primary.tab2.is_active()


def test_separate_content_tabs(browser):
    view = TabsTestView(browser)
    view.separate.tab1.select()
    assert view.separate.tab2.is_displayed
    assert view.separate.tab1.is_active()
    assert not view.separate.tab2.is_active()
    assert view.separate.tab1.content.text == "Tab 1 section"
    view.separate.tab2.select()
    assert not view.separate.tab1.is_active()
    assert view.separate.tab2.is_active()
    assert view.separate.tab2.content.text == "Tab 2 section"
