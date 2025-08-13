from PIL import Image
import argparse
import subprocess
import os

POTRACE_PATH = "/usr/bin/potrace"

def convert_to_svg(input_path, output_path):
    try:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"File not found: {input_path}")

        image = Image.open(input_path)
        image = image.convert("L")

        bitmap_path = os.path.splitext(output_path)[0] + "_temp.bmp"
        image.save(bitmap_path)

        result = subprocess.run([POTRACE_PATH, bitmap_path, "-o", output_path, '--svg'], 
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if os.path.exists(bitmap_path):
            os.remove(bitmap_path)

        return output_path

    except subprocess.CalledProcessError as e:
        print(f"Potrace error: {e}")
        raise
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"Weird stuff: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Convert image to SVG.")
    parser.add_argument(
        "--input",
        required=True,
        help="path to input file"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="path to output file"
    )
    args = parser.parse_args()

    svg_file = convert_to_svg(args.input, args.output)
    print(f"{svg_file} generated")

if __name__ == "__main__":
    main()
