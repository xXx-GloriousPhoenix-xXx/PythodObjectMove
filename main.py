# ==================== Library imports ==================== #
import tkinter as tk
import pygame
import os
import math
# ========================================================= #

# ==================== Window init ==================== #
root = tk.Tk()
# ===================================================== #

# ==================== Window settings ==================== #
# Fullscreen window mode
root.state('zoomed')
root.update_idletasks()

# Window title
root.title("Переміщення об'єкта")
# ========================================================= #

# ==================== Miscellaneous ==================== #
background_color = "#1e1e1e"
object_color = "#ff6464"
# ======================================================= #

# ==================== Dimensions ==================== #
# Screen
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

# Segment
control_width = int(0.25 * width)
embed_width = int(0.75 * width)
separator_width = 4

# Area borders
area_border_left = 0
area_border_right = width - separator_width - control_width
area_border_top = height
area_border_bottom = 0

# Object
object_border_width = 4
object_center_x = embed_width // 2
object_center_y = height // 2
object_inner_r = embed_width / 50
object_outer_r = int(2.5 * object_inner_r)
# ================================================== #

# ==================== Segment init ==================== #
# Control panel
control_frame = tk.Frame(root, width=control_width, height=height, bg=background_color)
control_frame.pack(side="left")
control_frame.pack_propagate(False)

# Separator
separator = tk.Frame(root, width=4, bg=object_color)
separator.pack(side="left", fill="y")

# Pygame area
embed = tk.Frame(root, width=embed_width, height=height)
embed.pack(side="right")
# ====================================================== #

# ==================== Components init ==================== #
# Tkinter init
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'

# Pygame init
pygame.display.init()
pygame.font.init()
screen = pygame.display.set_mode((width, height))
pygame.display.update()
# ========================================================= #

# ==================== Object create ==================== #
def create_star_points(x, y, inner_r, outer_r, num_points = 5):
    points = []
    angle = -math.pi / 2
    angle_step = math.pi / num_points
    radius_list = [outer_r, inner_r]

    for i in range(2 * num_points):
        r = radius_list[i % 2]
        px = int(x + r * math.cos(angle))
        py = int(y + r * math.sin(angle))
        points.append((px, py))

        angle += angle_step

    return points
star_point = create_star_points(object_center_x, object_center_y, object_inner_r, object_outer_r, 5)
text_center_x = object_center_x
text_center_y = object_center_y
# ======================================================= #

# ==================== Checks ==================== #
def is_out_of_bounds(point):
    (x, y) = point
    if x < area_border_left or x > area_border_right:
        return True
    if y > area_border_top or y < area_border_bottom:
        return True
    return False
# ================================================ #

# ==================== Object operate ==================== #
def translate_object(points, dx, dy):
    # foreach point in points add vector (dx, dy)
    translated = []
    for (x, y) in points:
        new_point = (x + dx, y + dy)
        if (is_out_of_bounds(new_point)):
            return points
        translated.append((x + dx, y + dy))
    return translated

def find_center(points):
    return (sum([x for (x, y) in points]) / len(points),
            sum([y for (x, y) in points]) / len(points))

def rotate_object(points, angle):
    (cx, cy) = find_center(points)

    cos = math.cos(angle)
    sin = math.sin(angle)

    rotated = []
    for (x, y) in points:
        xr = x - cx
        yr = y - cy
        x_new = xr * cos - yr * sin + cx
        y_new = xr * sin + yr * cos + cy
        rotated.append((x_new, y_new))

    return rotated

def reflect_object(points, axis='x'):
    match axis:
        case 'x':
            return reflect_object_x(points)
        case 'y':
            return reflect_object_y(points)
        case _:
            return points

def reflect_object_x(points):
    (cx, cy) = find_center(points)
    return [(2 * cx - x, y) for (x, y) in points]

def reflect_object_y(points):
    (cx, cy) = find_center(points)
    return [(x, 2 * cy - y) for (x, y) in points]

def scale_object(points, sx, sy):
    # foreach point in points multiply:
    # x by sx
    # y by sy
    scaled = []
    (cx, cy) = find_center(points)
    for (x, y) in points:
        x_new = cx + (x - cx) * sx
        y_new = cy + (y - cy) * sy
        scaled.append((x_new, y_new))
    return scaled
# ======================================================== #
 
# ==================== Key bind ==================== #
pressed_keys = set()

def on_key_press(event):
    pressed_keys.add(event.keysym.lower())

def on_key_release(event):
    pressed_keys.discard(event.keysym.lower())

root.bind("<KeyPress>", on_key_press)
root.bind("<KeyRelease>", on_key_release)
# ================================================== #

# ==================== Controls ==================== #
def translate_object_horizontal(value):
    global star_point, text_center_x
    try:
        dx = int(value)
        if not mode_var.get():
            star_point = translate_object(star_point, dx, 0)
        else:
            text_center_x += dx
    except ValueError:
        pass

def translate_object_vertical(value):
    global star_point, text_center_y
    try:
        dy = int(value)
        if not mode_var.get():
            star_point = translate_object(star_point, 0, -dy)
        else:
            text_center_y -= dy 
    except ValueError:
        pass

def scale_object_horizontal(value):
    global star_point
    try:
        sx = float(value)
        star_point = scale_object(star_point, sx, 1)
    except ValueError:
        pass

def scale_object_vertical(value):
    global star_point
    try:
        sy = float(value)
        star_point = scale_object(star_point, 1, sy)
    except ValueError:
        pass

def rotate_object_degrees(value):
    global star_point
    try:
        angle = math.radians(float(value))
        star_point = rotate_object(star_point, angle)
    except ValueError:
        pass

def reflect_object_horizontal(value=None):
    global star_point
    star_point = reflect_object(star_point, axis='x')

def reflect_object_vertical(value=None):
    global star_point
    star_point = reflect_object(star_point, axis='y')

entry_style = {
    "fg": object_color,
    "bg": background_color,
    "font": ("Segoe UI", 12),
    "bd": 2,
    "relief": "solid",
    "highlightthickness": 2,
    "highlightbackground": object_color,
    "highlightcolor": object_color
}

button_style = {
    "fg": object_color,
    "bg": background_color,
    "font": ("Segoe UI", 12, "bold"),
    "bd": 2,
    "relief": "solid",
    "cursor": "hand2",
    "activebackground": background_color
}

controls = {}

def add_control (name, label, command):
    frame, entry, button = create_entry_with_button(control_frame, label, command)
    frame.pack(side="top", padx=5, pady=(20, 0))
    controls[name] = {'frame': frame, 'entry': entry, 'button': button}

def create_entry_with_button(parent, button_text, command):
    frame = tk.Frame(parent, bg=background_color)
    
    entry = tk.Entry(frame, **entry_style, width=10)
    entry.pack(side="left", padx=(0,15), ipady=5)
    
    button = tk.Button(frame, text=button_text, **button_style, width=20, height=1,
                       command=lambda: command(entry.get()))
    button.pack(side="right", padx=2, pady=2)

    return frame, entry, button

add_control("move_h", "Перемістити (Гор.)", translate_object_horizontal)
add_control("move_v", "Перемістити (Вер.)", translate_object_vertical)
add_control("scale_h", "Розтягнути (Гор.)", scale_object_horizontal)
add_control("scale_v", "Розтягнути (Вер.)", scale_object_vertical)
add_control("rotate", "Повернути (Град.)", rotate_object_degrees)

def create_custom_button(parent, text, command):
    button = tk.Button(parent, text=text, **button_style, width=32, height=1,
                       command=command)
    button.pack(side="top", padx=5, pady=(20, 0))
    return button

create_custom_button(control_frame, "Відобразити по X", reflect_object_horizontal)
create_custom_button(control_frame, "Відобразити по Y", reflect_object_vertical)

# ================================================== #

# ==================== Object mode toggle ==================== #
mode_var = tk.BooleanVar(value=False)

mode_slider = tk.Scale(
    control_frame,
    from_=0, to=1,
    orient="horizontal",
    length=150,
    label="Фігура - Текст",
    fg=object_color,
    bg=background_color,
    troughcolor=object_color,
    highlightthickness=0,
    width=35,
    variable=mode_var
)
mode_slider.pack(side="top", pady=(30, 0))
# ============================================================ #

# ==================== Game loop ==================== #
def game_loop():
    global star_point

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            root.destroy()
            return

    # Control keys
    if 'left' in pressed_keys:
        translate_object_horizontal(-5)
    if 'right' in pressed_keys:
        translate_object_horizontal(5)
    if 'up' in pressed_keys:
        translate_object_vertical(5)
    if 'down' in pressed_keys:
        translate_object_vertical(-5)

    # Clear
    screen.fill(background_color)

    # Draw object
    if (not mode_var.get()):
        pygame.draw.polygon(screen, object_color, star_point, object_border_width)
    else:
        font = pygame.font.SysFont("Segoe UI", 72)
        text_surface = font.render("Hello!", True, object_color)
        text_rect = text_surface.get_rect(center=(text_center_x, text_center_y))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()
    root.after(16, game_loop)  # ~60 FPS
# =================================================== #

# launch
game_loop()
root.mainloop()

# quit pygame
pygame.quit()