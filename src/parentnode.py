from typing import Dict, List
from htmlnode import HTMLNode
from leafnode import LeafNode


class ParentNode(HTMLNode):
  def __init__(self, 
               tag: str, 
               children: List[HTMLNode], 
               props: Dict[str, str] = None) -> None:
    super().__init__(tag, None, children, props)

  def append_child(self, child: HTMLNode) -> None:
    self.children.append(child)

  def __repr__(self) -> str:
    return f"ParentNode({self.tag}, {self.children}, {self.props})"
   
  def to_html(self) -> str:

    if(self.tag == None):
      raise ValueError("all parent nodes must have a tag")
    
    if(self.children == None):
      raise ValueError(f"a parent node must have at lease 1 child, current node: {self}")
    
    children_html = "" 
    for child in self.children:
      children_html = children_html + child.to_html()

    props_html: str = self.props_to_html()
    if(len(props_html) > 0):
      props_html = f" {props_html}"

    return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"