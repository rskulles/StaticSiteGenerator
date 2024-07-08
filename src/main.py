import os
import shutil
import textnode

def extract_title(markdown:str)->str:
    lines = markdown.split("\n",1)
    if not lines[0].startswith("# "):
        raise Exception("Markdown File Must Start with a h1 heading.")
    return lines[0][2:]

def generate_page(from_path, template_path, dest_path):

    md_file = open(from_path,'r')
    markdown = md_file.read()
    title = extract_title(markdown)
    md_file.close()

    template_file= open(template_path,'r')
    template =template_file.read()
    template_file.close()
    template = template.replace("{{ Title }}",title)

    node = textnode.markdown_to_html_node(markdown)
    content=node.to_html()

    out_dir = os.path.dirname(dest_path)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    template = template.replace("{{ Content }}",content)
    html_file =  open(dest_path,'w')
    html_file.write(template)
    html_file.close()

def generate_page_recursive(base_dir:str,template_path:str, out_dir:str):
    print(f"Generating page(s) from {base_dir} to {out_dir} using {template_path}...")
    items = os.listdir(base_dir)
    for item in items:
          from_path = os.path.join(base_dir,item)
          to_path = os.path.join(out_dir,item.replace(".md",".html"))

          if os.path.isfile(from_path):
            generate_page(from_path,template_path,to_path)
          else:
            generate_page_recursive(from_path,template_path,to_path)

def copy(frm:str, to:str):
    items = os.listdir(frm)
    print(f"In directory {frm}...")
    for item in items:
       print(f"\t{item}")
       frm_path = os.path.join(frm,item)
       if os.path.isfile(frm_path):
           print(f"\t\tcopying file {item}")
           shutil.copy(frm_path,to)
       else:
           destination = os.path.join(to,item)
           os.mkdir(destination)
           copy(frm_path,destination)

def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
        os.mkdir("./public")

    copy("./static","./public")
    generate_page_recursive("./content","./template.html","./public")

if __name__ == '__main__':
    main()
