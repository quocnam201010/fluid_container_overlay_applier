import os
from PIL import Image

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def parse_java_hex_literal(s):
    """
    Accepts:
      0xRRGGBB
      0XRRGGBB
      lowercase or uppercase
    Returns (R, G, B)
    """
    original = s.strip()           # keep original for naming
    s = original.lower()

    if s.startswith("0x"):
        s = s[2:]

    if len(s) != 6:
        raise ValueError("Invalid Java hex literal. Expected format 0xRRGGBB")

    rgb = tuple(int(s[i:i+2], 16) for i in (0, 2, 4))
    return rgb, original


def tint_image(img, rgb):
    r, g, b = rgb
    tinted = Image.new("RGBA", img.size)
    width, height = img.size
    base_pix = img.load()
    out_pix = tinted.load()

    for y in range(height):
        for x in range(width):
            pr, pg, pb, pa = base_pix[x, y]
            tr = pr * r // 255
            tg = pg * g // 255
            tb = pb * b // 255
            out_pix[x, y] = (tr, tg, tb, pa)

    return tinted


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    color_input = input("Enter Java hex literal color (example: 0x3333FF): ").strip()
    tint_rgb, original_literal = parse_java_hex_literal(color_input)

    for filename in os.listdir(INPUT_DIR):
        if not filename.endswith("_overlay.png"):
            continue

        overlay_path = os.path.join(INPUT_DIR, filename)
        base_path = os.path.join(INPUT_DIR, filename.replace("_overlay.png", ".png"))

        if not os.path.exists(base_path):
            print("No base image found for", filename)
            continue

        base = Image.open(base_path).convert("RGBA")
        overlay = Image.open(overlay_path).convert("RGBA")

        tinted_overlay = tint_image(overlay, tint_rgb)
        result = Image.alpha_composite(base, tinted_overlay)

        # Naming: base_final_0xRRGGBB.png
        name_without_overlay = filename.replace("_overlay.png", "")
        output_name = f"{name_without_overlay}_{original_literal}.png"

        output_path = os.path.join(OUTPUT_DIR, output_name)
        result.save(output_path)

        print("Exported ->", output_path)

    print("Done.")


if __name__ == "__main__":
    main()
