
from textnode import TextNode, TextType


def main() -> None:
  newNode = TextNode("This is a text node",
                     TextType.BOLD,
                     "https://www.boot.dev")
  print(newNode)


main()
