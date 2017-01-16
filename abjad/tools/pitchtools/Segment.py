# -*- coding: utf-8 -*-
import abc
import collections
import types
from abjad.tools import expressiontools
from abjad.tools import mathtools
from abjad.tools import systemtools
from abjad.tools.datastructuretools import TypedTuple


class Segment(TypedTuple):
    r'''Segment base class.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_frozen_expression',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        item_class=None,
        name=None,
        name_markup=None,
        ):
        from abjad.tools import datastructuretools
        prototype = (
            collections.Iterator,
            types.GeneratorType,
            )
        if isinstance(items, str):
            items = items.split()
        elif isinstance(items, prototype):
            items = [item for item in items]
        if item_class is None:
            item_class = self._named_item_class
            if items is not None:
                if (isinstance(items, datastructuretools.TypedCollection) and
                    issubclass(items.item_class, self._parent_item_class)):
                    item_class = items.item_class
                elif len(items):
                    if isinstance(items, collections.Set):
                        items = tuple(items)
                    if isinstance(items[0], str):
                        item_class = self._named_item_class
                    elif isinstance(items[0], (int, float)):
                        item_class = self._numbered_item_class
                    elif isinstance(items[0], self._parent_item_class):
                        item_class = type(items[0])
        if isinstance(item_class, str):
            import abjad
            globals_ = {'abjad': abjad}
            globals_.update(abjad.__dict__.copy())
            item_class = eval(item_class, globals_)
        assert issubclass(item_class, self._parent_item_class)
        TypedTuple.__init__(
            self,
            items=items,
            item_class=item_class,
            name=name,
            name_markup=name_markup,
            )
        self._frozen_expression = None

    ### SPECIAL METHODS ###

    def __illustrate__(
        self,
        name_markup_direction=Up,
        **keywords
        ):
        r'''Illustrates segment.

        Returns LilyPond file.
        '''
        import abjad
        notes = []
        for item in self:
            note = abjad.Note(item, abjad.Duration(1, 8))
            notes.append(note)
        expression_markup = \
            abjad.expressiontools.Expression._get_expression_markup(
            self,
            direction=name_markup_direction,
            )
        if expression_markup is not None:
            abjad.attach(expression_markup, notes[0])
        voice = abjad.Voice(notes)
        staff = abjad.Staff([voice])
        score = abjad.Score([staff])
        score.add_final_bar_line()
        abjad.override(score).bar_line.transparent = True
        abjad.override(score).bar_number.stencil = False
        abjad.override(score).beam.stencil = False
        abjad.override(score).flag.stencil = False
        abjad.override(score).stem.stencil = False
        abjad.override(score).time_signature.stencil = False
        string = 'override Score.BarLine.transparent = ##f'
        command = abjad.LilyPondCommand(string, format_slot='after')
        last_leaf = abjad.select().by_leaf()(score)[-1][-1]
        abjad.attach(command, last_leaf)
        moment = abjad.schemetools.SchemeMoment((1, 12))
        abjad.set_(score).proportional_notation_duration = moment
        lilypond_file = abjad.lilypondfiletools.LilyPondFile.new(music=score)
        if 'title' in keywords:
            title = keywords.get('title')
            if not isinstance(title, abjad.Markup):
                title = abjad.Markup(title)
            lilypond_file.header_block.title = title
        if 'subtitle' in keywords:
            markup = abjad.Markup(keywords.get('subtitle'))
            lilypond_file.header_block.subtitle = markup
        command = abjad.LilyPondCommand('accidentalStyle forget')
        lilypond_file.layout_block.items.append(command)
        lilypond_file.layout_block.indent = 0
        string = 'markup-system-spacing.padding = 8'
        command = abjad.LilyPondCommand(string, prefix='')
        lilypond_file.paper_block.items.append(command)
        string = 'system-system-spacing.padding = 10'
        command = abjad.LilyPondCommand(string, prefix='')
        lilypond_file.paper_block.items.append(command)
        string = 'top-markup-spacing.padding = 4'
        command = abjad.LilyPondCommand(string, prefix='')
        lilypond_file.paper_block.items.append(command)
        return lilypond_file

    def __str__(self):
        r'''Gets string representation of segment.

        Returns string.
        '''
        parts = [str(x) for x in self]
        return '<{}>'.format(', '.join(parts))

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        return self._item_class

    @abc.abstractproperty
    def _named_item_class(self):
        raise NotImplementedError

    @abc.abstractproperty
    def _numbered_item_class(self):
        raise NotImplementedError

    @abc.abstractproperty
    def _parent_item_class(self):
        raise NotImplementedError

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        items = []
        if self.item_class.__name__.startswith('Named'):
            items = [str(x) for x in self]
        elif hasattr(self.item_class, 'pitch_number'):
            items = [x.pitch_number for x in self]
        elif hasattr(self.item_class, 'pitch_class_number'):
            items = [x.pitch_class_number for x in self]
        elif self.item_class.__name__.startswith('Numbered'):
            items = [mathtools.integer_equivalent_number_to_integer(float(x))
                for x in self]
        elif hasattr(self.item_class, '__abs__'):
            items = [abs(x) for x in self]
        else:
            raise ValueError
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=False,
            repr_kwargs_names=['name'],
            repr_args_values=[items],
            storage_format_args_values=[tuple(self._collection)],
            )

    def _get_padded_string(self, width=2):
        strings = []
        for item in self:
            string = '{{!s:>{}}}'
            string = string.format(width)
            string = string.format(item)
            strings.append(string)
        return '<{}>'.format(', '.join(strings))

    def _make_callback(self, frame, formula_string_template=None):
        assert self._frozen_expression, repr(self._frozen_expression)
        Expression = expressiontools.Expression
        template = Expression._make_evaluation_template(frame)
        return self._frozen_expression.append_callback(
            evaluation_template=template,
            formula_string_template=formula_string_template,
            )

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def has_duplicates(self):
        r'''Is true when segment has duplicates. Otherwise false.

        Returns true or false.
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def from_selection(
        class_,
        selection,
        item_class=None,
        ):
        r'''Makes segment from `selection`.

        Returns new segment.
        '''
        raise NotImplementedError
