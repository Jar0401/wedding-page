import os
import shutil

def clean_folder(path, desc):
    if not os.path.exists(path):
        print(f"[跳过] {desc}: 路径不存在")
        return 0, 0
    cnt = 0
    sz = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            try:
                sz += os.path.getsize(fp)
                os.remove(fp)
                cnt += 1
            except:
                pass
        for d in list(dirs):
            dp = os.path.join(root, d)
            try:
                shutil.rmtree(dp)
                dirs.remove(d)
            except:
                pass
    print(f"[已清理] {desc}: {cnt} 个文件, 约 {sz/1024/1024:.1f} MB")
    return cnt, sz

# 1. 用户临时文件
clean_folder(r"C:\Users\Ren\AppData\Local\Temp", "用户临时文件")

# 2. Windows 更新下载缓存
clean_folder(r"C:\Windows\SoftwareDistribution\Download", "Windows 更新缓存")

# 3. NVIDIA 缓存 (驱动着色器缓存，可安全删除)
clean_folder(r"C:\Users\Ren\AppData\Local\NVIDIA\GLCache", "NVIDIA GLCache")
clean_folder(r"C:\Users\Ren\AppData\Local\NVIDIA\DXCache", "NVIDIA DXCache")

# 4. Windows 临时文件
clean_folder(r"C:\Windows\Temp", "Windows 临时文件")

# 5. 浏览器缓存 (Edge)
clean_folder(r"C:\Users\Ren\AppData\Local\Microsoft\Edge\User Data\Default\Cache", "Edge 浏览器缓存")

print("\n安全清理完成！建议重启电脑让系统重建必要缓存。")
