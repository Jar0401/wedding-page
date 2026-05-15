import os

def fast_size(path):
    total = 0
    try:
        with os.scandir(path) as it:
            for entry in it:
                try:
                    if entry.is_file(follow_symlinks=False):
                        total += entry.stat(follow_symlinks=False).st_size
                    elif entry.is_dir(follow_symlinks=False):
                        # 只递归一层子目录，避免太慢
                        with os.scandir(entry.path) as it2:
                            for e2 in it2:
                                if e2.is_file(follow_symlinks=False):
                                    total += e2.stat(follow_symlinks=False).st_size
                except:
                    pass
    except:
        pass
    return total

def fmt(b):
    for u in ['B','KB','MB','GB']:
        if b < 1024: return f"{b:.1f} {u}"
        b /= 1024
    return f"{b:.2f} TB"

paths = [
    (r"C:\Users\Ren\Downloads", "下载文件夹"),
    (r"C:\Users\Ren\Desktop", "桌面"),
    (r"C:\Users\Ren\Documents", "文档"),
    (r"C:\Windows\Temp", "Windows 临时文件"),
    (r"C:\Users\Ren\AppData\Local\Temp", "用户临时文件"),
    (r"C:\Windows\SoftwareDistribution\Download", "Windows 更新缓存"),
    (r"C:\ProgramData", "程序数据"),
    (r"C:\Program Files", "程序文件 (x64)"),
    (r"C:\Program Files (x86)", "程序文件 (x86)"),
]

print("="*55)
print("C 盘空间占用扫描 (快速模式)")
print("="*55)

res = []
for p, name in paths:
    if os.path.exists(p):
        s = fast_size(p)
        res.append((s, name))
    else:
        res.append((0, name + " (不存在)"))

res.sort(reverse=True)
for s, n in res:
    print(f"{fmt(s):>12}  |  {n}")

# AppData Local 快速扫描
print("\n" + "="*55)
print("AppData\\Local 大文件夹 (>300MB)")
print("="*55)

app = r"C:\Users\Ren\AppData\Local"
if os.path.exists(app):
    app_res = []
    for entry in os.scandir(app):
        if entry.is_dir(follow_symlinks=False):
            s = fast_size(entry.path)
            if s > 300*1024*1024:
                app_res.append((s, entry.name))
    app_res.sort(reverse=True)
    for s, n in app_res:
        print(f"{fmt(s):>12}  |  {n}")

print("\n扫描完成!")
