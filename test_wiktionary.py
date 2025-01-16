from json import loads

import pytest
from click.testing import CliRunner
from wiktionary import cli


@pytest.mark.parametrize(
    ("word", "found"),
    [
        # Слово в не нормализированной форме. Страница поиска выдаёт
        # множество результатов. На страничке wiki есть таблица со
        # всеми формами слова.
        pytest.param("мудаков", True, id="0"),
        # Слово в нормальной форме. Страница поиска сразу же
        # переадресует на страничку с wiki.
        pytest.param("ёбаная", True, id="1"),
        # У слова есть собственная страничка wiki, что подтверждает
        # его корректность. Но на данной странице отсутствует страница
        # с формами слова.
        pytest.param("бля", True, id="2"),
        pytest.param("Бля", True, id="3"),
        # У слова есть страничка wiki на которой есть таблица с
        # формами слова. Но в таблице форм не совпадает регистр
        # написания слова с вариантом использованным в тексте.
        pytest.param("Ачивка", True, id="4"),
        # У слова есть собственная страничка wiki, на которой
        # отсутствует таблица с формами слова. Регистр написания слова
        # в адресной строке не совпадает с вариантом использованным в
        # тексте.
        pytest.param("Korn", True, id="5"),
        # У слова есть своя собственная страничка wiki, но она не
        # является первой в результатах поиска.
        pytest.param("Ебанёт", True, id="6"),
        # У слова есть своя собственная страничка wiki, но в таблице
        # форм слова используется многострочное написание с
        # применением html тега <br>.
        pytest.param("Жопой", True, id="7"),
        # У слова в таблице форм есть несколько знаков ударения.
        pytest.param("сельхозярмарки", True, id="8"),
        # У слова есть дополнительный разделитель в виде // в таблице
        # форм слова.
        pytest.param("хуем", True, id="9"),
        # Слово не найдено.
        pytest.param("БКРР", False, id="10"),
    ],
)
def test_cli_ok(word: str, found: bool) -> None:
    runner = CliRunner()
    result = runner.invoke(cli, [word])
    assert result.exit_code == 0
    assert loads(result.output) == {word: found}