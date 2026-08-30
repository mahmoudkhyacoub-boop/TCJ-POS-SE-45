from pathlib import Path
from PIL import Image

root = Path('/home/ubuntu/trend_center_advanced/brand_logos')
required = ['apple.png', 'samsung.png', 'xiaomi.png', 'hp.png', 'dell.png', 'lenovo.png', 'playstation.png', 'hikvision.png', 'dahua.png']
for name in required:
    path = root / name
    assert path.exists(), name
    with Image.open(path) as image:
        assert image.width > 0 and image.height > 0, name
        assert image.mode in ('RGBA', 'RGB'), (name, image.mode)
print('V133 theme assets passed:', len(required), 'brand logos')
