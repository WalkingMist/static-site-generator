import os
import shutil
import sys
from typing import List

from markdown_parser import MarkdownParser
from parentnode import ParentNode

def generate_page(from_path: str , template_path: str, dest_path: str, basepath: str) -> None:
  print(f"Generating pages from {from_path} to {dest_path} using {template_path}")

  template_file = open(template_path, "r")
  template = template_file.read()
  template_file.close()

  markdown_pages:List[str] = []
  for root, dirs, files in os.walk(from_path):
    for file in files:
      if file.endswith(".md"):
        markdown_pages.append(os.path.join(root, file))
    
  for page in markdown_pages:
    input_file = open(page, "r")
    markdown = input_file.read()
    input_file.close()

    page_title = MarkdownParser.extract_title(markdown)
    html_content = MarkdownParser.markdown_to_html_node(markdown).to_html()
    output_page = template.replace("{{ Title }}", page_title).replace("{{ Content }}", html_content)
    output_page = output_page.replace('href=/"', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    output_file_path = os.path.join(dest_path, 
                                    os.path.dirname(page).replace(from_path, "").lstrip("/"),
                                    f"{os.path.splitext(os.path.basename(page))[0]}.html")

    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    output_file = open(output_file_path, "w")
    output_file.write(output_page)
    output_file.close()

def recussive_copy(source: str, target: str) -> None:
  if not os.path.exists(source):
    raise Exception(f"source path {source}, does not exists.")
  
  if not os.path.exists(target):
    os.makedirs(target)
  
  entities_need_copying = os.listdir(source)
  for entity in entities_need_copying:
    final_path = os.path.join(source, entity)
    
    if not os.path.isfile(final_path):
      recussive_copy(final_path, os.path.join(target, entity))
    else:
      print(f"copying {final_path} to destination {target}...")
      shutil.copy(final_path, target)

def copy_static(static_path:str, output_path:str) -> None:
  source_path = os.path.join(os.getcwd(), static_path)
  recussive_copy(source_path, output_path)

def clear_output_directory(output_path:str) -> None:
  target_path = os.path.join(os.getcwd(), output_path)

  if os.path.exists(output_path):
    shutil.rmtree(target_path, ignore_errors = False)
    os.makedirs(target_path)

def main() -> None:
  basepath: str = sys.argv[0] if sys.argv[0] else "/"

  static_directory: str  = "./static"
  output_directory: str = "./docs"
  content_directory: str  = "./content"
  template_path: str = "./template.html"

  clear_output_directory(output_directory)
  copy_static(static_directory, output_directory)
  generate_page(content_directory, template_path, output_directory, basepath)

main()
