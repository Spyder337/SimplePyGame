
class SceneGraph:
    root_node = None
    node_map = {}

    def __init__(self, rootNode):
        root_node = root_node
        pass
    pass

class SceneGraphNode:
    is_root = True
    is_leaf = True
    children = []
    parent = None
    game_obj = None

    def __init__(self, data, parent = None, childList = None):

        pass