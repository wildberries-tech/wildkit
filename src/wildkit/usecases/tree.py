

def print_list_as_tree(title: str, all_elems: list, id_prop: str, parent_id_prop: str):
    print(f"\n\n{title}:")
    _print_children_of(0, "", all_elems, id_prop, parent_id_prop)


def _print_children_of(elem_id, tab: str, all_elems: list, id_prop: str, parent_id_prop: str):
    if elem_id:
        children = [x for x in all_elems if getattr(x, parent_id_prop) == elem_id]
    else:
        children = [x for x in all_elems if not getattr(x, parent_id_prop)]

    for x in children:
        print(f"{tab}{x}")
        _print_children_of(getattr(x, id_prop), "    "+tab, all_elems, id_prop, parent_id_prop)
