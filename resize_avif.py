import os
from PIL import Image
from pillow_heif import register_heif_opener

# Enable modern AVIF image support in Python
register_heif_opener()

# --- CONFIGURATION ---
target_width = 83  
target_height = 110  

# Drop quality to 65. AVIF at 60-70 looks as clear as JPEG at 85 but with tiny files.
quality_setting = 65  

# Speed 0 or 1 forces the compressor to work much harder to find the smallest file size.
speed_setting = 1     
# ---------------------

output_folder = "./resized_images/"
os.makedirs(output_folder, exist_ok=True)

print(f"Starting batch resize to EXACTLY {target_width}x{target_height}px...")
count = 0

for filename in os.listdir("."):
    if filename.lower().endswith(".avif"):
        try:
            original_size = os.path.getsize(filename)
            img = Image.open(filename)
            
            # Resize the image
            resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            # Define output path
            out_path = os.path.join(output_folder, filename)
            
            # Save using tighter compression and slower speed settings
            resized_img.save(
                out_path, 
                "AVIF", 
                quality=quality_setting, 
                speed=speed_setting
            )
            
            # --- SAFETY CHECK ---
            # If the new file is somehow still bigger than the original, use the original file
            new_size = os.path.getsize(out_path)
            if new_size > original_size:
                # Copy original file instead to preserve the smaller size
                import shutil
                shutil.copy2(filename, out_path)
                print(f"PRESERVED: Original was already smaller than resized version ({filename})")
            else:
                print(f"SUCCESS: Resized {filename} (Saved {original_size - new_size} bytes)")
                
            count += 1
        except Exception as e:
            print(f"ERROR processing {filename}: {e}")

print(f"\nDone! Successfully processed {count} AVIF images.")
print(f"Your resized images are inside the folder: {output_folder}")
