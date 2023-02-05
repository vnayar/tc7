# The @dataclass annotiation defines __init__ for simple classes.
from dataclasses import dataclass, field

"""The raw data for the contents of a pitch deck slide."""
@dataclass
class Slide:
    """The title of the slide."""
    title: str
    """A list of bullet points in the slide."""
    items: list[str] = field(default_factory=list)


"""
Given text in the form below, extract the data of a pitch deck:

Slide 1: The slide title.
 - First item
 - Second item
 - ...

Slide 2: ...
"""
def parseSlides(text: str) -> list[Slide]:
    slides: list[Slide] = []
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("Slide "):
            slides.append(Slide(line.split(":", 1)[1].strip()))
        elif line.startswith("- "):
            slide = slides[-1]
            slide.items.append(line.split("- ", 1)[1])
    print("Extracted Slide Data:")
    print(slides)
    return slides

    
"""The raw data for the contents of a pitch deck."""
@dataclass
class PitchDeck:
    title: str
    subtitle: str
    date: str
    slides: list[Slide] = field(default_factory=list)

