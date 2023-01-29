from db_create_new_check import is_new
from filters_func import project_name
from filters_func import poject_cat
from filters_func import summ_under
from filters_func import summ_up
import pytest


@pytest.mark.parametrize("input, correct, ans", [(0, 1, False),
                                                 (1, 0, True),
                                                 (0, 0, False),
                                                 (299, 300, False),
                                                 (-5, -4, False),
                                                 (10, 0, True),
                                                 (3, "", False)])
def test_is_new_good(input, correct, ans):
    assert is_new(input, correct) == ans


@pytest.mark.parametrize("input, ans", [("Название проекта", False),
                                        ("Название проекта Qwerty", True),
                                        ("Название проектаasdf", False),
                                        ("Название проекта Кафе у дома", True),
                                        ("yfpdfybt ghjtrnf", False),
                                        ("asdasdasd", False)])
def test_project_name_good(input, ans):
    assert project_name(input) == ans


@pytest.mark.parametrize("input, ans", [("Категория проекта", False),
                                        ("Категория проекта it", True),
                                        ("Категория проектаasdf", False),
                                        ("Категория проекта B2B", True),
                                        ("Rfntujhbz ghjtrnf it", False),
                                        ("asfgfhgfdbfe", False)])
def test_poject_cat_good(input, ans):
    assert poject_cat(input) == ans


@pytest.mark.parametrize("input, ans", [("Сумма меньше", False),
                                        ("Сумма меньше 10000", True),
                                        ("Сумма меньше1000", False),
                                        ("Сумма меньше 23552310", True),
                                        ("Cevvf vtymit", False),
                                        ("canoisbcv 12437", False)])
def test_summ_under_good(input, ans):
    assert summ_under(input) == ans


@pytest.mark.parametrize("input, ans", [("Сумма больше", False),
                                        ("Сумма больше 1000", True),
                                        ("Сумма больше24999", False),
                                        ("Сумма больше 901249", True),
                                        ("Cevvf ,jkmit", False),
                                        ("fasjpif dsani 123000", False)])
def test_summ_up_good(input, ans):
    assert summ_up(input) == ans