
import unittest

from htmlnode import HTMLNode


#class HTMLNodeTest(unittest.TestCase):
#  def test_to_html(self):
#    this_node = HTMLNode("a", 
#                         "This is a link to something...", 
#                         None, 
#                         {"href": "https://www.google.com"})#

#    self.assertRaises(NotImplementedError, this_node.to_html)#

#  def test_repr(self):
#    this_node = HTMLNode("a",
#                         "GMail",
#                         None,
#                         {"href": "https://www.google.com",
#                          "target": "_blank"})
#    
#    expected = f"HTMLNode(a, GMail, None, {{'href': 'https://www.google.com', 'target': '_blank'}})"
#    actual = this_node.__repr__()#

#    self.assertEqual(expected, actual)#

#  def test_prop_to_html(self):
#    this_node = HTMLNode("a",
#                         "GMail",
#                         None,
#                         {"href": "https://www.google.com",
#                          "target": "_blank"})
#    
#    expected = f'href="https://www.google.com" target="_blank"'
#    actual = this_node.props_to_html()#

#    self.assertEqual(expected, actual)#

#if __name__ == "__main__":
#  unittest.main()