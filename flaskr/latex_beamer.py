import re
from tempfile import NamedTemporaryFile

from .pitchdeck import PitchDeck

class LatexBeamer:
    """Accumulated text used to write a LaTeX beamer file."""
    file : NamedTemporaryFile = None
    
    """Escapes any characters with special meaning to LaTeX."""
    def latexEscape(self, s):
        return re.sub(r'([&%$#_{}])', r'\\\1', s)

    def startDoc(self) -> None:
        self.file = NamedTemporaryFile(suffix=".tex", mode="wt", encoding="utf-8", delete=False)
        print("LatexBeamer.startDoc 0:")
        print(self.file)
        self.file.write("\\documentclass{beamer}\n\n")

    """
    Create the document's title page and define preamble information that
    proceeds the first slide.
    """
    def writePreamble(
            self,
            title: str = '',
            subtitle: str = '',
            author: str = '',
            institute: str = '',
            date: str = '',
            logoFileName: str = '') -> None:
        if title:
            self.file.write("\\title{{{}}}\n".format(self.latexEscape(title)))
        if subtitle:
            self.file.write("\\subtitle{{{}}}\n".format(self.latexEscape(subtitle)))
        if author:
            self.file.write("\\author{{{}}}\n".format(self.latexEscape(author)))
        if institute:
            self.file.write("\\institute{{{}}}\n".format(self.latexEscape(institute)))
        if date:
            self.file.write("\\date{{{}}}\n".format(date))
        if logoFileName:
            self.file.write("\\logo{{\\includegraphics[height=1cm]{{{}}}}}\n".format(logoFileName))

        self.file.write("\\usetheme{Madrid}\n\n")

    def startBody(self) -> None:
        self.file.write("\\begin{document}\n\n")
        # Define the title page as the first slide.
        self.file.write("\\frame{\\titlepage}\n\n")

    def addSlide(self, title: str, items: list[str], imageFileName: str = '') -> None:
        self.file.write("\\begin{frame}\n")
        self.file.write("\\frametitle{{{}}}\n".format(self.latexEscape(title)))

        if imageFileName:
            self.file.write("\\begin{columns}\n")
            self.file.write("\\begin{column}{0.5\\textwidth}\n")
            self.file.write("  \\centering\n")
            self.file.write("    \\includegraphics[width=4cm]{{{}}}\n".format(self.latexEscape(imageFileName)))
            self.file.write("\\end{column}\n")
            self.file.write("\\begin{column}{0.5\\textwidth}\n")

        self.file.write("\\begin{itemize}\n")
        for item in items:
            self.file.write("\item {}".format(self.latexEscape(item)) + "\n")
        self.file.write("\\end{itemize}\n")

        if imageFileName:
            self.file.write("\\end{column}\n")
            self.file.write("\\end{columns}\n")

        self.file.write("\\end{frame}\n")

    def endBody(self) -> None:
        self.file.write("\\end{document}\n")

    def endDoc(self) -> any:
        print("LatexBeamer.endDoc 0:")
        print(self.file)
        self.file.close()
        print("LatexBeamer.endDoc 1:")
        print(self.file)
        return self.file
        
"""Returns a file-object associated with a temporary LaTeX file representing the PitchDeck."""
def createPitchDeckLatexFile(pitchDeck: PitchDeck) -> any:
    # Write the slide data into a new LaTeX document in beamer syntax.
    latex = LatexBeamer()
    latex.startDoc()
    latex.writePreamble(
        title=pitchDeck.title,
        subtitle=pitchDeck.subtitle,
        date=pitchDeck.date,
        logoFileName=pitchDeck.logoFileName)
    latex.startBody()
    for slide in pitchDeck.slides:
        latex.addSlide(slide.title, slide.items, slide.imageFileName)
    latex.endBody()
    latexFile = latex.endDoc()
    print("Creating LaTeX file: ", latexFile.name)
    return latexFile
