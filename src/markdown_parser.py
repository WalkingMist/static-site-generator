import re

from enum import Enum
from typing import List
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode
from utilities import isEmptyOrWhitespaces


class BlockType(Enum):
  CODE = "code"
  HEADING = "heading"
  ORDERED_LIST = "ordered list"
  PARAGRAPH = "paragraph"
  QUOTE = "quote"
  UNORDERED_LIST = "unordered list"
  LINK = "link"
  IMAGE = "image"

  def __str__(self) -> str:
    return str(self.value)


class MarkdownParser:
  def is_quote_block(current_block:List[str]) -> bool:
    quote_found = False
    if current_block:
      quote_found = all(line.startswith(">") for line in current_block)

    return quote_found
  
  def is_code_block(current_block:List[str]) -> bool:
    code_found = False
    if current_block:
      code_found = current_block[0].startswith("```")

    return code_found
  
  def is_heading_block(current_block: List[str]) -> bool:
    heading_found = False
    if current_block:
      heading_found = (len(current_block) == 1 and current_block[0].startswith('#'))

    return heading_found
  
  def is_list_block(current_block: List[str]) -> bool:
    list_started = False
    if current_block:
      list_started = all(line.startswith("*") or line.startswith("-") or line[:1].isdigit() for line in current_block)

    return list_started
  
  def is_ordered_list_continuation(previous_lines: List[str], current_line:str) -> bool:
    # Get number of exisiting items
    item_count = len([l for l in previous_lines if l.strip()])

    # Next item should be number + 1
    expected_prefix = f"{item_count + 1}. "
    return current_line.startswith(expected_prefix) 
           
  def is_unordered_list_continuation(current_line: str) -> bool:
    return (current_line.startswith("*") or current_line.startswith("-"))
  
  def is_quote_continuation(current_line: str) -> bool:
    return current_line.startswith(">")

  def markdown_to_blocks(markdown: str) -> List[str]:
    blocks: List[str] = []
    current_block: List[str] = []
  
    for line in markdown.splitlines():
      if isEmptyOrWhitespaces(line): 
        if MarkdownParser.is_quote_block(current_block):
          blocks.append("\n".join(current_block))
          current_block = []
        elif not MarkdownParser.is_code_block(current_block):
          # Don't split block if next non-empty line contunues a list
          continue
      
      if MarkdownParser.is_code_block(current_block):
        current_block.append(line)

        if line.endswith("```"):
          blocks.append("\n".join(current_block))
          current_block = []
        
      elif line.startswith('#') and MarkdownParser.is_heading_block(current_block):
        blocks.append("\n".join(current_block))
        current_block = [ line ]

      # If we're in a list block and this line continues it
      elif current_block and MarkdownParser.is_list_block(current_block):
        if MarkdownParser.is_ordered_list_continuation(current_block, line) or \
           MarkdownParser.is_unordered_list_continuation(line):
          current_block.append(line)
        else:
          # Starts a new block
          blocks.append("\n".join(current_block))
          current_block = [ line ]
      
      elif current_block and MarkdownParser.is_quote_block(current_block):
        if MarkdownParser.is_quote_continuation(line):
          current_block.append(line)
        else:
          blocks.append("\n".join(current_block))
          current_block = [ line ]
      
      else:
          if current_block:
            blocks.append("\n".join(current_block))
          
          current_block = [ line ]

    # append the remaining content
    if current_block:
      blocks.append("\n".join(current_block))
    
    return blocks

  def block_to_block_type(block: str) -> BlockType:
    heading_pattern = r"^\#{1,6}\ "
    lines = block.splitlines()
    stripped_block = block.strip()

    if(re.search(heading_pattern, block)):
      return BlockType.HEADING
    elif(block.startswith("```") and block.endswith("```")):
      return BlockType.CODE
    elif(all(line.startswith(">") for line in lines)):
      return BlockType.QUOTE
    elif(all(line.startswith("* ") or line.startswith("- ") for line in lines)):
      return BlockType.UNORDERED_LIST
    elif(all(line.startswith(f"{i + 1}. ") for i, line in enumerate(lines))):
      return BlockType.ORDERED_LIST
    elif(stripped_block.startswith("![") and stripped_block.endswith(")")):
      return BlockType.IMAGE
    elif(stripped_block.startswith("[") and stripped_block.endswith(")")):
      return BlockType.LINK
    else:
      return BlockType.PARAGRAPH
    
  def text_to_children(block: str) -> List[HTMLNode]:
    children_as_text_nodes: List[TextNode] = TextNode.text_to_textnodes(block)
    html_nodes: List[HTMLNode] = [textNode.to_leafnode() for textNode in children_as_text_nodes]

    return html_nodes      

  def markdown_to_html_node(markdown: str) -> ParentNode:
    if isEmptyOrWhitespaces(markdown):
      return 
    
    blocks = MarkdownParser.markdown_to_blocks(markdown)
    html_nodes: List[HTMLNode] = []

    for block in blocks:
      if isEmptyOrWhitespaces(block):
        continue

      block_type = MarkdownParser.block_to_block_type(block)

      match block_type:
        case BlockType.CODE:
          code_node = ParentNode("code", [LeafNode(block.strip("```"))])
          html_nodes.append(ParentNode("pre", [ code_node ]))

        case BlockType.HEADING:
          heading_pattern = r"^(\#{1,6})\ ?"
          matches = re.match(heading_pattern, block)
          heading_level = matches[0].count("#") if matches else 0

          html_nodes.append(ParentNode(f'h{heading_level}', 
                                       MarkdownParser.text_to_children(block.lstrip("#").strip())))

        case BlockType.IMAGE:
          for node in MarkdownParser.text_to_children(block):
            html_nodes.append(node)
          
        case BlockType.LINK:
          for node in MarkdownParser.text_to_children(block):
            html_nodes.append(node)

        case BlockType.ORDERED_LIST:
          li_nodes = [
            ParentNode('li',
                       MarkdownParser.text_to_children(line.strip().lstrip("0123456789.").strip()))
            for line in block.splitlines()
            if line.strip()]
          html_nodes.append(ParentNode("ol",
                                       li_nodes))

        case BlockType.PARAGRAPH:
          html_nodes.append(ParentNode('p', 
                                       MarkdownParser.text_to_children(block)))
          
        case BlockType.QUOTE:
          pattern_for_marker = r"^([>|> ]+)"
          current_level = 0

          quotes: List[ParentNode] = []
          text_at_current_level: str = ""

          for line in block.splitlines():
            matches = re.match(pattern_for_marker, line)
            line_level = matches[0].count(">") if matches else 0
            
            if line_level != 0:
              if line_level > current_level:
                if text_at_current_level:
                  children = MarkdownParser.text_to_children(text_at_current_level)
                  for child in children:
                    quotes[-1].append_child(child)

                quotes.append(ParentNode("blockquote", []))
                text_at_current_level = line[len(matches[0]):].strip()
                current_level = line_level

              elif line_level < current_level:
                if text_at_current_level:
                  children = MarkdownParser.text_to_children(text_at_current_level)
                  for child in children:
                    quotes[-1].append_child(child)
                  
                while (current_level - line_level > 0):               
                  child_blockquote = quotes.pop()
                  quotes[-1].append_child(child_blockquote)
                  current_level -= 1

                text_at_current_level = line[len(matches[0]):].strip()

              elif line_level == current_level:
                text_at_current_level += "\n" + line[len(matches[0]):].strip()                
         
          if text_at_current_level:
            children = MarkdownParser.text_to_children(text_at_current_level)
            for child in children:
              quotes[-1].append_child(child)
            
          html_nodes.append(quotes[0])

        case BlockType.UNORDERED_LIST:
          li_nodes = [
            ParentNode('li',
                       MarkdownParser.text_to_children(line.strip().lstrip("*-").strip()))
            for line in block.splitlines()
            if line.strip()]

          html_nodes.append(ParentNode('ul',
                                       li_nodes))

          
    return ParentNode("div", html_nodes)

  def extract_title(markdown: str) -> str:
    lines = markdown.splitlines()
    h1_markdown_patter: str = r"^#(?!#)\s?"

    for line in lines:
      matches = re.match(h1_markdown_patter, line)
      
      if matches:
        return line[len(matches[0]):].strip()
      
    raise Exception("Header markup not found.")