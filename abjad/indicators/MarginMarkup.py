import typing
from abjad.markups import Markup
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.top.new import new


class MarginMarkup(object):
    r"""
    Margin markup.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> margin_markup = abjad.MarginMarkup(
        ...     markup=abjad.Markup('Vc.'),
        ...     )
        >>> abjad.attach(margin_markup, staff[0])
        >>> abjad.show(staff, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \set Staff.shortInstrumentName =
                \markup { Vc. }
                c'4
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Set markup to externally defined command string like this:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> margin_markup = abjad.MarginMarkup(
        ...     markup=r'\my_custom_instrument_name',
        ...     )
        >>> abjad.attach(margin_markup, staff[0])

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \set Staff.shortInstrumentName = \my_custom_instrument_name
                c'4
                d'4
                e'4
                f'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_context", "_format_slot", "_markup")

    _latent = True

    _persistent = True

    _publish_storage_format = True

    _redraw = True

    ### INITIALIZER ##

    def __init__(
        self,
        *,
        context: str = "Staff",
        format_slot: str = "before",
        markup: typing.Union[str, Markup] = None,
    ) -> None:
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context = context
        if format_slot is not None:
            assert isinstance(format_slot, str), repr(format_slot)
        self._format_slot = format_slot
        if markup is not None:
            assert isinstance(markup, (str, Markup)), repr(markup)
        self._markup = markup

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is margin markup with context and markup
        equal to those of this margin markup.

        ..  container:: example

            >>> margin_markup_1 = abjad.MarginMarkup(
            ...     context='PianoStaff',
            ...     markup=abjad.Markup('Hp.'),
            ...     )
            >>> margin_markup_2 = abjad.MarginMarkup(
            ...     context='PianoStaff',
            ...     markup=abjad.Markup('Hp.'),
            ...     )
            >>> margin_markup_3 = abjad.MarginMarkup(
            ...     context='Staff',
            ...     markup=abjad.Markup('Hp.'),
            ...     )

            >>> margin_markup_1 == margin_markup_1
            True
            >>> margin_markup_1 == margin_markup_2
            True
            >>> margin_markup_1 == margin_markup_3
            False

            >>> margin_markup_2 == margin_markup_1
            True
            >>> margin_markup_2 == margin_markup_2
            True
            >>> margin_markup_2 == margin_markup_3
            False

            >>> margin_markup_3 == margin_markup_1
            False
            >>> margin_markup_3 == margin_markup_2
            False
            >>> margin_markup_3 == margin_markup_3
            True

        """
        if not isinstance(argument, type(self)):
            return False
        if self.context == argument.context and self.markup == argument.markup:
            return True
        return False

    def __hash__(self) -> int:
        r"""
        Hashes margin markup.

        Redefined in tandem with __eq__.

        ..  container:: example

            >>> margin_markup = abjad.MarginMarkup(
            ...     context='PianoStaff',
            ...     markup=abjad.Markup('Hp.'),
            ...     )

            >>> hash_ = hash(margin_markup)
            >>> isinstance(hash_, int)
            True

        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_type(self):
        if isinstance(self.context, type):
            return self.context.__name__
        elif isinstance(self.context, str):
            return self.context
        else:
            return type(self.context).__name__

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self, context=None):
        result = []
        if isinstance(context, str):
            pass
        elif context is not None:
            context = context.lilypond_type
        else:
            context = self._lilypond_type
        if isinstance(self.markup, Markup):
            markup = self.markup
            if markup.direction is not None:
                markup = new(markup, direction=None)
            pieces = markup._get_format_pieces()
            result.append(rf"\set {context!s}.shortInstrumentName =")
            result.extend(pieces)
        else:
            assert isinstance(self.markup, str)
            string = rf"\set {context!s}.shortInstrumentName = {self.markup}"
            result.append(string)
        return result

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        slot = bundle.get(self.format_slot)
        slot.commands.extend(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> str:
        """
        Gets default context of margin markup.

        ..  container:: example

            >>> abjad.MarginMarkup().context
            'Staff'

        """
        return self._context

    @property
    def format_slot(self) -> str:
        """
        Gets format slot.

        ..  container:: example

            >>> abjad.MarginMarkup().format_slot
            'before'

        """
        return self._format_slot

    @property
    def latent(self) -> bool:
        """Is true.

        ..  container::

            >>> margin_markup = abjad.MarginMarkup(
            ...     markup=abjad.Markup('Vc.'),
            ...     )
            >>> margin_markup.latent
            True

        Class constant.
        """
        return self._latent

    @property
    def markup(self) -> typing.Optional[typing.Union[str, Markup]]:
        """
        Gets (instrument name) markup.
        """
        return self._markup

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> margin_markup = abjad.MarginMarkup(
            ...     markup=abjad.Markup('Vc.'),
            ...     )
            >>> margin_markup.persistent
            True

        Class constant.
        """
        return self._persistent

    @property
    def redraw(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> margin_markup = abjad.MarginMarkup(
            ...     markup=abjad.Markup('Vc.'),
            ...     )
            >>> margin_markup.redraw
            True

        Class constant.
        """
        return self._redraw

    @property
    def tweaks(self) -> None:
        r"""
        Are not implemented on margin markup.
        
        The LilyPond ``\shortInstrumentName`` command refuses tweaks.

        Craft explicit markup instead.
        """
        pass
