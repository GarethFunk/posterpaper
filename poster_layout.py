class Poster:
    def __init__(self, doc):
        self.columns = []
        self.author = ""
        self.title = ""
        self.preamble = ""
        self.boxes = []
        self._makeBoxes()
        self.total_char_count = self._charCount()
        self.text_space = self._textSpace()
        self._makeColumns()
        return

    def _makeBoxes(self, doc):
        box = Box(doc)
        box.title = "Abstract"
        box.reference = "section0"
        box.content = doc.abstract
        box.char_count = len(doc.abstract)
        self.boxes.append(box)
        for i, section in enumerate(doc.sections):
            if section.include is True:
                box = Box(doc)
                box.figures = section.figures
                box.content = section.content
                box.title = section.title
                box.char_count = section.char_count
                box.reference = "section" + str(i+1)
                self.boxes.append(box)
        return

    def _charCount(self):
        cumulative_char_count = 0
        for box in self.boxes:
            cumulative_char_count += box.char_count
        return cumulative_char_count

    def _textSpace(self):
        cumulative_space_taken = 0
        for box in self.boxes:
            cumulative_space_taken += box.size_without_text
        return 632 * 3 - cumulative_space_taken

    def _makeColumns(self, doc):
        self.columns = [Column(), Column(), Column()]
        for box in self.boxes:
            box.size_of_text = box.sizeOfText(self, doc, self.total_char_count, self.text_space)
            box.total_size = box.totalSize()
        

        self.columns[0].boxes.append(self.boxes[0])



class Column:
    def __init__(self):
        self.boxes = []
        self.cumulative_size = 0
        return

class Box:
    def __init__(self, doc):
        self.figures = []
        self.content = ""
        self.title = ""
        self.reference = ""
        self.char_count = 0
        self.size_without_text = 0
        self.size_of_text = 0
        self.total_size = 0
        self._sizeWithoutText(doc)
        return

    def _sizeWithoutText(self, doc):
        figure_space = 0
        for figure in self.figures:
            if figure.include is True:
                figure_space += 0.9 * 325 * figure.height + 20 #20 is an approximation of the caption size
        self.size_without_text = 9 + 16 + figure_space
        return

    def sizeOfText(self, total_char_count, text_space):
        self.size_of_text = self.char_count / total_char_count * text_space
        return

    def totalSize(self):
        self.total_size = self.size_of_text + self.size_without_text
        return

