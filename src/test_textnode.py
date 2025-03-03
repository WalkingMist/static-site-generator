import unittest

from leafnode import LeafNode
from parentnode import ParentNode
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

    expected = ParentNode("b", [ LeafNode("This is a bold text node") ])
    actual = this_node.to_leafnode()

    self.assertEqual(expected, actual)

  def test_to_leafnode_ITALIC(self):
    this_node = TextNode("This is a italic text node", TextType.ITALIC)

    expected = ParentNode("i", [ LeafNode("This is a italic text node") ])
    actual = this_node.to_leafnode()

    self.assertEqual(expected, actual)

  def test_to_leafnode_CODE(self):
    this_node = TextNode("This is a code block", TextType.CODE)

    expected = ParentNode("code", [ LeafNode("This is a code block") ])
    actual = this_node.to_leafnode()

    self.assertEqual(expected, actual)
  
  def test_to_leafnode_LINK(self):
    this_node = TextNode("This is a Hyperlink", TextType.LINK, "https://www.gmail.com")

    expected = ParentNode("a", [ LeafNode("This is a Hyperlink") ], { "href": "https://www.gmail.com"})
    actual = this_node.to_leafnode()

    self.assertEqual(expected, actual)

  def test_to_leafnode_IMAGE(self):
    this_node = TextNode("This is an image", TextType.IMAGE, "https://www.gmail.com")

    expected = LeafNode("", "img", { "src": "https://www.gmail.com", "alt": "This is an image"})
    actual = this_node.to_leafnode()

    self.assertEqual(expected, actual)

  def test_split_nodes_delimiter_BOLD(self):
    this_node = TextNode("This is text with **BOLD** word", TextType.TEXT)

    expected = [TextNode("This is text with ", TextType.TEXT), TextNode("BOLD", TextType.BOLD), TextNode(" word", TextType.TEXT)]
    actual = TextNode.split_nodes_delimiter([this_node], TextType.BOLD)

    self.assertEqual(expected, actual)

  def test_split_nodes_delimiter_TEXT(self):
    this_node = TextNode("This is just plain text", TextType.TEXT)

    expected = [TextNode("This is just plain text", TextType.TEXT)]
    actual = TextNode.split_nodes_delimiter([this_node], TextType.TEXT)

    self.assertEqual(expected, actual)

  def test_split_nodes_delimiter_ITALIC(self):
    this_node = TextNode("This is text with *ITALIC* word", TextType.TEXT)

    expected = [TextNode("This is text with ", TextType.TEXT), TextNode("ITALIC", TextType.ITALIC), TextNode(" word", TextType.TEXT)]
    actual = TextNode.split_nodes_delimiter([this_node], TextType.ITALIC)

    self.assertEqual(expected, actual)

  def test_split_nodes_delimiter_CODE(self):
    this_node = TextNode("This is text with `CODE` word", TextType.TEXT)

    expected = [TextNode("This is text with ", TextType.TEXT), TextNode("CODE", TextType.CODE), TextNode(" word", TextType.TEXT)]
    actual = TextNode.split_nodes_delimiter([this_node], TextType.CODE)

    self.assertEqual(expected, actual)

  def test_split_nodes_delimiter_LINK(self):
    this_node = TextNode("This is text with [LINK](https://www.gmail.com)", TextType.TEXT)

    expected = [TextNode("This is text with [LINK](https://www.gmail.com)", TextType.TEXT)]
    actual = TextNode.split_nodes_delimiter([this_node], TextType.LINK)

    self.assertEqual(expected, actual)

  def test_split_nodes_delimiter_IMAGE(self):
    this_node = TextNode("This is text with ![IMAGE](https://ssl.gstatic.com/ui/v1/icons/mail/rfr/logo_gmail_lockup_dark_1x_r5.png)", TextType.TEXT)

    expected = [TextNode("This is text with ![IMAGE](https://ssl.gstatic.com/ui/v1/icons/mail/rfr/logo_gmail_lockup_dark_1x_r5.png)", TextType.TEXT)]
    actual = TextNode.split_nodes_delimiter([this_node], TextType.IMAGE)

    self.assertEqual(expected, actual)
   
  def test_split_nodes_delimiter_not_found(self):
    this_node = TextNode("This is text with *ITALIC* word", TextType.TEXT)

    expected = [TextNode("This is text with *ITALIC* word", TextType.TEXT)]
    actual = TextNode.split_nodes_delimiter([this_node], TextType.BOLD)

    self.assertEqual(expected, actual)

  def test_split_nodes_delimiter_multiple(self):
    this_node = TextNode("This is text with **THIS** and **THAT** word", TextType.TEXT)

    expected = [TextNode("This is text with ",TextType.TEXT), TextNode("THIS", TextType.BOLD), TextNode(" and ", TextType.TEXT), TextNode("THAT", TextType.BOLD), TextNode(" word", TextType.TEXT)]
    actual = TextNode.split_nodes_delimiter([this_node], TextType.BOLD)

    self.assertEqual(expected, actual)

  def test_split_nodes_delimiter_not_closing(self):
    this_node = TextNode("This is text with *ITALIC word", TextType.TEXT)

    self.assertRaises(Exception, TextNode.split_nodes_delimiter([this_node], TextType.ITALIC))

  def test_split_nodes_delimiter_empty_segment(self):
    this_node = TextNode("This is text with **BOLD WORDS** ", TextType.TEXT)

    expected = [TextNode("This is text with ",TextType.TEXT), TextNode("BOLD WORDS", TextType.BOLD)]
    actual = TextNode.split_nodes_delimiter([this_node], TextType.BOLD)

    self.assertEqual(expected, actual)

  def test_split_nodes_delimiter_ends_text(self):
    this_node = TextNode("This is text with **BOLD WORDS**", TextType.TEXT)

    expected = [TextNode("This is text with ",TextType.TEXT), TextNode("BOLD WORDS", TextType.BOLD)]
    actual = TextNode.split_nodes_delimiter([this_node], TextType.BOLD)

    self.assertEqual(expected, actual)

  def test_split_nodes_delimiter_nested(self):
    this_node = TextNode("This is text with **BOLD *Italic* WORD**", TextType.TEXT)

    expected = [TextNode("This is text with ",TextType.TEXT), TextNode("BOLD *Italic* WORD", TextType.BOLD)]
    actual = TextNode.split_nodes_delimiter([this_node], TextType.BOLD)

    self.assertEqual(expected, actual)

  def test_extract_markdown_images_multiple(self):
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

    expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
    actual = TextNode.extract_markdown_images(text)

    self.assertEqual(expected, actual)

  def test_extract_markdown_images_single(self):
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif), what a pic!"

    expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
    actual = TextNode.extract_markdown_images(text)

    self.assertEqual(expected, actual)

  def test_extract_markdown_images_missing_link(self):
    text = "This is text with a ![rick roll], what a pic!"

    expected = []
    actual = TextNode.extract_markdown_images(text)

    self.assertEqual(expected, actual)

  def test_extract_markdown_images_sqaure_brackets_in_alt_text(self):
    text = "This is text with a ![rick [SQUARE BRACKETS] roll](https://i.imgur.com/aKaOqIh.gif), what a pic!"

    expected = [("rick [SQUARE BRACKETS] roll", "https://i.imgur.com/aKaOqIh.gif")]
    actual = TextNode.extract_markdown_images(text)

    self.assertEqual(expected, actual)

  def test_extract_markdown_images_sqaure_brackets_in_alt_text_nested(self):
    text = "This is text with a ![rick [[SQUARE BRACKETS]] roll](https://i.imgur.com/aKaOqIh.gif), what a pic!"

    expected = [("rick [[SQUARE BRACKETS]] roll", "https://i.imgur.com/aKaOqIh.gif")]
    actual = TextNode.extract_markdown_images(text)

    self.assertEqual(expected, actual)

  def test_extract_markdown_images_sqaure_brackets_in_alt_text_siblings(self):
    text = "This is text with a ![rick [SQUARE] [BRACKETS] roll](https://i.imgur.com/aKaOqIh.gif), what a pic!"

    expected = [("rick [SQUARE] [BRACKETS] roll", "https://i.imgur.com/aKaOqIh.gif")]
    actual = TextNode.extract_markdown_images(text)

    self.assertEqual(expected, actual)
  
  def test_extract_markdown_images_empty_alt_text(self):
    text = "This is text with a ![](https://i.imgur.com/aKaOqIh.gif), what a pic!"

    expected = [("", "https://i.imgur.com/aKaOqIh.gif")]
    actual = TextNode.extract_markdown_images(text)

    self.assertEqual(expected, actual)

  def test_extract_markdown_images_parentheses_in_link(self):
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh(2).gif), what a pic!"

    expected = [("rick roll", "https://i.imgur.com/aKaOqIh(2).gif")]
    actual = TextNode.extract_markdown_images(text)

    self.assertEqual(expected, actual)

  def test_extract_markdown_images_special_chars_in_alt_text(self):
    text = "This is text with a ![rick roll !@#$](https://i.imgur.com/aKaOqIh.gif), what a pic!"

    expected = [("rick roll !@#$", "https://i.imgur.com/aKaOqIh.gif")]
    actual = TextNode.extract_markdown_images(text)

    self.assertEqual(expected, actual)

  def test_extract_markdown_images_malformed_markdown_alttext(self):
    text = "This is text with a ![rick roll(https://i.imgur.com/aKaOqIh.gif), what a pic!"

    expected = []
    actual = TextNode.extract_markdown_images(text)

    self.assertEqual(expected, actual)

  def test_extract_markdown_images_malformed_markdown_url(self):
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif, what a pic!"

    expected = []
    actual = TextNode.extract_markdown_images(text)

    self.assertEqual(expected, actual)

  def test_extract_markdown_links_multiple(self):
    text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

    expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
    actual = TextNode.extract_markdown_links(text)

    self.assertEqual(expected, actual)

  def test_extract_markdown_link_single(self):
    text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif), what a pic!"

    expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
    actual = TextNode.extract_markdown_links(text)

    self.assertEqual(expected, actual)

  def test_extract_markdown_link_missing_url(self):
    text = "This is text with a [rick roll], what a pic!"

    expected = []
    actual = TextNode.extract_markdown_links(text)

    self.assertEqual(expected, actual)

  def test_extract_markdown_links_sqaure_brackets_in_anchor_text(self):
    text = "This is text with a [rick [SQUARE BRACKETS] roll](https://i.imgur.com/aKaOqIh.gif), what a pic!"

    expected = [("rick [SQUARE BRACKETS] roll", "https://i.imgur.com/aKaOqIh.gif")]
    actual = TextNode.extract_markdown_links(text)

    self.assertEqual(expected, actual)

  def test_extract_markdown_links_sqaure_brackets_in_anchor_text_nested(self):
    text = "This is text with a [rick [[SQUARE BRACKETS]] roll](https://i.imgur.com/aKaOqIh.gif), what a pic!"

    expected = [("rick [[SQUARE BRACKETS]] roll", "https://i.imgur.com/aKaOqIh.gif")]
    actual = TextNode.extract_markdown_links(text)

    self.assertEqual(expected, actual)

  def test_extract_markdown_links_sqaure_brackets_in_anchor_text_siblings(self):
    text = "This is text with a [rick [SQUARE] [BRACKETS] roll](https://i.imgur.com/aKaOqIh.gif), what a pic!"

    expected = [("rick [SQUARE] [BRACKETS] roll", "https://i.imgur.com/aKaOqIh.gif")]
    actual = TextNode.extract_markdown_links(text)

    self.assertEqual(expected, actual)
  
  def test_extract_markdown_links_empty_anchor_text(self):
    text = "This is text with a [](https://i.imgur.com/aKaOqIh.gif), what a pic!"

    expected = [("", "https://i.imgur.com/aKaOqIh.gif")]
    actual = TextNode.extract_markdown_links(text)

    self.assertEqual(expected, actual)
    
  def test_extract_markdown_links_parentheses_in_url(self):
    text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh(2).gif), what a pic!"

    expected = [("rick roll", "https://i.imgur.com/aKaOqIh(2).gif")]
    actual = TextNode.extract_markdown_links(text)

    self.assertEqual(expected, actual)

  def test_extract_markdown_links_special_chars_in_anchor_text(self):
    text = "This is text with a [rick roll !@#$](https://i.imgur.com/aKaOqIh.gif), what a pic!"

    expected = [("rick roll !@#$", "https://i.imgur.com/aKaOqIh.gif")]
    actual = TextNode.extract_markdown_links(text)

    self.assertEqual(expected, actual)

  def test_extract_markdown_links_malformed_markdown_anchor_text(self):
    text = "This is text with a [rick roll(https://i.imgur.com/aKaOqIh.gif), what a pic!"

    expected = []
    actual = TextNode.extract_markdown_links(text)

    self.assertEqual(expected, actual)

  def test_extract_markdown_links_malformed_markdown_url(self):
    text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif, what a pic!"

    expected = []
    actual = TextNode.extract_markdown_links(text)

    self.assertEqual(expected, actual)

  def test_split_node_image(self):
    old_nodes = [TextNode("This is text with an image ![to boot dev](https://www.boot.dev)", TextType.TEXT)]
    
    expected = [
      TextNode("This is text with an image ", TextType.TEXT),
      TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev")
      ]
    actual = TextNode.split_nodes_image(old_nodes)

    self.assertEqual(expected, actual)

  def test_split_node_image_start(self):
    old_nodes = [TextNode("![to boot dev](https://www.boot.dev) This text is with the above image", TextType.TEXT)]
    
    expected = [
      TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
      TextNode(" This text is with the above image", TextType.TEXT)
      ]
    actual = TextNode.split_nodes_image(old_nodes)

    self.assertEqual(expected, actual)

  def test_split_node_image_end(self):
    old_nodes = [TextNode("This is text with an image ![to boot dev](https://www.boot.dev) ", TextType.TEXT)]
    
    expected = [
      TextNode("This is text with an image ", TextType.TEXT),
      TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev")
      ]
    actual = TextNode.split_nodes_image(old_nodes)

    self.assertEqual(expected, actual)

  def test_split_node_image_multiple(self):
    old_nodes = [TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)]

    expected = [
      TextNode("This is text with a ", TextType.TEXT),
      TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
      TextNode(" and ", TextType.TEXT),
      TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")]
    actual = TextNode.split_nodes_image(old_nodes)

    self.assertEqual(expected, actual)

  def test_split_node_image_empty_text_between_images(self):
    old_nodes = [TextNode("This is text with multiple links with empty text between ![rick roll](https://i.imgur.com/aKaOqIh.gif) ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)]

    expected = [
      TextNode("This is text with multiple links with empty text between ", TextType.TEXT),
      TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
      TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")]      
    actual = TextNode.split_nodes_image(old_nodes)

    self.assertEqual(expected, actual)

  def test_split_node_image_invalid_markdown_syntax(self):
    old_nodes = [TextNode("This is text with an image ![to boot dev](https://www.boot.dev", TextType.TEXT)]

    expected = [TextNode("This is text with an image ![to boot dev](https://www.boot.dev", TextType.TEXT)]
    actual = TextNode.split_nodes_image(old_nodes)

    self.assertEqual(expected, actual)

  def test_split_node_link(self):
    old_nodes = [TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.TEXT)]
    
    expected = [
      TextNode("This is text with a link ", TextType.TEXT),
      TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
      ]
    actual = TextNode.split_nodes_link(old_nodes)

    self.assertEqual(expected, actual)

  def test_split_node_link_start(self):
    old_nodes = [TextNode("[to boot dev](https://www.boot.dev) This text is with the above link", TextType.TEXT)]
    
    expected = [
      TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
      TextNode(" This text is with the above link", TextType.TEXT)
      ]
    actual = TextNode.split_nodes_link(old_nodes)

    self.assertEqual(expected, actual)

  def test_split_node_link_end(self):
    old_nodes = [TextNode("This is text with an link [to boot dev](https://www.boot.dev) ", TextType.TEXT)]
    
    expected = [
      TextNode("This is text with an link ", TextType.TEXT),
      TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
      ]
    actual = TextNode.split_nodes_link(old_nodes)

    self.assertEqual(expected, actual)

  def test_split_node_link_multiple(self):
    old_nodes = [TextNode("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)]

    expected = [
      TextNode("This is text with a ", TextType.TEXT),
      TextNode("rick roll", TextType.LINK, "https://i.imgur.com/aKaOqIh.gif"),
      TextNode(" and ", TextType.TEXT),
      TextNode("obi wan", TextType.LINK, "https://i.imgur.com/fJRm4Vk.jpeg")]
    actual = TextNode.split_nodes_link(old_nodes)

    self.assertEqual(expected, actual)

  def test_split_node_link_empty_text_between_images(self):
    old_nodes = [TextNode("This is text with multiple links with empty text between [rick roll](https://i.imgur.com/aKaOqIh.gif) [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)]

    expected = [
      TextNode("This is text with multiple links with empty text between ", TextType.TEXT),
      TextNode("rick roll", TextType.LINK, "https://i.imgur.com/aKaOqIh.gif"),
      TextNode("obi wan", TextType.LINK, "https://i.imgur.com/fJRm4Vk.jpeg")]      
    actual = TextNode.split_nodes_link(old_nodes)

    self.assertEqual(expected, actual)

  def test_split_node_image_invalid_markdown_syntax(self):
    old_nodes = [TextNode("This is text with an link [to boot dev](https://www.boot.dev", TextType.TEXT)]

    expected = [TextNode("This is text with an link [to boot dev](https://www.boot.dev", TextType.TEXT)]
    actual = TextNode.split_nodes_link(old_nodes)

    self.assertEqual(expected, actual)

  def test_text_to_textnodes(self):
    text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

    expected = [
      TextNode("This is ", TextType.TEXT),
      TextNode("text", TextType.BOLD),
      TextNode(" with an ", TextType.TEXT),
      TextNode("italic", TextType.ITALIC),
      TextNode(" word and a ", TextType.TEXT),
      TextNode("code block", TextType.CODE),
      TextNode(" and an ", TextType.TEXT),
      TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
      TextNode(" and a ", TextType.TEXT),
      TextNode("link", TextType.LINK, "https://boot.dev"),
    ]
    actual = TextNode.text_to_textnodes(text)

    self.assertEqual(expected, actual)

  def test_text_to_textnodes_empty_text(self):
    text = ""

    expected = []
    actual = TextNode.text_to_textnodes(text)

    self.assertEqual(expected, actual)

  def test_text_to_textnodes_nested_markup_not_supported(self):
    text = "This is **bolded text with an *italic* word nested inside** and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

    expected = [
      TextNode("This is ", TextType.TEXT),
      TextNode("bolded text with an *italic* word nested inside", TextType.BOLD),
      TextNode(" and a ", TextType.TEXT),
      TextNode("code block", TextType.CODE),
      TextNode(" and an ", TextType.TEXT),
      TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
      TextNode(" and a ", TextType.TEXT),
      TextNode("link", TextType.LINK, "https://boot.dev"),
    ]
    actual = TextNode.text_to_textnodes(text)

    self.assertEqual(expected, actual)

  def test_text_to_textnodes_malformed_delimiters_BOLD(self):
    text = "This is **text with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

    self.assertRaises(Exception, TextNode.text_to_textnodes(text))

  def test_text_to_textnodes_malformed_delimiters_ITALIC(self):
    text = "This is **text** with an *italic word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

    self.assertRaises(Exception, TextNode.text_to_textnodes(text))

  def test_text_to_textnodes_malformed_delimiters_CODE(self):
    text = "This is **text** with an *italic* word and a `code block and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

    self.assertRaises(Exception, TextNode.text_to_textnodes(text))


if __name__ == "__main__":
  unittest.main()