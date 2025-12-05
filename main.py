import cv2
import numpy as np
import os
import glob
import pandas as pd
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
import re
from rich.progress import Progress
import random
import matplotlib.pyplot as plt

input_dirs = {
    "Blur": "dataset/Synthetic/Blur/Blur_level_2",
    "Low_illumination": "dataset/Synthetic/Low illumination/Low_Level_2",
    "Shadow": "dataset/Synthetic/Shadow/Shadow_level_2",
}

gt_dir = "dataset/gt"
output_dir = "dataset/output/"
os.makedirs(output_dir, exist_ok=True)

sample_target = {
    "Blur": 20,
    "Low_illumination": 20,
    "Shadow": 20,
}

categorized_files = {}
for category, d in input_dirs.items():
    files = sorted(glob.glob(os.path.join(d, "*.jpg")) )
    random.shuffle(files)
    categorized_files[category] = files

final_samples = []
results = []


def plot_bar_metrics(df):
    categories = df["Kategori"].unique()

    summary = df.groupby("Kategori")[["PSNR Sebelum", "PSNR Sesudah", "SSIM Sebelum", "SSIM Sesudah"]].mean()

    x = np.arange(len(categories))
    width = 0.2

    plt.figure(figsize=(10, 5))
    plt.bar(x - width, summary["PSNR Sebelum"], width, label="PSNR Sebelum")
    plt.bar(x, summary["PSNR Sesudah"], width, label="PSNR Sesudah")
    plt.xticks(x, categories)
    plt.ylabel("PSNR")
    plt.title("Rata-rata PSNR per Kategori")
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.bar(x - width, summary["SSIM Sebelum"], width, label="SSIM Sebelum")
    plt.bar(x, summary["SSIM Sesudah"], width, label="SSIM Sesudah")
    plt.xticks(x, categories)
    plt.ylabel("SSIM")
    plt.title("Rata-rata SSIM per Kategori")
    plt.legend()
    plt.show()


def plot_metrics(df):
    categories = df["Kategori"].unique()

    for cat in categories:
        df_cat = df[df["Kategori"] == cat]

        plt.figure(figsize=(12, 5))
        plt.plot(df_cat["Nomor"], df_cat["PSNR Sebelum"], 'b.-', label="PSNR Sebelum")
        plt.plot(df_cat["Nomor"], df_cat["PSNR Sesudah"], 'r.-', label="PSNR Sesudah")
        plt.title(f"PSNR - {cat}")
        plt.xlabel("Nomor Gambar")
        plt.ylabel("PSNR")
        plt.legend()
        plt.grid(True)
        plt.show()

        plt.figure(figsize=(12, 5))
        plt.plot(df_cat["Nomor"], df_cat["SSIM Sebelum"], 'b.-', label="SSIM Sebelum")
        plt.plot(df_cat["Nomor"], df_cat["SSIM Sesudah"], 'r.-', label="SSIM Sesudah")
        plt.title(f"SSIM - {cat}")
        plt.xlabel("Nomor Gambar")
        plt.ylabel("SSIM")
        plt.legend()
        plt.grid(True)
        plt.show()



for category, files in categorized_files.items():
    target = sample_target[category]

    if len(files) < target:
        print(f"WARNING: Kategori {category} hanya memiliki {len(files)} file, kurang dari target {target}.")
        chosen = files  # ambil semua
    else:
        chosen = files[:target]

    final_samples.extend(chosen)

random.shuffle(final_samples)

input_files = final_samples

print(f"Total gambar terpilih: {len(input_files)}")

def extract_category(filename):
    if filename.startswith("Blur_level_2"):
        return "Blur"
    elif filename.startswith("Low_illumination_level_2"):
        return "Low_illumination"
    elif filename.startswith("Shadow_level_2"):
        return "Shadow"
    return "Unknown"

def extract_number(filename):
    match = re.search(r"\((\d+)\)", filename)
    return int(match.group(1)) if match else -1
def unsharp_with_laplacian_mask(img, amount=1.5, lap_ksize=3, edge_threshold=10):
    blur = cv2.GaussianBlur(img, (5, 5), 0)

    detail = cv2.subtract(img, blur)

    lap = cv2.Laplacian(img, cv2.CV_16S, ksize=lap_ksize)
    lap_abs = cv2.convertScaleAbs(lap)

    _, mask = cv2.threshold(lap_abs, edge_threshold, 255, cv2.THRESH_BINARY)
    mask = mask.astype(np.float32) / 255.0  # normalize to 0–1

    sharpened = img.astype(np.float32) + (amount * detail.astype(np.float32) * mask)

    sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
    return sharpened

with Progress() as progress:
    task = progress.add_task("[Image Improvement] Processing....", total=len(input_files))
    for in_path in input_files:
        name = os.path.basename(in_path)
        num = extract_number(name)
        gt_name = f"Ground_Truth ({num}).jpg"
        gt_path = os.path.join(gt_dir, gt_name)

        if not os.path.exists(gt_path):
            print(f"Ground truth tidak ditemukan untuk {name}")
            continue
        img_input = cv2.imread(in_path, cv2.IMREAD_GRAYSCALE)
        img_gt = cv2.imread(gt_path, cv2.IMREAD_GRAYSCALE)

        if img_gt.shape != img_input.shape:
            img_gt = cv2.resize(img_gt, (img_input.shape[1], img_input.shape[0]))

        img_denoised = cv2.fastNlMeansDenoising(img_input, None, h=10, templateWindowSize=7, searchWindowSize=21)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        img_clahe = clahe.apply(img_denoised)
        edges = cv2.Canny(img_input, 50, 150)
        lap = cv2.Laplacian(img_clahe, cv2.CV_64F)
        sharp = img_clahe - 0.25 * lap

        img_sharp = np.where(edges > 5, sharp, img_clahe)
        img_sharp = cv2.convertScaleAbs(img_sharp)
        cv2.imwrite(os.path.join(output_dir, name), img_sharp)
        psnr_before = psnr(img_gt, img_input, data_range=255)
        ssim_before = ssim(img_gt, img_input, data_range=255)

        psnr_after = psnr(img_gt, img_sharp, data_range=255)
        ssim_after = ssim(img_gt, img_sharp, data_range=255)
        category = extract_category(name)
        results.append({
            "Nama File": name,
            "Kategori": category,
            "Nomor" : num,
            "PSNR Sebelum": psnr_before,
            "SSIM Sebelum": ssim_before,
            "PSNR Sesudah": psnr_after,
            "SSIM Sesudah": ssim_after,
            "ΔPSNR": psnr_after - psnr_before,
            "ΔSSIM": ssim_after - ssim_before
        })
        progress.update(task, advance=1)
df = pd.DataFrame(results)
# plot_metrics(df)
plot_bar_metrics(df)
summary = df.groupby("Kategori").mean(numeric_only=True)

df.to_csv("hasil_evaluasi_dataset.csv", index=False)
summary.to_csv("ringkasan_statistik.csv")
print("\n=== HASIL PER GAMBAR ===")
print(df.round(4))

print("\n=== STATISTIK KESELURUHAN ===")
print(summary.round(4))