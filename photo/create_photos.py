from PIL import Image, ImageDraw, ImageFont
import pillow_heif
import os
import zipfile

# =============================
# ⚙️ НАСТРОЙКИ ПОЛЬЗОВАТЕЛЯ
# =============================

FORMAT = "PNG"   # 👉 варианты: HEIF, PJPEG, JPEG, PNG, BMP, TIFF, GIF, WEBP, ICO, SVG
BACKGROUND = "black"
TEXT_COLOR = "white"
QUALITY = 95
OUTPUT_FOLDER = "generated_images"

# =============================
# 📏 СПИСОК РАЗМЕРОВ
# =============================
SIZES = [
    (100, 100), (200, 200), (320, 240), (640, 480),
    (800, 600), (1024, 768), (1280, 720), (1920, 1080),
    (2560, 1440), (3840, 2160), (5472, 3648), (7680, 4320)
]

# =============================
# 🚀 ОСНОВНАЯ ЛОГИКА
# =============================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for w, h in SIZES:
    if FORMAT == "SVG":
        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">
  <rect width="100%" height="100%" fill="{BACKGROUND}" />
  <text x="50%" y="50%" fill="{TEXT_COLOR}" font-size="{min(w,h)//8}" font-family="Arial"
        text-anchor="middle" dominant-baseline="middle">{w}x{h}</text>
</svg>'''
        file_path = os.path.join(OUTPUT_FOLDER, f"{w}x{h}.svg")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        continue

    img = Image.new("RGB", (w, h), color=BACKGROUND)
    draw = ImageDraw.Draw(img)
    text = f"{w}x{h}"

    font_size = max(12, min(w, h) // 8)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    draw.text(((w - text_w) / 2, (h - text_h) / 2), text, fill=TEXT_COLOR, font=font)

    file_path = os.path.join(OUTPUT_FOLDER, f"{w}x{h}.{FORMAT.lower()}")
    save_kwargs = {}

    if FORMAT == "HEIF":
        save_kwargs = {"quality": QUALITY, "format": "HEIF"}
        pillow_heif.register_heif_opener()
        img.save(file_path, **save_kwargs)
    elif FORMAT == "JPEG":
        img.save(file_path, format="JPEG", quality=QUALITY)
    elif FORMAT == "PNG":
        img.save(file_path, format="PNG")
    elif FORMAT == "TIFF":
        img.save(file_path, format="TIFF", compression="tiff_lzw")
    elif FORMAT == "WEBP":
        img.save(file_path, format="WEBP", quality=QUALITY)
    elif FORMAT == "BMP":
        img.save(file_path, format="BMP")
    elif FORMAT == "GIF":
        img.save(file_path, format="GIF")
    elif FORMAT == "ICO":
        img.save(file_path, format="ICO", sizes=[(w, h)])
    elif FORMAT == "PJPEG":
        img.save(file_path, format="JPEG", quality=QUALITY, progressive=True)
    else:
        raise ValueError(f"Неизвестный формат: {FORMAT}")

# =============================
# 📦 АРХИВАЦИЯ
# =============================

archive_path = f"{FORMAT.lower()}_images.zip"
with zipfile.ZipFile(archive_path, "w") as zipf:
    for file in os.listdir(OUTPUT_FOLDER):
        zipf.write(os.path.join(OUTPUT_FOLDER, file), arcname=file)

print(f"✅ Готово! Архив сохранён как {archive_path}")
