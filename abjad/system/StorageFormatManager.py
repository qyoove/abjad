import collections
import importlib
import inspect
import types
from .FormatSpecification import FormatSpecification

# from abjad.utilities.OrderedDict import OrderedDict


class StorageFormatManager(object):
    """
    Manages Abjad object storage formats.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Storage formatting"

    __slots__ = (
        "_client",
        "_format_specification",
        "_signature_accepts_args",
        "_signature_accepts_kwargs",
        "_signature_keyword_names",
        "_signature_positional_names",
    )

    _exclude_tools_package = (
        "core",
        "indicators",
        "markup",
        "mathtools",
        "meter",
        "pitch",
        "scheme",
        "timespans",
        "utilities",
    )

    _unindented_whitespace = "", "", ", "

    _indented_whitespace = "    ", "\n", ",\n"

    ### INITIALIZER ###

    def __init__(self, client=None):
        self._client = client
        self._format_specification = None
        (
            self._signature_positional_names,
            self._signature_keyword_names,
            self._signature_accepts_args,
            self._signature_accepts_kwargs,
        ) = self.inspect_signature(self._client)

    ### PRIVATE METHODS ###

    def _dispatch_formatting(self, as_storage_format=True, is_indented=True):
        from abjad.utilities.OrderedDict import OrderedDict

        if isinstance(self._client, types.MethodType):
            return self._format_method()
        elif isinstance(self._client, type):
            return self._format_class(as_storage_format, is_indented)
        elif as_storage_format and (
            hasattr(self._client, "_get_storage_format_specification")
            or hasattr(self._client, "_get_format_specification")
        ):
            pieces = self._format_specced_object(
                as_storage_format=as_storage_format
            )
            return list(pieces)
        elif not as_storage_format and hasattr(
            self._client, "_get_format_specification"
        ):
            pieces = self._format_specced_object(
                as_storage_format=as_storage_format
            )
            return list(pieces)
        elif isinstance(self._client, (list, tuple)):
            return self._format_sequence(as_storage_format, is_indented)
        elif isinstance(self._client, (OrderedDict, collections.OrderedDict)):
            return self._format_ordered_mapping(as_storage_format, is_indented)
        elif isinstance(self._client, dict):
            return self._format_mapping(as_storage_format, is_indented)
        elif isinstance(self._client, float):
            return repr(round(self._client, 15)).split("\n")
        return repr(self._client).split("\n")

    def _format_class(self, as_storage_format, is_indented):
        if as_storage_format:
            root_package_name = self.get_root_package_name()
            root_package = importlib.import_module(root_package_name)
            parts = [root_package_name]
            if self._client.__name__ not in dir(root_package):
                tools_package_name = self.get_tools_package_name()
                parts.append(tools_package_name)
            parts.append(self._client.__name__)
            result = ".".join(parts)
        else:
            result = self._client.__name__
        return [result]

    def _format_mapping(self, as_storage_format, is_indented):
        result = []
        prefix, infix, suffix = self._get_whitespace(is_indented)
        result.append("{" + infix)
        for key, value in sorted(self._client.items()):
            key_agent = type(self)(key)
            key_pieces = key_agent._dispatch_formatting(
                as_storage_format=as_storage_format, is_indented=is_indented
            )
            value_agent = type(self)(value)
            value_pieces = value_agent._dispatch_formatting(
                as_storage_format=as_storage_format, is_indented=is_indented
            )
            for line in key_pieces[:-1]:
                result.append(prefix + line)
            result.append(
                "{}{}: {}".format(prefix, key_pieces[-1], value_pieces[0])
            )
            for line in value_pieces[1:]:
                result.append(prefix + line)
            result[-1] = result[-1] + suffix
        if not is_indented:
            result[-1] = result[-1].rstrip(suffix) + infix
        result.append(prefix + "}")
        return result

    def _format_method(self, as_storage_format, is_indented):
        return []

    def _format_ordered_mapping(self, as_storage_format, is_indented):
        result = []
        prefix, infix, suffix = self._get_whitespace(is_indented)
        result.append("[" + infix)
        for item in list(self._client.items()):
            item_agent = type(self)(item)
            item_pieces = item_agent._dispatch_formatting(
                as_storage_format=as_storage_format, is_indented=is_indented
            )
            for line in item_pieces:
                result.append(prefix + line)
            result[-1] = result[-1] + suffix
        if not is_indented:
            result[-1] = result[-1].rstrip(suffix) + infix
        result.append(prefix + "]")
        return result

    def _format_sequence(self, as_storage_format, is_indented):
        result = []
        prefix, infix, suffix = self._get_whitespace(is_indented)
        # just return the repr, if all contents are builtin types
        prototype = (bool, int, float, str, type(None))
        if all(isinstance(x, prototype) for x in self._client):
            piece = repr(self._client)
            if len(piece) < 50:
                return [repr(self._client)]
        if isinstance(self._client, list):
            braces = "[", "]"
        else:
            braces = "(", ")"
        result.append(braces[0] + infix)
        for x in self._client:
            agent = type(self)(x)
            pieces = agent._dispatch_formatting(
                as_storage_format=as_storage_format, is_indented=is_indented
            )
            for line in pieces[:-1]:
                result.append(prefix + line)
            result.append(prefix + pieces[-1] + suffix)
        if not is_indented:
            if isinstance(self._client, list) or 1 < len(self._client):
                result[-1] = result[-1].rstrip(suffix)
            else:
                result[-1] = result[-1].rstrip()
        result.append(prefix + braces[1])
        return result

    def _format_specced_object(self, as_storage_format=True):
        if hasattr(self._client, "_get_format_specification"):
            specification = self._client._get_format_specification()
            if specification.storage_format_forced_override is not None:
                return [specification.storage_format_forced_override]
        formatting_keywords = self._get_formatting_keywords(as_storage_format)
        args_values = formatting_keywords["args_values"]
        as_storage_format = formatting_keywords["as_storage_format"]
        is_bracketed = formatting_keywords["is_bracketed"]
        is_indented = formatting_keywords["is_indented"]
        kwargs_names = formatting_keywords["kwargs_names"]
        text = formatting_keywords["text"]
        result = []
        if is_bracketed:
            result.append("<")
        if text is not None:
            result.append(text)
        else:
            prefix, infix, suffix = self._get_whitespace(is_indented)
            class_name_prefix = self.get_class_name_prefix(as_storage_format)
            positional_argument_pieces = []
            for value in args_values:
                agent = type(self)(value)
                pieces = agent._dispatch_formatting(
                    as_storage_format=as_storage_format,
                    is_indented=is_indented,
                )
                for piece in pieces[:-1]:
                    positional_argument_pieces.append(prefix + piece)
                positional_argument_pieces.append(prefix + pieces[-1] + suffix)
            keyword_argument_pieces = []
            for name in kwargs_names:
                value = self._get(name)
                if value is None or isinstance(value, types.MethodType):
                    continue
                agent = type(self)(value)
                pieces = agent._dispatch_formatting(
                    as_storage_format=as_storage_format,
                    is_indented=is_indented,
                )
                pieces[0] = "{}={}".format(name, pieces[0])
                for piece in pieces[:-1]:
                    keyword_argument_pieces.append(prefix + piece)
                keyword_argument_pieces.append(prefix + pieces[-1] + suffix)
            if not positional_argument_pieces and not keyword_argument_pieces:
                result.append("{}()".format(class_name_prefix))
            else:
                result.append("{}({}".format(class_name_prefix, infix))
                result.extend(positional_argument_pieces)
                if positional_argument_pieces and not keyword_argument_pieces:
                    result[-1] = result[-1].rstrip(suffix) + infix
                else:
                    result.extend(keyword_argument_pieces)
                if not as_storage_format:
                    result[-1] = result[-1].rstrip(suffix) + infix
                if is_indented:
                    result.append("{})".format(prefix))
                else:
                    result.append(")")
        if is_bracketed:
            result.append(">")
        if not is_indented:
            return ["".join(result)]
        return result

    def _get(self, name):
        value = None
        try:
            value = getattr(self._client, name, None)
            if value is None:
                value = getattr(self._client, "_" + name, None)
            if value is None:
                value = getattr(self._client, "_" + name.rstrip("_"), None)
        except AttributeError:
            try:
                value = self._client[name]
            except (TypeError, KeyError):
                value = None
        return value

    def _get_formatting_keywords(self, as_storage_format=True):
        # NOTE: This acts to abstract-away our competing spec-specs.
        #       It can probably be removed/reduced in the near future.
        if as_storage_format:
            spec = None
            if hasattr(self._client, "_get_storage_format_specification"):
                spec = self._client._get_storage_format_specification()
            if spec:
                # print('STORAGE', type(self._client), getattr(self._client, 'name', None))
                via = "_get_storage_format_specification()"
                args_values = spec.positional_argument_values
                is_bracketed = False
                is_indented = spec.is_indented
                kwargs_names = spec.keyword_argument_names
                text = spec.storage_format_text
            else:
                spec = self.format_specification
                via = "_get_format_specification()"
                args_values = spec.storage_format_args_values
                is_bracketed = spec.storage_format_is_bracketed
                is_indented = spec.storage_format_is_indented
                kwargs_names = spec.storage_format_kwargs_names
                text = spec.storage_format_text
        else:
            spec = self.format_specification
            via = "_get_format_specification()"
            args_values = spec.repr_args_values
            if args_values is None:
                args_values = spec.storage_format_args_values
            is_bracketed = spec.repr_is_bracketed
            is_indented = spec.repr_is_indented
            kwargs_names = spec.repr_kwargs_names
            if kwargs_names is None:
                kwargs_names = spec.storage_format_kwargs_names
            text = spec.repr_text
            if text is None:
                text = spec.storage_format_text
        if kwargs_names is None:
            kwargs_names = self.signature_keyword_names
        if args_values is None:
            args_values = tuple(
                self._get(_) for _ in self.signature_positional_names
            )
        if args_values:
            kwargs_names = list(kwargs_names)
            names = self.signature_positional_names
            if not self.signature_accepts_args:
                names += self.signature_keyword_names
            names = names[: len(args_values)]
            for name in names:
                if name in kwargs_names:
                    kwargs_names.remove(name)
            kwargs_names = tuple(kwargs_names)
        return dict(
            args_values=args_values,
            as_storage_format=as_storage_format,
            is_bracketed=is_bracketed,
            is_indented=is_indented,
            kwargs_names=kwargs_names,
            text=text,
            via=via,
        )

    @staticmethod
    def _get_module_path_parts(subject):
        if isinstance(subject, type):
            class_ = subject
        elif type(subject) is subject.__class__:
            class_ = type(subject)
        class_name = class_.__name__
        parts = class_.__module__.split(".")
        while parts and parts[-1] == class_name:
            parts.pop()
        parts.append(class_name)
        return parts

    def _get_whitespace(self, is_indented):
        if is_indented:
            return self._indented_whitespace
        return self._unindented_whitespace

    @staticmethod
    def _make_hashable(value):
        if isinstance(value, dict):
            value = tuple(value.items())
        elif isinstance(value, list):
            value = tuple(value)
        elif isinstance(value, (set, frozenset)):
            value = tuple(value)
        return value

    def _map_positional_values_to_names(self, values):
        names = self.signature_positional_names
        if not self.signature_accepts_args:
            names += self.signature_keyword_names
        names = names[: len(values)]
        return names

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        return self._client

    @property
    def format_specification(self):
        if self._format_specification is None:
            if not isinstance(self._client, type) and hasattr(
                self._client, "_get_format_specification"
            ):
                self._format_specification = (
                    self._client._get_format_specification()
                )
            else:
                self._format_specification = FormatSpecification(self._client)
        return self._format_specification

    @property
    def signature_accepts_args(self):
        return self._signature_accepts_args

    @property
    def signature_accepts_kwargs(self):
        return self._signature_accepts_kwargs

    @property
    def signature_keyword_names(self):
        return self._signature_keyword_names

    @property
    def signature_names(self):
        return self.signature_positional_names + self.signature_keyword_names

    @property
    def signature_positional_names(self):
        return self._signature_positional_names

    ### PUBLIC METHODS ###

    @staticmethod
    def compare_objects(object_one, object_two) -> bool:
        """
        Compares ``object_one`` to ``object_two``.
        """
        manager_one = StorageFormatManager(object_one)
        if manager_one.format_specification.coerce_for_equality:
            try:
                object_two = type(object_one)(object_two)
            except (TypeError, ValueError):
                return False
        elif not isinstance(object_two, type(object_one)):
            return False
        manager_two = StorageFormatManager(object_two)
        template_1 = manager_one.get_template_dict()
        template_2 = manager_two.get_template_dict()
        return template_1 == template_2

    def get_class_name_prefix(
        self, as_storage_format, include_root_package=None
    ) -> str:
        """
        Gets class name prefix.
        """
        manager = StorageFormatManager(self._client)
        if not isinstance(self._client, type):
            class_name = type(self._client).__name__
        else:
            class_name = self._client.__name__
        if as_storage_format:
            root_package_name = self.get_root_package_name()
            root_package = importlib.import_module(root_package_name)
            parts = [root_package_name]
            if class_name not in dir(root_package):
                tools_package_name = manager.get_tools_package_name()
                parts.append(tools_package_name)
            parts.append(class_name)
            return ".".join(parts)
        return class_name

    def get_hash_values(self):
        """
        Gets hash values.
        """
        values = []
        if isinstance(self._client, type):
            values.append(self._client)
        else:
            values.append(type(self._client))
        template_items = sorted(self.get_template_dict().items())
        values.extend(self._make_hashable(v) for k, v in template_items)
        return tuple(values)

    def get_repr_format(self):
        """
        Gets repr format.
        """
        pieces = self._format_specced_object(as_storage_format=False)
        return "".join(pieces)

    def get_repr_keyword_dict(self):
        """
        Gets repr keyword dictionary.
        """
        from .StorageFormatSpecification import StorageFormatSpecification

        names = self.specification.repr_kwargs_names
        if names is None:
            specification = StorageFormatSpecification(self.client)
            names = specification.keyword_argument_names or ()
        keyword_dict = {}
        for name in names:
            keyword_dict[name] = self._get(name)
        return keyword_dict

    def get_repr_positional_values(self):
        """
        Gets repr positional values.
        """
        from .StorageFormatSpecification import StorageFormatSpecification

        values = self.specification.repr_args_values
        if values is None:
            specification = StorageFormatSpecification(self.client)
            values = specification.positional_argument_values or ()
        return tuple(values)

    def get_root_package_name(self) -> str:
        """
        Gets root package name.
        """
        return self._get_module_path_parts(self._client)[0]

    def get_storage_format(self) -> str:
        """
        Gets storage format.
        """
        pieces = self._format_specced_object(as_storage_format=True)
        result = "".join(pieces)
        return result

    def get_storage_format_keyword_dict(self):
        """
        Gets storage format keyword dictionary.
        """
        from .StorageFormatSpecification import StorageFormatSpecification

        names = self.specification.storage_format_kwargs_names
        if names is None:
            if hasattr(self.client, "_get_storage_format_specification"):
                specification = self.client._get_storage_format_specification()
            else:
                specification = StorageFormatSpecification(self.client)
            names = specification.keyword_argument_names or ()
        keyword_dict = {}
        for name in names:
            keyword_dict[name] = self._get(name)
        return keyword_dict

    def get_storage_format_positional_values(self):
        """
        Gets storage format positional values.
        """
        from .StorageFormatSpecification import StorageFormatSpecification

        values = self.specification.storage_format_args_values
        if values is None:
            if hasattr(self.client, "_get_storage_format_specification"):
                specification = self.client._get_storage_format_specification()
            else:
                specification = StorageFormatSpecification(self.client)
            values = specification.positional_argument_values or ()
        return tuple(values)

    def get_template_dict(self):
        """
        Gets template dictionary.
        """
        template_names = self.format_specification.template_names
        if template_names is None:
            template_names = self.signature_names
            # TODO: This will be factored out when SFS/SFM are removed.
            if hasattr(self.client, "_get_storage_format_specification"):
                specification = self.client._get_storage_format_specification()
                template_names.extend(
                    specification._keyword_argument_names or ()
                )
            else:
                template_names.extend(
                    self.format_specification.storage_format_kwargs_names or ()
                )
            template_names = sorted(set(template_names))
        template_dict = collections.OrderedDict()
        for name in template_names:
            template_dict[name] = self._get(name)
        return template_dict

    def get_tools_package_name(self):
        """
        Gets tools package name.
        """
        parts = self._get_module_path_parts(self._client)
        if parts[0] in ("abjad", "abjadext", "ide"):
            for part in reversed(parts):
                if part == parts[-1]:
                    continue
                return part
        return ".".join(parts[:-1])

    @classmethod
    def inspect_signature(class_, subject):
        """
        Inspects signature of ``subject``.
        """
        positional_names = []
        keyword_names = []
        accepts_args = False
        accepts_kwargs = False
        if not isinstance(subject, type):
            subject = type(subject)
        try:
            signature = inspect.signature(subject)
        except ValueError:
            return (
                positional_names,
                keyword_names,
                accepts_args,
                accepts_kwargs,
            )
        for name, parameter in signature.parameters.items():
            if parameter.kind == inspect._POSITIONAL_OR_KEYWORD:
                if parameter.default == parameter.empty:
                    positional_names.append(name)
                else:
                    keyword_names.append(name)
            # Python 3 allow keyword only parameters:
            elif (
                hasattr(inspect, "_KEYWORD_ONLY")
                and parameter.kind == inspect._KEYWORD_ONLY
            ):
                keyword_names.append(name)
            elif parameter.kind == inspect._VAR_POSITIONAL:
                accepts_args = True
            elif parameter.kind == inspect._VAR_KEYWORD:
                accepts_kwargs = True
        return (positional_names, keyword_names, accepts_args, accepts_kwargs)
