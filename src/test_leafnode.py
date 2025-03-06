import unittest

from leafnode import LeafNode


class LeafNodeTest(unittest.TestCase):
  def test_to_html(self):
    this_node = LeafNode("GMail",
                        "a",
                        {
                          "href": "https://www.gmail.com",
                          "target": "_self"
                        })
    expected = f'<a href="https://www.gmail.com" target="_self">GMail</a>'
    actual = this_node.to_html()

    self.assertEqual(expected, actual)

  def test_to_html_no_value(self):
    this_node = LeafNode(None,
                        "a",
                        {
                          "href": "https://www.gmail.com",
                          "target": "_self"
                        })
    with self.assertRaises(ValueError):
      this_node.to_html()

  def test_to_html_no_tag(self):
    this_node = LeafNode("GMail",
                        None,
                        {
                          "href": "https://www.gmail.com",
                          "target": "_self"
                        })
    expected = "GMail"
    actual = this_node.to_html()

    self.assertEqual(expected, actual)

if __name__ == "__main__":
  unittest.main()