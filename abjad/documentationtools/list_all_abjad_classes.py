def list_all_abjad_classes(modules=None, ignored_classes=None):
    """
    Lists all public classes defined in Abjad.

    ..  container:: example

        >>> all_classes = abjad.documentationtools.list_all_abjad_classes()

    """
    from abjad import documentationtools
    return documentationtools.list_all_classes(
        modules='abjad',
        ignored_classes=ignored_classes,
        )