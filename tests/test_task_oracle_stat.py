from unittest import mock
import aiohttp
import pytest

from task_oracle_stat import check_url, fetch_method_status, check_methods_for_url, process_urls, run_main


@pytest.mark.parametrize("url, valid", [
    ("https://google.com", True),
    ("http://cbr.ru", True),
    ("test.site", False),
    ("ftp://obmennik.com", False)
])
@pytest.mark.asyncio
async def test_check_url(url, valid):
    assert await check_url(url) is valid


@pytest.mark.parametrize("url, method, expected_status", [
    ("https://www.google.com", "GET", 200),
    ("https://www.google.com", "POST", 405),
    ("https://nonexistent.google.com", "GET", None),
    ("https://httpbin.org/status/404", "GET", 404),
])
@pytest.mark.asyncio
async def test_fetch_method_status(url, method, expected_status):
    async with aiohttp.ClientSession() as session:
        status = await fetch_method_status(session, url, method)
        assert status == expected_status, f"Для {url} ожидался статус {expected_status}, но получен {status}"


@pytest.mark.parametrize("url, expected_methods", [
    ("https://httpbin.org", {'GET': 200, 'HEAD': 200, 'OPTIONS': 200}),
    ("https://www.google.com", {"GET": 200, "HEAD": 200}),
    ("https://nonexistent.google.com", {}),
])
@pytest.mark.asyncio
async def test_check_methods_for_url(url, expected_methods):
    available_methods = await check_methods_for_url(url)
    assert available_methods == expected_methods, (f"Для {url} ожидались методы {expected_methods}, "
                                                   f"но получены {available_methods}")


@pytest.mark.parametrize("urls, expected_results", [
    (["https://httpbin.org", "https://www.google.com"], {
        "https://httpbin.org": {"GET": 200, "HEAD": 200, "OPTIONS": 200},
        "https://www.google.com": {"GET": 200, "HEAD": 200}
    }),
    (["https://nonexistent.google.com", "http://cbr.ru"], {
        "https://nonexistent.google.com": {},
        "http://cbr.ru": {'GET': 200, 'PUT': 200, 'PATCH': 200, 'DELETE': 200, 'HEAD': 200, 'OPTIONS': 200}
    }),
    (["test.site", "ftp://obmennik.com"], {})
])
@pytest.mark.asyncio
async def test_process_urls(urls, expected_results):
    results = await process_urls(urls)
    assert results == expected_results, f"Для URL {urls} ожидался результат {expected_results}, но получен {results}"


def test_run_main():
    expected_output = {
        "https://google.com": {"GET": 200, "HEAD": 200},
        "http://cbr.ru": {"GET": 200, "HEAD": 200, "OPTIONS": 200},
        "test.site": {},
        "ftp://obmennik.com": {}
    }

    with mock.patch("task_oracle_stat.process_urls") as mock_process_urls, \
            mock.patch("builtins.print") as mock_print:
        mock_process_urls.return_value = expected_output

        run_main()

        mock_process_urls.assert_called_once_with([
            "https://google.com",
            "http://cbr.ru",
            "test.site",
            "ftp://obmennik.com"
        ])

        mock_print.assert_called_once_with(expected_output)
