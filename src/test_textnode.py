import unittest

from leafnode import LeafNode
from textnode import TextNode, TextType


class TextNodeTest(unittest.TestCase):
  def test_not_eq(self):
    expected = TextNode("This is a text node", TextType.BOLD)
    actual = TextNode("This is another text node", TextType.ITALIC)
    
    self.assertNotEqual(expected, actual)
    
  def test_eq(self):
    expected = TextNode("This is a text node", TextType.BOLD)
    actual = TextNode("This is a text node", TextType.BOLD)

    self.assertEqual(expected, actual)

  def test_eq_url_not_same(self):
    this_node = TextNode("This is a text node", TextType.TEXT, "https://www.gmail.com")
    that_node = TextNode("This is a text node", TextType.TEXT, "https://www.hotmail.com")
    expected = False
    actual = this_node == that_node

    self.assertEqual(expected, actual)

  def test_eq_textType_not_same(self):
    this_node = TextNode("This is a text node", TextType.BOLD, "https://www.gmail.com")
    that_node = TextNode("This is a text node", TextType.TEXT, "https://www.gmail.com")
    expected = False
    actual = this_node == that_node

    self.assertEqual(expected, actual)

  def test_eq_text_not_same(self):
    this_node = TextNode("This is a special text node", TextType.TEXT, "https://www.gmail.com")
    that_node = TextNode("This is a text node", TextType.TEXT, "https://www.gmail.com")
    expected = False
    actual = this_node == that_node

    self.assertEqual(expected, actual)

  def test_eq_type_not_same(self):
    this_node = TextNode("This is a text node", TextType.TEXT, "https://www.gmail.com")
    that_object = ("A", "B")
    expected = False
    actual = this_node == that_object

    self.assertEqual(expected, actual)    

  def test_repr(self):
    this_node = TextNode("This is a text node", TextType.TEXT, "https://www.gmail.com")
    expected = "TextNode(This is a text node, text, https://www.gmail.com)"
    actual = this_node.__repr__()

    self.assertEqual(expected, actual)

  def test_to_leafnode_TEXT(self):
    this_node = TextNode("This is a text node", TextType.TEXT)

    expected = LeafNode("This is a text node")
    actual = this_node.to_leafnode()

    self.assertEqual(expected, actual)

  def test_to_leafnode_BOLD(self):
    this_node = TextNode("This is a bold text node", TextType.BOLD)

    expected = LeafNode("This is a bold text node", "b")
    actual = this_node.to_leafnode()

    self.assertEqual(expected, actual)

  def test_to_leafnode_ITALIC(self):
    this_node = TextNode("This is a italic text node", TextType.ITALIC)

    expected = LeafNode("This is a italic text node", "i")
    actual = this_node.to_leafnode()

    self.assertEqual(expected, actual)

  def test_to_leafnode_CODE(self):
    this_node = TextNode("This is a code block", TextType.CODE)

    expected = LeafNode("This is a code block", "code")
    actual = this_node.to_leafnode()

    self.assertEqual(expected, actual)
  
  def test_to_leafnode_LINK(self):
    this_node = TextNode("This is a Hyperlink", TextType.LINK, "https://www.gmail.com")

    expected = LeafNode("This is a Hyperlink", "a", { "href": "https://www.gmail.com"})
    actual = this_node.to_leafnode()

    self.assertEqual(expected, actual)

  def test_to_leafnode_IMAGE(self):
    this_node = TextNode("This is an image", TextType.IMAGE, "https://www.gmail.com")

    expected = LeafNode("", "img", { "src": "https://www.gmail.com", "alt": "This is an image"})
    actual = this_node.to_leafnode()

    self.assertEqual(expected, actual)

if __name__ == "__main__":
  unittest.main()