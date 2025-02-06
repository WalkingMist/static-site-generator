from enum import Enum

from leafnode import LeafNode

class TextType(Enum):
  TEXT = "text",
  BOLD = "bold",
  ITALIC = "italic",
  CODE = "code",
  LINK = "link",
  IMAGE = "image"

  def __str__(self) -> str:
    return str(self.value[0])
  
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
        return LeafNode(self.text, "b")
      case TextType.ITALIC:
        return LeafNode(self.text, "i")
      case TextType.CODE:
        return LeafNode(self.text, "code")
      case TextType.LINK:
        return LeafNode(self.text, "a", { "href": self.url })
      case TextType.IMAGE:
        return LeafNode("", "img", { "src": self.url, "alt": self.text })
      case _:
        raise Exception("unknown text type")