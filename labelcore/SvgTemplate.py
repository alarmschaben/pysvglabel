import xml.etree.ElementTree as ET
from typing import Any, Dict, Callable, Optional
from copy import deepcopy


class BadTemplateException(Exception):
  """Base class for all template errors."""
  pass


NAMESPACE = {
  'svg': 'http://www.w3.org/2000/svg',
}


def text_of(elt: ET.Element) -> str:
  subtexts = [text_of(child) for child in elt.findall('svg:tspan', NAMESPACE)]
  return (elt.text or "") + "".join(subtexts)


class SvgTemplate:
  @classmethod
  def visit(cls, elt: ET.Element, fn: Callable[[ET.Element], None]) -> None:
    fn(elt)
    for child in elt.findall('svg:g', NAMESPACE):
      cls.visit(child, fn)

  def __init__(self, root: ET.ElementTree):
    self.root = root
    self.env: Optional[Dict[str, Any]] = None

    def replace_start(elt: ET.Element) -> None:
      for child in elt.findall('svg:text', NAMESPACE):
        child_text = text_of(child)
        if child_text.startswith('🏁'):
          if self.env is not None:
            raise BadTemplateException("multiple starting blocks (textboxes starting with 🏁) found")

          start_code = child_text.strip('🏁')
          print(start_code)

          self.env = {}  # TODO actually run the block and get the env


          elt.remove(child)


    self.visit(self.root.getroot(), replace_start)

    # look for an init block and run it
    # for child in self.root.getroot():
    #   print(child.tag)

  def create_sheet(self) -> ET.ElementTree:  # TODO proper ETree type
    raise NotImplementedError

  def apply(self, row: Dict[str, str]) -> ET.Element:
    new = deepcopy(self.root.getroot())
    raise NotImplementedError
    return new
