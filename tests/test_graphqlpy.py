import pytest
from gql import gql

from graphqlpy import field, mutation, params, query


class TestParams(object):

    def test_integer(self):
        assert params(1) == "1"
        assert params(1000) == "1000"

    def test_boolean(self):
        assert params(True) == "true"
        assert params(False) == "false"

    def test_list(self):
        assert params([1, True, "str"]) == '[1, true, "str"]'

    def test_dict(self):
        actual = params({
            'int': 1,
            'str': "str",
            'bool': True,
            'list': [1, True, "str"],
            'dict': {
                'list': ["one", "two", 3],
                'int': 1,
            }
        })

        expected = (
            '{bool: true, dict: {int: 1, list: ["one", "two", 3]}, '
            'int: 1, list: [1, true, "str"], str: "str"}'
        )

        assert actual == expected

    def test_unknown(self):
        class Foo():
            pass

        with pytest.raises(TypeError) as err:
            params(Foo())

        assert str(err.value) == "Type 'Foo' is not supported."


class TestField(object):

    def test_name_only(self):
        assert field("name") == "name"

    def test_name_and_alias(self):
        assert field("alias", "name") == "alias: name"

    def test_name_and_params(self):
        assert field("name", paramOne=1) == "name(paramOne: 1)"

    def test_alias_name_and_params(self):
        assert field("alias", "name", paramOne=1) == "alias: name(paramOne: 1)"


class TestQuery(object):

    def test_string_fields(self):
        actual = query(
            {'me': (
                'id',
                'firstName',
                'lastName',
                {'birthday': (
                    'month',
                    'day',
                )},
                {'friends': (
                    'name'
                )},
            )}
        )

        gql(actual)

        expected = "query { me { id firstName lastName birthday { month day } friends { name } } }"

        assert actual == expected

    def test_custom_fields(self):
        actual = query(
            {field("user", id=4): (
                'firstName',
                'lastName',
                {'birthday': (
                    'month',
                    'day',
                )},
            )}
        )

        gql(actual)

        expected = "query { user(id: 4) { firstName lastName birthday { month day } } }"

        assert actual == expected

    def test_field_with_arguments(self):
        actual = query(
            {field("user", id=4): (
                'id',
                'name',
                field("profilePic", width=100, height=50),
            )}
        )

        gql(actual)

        expected = "query { user(id: 4) { id name profilePic(height: 50, width: 100) } }"

        assert actual == expected

    def test_field_with_alias(self):
        actual = query(
            {field("user", id=4): (
                'id',
                'name',
                field("smallPic", "profilePic", size=64),
                field("bigPic", "profilePic", size=1024),
            )}
        )

        gql(actual)

        expected = "query { user(id: 4) { id name smallPic: profilePic(size: 64) bigPic: profilePic(size: 1024) } }"

        assert actual == expected


class TestMutation(object):

    def test_mutation(self):
        actual = mutation(
            {field("user", id=4, firstName="John", lastName="Doe"): (
                "ok",
            )}
        )

        gql(actual)

        expected = 'mutation { user(firstName: "John", id: 4, lastName: "Doe") { ok } }'

        assert actual == expected

    def test_mutation_no_tuple(self):
        actual = mutation(
            {field("user", id=4, firstName="John", lastName="Doe"): (
                "ok"
            )}
        )

        gql(actual)

        expected = 'mutation { user(firstName: "John", id: 4, lastName: "Doe") { ok } }'

        assert actual == expected
