import pytest

from src.domain import CustomerHasDebt, Order


def test_confirm_normal_order():
    order = Order(total=100)

    result = order.confirm()

    assert result == 100
    assert order.status == "CONFIRMED"
    assert order.discount == 0.0


def test_confirm_vip_order():
    order = Order(total=100, vip=True)

    result = order.confirm()

    assert result == 85
    assert order.discount == 15.0
    assert order.status == "CONFIRMED"


def test_reject_negative_total():
    order = Order(total=-10)

    with pytest.raises(ValueError):
        order.confirm()


def test_reject_order_with_debt():
    order = Order(total=100)

    with pytest.raises(CustomerHasDebt):
        order.confirm(customer_debt=50)


def test_accept_small_vip_order():
    order = Order(total=0.001, vip=True)

    result = order.confirm()

    assert result == 0.001
    assert order.discount == 0.0
    assert order.status == "CONFIRMED"