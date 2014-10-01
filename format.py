#!/usr/bin/python

import os, sys, re, codecs, subprocess

tmp_folder = 'tmp'

def main ():
   public = Convert( "." )
   private = Convert( "../private/" )
   
   public.toEpub()
   public.toHtml()
   private.toHtml()

   private.toFanFiktionDe()
   public.toFanFiktionDe( "../private/" )

class Convert( object ):
   in_path  = ""


   def __init__ ( self, in_path ):
      self.in_path  = in_path

   def toEpub ( self, out_path = False ):
      self.convert ( 'epub', out_path )


   def toHtml ( self, out_path = False ):
      self.convert ( 'html', out_path )


   def toFanFiktionDe ( self, out_path = False ):
      self.convert ( 'fanfiktionde', out_path )


   def convert ( self, out_format, out_path ):
      if not out_path:
         out_path = self.in_path
      out_path =  out_path + "/formated/"

      if not os.path.isdir( self.in_path ) or not os.path.isdir( out_path ):
         return

      language  = 'de'
      in_path   = self.in_path + "/" + language + "/"
      out_files = []

      for in_file in os.listdir( in_path ):
         if in_file.endswith(".md"):
            out_file = self.convert_file( in_path + in_file, out_path, out_format, language )

            if out_format is "epub":
               out_files += [out_file]

      if out_format is "epub":
         print ( "pandoc -o " + out_path + "epub/avilu-" + language + ".epub src/epub/title-"
            + language + ".txt src/epub/preamble-" + language + ".md " + " ".join( out_files ) );
         subprocess.call( ["pandoc -o " + out_path + "epub/avilu-" + language + ".epub src/epub/title-"
            + language + ".txt src/epub/preamble-" + language + ".md " + " ".join( out_files )] )

      #for tmp_file in out_files:
      #   os.remove( tmp_file )

   def convert_file ( self, in_file, out_path, out_format, language ):
      file_name = os.path.splitext( os.path.basename( in_file ) )[0]

      if out_format is 'html':
         out_file = out_path + "html/" + language + "/" + file_name + ".html"
      elif out_format is 'fanfiktionde':
         out_file = out_path + "fanfiktion.de/" + language + "/" + file_name + ".txt"
      elif out_format is "epub":
         out_file = "./tmp/" + file_name + ".md"

      # if os.path.isfile( out_file ) and os.path.getmtime( out_file ) >= os.path.getmtime( in_file ):
      #   return out_file

      f = codecs.open( in_file, 'r', 'utf-8' )
      md = f.read()
      f.close()

      md = re.sub( r'\r', '', md )
      md = re.sub( r'([ \n])\'(.*?)\'', r'\1›\2‹', md )
      md = re.sub( r'"(.*?)"', r'»\1«', md )
      md = re.sub( r'\'', r'’', md )
      md = re.sub( r'\.\.\.', r'…', md )

      if out_format is "epub":
         md = re.sub( r'(#.*\n+)', r'\n\1', md )
      else:
         md = re.sub( r'#.*\n+', '', md )

      if out_format is "html":
         md = re.sub(r'\*(.*?)\*', r'<em>\1</em>', md )
         md = re.sub(r'---\n', r'<hr/>\n', md )
      elif out_format is "fanfiktionde":
         md = re.sub(r'\*(.*?)\*', r'[style type="italic"]\1[/style]', md )
         md = re.sub(r'---\n', '[align type="center"]~~~[/align]\n', md )

      f = codecs.open( out_file, "w", 'utf-8' )
      f.write(md)
      f.close()

      return out_file


if __name__ == "__main__":
   main()