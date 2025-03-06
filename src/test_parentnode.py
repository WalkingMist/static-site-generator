import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class ParentNodeTest(unittest.TestCase):
  def test_to_html_no_tag(self):
    this_node = ParentNode(None,
                           children = [ 
                             LeafNode("Gmail",
                                      "a",
                                      {
                                        "href": "https://www.gmail.com"
                                      })],
                           props=None)
    with self.assertRaises(ValueError):
      this_node.to_html()

  def test_to_html_no_children(self):
    this_node = ParentNode(None,
                           children = None,
                           props=None)
    
    with self.assertRaises(ValueError):
      this_node.to_html()

  def test_to_html(self):
    this_node = ParentNode("p",
                           children = [ 
                             LeafNode("Gmail",
                                      "a",
                                      {
                                        "href": "https://www.gmail.com"
                                      })],
                           props=None)
    expected = '<p><a href="https://www.gmail.com">Gmail</a></p>'
    actual = this_node.to_html()

    self.assertEqual(expected, actual)

  def test_to_html_icon(self):
    span_leafnode = LeafNode("Home", "span")
    span_containing_icon = ParentNode("span",
                                      children=[
                                        LeafNode("", "i", {"class": "fas fa-home"})],
                                      props = { "class": "icon"})
    this_node = ParentNode("span",
                           children = [
                             span_containing_icon,
                             span_leafnode],
                           props = {
                             "class": "icon-text"})
    
    expected = '<span class="icon-text"><span class="icon"><i class="fas fa-home"></i></span><span>Home</span></span>'
    actual = this_node.to_html()

    self.assertEqual(expected, actual)

if __name__ == "__main__":
  unittest.main()