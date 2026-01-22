import os
import re

def extract_nested_files():
    # Define the root directories to scan based on your tree structure
    target_directories = ['maths', 'science', 'social-science']

    # Regex pattern to capture the filepath and the content
    # Group 1: The filename inside the tag
    # Group 2: The actual content
    pattern = re.compile(
        r"^<<<FILE_START:\s*(.+?)>>>\s*\n(.*?)\n<<<FILE_END>>>",
        re.DOTALL | re.MULTILINE
    )

    for directory in target_directories:
        if not os.path.exists(directory):
            print(f"Skipping {directory} (not found)")
            continue

        # Walk through the directory tree
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".md"):
                    source_path = os.path.join(root, file)

                    # Determine output directory:
                    # If source is "maths/1.md", output base is "maths/1"
                    output_base_dir = os.path.splitext(source_path)[0]

                    print(f"Processing: {source_path}...")

                    try:
                        with open(source_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        matches = pattern.findall(content)

                        if not matches:
                            print(f"  -- No delimited files found in {file}")
                            continue

                        for relative_path, file_content in matches:
                            # Clean up potential whitespace around filename
                            relative_path = relative_path.strip()

                            # Construct full destination path
                            # e.g. maths/1/topics/01-patterns.mdx
                            dest_path = os.path.join(output_base_dir, relative_path)

                            # Create necessary subdirectories
                            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                            # Write the extracted content
                            with open(dest_path, 'w', encoding='utf-8') as out_f:
                                out_f.write(file_content)

                            print(f"  -> Extracted: {dest_path}")

                    except Exception as e:
                        print(f"Error processing {source_path}: {e}")

if __name__ == "__main__":
    extract_nested_files()
    print("\nExtraction complete.")
