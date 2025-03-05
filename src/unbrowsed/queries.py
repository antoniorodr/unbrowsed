from typing import Optional

from selectolax.parser import Node
from selectolax.lexbor import LexborHTMLParser


class MultipleElementsFoundError(AssertionError):
    def __init__(self, text, count, query_type="label text"):
        query_all_method = f"query_all_by_{query_type.replace(' ', '_')}"
        super().__init__(
            f"Found {count} elements with {query_type} '{text}'. "
            f"Use {query_all_method} if multiple matches are expected."
        )


def query_by_label_text(dom: LexborHTMLParser, text: str) -> Optional[Node]:
    search_text = text.strip().lower()
    matches = []

    for label in dom.css("label"):
        label_text = label.text(deep=True, strip=True).lower()
        if search_text == label_text:
            target_id = label.attributes.get("for")
            if target_id:
                target = dom.css_first(f"#{target_id}")
                if target:
                    matches.append(target)

    if len(matches) > 1:
        raise MultipleElementsFoundError(text, len(matches), "label text")

    return matches[0] if matches else None


def query_by_text(dom: LexborHTMLParser, text: str) -> Optional[Node]:
    search_text = " ".join(text.strip().lower().split())
    matches = []

    for element in dom.css("*"):
        element_text = element.text(deep=True, strip=True).lower()
        element_text = " ".join(element_text.split())

        if element_text == search_text:
            matches.append(element)

    if len(matches) > 1:
        filtered_matches = [m for m in matches if m.tag not in ("html", "body")]

        if filtered_matches:
            matches = filtered_matches

        if len(matches) > 1:
            raise MultipleElementsFoundError(text, len(matches), "text")

    return matches[0] if matches else None
