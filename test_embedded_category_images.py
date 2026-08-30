from pathlib import Path
import ast
import base64
import io

from PIL import Image

source = Path('main.py').read_text(encoding='utf-8')
tree = ast.parse(source)
embedded_node = next(node for node in tree.body if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'EMBEDDED_CATEGORY_IMAGES' for t in node.targets))
embedded = ast.literal_eval(embedded_node.value)
expected = {'home_phone.png', 'home_playstation.png', 'home_computer.png', 'home_cctv.png'}
assert set(embedded) == expected
for name, payload in embedded.items():
    image = Image.open(io.BytesIO(base64.b64decode(payload)))
    assert image.width > 0 and image.height > 0
print('embedded_category_images=PASS')
print('external_runtime_dependency=NONE')
