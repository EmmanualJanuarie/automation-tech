from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "tmp" / "pdfs" / "rendered"


def make(folder: str, output_prefix: str):
    files = sorted((BASE / folder).glob("page-*.png"))
    for batch_no, start in enumerate(range(0, len(files), 16), 1):
        subset = files[start:start + 16]
        thumb_w, thumb_h, label_h = 200, 283, 20
        sheet = Image.new("RGB", (4 * thumb_w, 4 * (thumb_h + label_h)), "#d8dee5")
        draw = ImageDraw.Draw(sheet)
        for idx, path in enumerate(subset):
            im = Image.open(path).convert("RGB")
            im.thumbnail((thumb_w - 8, thumb_h - 8))
            x = (idx % 4) * thumb_w + (thumb_w - im.width) // 2
            y = (idx // 4) * (thumb_h + label_h) + 4
            sheet.paste(im, (x, y))
            draw.text(((idx % 4) * thumb_w + 8, y + thumb_h - 2), f"Page {start + idx + 1}", fill="black")
        sheet.save(BASE / f"{output_prefix}-{batch_no}.png")


make("syllabus_new", "syllabus-new-contact")
make("portfolio_new", "portfolio-new-contact")
make("guide_new", "guide-new-contact")
make("portfolio_simulated_four", "portfolio-simulated-four-contact")
