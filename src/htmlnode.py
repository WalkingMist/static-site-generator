from abc import ABC, abstractmethod
from typing import Dict, List
from typing_extensions import Self


class HTMLNode(ABC):

  @abstractmethod
  def __init__(self, 
               tag: str = None, 
               value: str = None, 
               children: List[Self] = None,
               props: Dict[str, str] = None) -> None:
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  @abstractmethod
  def to_html(self: Self) -> str:
    pass  

  def props_to_html(self: Self) -> str:
    if(not self.props):
      return ""
    
    return " ".join(map(lambda x: f'{x[0]}="{x[1]}"', self.props.items()))
  
  def __repr__(self: Self) -> str:
    return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
  
  def __eq__(self: Self, other: object) -> bool:
    if (not isinstance(other, HTMLNode)):
      return False
    
    return ((self.tag == other.tag) and
            (self.value == other.value) and
            (self.children == other.children) and
            (self.props == other.props))