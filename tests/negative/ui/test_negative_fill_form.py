import pytest

@pytest.mark.ui
@pytest.mark.negativeUi
def test_add_number_missing_fullname(logged_in_page):
    page = logged_in_page

    page.click('button.bp5-button.bp5-small:has-text("Добавить номер")')

    page.fill('input[name="position"]', 'Менеджер')
    page.fill('input._maskInput_udrzt_4', '+77001234567')
    page.fill('textarea[name="comment"]', 'Комментарий к записи')

    page.click('button.bp5-button.bp5-intent-primary:has-text("Сохранить")')

    error_selector = 'div.bp5-form-helper-text:has-text("Обязательное поле")'

    try:
        element = page.wait_for_selector(error_selector, timeout=3000)
        assert element.is_visible(), "Сообщение об ошибке не видно на странице"
    except playwright._impl._errors.TimeoutError:
        pytest.fail("Ошибка: сообщение 'Обязательное поле' не появилось на странице в течение 3 секунд")

@pytest.mark.ui
@pytest.mark.negativeUi
def test_add_number_invalid_phone(logged_in_page):
    page = logged_in_page

    page.click('button.bp5-button.bp5-small:has-text("Добавить номер")')

    page.fill('input[name="fullName"]', 'Иван Иванов')
    page.fill('input[name="position"]', 'Менеджер')

    page.fill('input._maskInput_udrzt_4', '+7')

    page.fill('textarea[name="comment"]', 'Комментарий к записи')

    page.click('button.bp5-button.bp5-intent-primary:has-text("Сохранить")')

    error_selector = 'div.bp5-form-helper-text:has-text("Неверный формат телефона")'
    try:
        element = page.wait_for_selector(error_selector, timeout=3000)
        assert element.is_visible(), "Сообщение об ошибке не видно на странице"
    except playwright._impl._errors.TimeoutError:
        pytest.fail("Ошибка: сообщение 'Обязательное поле' не появилось на странице в течение 3 секунд")


@pytest.mark.ui
@pytest.mark.negativeUi
@pytest.mark.parametrize("invalid_email", [
    "a@b",
    "plainaddress",
    "user@",
    "user@ domain.com",
    "user@domain!com",
    "user@domain..com",
    "a" * 51 + "@example.com"
])
def test_add_number_with_invalid_email(logged_in_page, invalid_email):
    page = logged_in_page
    page.click('button.bp5-button.bp5-small:has-text("Добавить номер")')

    page.fill('input[name="fullName"]', 'Иван Иванов')
    page.fill('input[name="position"]', 'Менеджер')

    page.select_option('select[name="contactMethod[0].method"]', 'email')
    page.fill('input[name="contactMethod[0].value"]', invalid_email)

    page.click('button.bp5-button.bp5-intent-primary:has-text("Сохранить")')

    error_selector = 'div.bp5-form-helper-text:has-text("Неверный формат")'
    try:
        element = page.wait_for_selector(error_selector, timeout=3000)
        assert element.is_visible(), "Сообщение об ошибке не видно на странице"
    except playwright._impl._errors.TimeoutError:
        pytest.fail("Ошибка: сообщение 'Обязательное поле' не появилось на странице в течение 3 секунд")


MIN_FULLNAME_LEN = 2
MAX_FULLNAME_LEN = 100
MIN_POSITION_LEN = 2
MAX_POSITION_LEN = 50
MAX_COMMENT_LEN = 300

@pytest.mark.ui
@pytest.mark.negativeUi
@pytest.mark.parametrize("fullName, position, comment", [
    ("", "", ""),
    ("Иван Иванов", "Менеджер", "Комментарий"),
    ("И", "М", "К"),
    ("И" * 100, "Менеджер", ""),
    ("Иван Иванов", "Д" * 200, "Комментарий"),
    ("", "Менеджер", "Комментарий"),
    ("Иван Иванов", "Селер", "К" * 500),
])
def test_add_number(logged_in_page, fullName, position, comment):
    page = logged_in_page
    page.click('button.bp5-button.bp5-small:has-text("Добавить номер")')

    page.fill('input[name="fullName"]', fullName)
    page.fill('input[name="position"]', position)
    page.fill('input._maskInput_udrzt_4', '+77001234567')
    page.fill('textarea[name="comment"]', comment)
    page.click('button.bp5-button.bp5-intent-primary:has-text("Сохранить")')

    error_selector = 'div.bp5-form-helper-text:has-text("Обязательное поле"), div.bp5-form-helper-text:has-text("слишком")'

    def error_found():
        try:
            return page.wait_for_selector(error_selector, timeout=3000).is_visible()
        except TimeoutError:
            return False

    # Проверяем валидность полей
    fullName_valid = MIN_FULLNAME_LEN <= len(fullName) <= MAX_FULLNAME_LEN
    position_valid = (len(position) == 0) or (MIN_POSITION_LEN <= len(position) <= MAX_POSITION_LEN)
    comment_valid = len(comment) <= MAX_COMMENT_LEN

    if not fullName_valid or not position_valid or not comment_valid:
        assert error_found(), "Ожидалась ошибка валидации, но её нет"
        assert page.is_visible('button.bp5-button.bp5-intent-primary:has-text("Сохранить")'), "Форма закрылась, хотя есть ошибка"
    else:
        try:
            page.wait_for_selector('button.bp5-button.bp5-intent-primary:has-text("Сохранить")', state='detached', timeout=3000)
            saved = True
        except TimeoutError:
            saved = False
        assert saved, "Форма не сохранилась, хотя данные корректны"