import os
import sys


def collect_files_content(output_file='collected_contents.txt', encoding='utf-8'):
    """
    Collect and save the paths and contents of all files in the current directory
    in a specified format to an output file.
    Format:
    <relative_path>
    <content>
    
    Args:
        output_file (str): Name of the output file
        encoding (str): File encoding, defaults to utf-8
    """

    def is_binary_file(file_path):
        """
        Check if a file is binary
        
        Returns:
            bool: True if file is binary, False otherwise
        """
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read(1024)
                return False
        except UnicodeDecodeError:
            return True

    def write_file_content(file_path, out_file):
        """
        Write a single file's path and content to the output file
        
        Args:
            file_path (str): Path to the file to process
            out_file (file): Output file handle to write to
        """
        rel_path = os.path.relpath(file_path)

        # Skip the output file itself
        if rel_path == output_file:
            return

        out_file.write(f"<{rel_path}>\n")

        # Check if file is binary
        if is_binary_file(file_path):
            out_file.write("[Binary file, content skipped]\n")
        else:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                    out_file.write(f"{content}\n")
            except Exception as e:
                out_file.write(f"[Failed to read file: {str(e)}]\n")

        out_file.write("\n")  # Add blank line between file records

    # Get all file paths and sort them to ensure consistent output order
    all_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file != output_file:  # Exclude output file
                file_path = os.path.join(root, file)
                all_files.append(file_path)

    all_files.sort()  # Sort file paths

    # Write all file contents to output file
    with open(output_file, 'w', encoding=encoding) as out_file:
        for file_path in all_files:
            write_file_content(file_path, out_file)


if __name__ == "__main__":
    try:
        # Output file name and encoding can be specified via command line arguments
        output_file = sys.argv[1] if len(sys.argv) > 1 else 'collected_contents.txt'
        encoding = sys.argv[2] if len(sys.argv) > 2 else 'utf-8'

        collect_files_content(output_file, encoding)
        print(f"File contents collected to: {output_file}")

    except Exception as e:
        print(f"Error: {str(e)}")