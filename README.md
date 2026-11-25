# Roomly QA Assignment

Проверка формы бронирования переговорных на [демостенде Roomly](https://rcsi-science.github.io/demo-roomly/). Стек: Python 3.13, pytest, Playwright, Chromium.

[Исходное задание](https://github.com/rcsi-science/demo-roomly/blob/403f770/README.md) · [Требования в проекте](docs/assignment.md) · [Чек-лист](docs/checklist.md) · [Баг-репорты](docs/bug_reports.md)

## Запуск

Из корня проекта, с запущенным Docker Desktop и Compose v2:

```bash
docker compose run --build --rm tests
```

Локально на macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
python -m pytest
```

В PyCharm выберите `.venv/bin/python` и корень проекта как рабочую директорию. По умолчанию тесты идут на демостенд. URL можно задать через `--base-url` или `BASE_URL`. Отчёт JUnit сохраняется в `artifacts/junit.xml`, скриншоты и trace при падениях в `artifacts/browser/`.

## Автотесты и прогон

В [tests/test_booking.py](tests/test_booking.py) три сценария: подтверждение брони, отказ при превышении вместимости Малой и отказ при нулевой длительности (BUG-01, строгий `xfail`). Исходный smoke проверяет доступность страницы.


Самостоятельный прогон 25.11.2026: `pytest -v`, **3 passed, 1 xfailed in 11.59s**. Среда: macOS 26.2 (25C56), Python 3.13.9, pytest 8.3.5, Playwright 1.64.1, pytest-playwright 0.7.1, Chromium 156.0.8078.4.

Ручная проверка и браузерный прогон Playwright разделены в [чек-листе](docs/checklist.md). Версия браузера ручного прогона не зафиксирована.

Общее время выполнения: 45 минут.

Локальный запуск проверен на Linux с отдельным Chromium из-за ограничения доступа к CDN Playwright. В этой среде Docker отсутствует. Docker отдельно не проверял.

## Использование ИИ

### Использование ИИ

Codex использовал в качестве вспомогательного инструмента при подготовке автотестов, ревью кода, уточнении технических решений и редактировании документации. Ручное тестирование, воспроизведение дефектов и финальный прогон автотестов выполнил самостоятельно.

Самостоятельно проверил форму, граничные значения и обязательные поля, воспроизвёл BUG-01, BUG-02 и BUG-05, запустил автотесты на macOS. Для BUG-03 и BUG-04 наблюдал некорректное поведение, но изолированный ручной повтор отдельно не подтверждён.
