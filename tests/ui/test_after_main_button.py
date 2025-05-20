import pytest
from playwright.sync_api import Page


#Перед началом данного теста переключите кнопку основного контакта на другой контакт, не на Рудгерс
@pytest.mark.ui
def test_main_button_first(logged_in_page):
    page = logged_in_page

    assert page.locator("tr._tableRow_17k7x_34").nth(1).locator("td").nth(1).inner_text() == "Рудгерс"

    page.locator(
        'xpath=//tr[td[text()="Рудгерс"]]/preceding-sibling::tr[1]//label[contains(@class, "bp5-switch")]'
    ).click()

@pytest.mark.ui
def test_click_telegram_button_and_confirm_popup_opens(logged_in_page: Page):
    page = logged_in_page

    with page.expect_popup() as popup_info:
        page.click('a[href^="https://t.me/"]')

    new_page = popup_info.value
    new_page.wait_for_load_state('domcontentloaded')

    print("Открылась новая вкладка с URL:", new_page.url)
    assert "t.me" in new_page.url

@pytest.mark.ui
def test_click_whatsapp_button_and_check_popup(logged_in_page: Page):
    page = logged_in_page

    with page.expect_popup() as popup_info:
        page.click('a[href^="https://wa.me/"]')

    new_page = popup_info.value
    new_page.wait_for_load_state('domcontentloaded')

    print("Открылась новая вкладка с URL:", new_page.url)
    # Для отладки выведем url и длину строки
    print(f"URL length: {len(new_page.url)}")

    assert "api.whatsapp.com" in new_page.url or "wa.me" in new_page.url, f"Unexpected URL: {new_page.url}"

def click_duplicate_and_wait_toast(page: Page):
    duplicate_btn_selector = 'span.bp5-icon.bp5-icon-duplicate'
    toast_selector = 'div.bp5-toast.bp5-intent-success:has(span.bp5-toast-message:has-text("Cкопировано"))'

    page.wait_for_selector(duplicate_btn_selector, state='visible')
    page.click(duplicate_btn_selector)

    page.wait_for_selector(toast_selector, timeout=3000)
    assert page.locator(toast_selector).is_visible()


@pytest.mark.ui
def test_click_duplicate(logged_in_page: Page):
    click_duplicate_and_wait_toast(logged_in_page)