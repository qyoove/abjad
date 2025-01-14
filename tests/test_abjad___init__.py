import abjad
import enum
import inspect
import pytest


ignored_classes = (
    abjad.FormatSpecification,
    abjad.Path,
    abjad.StorageFormatManager,
    abjad.Tags,
)

classes = pytest.helpers.list_all_abjad_classes(
    ignored_classes=ignored_classes
)


@pytest.mark.parametrize("class_", classes)
def test_abjad___init___01(class_):
    """
    All concrete classes initialize from empty input.
    """
    if inspect.isabstract(class_):
        return
    if getattr(class_, "_is_abstract", None) is True:
        return
    instance = class_()
    assert instance is not None


valid_types = (
    bool,
    enum.Enum,
    abjad.Duration,
    float,
    int,
    abjad.mathtools.Infinity,
    abjad.mathtools.NegativeInfinity,
    str,
    tuple,
    type(None),
)

# TODO: port inspect.getargspec() to inspect.getfullargspec() for annotations
# @pytest.mark.parametrize('class_', classes)
# def test_abjad___init___02(class_):
#    r'''Make sure class initializer keyword argument values are immutable.
#    '''
#    if inspect.isabstract(class_):
#        return
#    if getattr(class_, '_is_abstract', None) is True:
#        return
#    object_ = class_()
#    initializer = object_.__init__
#    if not inspect.ismethod(initializer):
#        return
#    argument_specification = inspect.getargspec(initializer)
#    if argument_specification.keywords is None:
#        return
#    keyword_argument_names = argument_specification.args[1:]
#    keyword_argument_values = argument_specification.defaults or []
#    assert len(keyword_argument_names) == len(keyword_argument_values)
#    pairs = zip(keyword_argument_names, keyword_argument_values)
#    for name, value in pairs:
#        if value is NotImplemented:
#            continue
#        assert isinstance(value, valid_types), (name, value)
#        if isinstance(value, tuple):
#            assert all(isinstance(_, valid_types) for _ in value)
#
#
# functions = pytest.helpers.list_all_abjad_functions()
# if functions:
#    @pytest.mark.parametrize('function', functions)
#    def test_abjad___init___03(function):
#        r'''Function keyword argments are immutable.
#
#        Abjad no longer contains public function.s
#        '''
#        if isinstance(function, functools.partial):
#            function = function.function
#        argument_specification = inspect.getargspec(function)
#        keyword_argument_names = argument_specification.args[1:]
#        keyword_argument_values = argument_specification.defaults
#        if keyword_argument_values is None:
#            return
#        for name, value in zip(
#            keyword_argument_names, keyword_argument_values):
#            assert isinstance(value, valid_types), (name, value)
#            if isinstance(value, tuple):
#                assert all(isinstance(x, valid_types) for x in value)
