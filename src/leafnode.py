from typing import Dict
from htmlnode import HTMLNode


class LeafNode(HTMLNode):
  def __init__(self, 
               value: str, 
               tag: str = None,  
               props: Dict[str, str] = None) -> None:
    super().__init__(tag, value, None, props)

  def to_html(self):
    if (self.value == None):
      raise ValueError("all leaf nodes must have a value")

    if (self.tag == None):
      return str(self.value)
    
    props_html: str = self.props_to_html()
    if(len(props_html) > 0):
      props_html = f" {props_html}"

    return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"  
  
  def __eq__(self, other: object) -> bool:
    if(not isinstance(other, LeafNode)):
      return False
    
    return ((self.value == other.value) and 
            (self.tag == other.tag) and 
            (self.props == other.props))
  