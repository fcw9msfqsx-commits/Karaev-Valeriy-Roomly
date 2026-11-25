import re
from datetime import datetime, timedelta, timezone

import pytest
from playwright.sync_api import Page, expect


@pytest.fixture
def booking_form(page: Page, base_url: str) -> tuple[Page, str]:
    response = page.goto(base_url, wait_until="domcontentloaded")
    assert response is not None and response.ok, "Страница бронирования недоступна"

    date = (datetime.now(timezone.utc).date() + timedelta(days=2)).isoformat()
    page.get_by_label("Переговорная").select_option("small")
    page.get_by_label("Дата").fill(date)
    page.get_by_label("Начало").fill("10:00")
    page.get_by_label("Окончание").fill("11:00")
    page.get_by_label("Участники").fill("4")
    page.get_by_label("Ваше имя").fill("Анна Иванова")
    page.get_by_label("Рабочая почта").fill("anna@example.com")
    return page, date


def test_successful_booking(booking_form: tuple[Page, str]) -> None:
    page, date = booking_form
    page.get_by_role("button", name="Забронировать").click()

    expect(page.get_by_role("status")).to_have_text(
        re.compile(rf"^Бронирование создано\.\s*Малая, {date}, 10:00–11:00 · Анна Иванова$")
    )


def test_rejects_one_participant_above_room_capacity(booking_form: tuple[Page, str]) -> None:
    page, _ = booking_form
    page.get_by_label("Участники").fill("5")
    page.get_by_role("button", name="Забронировать").click()

    expect(page.locator('[data-error-for="participants"]')).to_contain_text("максимум 4")
    expect(page.get_by_role("status")).to_have_text("Проверьте, пожалуйста, заполнение формы.")


@pytest.fixture
def zero_duration_accepted(booking_form: tuple[Page, str]) -> bool:
    page, date = booking_form
    start_time = page.get_by_label("Начало").input_value()
    page.get_by_label("Окончание").fill(start_time)
    page.get_by_role("button", name="Забронировать").click()

    confirmation = rf"Бронирование создано\.\s*Малая, {date}, {start_time}–{start_time} · Анна Иванова"
    rejection = r"Проверьте, пожалуйста, заполнение формы\."
    status = page.get_by_role("status")
    expect(status).to_have_text(re.compile(rf"^(?:{confirmation}|{rejection})$"))

    accepted = status.inner_text().startswith("Бронирование создано.")
    if not accepted:
        expect(page.locator('[data-error-for="endTime"]')).to_have_text(re.compile(r"\S"))
    return accepted


@pytest.mark.xfail(
    strict=True,
    reason="BUG-01: форма принимает бронирование с нулевой длительностью",
    raises=AssertionError,
)
def test_rejects_equal_start_and_end_times(zero_duration_accepted: bool) -> None:
    assert not zero_duration_accepted, "Форма подтвердила бронь с нулевой длительностью"
