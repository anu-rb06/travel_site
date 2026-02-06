import uuid
from playwright.sync_api import sync_playwright

def test_homepage_loads():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("http://127.0.0.1:5000")

        assert page.title() == "Travel Website"

        browser.close()

def test_login_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("http://127.0.0.1:5000/login")

        page.fill("input[name=email]", "abrb270699@gmail.com")
        page.fill("input[name=password]", "12345")

        page.click("button")

        assert page.url == "http://127.0.0.1:5000/"

        browser.close()


def test_register_post(client):
    email = f"test_{uuid.uuid4()}@example.com"
    response = client.post("/register", data={
        "name":"Test",
        "email":"email",
        "password":"123456"
    })
    assert response.status_code == 302

def test_booking_flow():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("http://127.0.0.1:5000/login")

        page.fill("input[name=email]", "test@example.com")
        page.fill("input[name=password]", "123456")

        page.click("button")
        page.wait_for_load_state("networkidle")

        print("Current URL:", page.url)

        assert "Logout" in page.content()

        page.goto("http://127.0.0.1:5000/packages")
        page.click("text=Book Now")

        page.wait_for_load_state("networkidle")
        assert "Book Package" in page.content()

        browser.close()

