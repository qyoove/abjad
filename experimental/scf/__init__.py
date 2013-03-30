import chunks
import editors
import exceptions
import getters
import helpers
import makers
import menuing
import predicates
import proxies
import selectors
import specifiers
import studio
import wizards
import wranglers

'''SCF: Score Control Front-End:

Do the following to install SCF on your system:

    1. verify SCF directories
    2. set SCF environment variables
    3. add abjad/experimental/scr to your PATH
    4. create a scores directory
    5. start and stop SCF
    6. create Example Score I using SCF
    7. create Example Score II using SCF
    8. run the SCF py.test battery


1. Verify SCF directories. The following six directories should be 
on your filesystem:

    abjad/experimental/materials
    abjad/experimental/scf
    abjad/experimental/scm
    abjad/experimental/scr
    abjad/experimental/sketches
    abjad/experimental/specifiers


2. Set SCF environment variables. The following five environment variables 
should be set in your profile, or eqivalent:

    export SCFCHUNKSPATH=$ABJADEXPERIMENTAL/sketches
    export SCFMATERIALSPATH=$ABJADEXPERIMENTAL/materials
    export SCFOUTPUT=$HOME/.scf/output
    export SCFPATH=$ABJADEXPERIMENTAL/scf
    export SCFSPECIFIERSPATH=$ABJADEXPERIMENTAL/specifiers

You should also set the HANDLERS environment variable because SCF uses handlertools:

    export HANDLERS=$ABJADEXPERIMENTAL/tools/handlertools


3. Add the abjad/experimental/scr directory to your PATH.
This tells your shell where the scf start-up script is housed:

    export PATH=$ABJADEXPERIMENTAL/scr:$PATH


4. Create a scores directory. You can do this anywhere on your filesystem you wish.
Then create a SCORES environment variable in your profile and set it to your score directory:

    export SCORES=$DOCUMENTS/scores

    
5. Start and stop SCF. Type ...

    scf

... from the commandline and SCF should start.
This step hasn't yet been tested on a computer with a brand-new SCF installation.
What you see here probably won't be very interesting because you
won't yet have any SCF-managed scores created on your system.
But you should see an empt list of scores as well as three or four menu
options. The menu options will allow you to manage materials, specifiers and sketches.
There will also be a menu option to create a new score.
If the shell can't find SCF go back to step #3 and make sure you added
the abjad/experimental/scr directory to your PATH.
After SCF starts correctly enter 'q' to quit SCF and return to the shell.


6. Create Example Score I using SCF. Type 'scf' to start SCF again.
Once SCF starts you should see a menu item that says "new score (new)".
Type 'new'. You should then be presented with a 3-step score creation wizard.
Complete the wizard exactly as follows:

    (1/3) score title: Example Score I
    (2/3) package name: example_score_1
    (3/3) year of completion: 2013

Quit SCF once you finish the wizard. Check your scores directory. You should
see a example_score_1 directory. List the contents of the example_score_1 score directory:

    scores$ ls example_score_1/
    __init__.py dist        etc         exg         mus         tags.py

You should see the subdirectories and initializer shown above.


7. Create Example Score II using SCF. Repeat the steps listed for #6, above:

    (1/3) score title: Example Score II
    (2/3) package name: example_score_2
    (3/3) year of completion: 2013

Quit SCF when your are done. SCF tests parts of the system against 
Example Score I and Example Score II.

    
8. Run the py.test SCF battery. You're now in a position to run the SCF py.test battery.
Just run "py.test in abjad/experimental/scf" the same way you do for every other part
of Abjad. You're ready to read the SCF code if all tests pass.
'''
