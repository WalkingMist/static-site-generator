import unittest

from textnode import TextType


class TextTypeTest(unittest.TestCase):
  
  def test_str_text(self):
    expected = "text"
    actual = str(TextType.TEXT)

    self.assertEqual(expected, actual)

  def test_str_bold(self):
    expected = "bold"
    actual = str(TextType.BOLD)

    self.assertEqual(expected, actual)

  def test_str_italic(self):
    expected = "italic"
    actual = str(TextType.ITALIC)

    self.assertEqual(expected, actual)

  def test_str_code(self):
    expected = "code"
    actual = str(TextType.CODE)

    self.assertEqual(expected, actual)

  def test_str_link(self):
    expected = "link"
    actual = str(TextType.LINK)

    self.assertEqual(expected, actual)

  def test_str_image(self):
    expected = "image"
    actual = str(TextType.IMAGE)

    self.assertEqual(expected, actual)

