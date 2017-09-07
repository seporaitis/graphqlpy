__version__ = '0.0.1'


def params(value):
    if isinstance(value, dict):
        return "{" + ", ".join(["{}: {}".format(k, params(v)) for k, v in sorted(value.items())]) + "}"
    elif isinstance(value, list):
        return "[" + ", ".join(["{}".format(params(v)) for v in value]) + "]"
    elif isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, int):
        return str(value)
    elif isinstance(value, str):
        return '"{}"'.format(value)

    raise TypeError("Type '{}' is not supported.".format(type(value).__name__))


def field(*args, **kwargs):
    """Render a field signature.

    >>> field("someName", paramOne=1, paramTwo=2)
    'someName(paramOne: 1, paramTwo: 2)'

    >>> field("alias", "someName", paramOne=1, paramTwo=2)
    'alias: someName(paramOne: 1, paramTwo: 2)'
    """

    alias = None
    name = None
    if len(args) == 1:
        name = args[0]
    elif len(args) == 2:
        alias, name = args
    else:
        raise ValueError("Field name or alias and name must be provided to 'field', got '{}'".format(args))

    result = ""
    if alias:
        result = "{}: ".format(alias)

    if not kwargs:
        return result + name

    result += "{}({})".format(
        name,
        ", ".join(["{}: {}".format(k, params(v)) for k, v in sorted(kwargs.items())])
    )

    return result


def component(*args):
    args = tuple(args)

    results = []
    for arg in args:
        if isinstance(arg, str):
            results.append(arg)
        elif isinstance(arg, dict):
            for k, v in sorted(arg.items()):
                results.append(k)
                results.append("{")
                if isinstance(v, str):
                    results.append(component(v))
                else:
                    results.append(component(*v))
                results.append("}")
        elif isinstance(arg, tuple):
            for v in arg:
                results.append(component(v))

    results = " ".join(results)

    return results


def query(*args):
    return "query {{ {} }}".format(component(*args))


def mutation(*args, alias=None):
    if alias:
        return "{}: mutation {{ {} }}".format(alias, component(*args))

    return "mutation {{ {} }}".format(component(*args))
