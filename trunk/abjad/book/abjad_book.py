from abjad.book.parser.abjadhtmltag import AbjadHTMLTag
from abjad.book.parser.abjadlatextag import AbjadLatexTag
from abjad.book.parser.abjadresttag import AbjadReSTTag
import sys
import os

def _usage( ):
   return '''\nUsage: abjad-book FILE [OUTPUT] 

Process Abjad snippets in hybrid HTML, LaTeX, or ReST document.

Examples of usage:
 $ abjad-book my_input.tex
 $ abjad-book my_input.htm  my_result.html

About abjad-book:
All Abjad code placed between the <abjad> </abjad> tags in either HTML, LaTeX
or ReST type documents are interpreted and replaced with tags appropriate to 
the given file type.
Apart from the opening and closing Abjad tags, one internal *suffix* tag 
<hide is also reserved. 
All lines with <hide tag in them will be interpreted by Abjad but will not 
be displayed in the final document. 
Use the write(expr, name, template, title) function to have a 
LilyPond rendering of an Abjad snipped appear in the document. 
show( ) will do nothing.
Indentation is semantic and all Abjad snippets *must* start with no indentation in the document. All output generated by the snippet is captured and displayed.

Example (HTML document):

   This is an <b>HTML</b> document. Here is Abjad code:
   <abjad>
   v = Voice(construct.run(8))
   Beam(v)
   write_ly(v, 'example1') <hide ## this will insert an image here. 
   show(v)
   </abjad>
   More ordinary <b>HTML</b> text here.
   '''

def _abjad_book( ):
   ## get input parameters
   if len(sys.argv) == 1:
      print _usage( )
      sys.exit(2)

   fn = sys.argv[1]
   out_fn = None
   if len(sys.argv) > 2:
      out_fn = sys.argv[2]

   ## parse file name
   fn_dir = os.path.dirname(os.path.abspath(fn))
   fn = os.path.basename(fn)
   #fn_extension = fn.split('.')[-1]
   fn_root = fn.split('.')[0]
   
   ## chage to file dir and read input file
   os.chdir(fn_dir)
   file = open(fn, 'r')
   #lines = file.readlines( )
   lines = file.read( ).splitlines( ) ## send lines with no trailing '\n'
   file.close( )

   ## create Abjad tag parser type based on file extension
   #if 'htm' in fn_extension:
   if '.htm' in fn:
      a = AbjadHTMLTag(lines)
      fn_extension = '.html'
   #elif 'tex' in fn_extension:
   elif '.tex' in fn:
      a = AbjadLatexTag(lines)
      fn_extension = '.tex'
   #elif 'rst' in fn_extension:
   elif '.rst' in fn:
      a = AbjadReSTTag(lines)
      fn_extension = '.rst'

   ## open and write to output file
   if out_fn:
      file = open(out_fn, 'w')
   else:
      file = open('%s_abj%s' % (fn_root, fn_extension), 'w')

   file.writelines(a.process( ))
   file.close( )


if __name__ == '__main__':
   _abjad_book( )
