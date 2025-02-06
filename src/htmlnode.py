from typing import Dict, List
from typing_extensions import Self


class HTMLNode:
  def __init__(self, 
               tag: str = None, 
               value: str = None, 
               children: List[Self] = None,
               props: Dict[str, str] = None) -> None:
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def to_html(self: Self) -> str:
    raise NotImplementedError()  

  def props_to_html(self: Self) -> str:
    if(not self.props):
      return ""
    
    return " ".join(map(lambda x: f'{x[0]}="{x[1]}"', self.props.items()))
  
  def __repr__(self: Self) -> str:
    return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"