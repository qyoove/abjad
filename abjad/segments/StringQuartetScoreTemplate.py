from abjad.utilities.OrderedDict import OrderedDict
from .Part import Part
from .PartManifest import PartManifest
from .ScoreTemplate import ScoreTemplate


class StringQuartetScoreTemplate(ScoreTemplate):
    r"""
    String quartet score template.

    ..  container:: example

        >>> template = abjad.StringQuartetScoreTemplate()
        >>> abjad.show(template) # doctest: +SKIP

        >>> abjad.f(template.__illustrate__()[abjad.Score], strict=60)
        \context Score = "String_Quartet_Score"                     %! abjad.StringQuartetScoreTemplate
        <<                                                          %! abjad.StringQuartetScoreTemplate
            \context StaffGroup = "String_Quartet_Staff_Group"      %! abjad.StringQuartetScoreTemplate
            <<                                                      %! abjad.StringQuartetScoreTemplate
                \tag #'first-violin
                \context Staff = "First_Violin_Staff"               %! abjad.StringQuartetScoreTemplate
                {                                                   %! abjad.StringQuartetScoreTemplate
                    \context Voice = "First_Violin_Voice"           %! abjad.StringQuartetScoreTemplate
                    {                                               %! abjad.StringQuartetScoreTemplate
                        \clef "treble"                              %! abjad.ScoreTemplate.attach_defaults
                        s1                                          %! abjad.ScoreTemplate.__illustrate__
                    }                                               %! abjad.StringQuartetScoreTemplate
                }                                                   %! abjad.StringQuartetScoreTemplate
                \tag #'second-violin
                \context Staff = "Second_Violin_Staff"              %! abjad.StringQuartetScoreTemplate
                {                                                   %! abjad.StringQuartetScoreTemplate
                    \context Voice = "Second_Violin_Voice"          %! abjad.StringQuartetScoreTemplate
                    {                                               %! abjad.StringQuartetScoreTemplate
                        \clef "treble"                              %! abjad.ScoreTemplate.attach_defaults
                        s1                                          %! abjad.ScoreTemplate.__illustrate__
                    }                                               %! abjad.StringQuartetScoreTemplate
                }                                                   %! abjad.StringQuartetScoreTemplate
                \tag #'viola
                \context Staff = "Viola_Staff"                      %! abjad.StringQuartetScoreTemplate
                {                                                   %! abjad.StringQuartetScoreTemplate
                    \context Voice = "Viola_Voice"                  %! abjad.StringQuartetScoreTemplate
                    {                                               %! abjad.StringQuartetScoreTemplate
                        \clef "alto"                                %! abjad.ScoreTemplate.attach_defaults
                        s1                                          %! abjad.ScoreTemplate.__illustrate__
                    }                                               %! abjad.StringQuartetScoreTemplate
                }                                                   %! abjad.StringQuartetScoreTemplate
                \tag #'cello
                \context Staff = "Cello_Staff"                      %! abjad.StringQuartetScoreTemplate
                {                                                   %! abjad.StringQuartetScoreTemplate
                    \context Voice = "Cello_Voice"                  %! abjad.StringQuartetScoreTemplate
                    {                                               %! abjad.StringQuartetScoreTemplate
                        \clef "bass"                                %! abjad.ScoreTemplate.attach_defaults
                        s1                                          %! abjad.ScoreTemplate.__illustrate__
                    }                                               %! abjad.StringQuartetScoreTemplate
                }                                                   %! abjad.StringQuartetScoreTemplate
            >>                                                      %! abjad.StringQuartetScoreTemplate
        >>                                                          %! abjad.StringQuartetScoreTemplate

    Returns score template.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _part_manifest = PartManifest(
        Part(section="FirstViolin", section_abbreviation="VN-1"),
        Part(section="SecondViolin", section_abbreviation="VN-2"),
        Part(section="Viola", section_abbreviation="VA"),
        Part(section="Cello", section_abbreviation="VC"),
    )

    ### INITIALIZER ###

    def __init__(self):
        super().__init__()
        self.voice_abbreviations.update(
            {
                "vn1": "First Violin Voice",
                "vn2": "Second Violin Voice",
                "va": "Viola Voice",
                "vc": "Cello Voice",
            }
        )

    ### SPECIAL METHODS ###

    def __call__(self):
        """
        Calls string quartet score template.

        Returns score.
        """
        import abjad

        class_name = "abjad.StringQuartetScoreTemplate"

        # make first violin voice and staff
        first_violin_voice = abjad.Voice(
            [], name="First_Violin_Voice", tag=class_name
        )
        first_violin_staff = abjad.Staff(
            [first_violin_voice], name="First_Violin_Staff", tag=class_name
        )
        clef = abjad.Clef("treble")
        abjad.annotate(first_violin_staff, "default_clef", clef)
        violin = abjad.Violin()
        abjad.annotate(first_violin_staff, "default_instrument", violin)
        tag = abjad.LilyPondLiteral(r"\tag #'first-violin", "before")
        abjad.attach(tag, first_violin_staff)

        # make second violin voice and staff
        second_violin_voice = abjad.Voice(
            [], name="Second_Violin_Voice", tag=class_name
        )
        second_violin_staff = abjad.Staff(
            [second_violin_voice], name="Second_Violin_Staff", tag=class_name
        )
        clef = abjad.Clef("treble")
        abjad.annotate(second_violin_staff, "default_clef", clef)
        violin = abjad.Violin()
        abjad.annotate(second_violin_staff, "default_instrument", violin)
        tag = abjad.LilyPondLiteral(r"\tag #'second-violin", "before")
        abjad.attach(tag, second_violin_staff)

        # make viola voice and staff
        viola_voice = abjad.Voice([], name="Viola_Voice", tag=class_name)
        viola_staff = abjad.Staff(
            [viola_voice], name="Viola_Staff", tag=class_name
        )
        clef = abjad.Clef("alto")
        abjad.annotate(viola_staff, "default_clef", clef)
        viola = abjad.Viola()
        abjad.annotate(viola_staff, "default_instrument", viola)
        tag = abjad.LilyPondLiteral(r"\tag #'viola", "before")
        abjad.attach(tag, viola_staff)

        # make cello voice and staff
        cello_voice = abjad.Voice([], name="Cello_Voice", tag=class_name)
        cello_staff = abjad.Staff(
            [cello_voice], name="Cello_Staff", tag=class_name
        )
        clef = abjad.Clef("bass")
        abjad.annotate(cello_staff, "default_clef", clef)
        cello = abjad.Cello()
        abjad.annotate(cello_staff, "default_instrument", cello)
        tag = abjad.LilyPondLiteral(r"\tag #'cello", "before")
        abjad.attach(tag, cello_staff)

        # make string quartet staff group
        string_quartet_staff_group = abjad.StaffGroup(
            [
                first_violin_staff,
                second_violin_staff,
                viola_staff,
                cello_staff,
            ],
            name="String_Quartet_Staff_Group",
            tag=class_name,
        )

        # make string quartet score
        string_quartet_score = abjad.Score(
            [string_quartet_staff_group],
            name="String_Quartet_Score",
            tag=class_name,
        )

        # return string quartet score
        return string_quartet_score
