from PIL import Image
import numpy as np
import webcolors

# Українські переклади CSS назв
UA_COLOR_NAMES = {
    "white": "білий",
    "black": "чорний",
    "gray": "сірий",
    "lightgray": "світло-сірий",
    "darkgray": "темно-сірий",
    "red": "червоний",
    "darkred": "темно-червоний",
    "orange": "помаранчевий",
    "darkorange": "темно-помаранчевий",
    "yellow": "жовтий",
    "gold": "золотий",
    "green": "зелений",
    "darkgreen": "темно-зелений",
    "lightgreen": "світло-зелений",
    "blue": "синій",
    "darkblue": "темно-синій",
    "lightblue": "світло-синій",
    "navy": "морський синій",
    "cyan": "блакитний",
    "magenta": "пурпурний",
    "purple": "фіолетовий",
    "pink": "рожевий",
    "brown": "коричневий",
    "beige": "бежевий",
    "olive": "оливковий",
    "teal": "бірюзовий",
}

# Запасний набір назв HEX (мінімальний, щоб завжди були варіанти)
UA_HEX_PALETTE = {
    "white": "#ffffff",
    "black": "#000000",
    "gray": "#808080",
    "lightgray": "#d3d3d3",
    "darkgray": "#a9a9a9",
    "red": "#ff0000",
    "darkred": "#8b0000",
    "orange": "#ffa500",
    "darkorange": "#ff8c00",
    "yellow": "#ffff00",
    "gold": "#ffd700",
    "green": "#008000",
    "darkgreen": "#006400",
    "lightgreen": "#90ee90",
    "blue": "#0000ff",
    "darkblue": "#00008b",
    "lightblue": "#add8e6",
    "navy": "#000080",
    "cyan": "#00ffff",
    "magenta": "#ff00ff",
    "purple": "#800080",
    "pink": "#ffc0cb",
    "brown": "#a52a2a",
    "beige": "#f5f5dc",
    "olive": "#808000",
    "teal": "#008080",
}

def closest_color_name(rgb_tuple):
    # 1) Спроба точного зіставлення
    try:
        exact_name = webcolors.rgb_to_name(rgb_tuple)
        return UA_COLOR_NAMES.get(exact_name, exact_name)
    except ValueError:
        pass

    # Кандидати назв HEX: з webcolors або наш запасний словник
    css_dict = getattr(webcolors, "CSS3_NAMES_TO_HEX", None)
    candidates = css_dict if isinstance(css_dict, dict) and css_dict else UA_HEX_PALETTE

    # Пошук найближчого кольору
    min_dist = None
    best_name = None
    for name, hex_value in candidates.items():
        try:
            r_c, g_c, b_c = webcolors.hex_to_rgb(hex_value)
        except Exception:
            continue
        # перетворення до int
        r, g, b = (int(rgb_tuple[0]), int(rgb_tuple[1]), int(rgb_tuple[2]))
        dist = (r_c - r) ** 2 + (g_c - g) ** 2 + (b_c - b) ** 2
        if min_dist is None or dist < min_dist:
            min_dist = dist
            best_name = name

    # Якщо не знайшли (виключний випадок) — повертаємо RGB
    if best_name is None:
        return f"RGB{rgb_tuple}"

    return UA_COLOR_NAMES.get(best_name, best_name)

def pixelize_and_count(input_path, output_path, max_colors=30):
    im = Image.open(input_path)

    # квантування до max_colors
    im_quantized = im.convert("P", palette=Image.ADAPTIVE, colors=max_colors).convert("RGB")
    im_quantized.save(output_path)

    pixels = np.array(im_quantized)
    # якщо зображення порожнє або некоректне
    if pixels.size == 0:
        return {}, 0.0

    unique_colors, counts = np.unique(pixels.reshape(-1, 3), axis=0, return_counts=True)

    result = {}
    total_thread_length = 0.0

    for color, count in zip(unique_colors, counts):
        thread_length = count * 0.18  # см нитки на піксель (коефіцієнт)
        total_thread_length += thread_length
        color_name = closest_color_name(tuple(color))
        result[color_name] = result.get(color_name, 0.0) + thread_length

    # Округлення фінальних значень і сортування
    result = {k: round(v, 1) for k, v in result.items()}
    result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))

    return result, round(total_thread_length, 1)

