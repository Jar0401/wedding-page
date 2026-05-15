from PIL import Image

# 海报尺寸 (宽, 高) - 像素风格用小尺寸再放大
W, H = 64, 96
img = Image.new('RGB', (W, H), (15, 15, 35))
pixels = img.load()

# 调色板 - 复古低饱和色系
sky_top = (25, 25, 60)
sky_mid = (60, 40, 80)
sky_bottom = (120, 70, 90)
star = (220, 220, 240)
moon = (240, 240, 210)
moon_dark = (200, 200, 170)
mtn_far = (50, 45, 65)
mtn_mid = (70, 60, 75)
mtn_near = (45, 40, 50)
accent = (255, 100, 100)  # 点缀色

# 绘制天空渐变
for y in range(H):
    t = y / H
    r = int(sky_top[0] * (1-t) + sky_bottom[0] * t)
    g = int(sky_top[1] * (1-t) + sky_bottom[1] * t)
    b = int(sky_top[2] * (1-t) + sky_bottom[2] * t)
    for x in range(W):
        pixels[x, y] = (r, g, b)

# 添加星星 (随机分布)
import random
random.seed(42)
for _ in range(40):
    sx, sy = random.randint(0, W-1), random.randint(0, 55)
    # 偶尔画双像素星星
    pixels[sx, sy] = star
    if random.random() > 0.7:
        pixels[(sx+1)%W, sy] = (180, 180, 200)

# 绘制月亮 (圆形，像素风格)
moon_x, moon_y = 48, 18
for dy in range(-6, 7):
    for dx in range(-6, 7):
        d = (dx*dx + dy*dy) ** 0.5
        if d <= 6:
            px, py = moon_x + dx, moon_y + dy
            if 0 <= px < W and 0 <= py < H:
                if d > 4.5 and dx > 0:  # 月牙阴影
                    pixels[px, py] = moon_dark
                else:
                    pixels[px, py] = moon

# 绘制远山 (锯齿像素轮廓)
mtn_far_y = 65
for x in range(W):
    height = int(8 + 4 * (1 if x % 7 < 4 else 0) + 2 * (1 if x % 3 == 0 else 0))
    for dy in range(height):
        y = mtn_far_y - dy
        if 0 <= y < H:
            pixels[x, y] = mtn_far

# 绘制中山
mtn_mid_y = 72
for x in range(W):
    height = int(10 + 6 * (1 if x % 5 < 3 else 0) + 3 * (1 if x % 4 == 0 else 0))
    for dy in range(height):
        y = mtn_mid_y - dy
        if 0 <= y < H:
            pixels[x, y] = mtn_mid

# 绘制近山 (黑色剪影)
mtn_near_y = 82
for x in range(W):
    height = int(14 + 8 * (1 if x % 6 < 4 else 0) + 4 * (1 if x % 3 == 0 else 0))
    for dy in range(height):
        y = mtn_near_y - dy
        if 0 <= y < H:
            pixels[x, y] = mtn_near

# 底部地面
for y in range(88, H):
    for x in range(W):
        pixels[x, y] = (35, 30, 40)

# 添加一些点缀 "树" 的像素剪影
for tx in [8, 18, 35, 52]:
    for dy in range(8):
        y = 88 - dy
        if 0 <= y < H:
            pixels[tx, y] = (20, 18, 25)
            if dy < 4:
                pixels[tx-1, y] = (20, 18, 25)
                pixels[tx+1, y] = (20, 18, 25)

# 放大到海报尺寸 (640x960)，保持像素硬边缘
poster = img.resize((640, 960), Image.NEAREST)

# 保存到桌面
poster.save('C:/Users/Ren/Desktop/pixel_art_poster.png')
print("海报已生成：桌面 pixel_art_poster.png")
