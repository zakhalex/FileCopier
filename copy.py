import shutil
import os
import sys
import subprocess
from tqdm import tqdm

def compare_and_copy(src, dst):
    total_files = 0
    for root, dirs, files in os.walk(src):
        total_files += len(files)

    with tqdm(total=total_files, unit="file", desc="Copying Files") as pbar:
        for root, dirs, files in os.walk(src):
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dst, os.path.relpath(src_file, src))
                
                # Normalize the path to ensure consistent slashes
                src_file = os.path.normpath(src_file)
                
                # Normalize the path to ensure consistent slashes
                dst_file = os.path.normpath(dst_file)

                # Handle Cyrillic directories and files
                dst_file = dst_file.encode('utf-8').decode('utf-8')

                # Create destination directory if it doesn't exist
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)

                if not os.path.exists(dst_file) or os.path.getmtime(src_file) > os.path.getmtime(dst_file):
                    try:
                        shutil.copy2(src_file, dst_file)
                    except:
                        cp_command = f"cp -f \"{src_file}\" \"{dst_file}\""
                        subprocess.run(cp_command, shell=True, check=True)
                
                pbar.update(1)  # Update progress bar

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script.py source_folder destination_folder")
        sys.exit(1)

    source_folder = sys.argv[1]
    destination_folder = sys.argv[2]
    
    compare_and_copy(source_folder, destination_folder)