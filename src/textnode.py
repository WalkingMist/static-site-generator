from enum import Enum
from typing import Callable, List, Tuple
from typing_extensions import Self
import re

from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from utilities import find_all, isEmptyOrWhitespaces

class TextType(Enum):
  TEXT = "text"
  BOLD = "bold"
  ITALIC = "italic"
  CODE = "code"
  LINK = "link"
  IMAGE = "image"

  def get_delimiters(self):
    match self:
      case TextType.TEXT:
        return None
      case TextType.BOLD:
        return ("**", "**")
      case TextType.ITALIC:
        return ("_", "_")
      case TextType.CODE:
        return ("`", "`")
      case TextType.LINK:
        return ("[", "](", ")")
      case TextType.IMAGE:
        return ("![", "](", ")")
      case _:
        raise ValueError("Unknown Enum value")

  def __str__(self) -> str:
    return str(self.value)
   
class TextNode:
  
  def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
    self.text = text
    self.text_type = text_type
    self.url = url

  def __eq__(self, other: object) -> bool: 
    if (not isinstance(other, TextNode)):
      return False
    
    return ((self.text == other.text) and 
            (self.text_type == other.text_type) and 
            (self.url == other.url))

  def __repr__(self) -> str:
    return f"TextNode({self.text}, {self.text_type}, {self.url})"
  
  def to_leafnode(self) -> LeafNode:
    match self.text_type:
      case TextType.TEXT:
        return LeafNode(self.text)
      case TextType.BOLD:
        return ParentNode("b", [ LeafNode(self.text) ])
      case TextType.ITALIC:
        return ParentNode("i", [ LeafNode(self.text) ])
      case TextType.CODE:
        return ParentNode("code", [ LeafNode(self.text) ])
      case TextType.LINK:
        return ParentNode("a", [ LeafNode(self.text) ], { "href": self.url })
      case TextType.IMAGE:
        return LeafNode("", "img", { "src": self.url, "alt": self.text })
      case _:
        raise Exception("unknown text type")
      
  def split_nodes_delimiter(old_nodes: List[Self], text_type: TextType) -> List[Self]:
    new_nodes: List[Self] = []
    delimiter: Tuple = text_type.get_delimiters()

    for node in old_nodes:
      if (node.text_type != TextType.TEXT or 
          text_type == TextType.LINK or 
          text_type == TextType.IMAGE or 
          delimiter == None):
        new_nodes.append(node)
      else:
        indices = find_all(node.text, delimiter[0])

        current_index = 0
        is_normal = True
        open_marker_found = False
        text_segment = ""

        for index in indices:
          text_segment = node.text[current_index: index]

          if (len(text_segment) != 0) and (len(text_segment.strip()) > 0):             
            if is_normal:
              new_nodes.append(TextNode(text_segment, TextType.TEXT)) 
            else:
              new_nodes.append(TextNode(text_segment, text_type))
              open_marker_found = False

          is_normal = not is_normal
          current_index = index + len(delimiter[0])
          
          if (current_index < len(node.text) and
             (text_type == TextType.BOLD or text_type == TextType.CODE or text_type == TextType.ITALIC)):
            open_marker_found = True

        if open_marker_found and not is_normal:
          raise Exception(f"Malformed {text_type} segment.")
 
        if(current_index < len(node.text)):
          text_segment = node.text[current_index:]

          if (len(text_segment) != 0) and (len(text_segment.strip()) > 0):             
            new_nodes.append(TextNode(text_segment, TextType.TEXT))

    return new_nodes               

  def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    pattern = r"!\[(.*?)\]\((([^()]|\([^()]*\))*)\)"

    all_matches = re.finditer(pattern, text)
    images = []

    for match in all_matches:
      alt_text = match.group(1)
      url = match.group(2)

      images.append((alt_text, url))
    
    return images

  def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    pattern = r"(?<!!)\[(.*?)\]\((([^()]|\([^()]*\))*)\)"

    all_matches = re.finditer(pattern, text)
    links = []

    for match in all_matches:
      anchor_text = match.group(1)
      url = match.group(2)

      links.append((anchor_text, url))

    return links
  
  def _get_pattern_format(target: Tuple[str, str], text_type: TextType) -> str:
    match text_type:
      case TextType.LINK:
        return f"[{target[0]}]({target[1]})"
      case TextType.IMAGE:
        return f"![{target[0]}]({target[1]})"
      case _:
        raise NotImplementedError()
          
  def _split_nodes_helper(
      old_nodes: List[Self],
      text_type: TextType,
      extraction_method: Callable,
      pattern_format: Callable[[str, str], str] = _get_pattern_format
  ) -> List[Self]:
    new_nodes: List[Self] = []

    for old_node in old_nodes:
      targets_in_node = extraction_method(old_node.text)

      if (len(targets_in_node) == 0):
        new_nodes.append(old_node)
      else:
        current_text = old_node.text
        for target in targets_in_node:
          tokens = current_text.split(pattern_format(target, text_type), 1)

          if (len(tokens[0].strip()) > 0):
            new_nodes.append(TextNode(tokens[0], TextType.TEXT))

          new_nodes.append(TextNode(target[0], text_type, target[1]))
          current_text = tokens[1] 

        if (len(current_text.strip()) != 0):
          new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes

  def split_nodes_image(old_nodes: List[Self]) -> List[Self]:
    return TextNode._split_nodes_helper(old_nodes, 
                                        TextType.IMAGE, 
                                        TextNode.extract_markdown_images
                                        )

  def split_nodes_link(old_nodes: List[Self]) -> List[Self]:
    return TextNode._split_nodes_helper(old_nodes, 
                                        TextType.LINK, 
                                        TextNode.extract_markdown_links
                                        )
    
  def text_to_textnodes(text: str) -> List[Self]:
    original_node = TextNode(text, TextType.TEXT)

    nodes_after_images_extraction = TextNode.split_nodes_image([original_node])
    nodes_after_links_extraction  = TextNode.split_nodes_link(nodes_after_images_extraction)
    nodes_after_bolds_extraction  = TextNode.split_nodes_delimiter(nodes_after_links_extraction,
                                                                   TextType.BOLD)
    nodes_after_italic_extraction = TextNode.split_nodes_delimiter(nodes_after_bolds_extraction,
                                                                   TextType.ITALIC)
    nodes_after_code_extraction = TextNode.split_nodes_delimiter(nodes_after_italic_extraction,
                                                                 TextType.CODE)
    return nodes_after_code_extraction
  
