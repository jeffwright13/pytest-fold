import pytest
from faker import Faker


def divide_numbers(numerator, denominator):
    return numerator / denominator


def test_print_to_stdout():
    print("Printing to stdout!")


def test_random_sentences():
    fake = Faker()
    s1 = fake.paragraph(5)
    s2 = fake.paragraph(5)
    assert s1 == s2


def test_1():
    assert 1 == 1


def test_2():
    assert 0 == 0


def test_3():
    assert -1 == -1


def test_4():
    assert 0 == 1


def test_random_passwords():
    fake = Faker()
    s1 = fake.password(50)
    s2 = fake.password(30)
    assert s1 == s2


def test_5():
    assert abs(-1) == 1


def test_6():
    assert 0 != 0


def test_7():
    assert "a" in "abc"


def test_ok():
    pass


def test_words_fail():
    fruits1 = ["banana", "apple", "grapes", "melon", "kiwi"]
    fruits2 = ["banana", "apple", "orange", "melon", "kiwi"]
    assert fruits1 == fruits2


def test_numbers_fail():
    number_to_text1 = {str(x): x for x in range(5)}
    number_to_text2 = {str(x * 10): x * 10 for x in range(5)}
    assert number_to_text1 == number_to_text2


def test_long_text_fail():
    long_text = "Lorem ipsum dolor sit amet " * 10
    assert "hello world" in long_text


def test_11():
    assert 1 == 1


def test_12():
    assert 0 == 0


def test_13():
    assert -1 == -1


def test_14():
    assert 0 == 1


def test_15():
    assert abs(-1) == 1


def test_16():
    assert 0 != 0


def test_17():
    assert "a" not in "abc"


@pytest.mark.parametrize(
    "numerator, denominator, expected",
    [
        (1, 1, 1),
        (2, 2, 1),
        (3, 3, 1),
        (-1, -1, 1),
        (1, 1, 100),  # <= FAIL
        (-2, -2, 1),
        (1, 2, 0.5),
    ],
)
def test_paramtrized_divide(numerator, denominator, expected):
    assert divide_numbers(numerator, denominator) == expected


def test_raise_div_by_zero_error():
    with pytest.raises(ZeroDivisionError):
        divide_numbers(1, 0)
    with pytest.raises(ZeroDivisionError):
        divide_numbers(1, 1)


def test_21():
    assert 1 == 1


def test_22():
    assert 0 == 0


def test_23():
    assert -1 == -1


def test_24():
    assert 0 == 1


def test_25():
    assert abs(-1) == 1


def test_26():
    assert 0 != 0


def test_27():
    assert "a" in "abc"
