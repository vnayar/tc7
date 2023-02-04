import re
from tempfile import NamedTemporaryFile

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
            title: str = "",
            subtitle: str = "",
            author: str = "",
            institute: str = "",
            date: str = "") -> None:
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
        self.file.write("\\usetheme{Madrid}\n\n")

    def startBody(self) -> None:
        self.file.write("\\begin{document}\n\n")
        # Define the title page as the first slide.
        self.file.write("\\frame{\\titlepage}\n\n")

    def addSlide(self, title: str, items: list[str]) -> None:
        self.file.write("\\begin{frame}\n")
        self.file.write("\\frametitle{{{}}}\n".format(self.latexEscape(title)))
        self.file.write("\\begin{itemize}\n")
        for item in items:
            self.file.write("\item {}".format(self.latexEscape(item)) + "\n")
        self.file.write("\\end{itemize}\n")
        self.file.write("\\end{frame}\n")

    def endBody(self) -> None:
        self.file.write("\\end{document}\n")

    def endDoc(self) -> any:
        print("LatexBeamer.endDoc 0:")
        print(self.file)
        self.file.close()
        print("LatexBeamer.endDoc 1:")
        print(self.file)
        return self.file.name
        
        
        