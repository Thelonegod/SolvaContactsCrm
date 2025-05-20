import pytest
from playwright.sync_api import Page
#тест-кейсы с 1 по 10
@pytest.mark.ui
def test_open_add_number_popup(logged_in_page: Page):

    page = logged_in_page
    page.click('button.bp5-button.bp5-small:has-text("Добавить номер")')

    assert page.locator('button.bp5-button.bp5-small span.bp5-button-text:has-text("Добавить номер")').is_visible()

    assert page.locator('input[name="fullName"]').is_visible()
    assert page.locator('input[name="position"]').is_visible()
    assert page.locator('textarea[name="comment"]').is_visible()
    assert page.locator('button:has-text("Отмена")').is_visible()
    assert page.locator('button:has-text("Сохранить")').is_visible()

@pytest.mark.ui
def test_add_number_without_email(logged_in_page):
    page = logged_in_page
    page.click('button.bp5-button.bp5-small:has-text("Добавить номер")')

    page.fill('input[name="fullName"]', 'Иван Иванов')
    page.fill('input[name="position"]', 'Менеджер')
    page.fill('input._maskInput_udrzt_4', '+77001234567')

    page.fill('textarea[name="comment"]', 'Комментарий к записи')

    page.click('button.bp5-button.bp5-intent-primary:has-text("Сохранить")')

    assert page.wait_for_selector('div.bp5-toast:has(span.bp5-toast-message:has-text("Контакт добавлен"))',
                                  timeout=3000).is_visible()

@pytest.mark.ui
def test_add_number_with_email(logged_in_page):
    page = logged_in_page
    page.click('button.bp5-button.bp5-small:has-text("Добавить номер")')

    page.fill('input[name="fullName"]', 'Иван Иванов')
    page.fill('input[name="position"]', 'Менеджер')
    page.fill('input._maskInput_udrzt_4', '+77001234567')

    page.click('button.bp5-button.bp5-minimal.bp5-small.bp5-intent-success._addBtn_n7q98_22:has-text("Добавить")')
    page.select_option('select[name="contactMethod[1].method"]', 'email')
    page.fill('input[name="contactMethod[1].value"]', 'test@example.com')

    page.fill('textarea[name="comment"]', 'Комментарий к записи')

    page.click('button.bp5-button.bp5-intent-primary:has-text("Сохранить")')

    assert page.wait_for_selector('div.bp5-toast:has(span.bp5-toast-message:has-text("Контакт добавлен"))',
                                  timeout=3000).is_visible()

@pytest.mark.ui
def test_add_number_without_number(logged_in_page):
    page = logged_in_page
    page.click('button.bp5-button.bp5-small:has-text("Добавить номер")')

    page.fill('input[name="fullName"]', 'Иван Иванов')
    page.fill('input[name="position"]', 'Менеджер')

    page.select_option('select[name="contactMethod[0].method"]', 'email')
    page.fill('input[name="contactMethod[0].value"]', 'test@example.com')

    page.fill('textarea[name="comment"]', 'Комментарий к записи')

    page.click('button.bp5-button.bp5-intent-primary:has-text("Сохранить")')

    assert page.wait_for_selector('div.bp5-toast:has(span.bp5-toast-message:has-text("Контакт добавлен"))',
                                  timeout=3000).is_visible()

