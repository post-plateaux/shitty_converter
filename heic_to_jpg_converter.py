import sys
import os
from pathlib import Path
from PIL import Image
import pillow_heif

def convert_heic_to_jpg(input_dir, output_dir):
    """
    Converts all HEIC images in the input directory to JPG format
    and saves them in the output directory.
    """
    # Ensure the output directory exists
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"Output will be saved to: {output_path.resolve()}")

    # Register the HEIF opener with Pillow. This allows Pillow to open .heic files.
    pillow_heif.register_heif_opener()

    input_path = Path(input_dir)
    if not input_path.is_dir():
        print(f"Error: Input directory not found at '{input_dir}'", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning for .heic files in: {input_path.resolve()}")

    # Iterate over files in the source directory
    for file_path in input_path.iterdir():
        # Check if the file is a HEIC file (case-insensitive)
        if file_path.suffix.lower() == '.heic':
            print(f"Converting {file_path.name}...")
            try:
                # Open the HEIC image
                image = Image.open(file_path)

                # Create the output filename
                output_filename = file_path.stem + '.jpg'
                output_file_path = output_path / output_filename

                # Convert and save as JPG with high quality.
                # 'quality=95' is a good balance between quality and file size.
                # Use 'quality=100' for maximum quality, but larger files.
                image.save(output_file_path, format='JPEG', quality=95)
                print(f"Successfully converted to {output_file_path}")

            except Exception as e:
                print(f"Error converting {file_path.name}: {e}", file=sys.stderr)
        else:
            print(f"Skipping non-HEIC file: {file_path.name}")

def main():
    """
    Main function to handle command-line arguments and start the conversion.
    """
    if len(sys.argv) != 2:
        print("Usage: python heic_to_jpg_converter.py <path_to_directory_with_heic_files>")
        sys.exit(1)

    source_directory = sys.argv[1]
    
    # Define the output directory relative to the project's root
    project_root = Path(__file__).parent
    output_directory = project_root / 'output'

    convert_heic_to_jpg(source_directory, output_directory)

if __name__ == '__main__':
    main()
