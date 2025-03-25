import inspect


def generate_fixtures(*descriptions: tuple):
    # Get the caller's global namespace
    caller_frame = inspect.currentframe().f_back  # type: ignore
    caller_globals = caller_frame.f_globals  # type: ignore

    exec("import pytest", caller_globals)
    exec("import unittest.mock as mock", caller_globals)

    fixture_functions = []
    for description in descriptions:
        fixture_code = (
            f"@pytest.fixture\n"
            f"def {description[1]}():\n"
            f"    with mock.patch(\n"
            f'        "{description[0]}"\n'
            f"    ) as {description[1]}:\n"
            f"        yield {description[1]}\n"
        )
        fixture_functions.append(fixture_code)

    # Execute each function in the caller's global namespace
    for fixture_function in fixture_functions:
        exec(fixture_function, caller_globals)
