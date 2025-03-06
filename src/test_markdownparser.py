import unittest

from leafnode import LeafNode
from markdown_parser import BlockType, MarkdownParser
from parentnode import ParentNode


class MarkdownParserTest(unittest.TestCase):

  def test_markdown_to_blocks(self):
    markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""

    expected = ["# This is a heading", 
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]
    actual = MarkdownParser.markdown_to_blocks(markdown)

    self.assertEqual(expected, actual)

  def test_block_to_block_type_code(self):
    markdown = '```print("Hello World!")```'

    expected =  BlockType.CODE
    actual = MarkdownParser.block_to_block_type(markdown)

    self.assertEqual(expected, actual)

  def test_block_to_block_type_code_multiline(self):
    markdown = '''```
def find_all(self: str, pattern: str) -> Iterator[Tuple[int, str]]:

  # base case: the first search, if pattern is not found, while loop will be skipped and the iterator will be empty
  i = self.find(pattern)

  # loop: continue the search and return more matches
  while i != -1:
    yield i
    i = self.find(pattern, i + 1)```'''
    expected = BlockType.CODE
    actual = MarkdownParser.block_to_block_type(markdown)

    self.assertEqual(expected, actual)

  def test_block_to_block_type_heading1(self):
    markdown = '# Heading 1'

    expected = BlockType.HEADING
    actual = MarkdownParser.block_to_block_type(markdown)

    self.assertEqual(expected, actual)

  def test_block_to_block_type_heading2(self):
    markdown = '## Heading 2'

    expected = BlockType.HEADING
    actual = MarkdownParser.block_to_block_type(markdown)

    self.assertEqual(expected, actual)

  def test_block_to_block_type_heading3(self):
    markdown = '### Heading 3'

    expected = BlockType.HEADING
    actual = MarkdownParser.block_to_block_type(markdown)

    self.assertEqual(expected, actual)

  def test_block_to_block_type_heading4(self):
    markdown = '#### Heading 4'

    expected = BlockType.HEADING
    actual = MarkdownParser.block_to_block_type(markdown)

    self.assertEqual(expected, actual)
    
  def test_block_to_block_type_heading5(self):
    markdown = '##### Heading 5'

    expected = BlockType.HEADING
    actual = MarkdownParser.block_to_block_type(markdown)

    self.assertEqual(expected, actual)

  def test_block_to_block_type_heading6(self):
    markdown = '###### Heading 6'

    expected = BlockType.HEADING
    actual = MarkdownParser.block_to_block_type(markdown)

    self.assertEqual(expected, actual)
 
  def test_block_to_block_type_ordered_list_single(self):
    markdown = '1. First Item'

    expected = BlockType.ORDERED_LIST
    actual = MarkdownParser.block_to_block_type(markdown)

    self.assertEqual(expected, actual)

  def test_block_to_block_type_ordered_list_double(self):
    markdown = '''1. First Item
2. Second Item'''

    expected = BlockType.ORDERED_LIST
    actual = MarkdownParser.block_to_block_type(markdown)

    self.assertEqual(expected, actual)

  def test_block_to_block_type_ordered_list_ten_items(self):
    markdown = '''1. First Item
2. Second Item
3. Third Item
4. Fourth Item
5. Fifth Item
6. Sixth Item
7. Seventh Item
8. Eighth Item
9. Nineth Item
10. Tenth Item'''

    expected = BlockType.ORDERED_LIST
    actual = MarkdownParser.block_to_block_type(markdown)

    self.assertEqual(expected, actual)

  def test_block_to_block_type_quote_single(self):
    markdown = '>Single line quote'

    expected = BlockType.QUOTE
    actual = MarkdownParser.block_to_block_type(markdown)

    self.assertEqual(expected, actual)    

  def test_block_to_block_type_quote_double(self):
    markdown = '''>Single line quote
>Second line quote'''

    expected = BlockType.QUOTE
    actual = MarkdownParser.block_to_block_type(markdown)

    self.assertEqual(expected, actual)    

  def test_block_to_block_type_quote_ten_lines(self):
    markdown = '''>First line
>Second line
>Third line
>Fourth line
>Fifth line
>Sixth line
>Seventh line
>Eighth line
>Nineth line
>Tenth line'''

    expected = BlockType.QUOTE
    actual = MarkdownParser.block_to_block_type(markdown)

    self.assertEqual(expected, actual)

  def test_block_to_block_type_unordered_list_single(self):
    markdown = '* First Item'

    expected = BlockType.UNORDERED_LIST
    actual = MarkdownParser.block_to_block_type(markdown)

    self.assertEqual(expected, actual)

  def test_block_to_block_type_unordered_list_double(self):
    markdown = '''* First Item
* Second Item'''

    expected = BlockType.UNORDERED_LIST
    actual = MarkdownParser.block_to_block_type(markdown)

    self.assertEqual(expected, actual)

  def test_block_to_block_type_unordered_list_ten_items(self):
    markdown = '''* First Item
* Second Item
* Third Item
* Fourth Item
* Fifth Item
* Sixth Item
* Seventh Item
* Eighth Item
* Nineth Item
* Tenth Item'''

    expected = BlockType.UNORDERED_LIST
    actual = MarkdownParser.block_to_block_type(markdown)

    self.assertEqual(expected, actual)

  def test_block_to_block_type_unordered_list_single_alt_markup(self):
    markdown = '- First Item'

    expected = BlockType.UNORDERED_LIST
    actual = MarkdownParser.block_to_block_type(markdown)

    self.assertEqual(expected, actual)

  def test_block_to_block_type_unordered_list_double_alt_markup(self):
    markdown = '''- First Item
- Second Item'''

    expected = BlockType.UNORDERED_LIST
    actual = MarkdownParser.block_to_block_type(markdown)

    self.assertEqual(expected, actual)

  def test_block_to_block_type_unordered_list_ten_items_alt_markup(self):
    markdown = '''- First Item
- Second Item
- Third Item
- Fourth Item
- Fifth Item
- Sixth Item
- Seventh Item
- Eighth Item
- Nineth Item
- Tenth Item'''

    expected = BlockType.UNORDERED_LIST
    actual = MarkdownParser.block_to_block_type(markdown)

    self.assertEqual(expected, actual)

  def test_block_to_block_type_paragraph(self):
    markdown = 'This is a plain paragraph'

    expected = BlockType.PARAGRAPH
    actual = MarkdownParser.block_to_block_type(markdown)

    self.assertEqual(expected, actual)

  def test_markdown_to_html_node_empty_document(self):
    markdown = ''

    expected = None
    actual = MarkdownParser.markdown_to_html_node(markdown)

    self.assertEqual(expected, actual)

  def test_markdown_to_html_node_single_paragraph(self):
    markdown = 'A simple paragraph'

    expected = ParentNode("div", [ ParentNode("p", [ LeafNode("A simple paragraph")])])
    actual = MarkdownParser.markdown_to_html_node(markdown)

    self.assertEqual(expected, actual)

  def test_markdown_to_html_node_multiple_paragraphs_with_different_new_lines(self):
    markdown = '''1st paragraph

2nd paragraph



3rd paragraph'''

    expected = ParentNode("div", [ ParentNode("p", [ LeafNode("1st paragraph")]),
                                   ParentNode("p", [ LeafNode("2nd paragraph")]),
                                   ParentNode("p", [ LeafNode("3rd paragraph")])])
    actual = MarkdownParser.markdown_to_html_node(markdown)

    self.assertEqual(expected, actual)

  def test_markdown_to_html_node_headings(self):
    markdown = '''# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6'''

    expected = ParentNode("div", [ ParentNode("h1", [ LeafNode("Heading 1")]),
                                   ParentNode("h2", [ LeafNode("Heading 2")]),
                                   ParentNode("h3", [ LeafNode("Heading 3")]),
                                   ParentNode("h4", [ LeafNode("Heading 4")]),
                                   ParentNode("h5", [ LeafNode("Heading 5")]),
                                   ParentNode("h6", [ LeafNode("Heading 6")])
                                 ])
    actual = MarkdownParser.markdown_to_html_node(markdown)

    self.assertEqual(expected, actual)

  def test_markdown_to_html_node_list_unordered_single(self):
    markdown = '* First Item'

    expected = ParentNode("div", 
                [ ParentNode("ul", 
                  [
                    ParentNode("li", [ LeafNode("First Item") ]),
                  ])])
    actual = MarkdownParser.markdown_to_html_node(markdown)

    self.assertEqual(expected, actual)

  def test_markdown_to_html_node_list_unordered_multiple(self):
    markdown = '''* First Item
* Second Item
* Third Item
* Fourth Item
* Fifth Item
* Sixth Item
* Seventh Item
* Eighth Item
* Nineth Item
* Tenth Item'''

    expected = ParentNode("div", 
                [ ParentNode("ul", 
                  [
                    ParentNode(tag="li", children=[ LeafNode("First Item") ]),
                    ParentNode(tag="li", children=[ LeafNode("Second Item") ]),
                    ParentNode(tag="li", children=[ LeafNode("Third Item") ]),
                    ParentNode(tag="li", children=[ LeafNode("Fourth Item") ]),
                    ParentNode(tag="li", children=[ LeafNode("Fifth Item") ]),
                    ParentNode(tag="li", children=[ LeafNode("Sixth Item") ]),
                    ParentNode(tag="li", children=[ LeafNode("Seventh Item") ]),
                    ParentNode(tag="li", children=[ LeafNode("Eighth Item") ]),
                    ParentNode(tag="li", children=[ LeafNode("Nineth Item") ]),
                    ParentNode(tag="li", children=[ LeafNode("Tenth Item") ])
                  ])])
    actual = MarkdownParser.markdown_to_html_node(markdown)

    self.assertEqual(expected, actual)    

  def test_markdown_to_html_node_list_ordered_single(self):
    markdown = '1. First Item'

    expected = ParentNode("div", 
                [ ParentNode("ol", 
                  [
                    ParentNode("li", [ LeafNode("First Item") ])
                  ])])
    actual = MarkdownParser.markdown_to_html_node(markdown)
    
    self.assertEqual(expected, actual)

  def test_markdown_to_html_node_list_ordered_multiple(self):
    markdown = '''1. First Item
2. Second Item
3. Third Item
4. Fourth Item
5. Fifth Item
6. Sixth Item
7. Seventh Item
8. Eighth Item
9. Nineth Item
10. Tenth Item'''

    expected = ParentNode("div", 
                [ ParentNode("ol", 
                  [
                    ParentNode(tag="li", children=[ LeafNode("First Item") ]),
                    ParentNode(tag="li", children=[ LeafNode("Second Item") ]),
                    ParentNode(tag="li", children=[ LeafNode("Third Item") ]),
                    ParentNode(tag="li", children=[ LeafNode("Fourth Item") ]),
                    ParentNode(tag="li", children=[ LeafNode("Fifth Item") ]),
                    ParentNode(tag="li", children=[ LeafNode("Sixth Item") ]),
                    ParentNode(tag="li", children=[ LeafNode("Seventh Item") ]),
                    ParentNode(tag="li", children=[ LeafNode("Eighth Item") ]),
                    ParentNode(tag="li", children=[ LeafNode("Nineth Item") ]),
                    ParentNode(tag="li", children=[ LeafNode("Tenth Item") ])
                  ])])
    actual = MarkdownParser.markdown_to_html_node(markdown)

    self.assertEqual(expected, actual)      

  def test_markdown_to_html_node_list_unordered_multiple_lines_between(self):
    markdown = '''* First Item

* Second Item


* Third Item'''    

    expected = ParentNode("div", 
                [ ParentNode("ul", 
                  [
                    ParentNode("li", [ LeafNode("First Item") ]),
                    ParentNode("li", [ LeafNode("Second Item") ]),
                    ParentNode("li", [ LeafNode("Third Item") ])
                  ])])
    actual = MarkdownParser.markdown_to_html_node(markdown)

    self.assertEqual(expected, actual)

  def test_markdown_to_html_node_code_language_specifier(self):
    markdown = '''``` Python
def find_all(self: str, pattern: str) -> Iterator[Tuple[int, str]]:

  # base case: the first search, if pattern is not found, while loop will be skipped and the iterator will be empty
  i = self.find(pattern)

  # loop: continue the search and return more matches
  while i != -1:
    yield i
    i = self.find(pattern, i + 1)```'''
    
    expected = ParentNode("div", 
                [ ParentNode("pre", 
                  [
                    ParentNode("code", 
                    [ LeafNode(markdown.strip("```")) ])
                  ])])
    actual = MarkdownParser.markdown_to_html_node(markdown)

    self.assertEqual(expected, actual)

  def test_markdown_to_html_node_code_no_language_specifier(self):
    markdown = '''``` def find_all(self: str, pattern: str) -> Iterator[Tuple[int, str]]:

  # base case: the first search, if pattern is not found, while loop will be skipped and the iterator will be empty
  i = self.find(pattern)

  # loop: continue the search and return more matches
  while i != -1:
    yield i
    i = self.find(pattern, i + 1)```'''
    
    expected = ParentNode("div", 
                [ ParentNode("pre", 
                  [
                    ParentNode("code", 
                    [ LeafNode(markdown.strip("```")) ])
                  ])])
    actual = MarkdownParser.markdown_to_html_node(markdown)

    self.assertEqual(expected, actual)

  def test_markdown_to_html_node_quote_single_line(self):
    markdown = "> Single Line Quote"

    expected = ParentNode("div", 
                [ ParentNode("blockquote",
                  [ 
                    LeafNode("Single Line Quote")
                  ])
                ])
    actual = MarkdownParser.markdown_to_html_node(markdown)
    self.assertEqual(expected, actual)

  def test_markdown_to_html_node_quote_multi_line(self):
    markdown = '''> Multi Line Quote #1
> Multi Line Quote #2'''

    expected = ParentNode("div", 
                [ ParentNode("blockquote",
                  [ 
                    LeafNode("Multi Line Quote #1\nMulti Line Quote #2"), 
                  ])
                ])
    actual = MarkdownParser.markdown_to_html_node(markdown)

    self.assertEqual(expected, actual)

  def test_markdown_to_html_node_quote_multi_line_with_empty_line_between(self):
    markdown = '''> Multi Line Quote #1
> 
> Multi Line Quote #2'''

    expected = ParentNode("div", 
                [ ParentNode("blockquote",
                  [ 
                    LeafNode("Multi Line Quote #1\n\nMulti Line Quote #2"), 
                  ])
                ])
    actual = MarkdownParser.markdown_to_html_node(markdown)
    self.assertEqual(expected, actual)

  def test_markdown_to_html_node_quote_multi_line_with_empty_line_between_no_marker(self):
    markdown = '''> Multi Line Quote #1
 
> Multi Line Quote #2'''

    expected = ParentNode("div", 
                [ ParentNode("blockquote",
                  [ 
                    LeafNode("Multi Line Quote #1"), 
                  ]),
                  ParentNode("blockquote",
                  [ 
                    LeafNode("Multi Line Quote #2"), 
                  ])
                ])
    actual = MarkdownParser.markdown_to_html_node(markdown)
    self.assertEqual(expected, actual)

  def test_markdown_to_html_node_quote_nested(self):
    markdown = '''> Outer block quote
> > Inner block quote
> Back to outer block quote'''

    expected = ParentNode("div",
                [ ParentNode("blockquote",
                  [
                    LeafNode("Outer block quote"),
                    ParentNode("blockquote",
                      [
                        LeafNode("Inner block quote")
                      ]),
                    LeafNode("Back to outer block quote")
                  ])
                ])
    actual = MarkdownParser.markdown_to_html_node(markdown)
    self.assertEqual(expected, actual)

  def test_markdown_to_html_node_quote_nested_complex(self):
    markdown = '''> Level 1
>> Level 2
>>> Level 3
> Back to 1
>> Back to 2
> End at 1'''

    expected = ParentNode("div",
                [ ParentNode("blockquote",
                  [
                    LeafNode("Level 1"),
                    ParentNode("blockquote",
                      [
                        LeafNode("Level 2"),
                        ParentNode("blockquote",
                        [
                          LeafNode("Level 3")
                        ])
                      ]),
                    LeafNode("Back to 1"),
                    ParentNode("blockquote",
                    [
                      LeafNode("Back to 2")
                    ]),
                    LeafNode("End at 1")
                  ])
                ])
    actual = MarkdownParser.markdown_to_html_node(markdown)
    self.assertEqual(expected, actual)

  def test_extract_title_header_found(self):
    markdown = '''
# This is the title

This is the 1st paragraph'''

    expected = "This is the title"
    actual = MarkdownParser.extract_title(markdown)

    self.assertEqual(expected, actual)

  def test_extract_title_header_not_found(self):
    markdown = '''
This is NOT the title

This is the 1st paragraph'''
    
    with self.assertRaises(Exception):
      MarkdownParser.extract_title(markdown)

  def test_extract_title_header_only_h2_with_space(self):
    markdown = '''
## This is NOT the top-level title

This is the 1st paragraph'''
    
    with self.assertRaises(Exception):
      MarkdownParser.extract_title(markdown)

  def test_extract_title_header_no_space_after_marker(self):
    markdown = '''
#This is the title

This is the 1st paragraph'''
    expected = "This is the title"
    actual = MarkdownParser.extract_title(markdown)

    self.assertEqual(expected, actual)
  
  def test_extract_title_header_marker_not_at_start(self):
    markdown = '''
This #is the title

This is the 1st paragraph'''
    with self.assertRaises(Exception):
      MarkdownParser.extract_title(markdown)
      
if __name__ == "__main__":
  unittest.main()
