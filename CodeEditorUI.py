from Imports import  *

class SystemVerilogHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#138a76"))#FE099D
        keyword_format.setFontWeight(QFont.Bold)

        keyword_patterns = [
            r"\bmodule\b", r"\bendmodule\b", r"\binput\b", r"\boutput\b", r"\binout\b", r"\bwire\b", r"\breg\b",
            r"\blogic\b", r"\balways\b", r"\balways_ff\b", r"\balways_comb\b", r"\balways_latch\b", r"\bassign\b",
            r"\bbegin\b", r"\bend\b", r"\bif\b", r"\belse\b", r"\bcase\b", r"\bendcase\b", r"\bdefault\b",
            r"\bfor\b", r"\bwhile\b", r"\brepeat\b", r"\bforever\b", r"\bgenerate\b", r"\bendgenerate\b",
            r"\bgenvar\b", r"\bparameter\b", r"\blocalparam\b", r"\bfunction\b", r"\bendfunction\b",
            r"\btask\b", r"\bendtask\b", r"\breturn\b", r"\bposedge\b", r"\bnegedge\b", r"\btypedef\b",
            r"\bstruct\b", r"\bendstruct\b", r"\benum\b", r"\bendinterface\b", r"\binterface\b", r"\bpackage\b",
            r"\bendpackage\b", r"\bimport\b", r"\bexport\b", r"\bconst\b", r"\bstatic\b"
        ]


        self.highlighting_rules = [(QRegularExpression(pat), keyword_format) for pat in keyword_patterns]

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#FE099D"))
        self.highlighting_rules.append((QRegularExpression(r'"[^"]*"'), string_format))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#CCCCCC"))
        self.highlighting_rules.append((QRegularExpression(r"//.*"), comment_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                match = it.next()
                start, length = match.capturedStart(), match.capturedLength()
                self.setFormat(start, length, fmt)

'''class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(code_editor_style)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        font = QFont("Fira Code", 16)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)

        # Enable syntax highlighting
        self.highlighter = SystemVerilogHighlighter(self.document())'''
        
class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.code_editor.line_number_area_paint_event(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Font
        font = QFont("Fira Code", 12)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

        # Line number area
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width(0)
        self.highlight_current_line()

        # Syntax highlighter
        self.highlighter = SystemVerilogHighlighter(self.document())

    def line_number_area_width(self):
        digits = len(str(self.blockCount()))
        return 10 + self.fontMetrics().width('9') * digits

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def highlight_current_line(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(QColor("#3c4042"))
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#26292a"))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.gray)
                painter.drawText(
                    0, top,
                    self.line_number_area.width() - 4,
                    self.fontMetrics().height(),
                    Qt.AlignRight,
                    number
                )
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1



class CodeEditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.editor = CodeEditor()
        self.editor.setStyleSheet(code_editor_style)
        self.default_font_size = 10
        self.current_font_size = self.default_font_size
        #self._apply_font_size()

        # Button style
        btn_style = "margin-left: 4px; border: none; padding: 4px;"

        # File buttons
        self.open_button = QPushButton("")
        self.save_button = QPushButton("")
        self.open_button.setStyleSheet(code_editor_btn)
        self.save_button.setStyleSheet(code_editor_btn)
        self.open_button.clicked.connect(self.open_file)
        self.save_button.clicked.connect(self.save_file)
        self.open_button.setIcon(QIcon("icons/open_code.png"))
        self.save_button.setIcon(QIcon("icons/save_code.png"))
        self.open_button.setToolTip("Open File")
        self.save_button.setToolTip("Save File")
        self.open_button.setIconSize(QSize(20, 20))
        self.save_button.setIconSize(QSize(20, 20))

        # Zoom buttons
        zoom_in_btn = QPushButton()
        zoom_in_btn.setIcon(QIcon("icons/zin.png"))
        zoom_in_btn.setToolTip("Zoom In")
        zoom_in_btn.setIconSize(QSize(20, 20))
        zoom_in_btn.setStyleSheet(code_editor_btn)
        zoom_in_btn.clicked.connect(self.zoom_in)

        zoom_out_btn = QPushButton()
        zoom_out_btn.setIcon(QIcon("icons/zout.png"))
        zoom_out_btn.setToolTip("Zoom Out")
        zoom_out_btn.setIconSize(QSize(20, 20))
        zoom_out_btn.setStyleSheet(code_editor_btn)
        zoom_out_btn.clicked.connect(self.zoom_out)

        reset_zoom_btn = QPushButton()
        reset_zoom_btn.setIcon(QIcon("icons/reset.png"))
        reset_zoom_btn.setToolTip("Reset Zoom")
        reset_zoom_btn.setIconSize(QSize(20, 20))
        reset_zoom_btn.setStyleSheet(code_editor_btn)
        reset_zoom_btn.clicked.connect(self.reset_zoom)

        # Top bar layout
        top_bar = QHBoxLayout()
        top_bar.addWidget(self.open_button)
        top_bar.addWidget(self.save_button)
        top_bar.addStretch()
        top_bar.addWidget(zoom_in_btn)
        top_bar.addWidget(zoom_out_btn)
        top_bar.addWidget(reset_zoom_btn)
        

        # Final layout
        layout = QVBoxLayout()
        layout.addLayout(top_bar)
        layout.addWidget(self.editor)
        self.setLayout(layout)
        #self.setStyleSheet(code_editor_style)

    def _apply_font_size(self):
        font = self.editor.font()
        font.setPointSize(self.current_font_size)
        self.editor.setFont(font)
        self.editor.document().setDefaultFont(font)

        # Apply to existing text
        cursor = self.editor.textCursor()
        cursor.select(QTextCursor.Document)
        fmt = cursor.charFormat()
        fmt.setFontPointSize(self.current_font_size)
        cursor.setCharFormat(fmt)
        self.editor.moveCursor(QTextCursor.End)

    def zoom_in(self):
        self.current_font_size += 1
        self._apply_font_size()

    def zoom_out(self):
        self.current_font_size = max(6, self.current_font_size - 1)
        self._apply_font_size()

    def reset_zoom(self):
        self.current_font_size = self.default_font_size
        self._apply_font_size()

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "SystemVerilog Files (*.sv *.v);;All Files (*)")
        if path:
            try:
                with open(path, 'r') as f:
                    self.editor.setPlainText(f.read())
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to open file:\n{str(e)}")

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "SystemVerilog Files (*.sv *.v);;All Files (*)")
        if path:
            try:
                with open(path, 'w') as f:
                    f.write(self.editor.toPlainText())
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save file:\n{str(e)}")