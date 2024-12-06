import shutil
import os
from pathlib import Path
# import markdown  # type: ignore
from markdown_processor import markdown_to_html_node, extract_title

print("hello world")

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating page...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)


def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isdir(item_path):
            print(f"{item} — это директория")
            generate_pages_recursive(item_path, template_path, os.path.join(dest_dir_path, item))
        elif os.path.isfile(item_path):
            extension = os.path.splitext(item)[1]
            if extension == ".md":
                print(f"{item} — это файл с расширением .md")
                with open(item_path, 'r', encoding='utf-8') as md_file:
                    markdown_content = md_file.read()
                with open(template_path, 'r', encoding='utf-8') as template_file:
                    template_content = template_file.read()
                title_line = markdown_content.splitlines()[0]  
                title = title_line.strip('# ')
                node = markdown_to_html_node(markdown_content)
                html = node.to_html()
                generated_html_content = template_content.replace("{{ Title }}", title)
                generated_html_content = generated_html_content.replace("{{ Content }}", html)
                #markdown.markdown(markdown_content)
                if not os.path.exists(dest_dir_path):
                    os.makedirs(dest_dir_path)
                new_file_name = os.path.splitext(item)[0] + ".html"
                new_file_path = os.path.join(dest_dir_path, new_file_name)

                os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
            
                with open(new_file_path, 'w', encoding='utf-8') as file:
                    file.write(generated_html_content)
                print(f"HTML файл был записан: {new_file_path}")

        


if __name__ == "__main__":
    main()






