import os
import shutil
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
    # FIXED: Check for both .jpg and .jpeg file extensions
    if filename.lower().endswith((".jpg", ".jpeg")):
        try:
            original_size = os.path.getsize(filename)
            img = Image.open(filename)
            
            # Resize the image
            resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            # Define output path - Change extension to .avif for true AVIF encoding
            base_name, _ = os.path.splitext(filename)
            out_path = os.path.join(output_folder, f"{base_name}.avif")
            
            # Save using tighter AVIF compression and slower speed settings
            resized_img.save(
                out_path, 
                "AVIF",
                quality=quality_setting, 
                speed=speed_setting
            )
            
            # --- SAFETY CHECK ---
            # If the new file is somehow still bigger than the original, copy the original file instead
            new_size = os.path.getsize(out_path)
            if new_size > original_size:
                # FIXED: Preserves the correct original filename and extension (.jpg or .jpeg)
                backup_out_path = os.path.join(output_folder, filename)
                shutil.copy2(filename, backup_out_path)
                
                # Remove the failed larger AVIF file
                if os.path.exists(out_path):
                    os.remove(out_path)
                    
                print(f"PRESERVED: Original was already smaller than resized version ({filename})")
            else:
                print(f"SUCCESS: Resized {filename} to {base_name}.avif (Saved {original_size - new_size} bytes)")
                
            count += 1
        except Exception as e:
            print(f"ERROR processing {filename}: {e}")

print(f"\nDone! Successfully processed {count} image(s).")
print(f"Your resized images are inside the folder: {output_folder}")
