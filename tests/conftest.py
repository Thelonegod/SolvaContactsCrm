import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def logged_in_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            http_credentials={"username": "Df323Ds7232sdhU", "password": "fJllcMtdRUEYu91bsFUQ"}
        )
        page = context.new_page()
        page.goto("https://front-crm-lab-master.k8s.dev.solvatech.kz/crm/login")
        page.fill('input[name="email"]', 'mentor1@com')
        page.fill('input[name="password"]', 'mentor1.kz')
        with page.expect_navigation():
            page.click('button:has-text("Войти")')

        # Вот тут добавь нужные клики после логина:
        page.click('button.bp5-button:has-text("Меню")')
        page.click('a._link_12lhk_16:has-text("Партнеры")')
        page.click('a._name_16uf3_4[href="/crm/partner/28"]')

        yield page
        context.close()
        browser.close()
