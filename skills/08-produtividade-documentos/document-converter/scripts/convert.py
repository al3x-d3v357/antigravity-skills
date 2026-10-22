"""
Cross-Platform Document Converter Script for Antigravity IDE (Windows & POSIX)
"""
import sys
import os
import argparse
import subprocess
import shutil

def main():
    parser = argparse.ArgumentParser(description="Convert documents between Markdown, DOCX, and PDF")
    parser.add_argument("input_file", help="Input file path")
    parser.add_argument("output_file", help="Output file path")
    args = parser.parse_args()
    
    in_ext = os.path.splitext(args.input_file)[1].lower()
    out_ext = os.path.splitext(args.output_file)[1].lower()
    
    print(f"Converting {in_ext} -> {out_ext}...")
    
    if in_ext == ".docx" and out_ext == ".md":
        if shutil.which("markitdown"):
            res = subprocess.run(["markitdown", args.input_file], capture_output=True, text=True)
            if res.returncode == 0:
                with open(args.output_file, "w", encoding="utf-8") as f:
                    f.write(res.stdout)
                print(f"[+] Saved {args.output_file}")
                return
        if shutil.which("pandoc"):
            subprocess.run(["pandoc", args.input_file, "-o", args.output_file], check=True)
            print(f"[+] Saved {args.output_file}")
            return
            
    if in_ext == ".pdf" and out_ext == ".md":
        try:
            import pymupdf4llm
            md_text = pymupdf4llm.to_markdown(args.input_file)
            with open(args.output_file, "w", encoding="utf-8") as f:
                f.write(md_text)
            print(f"[+] Saved {args.output_file}")
            return
        except ImportError:
            pass
            
    if shutil.which("pandoc"):
        subprocess.run(["pandoc", args.input_file, "-o", args.output_file], check=True)
        print(f"[+] Saved {args.output_file}")
        return

    print("[-] No supported converter tool found (install pandoc, markitdown, or pymupdf4llm)")
    sys.exit(1)

if __name__ == "__main__":
    main()
