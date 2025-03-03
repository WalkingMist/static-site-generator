from markdown_parser import MarkdownParser
from parentnode import ParentNode

def main() -> None:
  markdown = '''
# Header 1

Paragraph 1

- Unorderlist Item 1
- Unorderlist Item 2

[Gmail](https://www.gmail.com)

![rick roll](https://i.imgur.com/aKaOqIh.gif)
'''
  document = MarkdownParser.markdown_to_html_node(markdown)
  
  if not isinstance(document, ParentNode):
    raise ValueError("Expected ParentNode for root div")

  print(document.to_html())

main()
