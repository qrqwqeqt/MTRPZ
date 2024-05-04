import unittest
from md import set_paragraphs, set_preformatted_parts, set_html_tags, nested_markers_checker

class TestMarkdownToHtml(unittest.TestCase):

    def test_set_paragraphs(self):
        text = "Hello\n\nWorld"
        result = set_paragraphs(text)
        self.assertEqual(result, "<p>Hello</p>\n<p>World</p>\n")

    def test_set_preformatted_parts(self):
        text = "  Hello  "
        result = set_preformatted_parts(text)
        self.assertEqual(result, "<pre>Hello</pre>\n")

    def test_set_html_tags(self):
        text = "**bold** _italic_ `monospaced`"
        result = set_html_tags(text)
        self.assertEqual(result, "<b>bold</b> <i>italic</i> <tt>monospaced</tt>")

    def test_nested_markers_checker(self):
        text = "**bold _italic_ bold**"
        regex = r"\*\*(?=\S)(.+?)(?<=\S)\*\*(?=\s|$)"
        marker = "**"
        with self.assertRaises(ValueError):
            nested_markers_checker(text, regex, marker)

if __name__ == '__main__':
    unittest.main()
