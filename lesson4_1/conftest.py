import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as OptionsChrome
from selenium.webdriver.firefox.options import Options as OptionsFirefox

def pytest_addoption(parser):

    parser.addoption('--browser_name', action='store', default='chrome',
                 help="Choose browser: chrome or firefox")
    parser.addoption('--language', action='store', default='en', 
                     help="Choose language: ru or another")

@pytest.fixture(scope="function")
def browser(request):
    
    browser_name=request.config.getoption("browser_name")
    user_language=request.config.getoption("language")
    browser = None
    # Параметр языка должен быть указан явно через командную строку!
    if (None == user_language):
        raise pytest.UsageError("--language should be set as --language=es or --language=fr")
    else:
        print("user_language=",user_language)

    if ('chrome' == browser_name):
        print("\nstart chrome browser for test..")
        # Chrome options
        options_chrome = OptionsChrome()
        options_chrome.add_experimental_option('prefs', {'intl.accept_languages': user_language})        
        browser = webdriver.Chrome(options=options_chrome)
    elif ('firefox' == browser_name):
        print("\nstart firefox browser for test..")
        # Для Firefox объявление нужного языка будет выглядеть немного иначе:
        options_firefox = OptionsFirefox()
        options_firefox.set_preference("intl.accept_languages", user_language)
        browser = webdriver.Firefox(options=options_firefox)
    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")

    yield browser
    print("\nquit browser..")
    browser.quit()
