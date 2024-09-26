import asyncio
import re
import aiohttp


async def check_url(url):
    """Проверка, что строка является URL"""
    URL_REGEX = re.compile(r'(http|https)://')
    if not URL_REGEX.match(url):
        return False
    return True


async def fetch_method_status(session, url, method):
    """Проверка статуса ответа выполнения HTTP запроса"""
    try:
        async with session.request(method, url) as response:
            return response.status
    except Exception:
        return None


async def check_methods_for_url(url):
    """Проверка доступных методов для URL"""
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS']
    available_methods = {}

    async with aiohttp.ClientSession() as session:
        for method in methods:
            status = await fetch_method_status(session, url, method)
            if status is not None and status != 405:
                available_methods[method] = status
    return available_methods


async def process_urls(urls):
    """Обработка списка URL, возвращает словарь с доступными методами"""
    results = {}

    for url in urls:
        if await check_url(url):
            results[url] = await check_methods_for_url(url)
        else:
            print(f'Строка "{url}" не является ссылкой.')
    return results


def run_main():
    """Запуск основного процесса обработки URL"""
    input_urls = [
        "https://google.com",
        "http://cbr.ru",
        "test.site",
        "ftp://obmennik.com"
    ]
    output = asyncio.run(process_urls(input_urls))
    print(output)


if __name__ == '__main__':
    run_main()
