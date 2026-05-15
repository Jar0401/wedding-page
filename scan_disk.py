import os
import shutil

def get_size(path):
    total = 0
    try:
        if os.path.isfile(path):
            return os.path.getsize(path)
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    total += os.path.getsize(fp)
                except:
                    pass
    except:
        pass
    return total

def format_size(bytes_val):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.2f} TB"

paths_to_check = [
    ("C:/Users/Ren/Downloads", "下载文件夹"),
    ("C:/Users/Ren/Desktop", "桌面"),
    ("C:/Users/Ren/Documents", "文档"),
    ("C:/Windows/Temp", "Windows 临时文件"),
    ("C:/Users/Ren/AppData/Local/Temp", "用户临时文件"),
    ("C:/$Recycle.Bin", "回收站"),
    ("C:/Windows/SoftwareDistribution/Download", "Windows 更新缓存"),
    ("C:/ProgramData", "程序数据"),
    ("C:/Program Files", "程序文件 (x64)"),
    ("C:/Program Files (x86)", "程序文件 (x86)"),
]

print("=" * 60)
print("C 盘空间占用扫描结果")
print("=" * 60)

results = []
for path, name in paths_to_check:
    if os.path.exists(path):
        size = get_size(path)
        results.append((size, name, path))
    else:
        results.append((0, name, path))

results.sort(reverse=True)

for size, name, path in results:
    status = "✓" if os.path.exists(path) else "✗ (不存在)"
    print(f"{format_size(size):>12}  |  {name:<20}  {status}")

# 扫描 AppData 里的大文件夹
print("\n" + "=" * 60)
print("AppData\\Local 里的大文件夹 (>500MB)")
print("=" * 60)

appdata_local = "C:/Users/Ren/AppData/Local"
if os.path.exists(appdata_local):
    appdata_results = []
    for item in os.listdir(appdata_local):
        full = os.path.join(appdata_local, item)
        if os.path.isdir(full):
            size = get_size(full)
            if size > 500 * 1024 * 1024:
                appdata_results.append((size, item))

    appdata_results.sort(reverse=True)
    for size, name in appdata_results:
        print(f"{format_size(size):>12}  |  {name}")

print("\n扫描完成！")
