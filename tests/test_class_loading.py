from unittest.mock import patch

from pytest_nuts.index import ModuleIndex
from tests.helpers.shared import YAML_EXTENSION


def test_load_class_and_execute_tests(testdir):
    arguments = {
        "test_class_loading": """
            ---
            - test_module: tests.base_tests.class_loading
              test_class: TestClass
              test_data: []
            """
    }
    testdir.makefile(YAML_EXTENSION, **arguments)

    result = testdir.runpytest()
    result.assert_outcomes(passed=2)


def test_load_class_multiple_times(testdir):
    arguments = {
        "test_class_loading": """
            ---
            - test_module: tests.base_tests.class_loading
              test_class: TestClass
              test_data: []
            - test_module: tests.base_tests.class_loading
              test_class: TestClass
              test_data: []
            """
    }
    testdir.makefile(YAML_EXTENSION, **arguments)

    result = testdir.runpytest()
    result.assert_outcomes(passed=4)


def test_injects_arguments_as_fixture(testdir):
    arguments = {
        "test_class_loading": """
            ---
            - test_module: tests.base_tests.class_loading
              test_class: TestFixture
              test_data: ['test1', 'test2']
            """
    }
    testdir.makefile(YAML_EXTENSION, **arguments)

    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_load_class_from_index(testdir):
    with patch("pytest_nuts.yaml_to_test.ModuleIndex") as module_index:
        module_index.return_value = ModuleIndex({"TestFixture": "tests.base_tests.class_loading"})
        arguments = {
            "test_class_loading": """
                ---
                - test_class: TestFixture
                  test_data: ['test1', 'test2']
                """
        }
        testdir.makefile(YAML_EXTENSION, **arguments)

        result = testdir.runpytest()
        result.assert_outcomes(passed=1)


def test_class_with_empty_test_execution_field(testdir):
    arguments = {
        "test_class_loading": """
            ---
            - test_module: tests.base_tests.class_loading
              test_class: TestTestExecutionParamsEmpty
              test_execution:
              test_data: ['test3', 'test4']
            """
    }
    testdir.makefile(YAML_EXTENSION, **arguments)

    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_class_with_test_execution_field(testdir):
    arguments = {
        "test_class_loading": """
            ---
            - test_module: tests.base_tests.class_loading
              test_class: TestTestExecutionParamsExist
              test_execution:
                count: 42
                ref: 23
              test_data: ['test3', 'test4']
            """
    }
    testdir.makefile(YAML_EXTENSION, **arguments)

    result = testdir.runpytest()
    result.assert_outcomes(passed=1)
