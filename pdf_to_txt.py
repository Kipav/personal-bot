from tika import parser
import re
import pathlib

def pdf_to_text(pdf_path):
    parsed = parser.from_file(pdf_path, xmlContent=True)
    xml_content = parsed.get("content", "")
    
    pages = re.findall(r'<div class="page">(.*?)</div>', xml_content, re.DOTALL)
    
    numbered_content = []
    for i, page_content in enumerate(pages, 1):
        clean_content = re.sub(r'<[^>]+>', '', page_content).strip()
        if clean_content:
            numbered_content.append(f"[Page {i}]\n{clean_content}")
    
    return "\n\n".join(numbered_content)

input_dir = pathlib.Path('data')
output_dir = pathlib.Path('data')
    
for pdf_file in input_dir.glob('*.pdf'):
    output_path = output_dir / f'{pdf_file.stem}.txt'
    print(f'Processing {pdf_file.name}...')
    output = pdf_to_text(str(pdf_file))
    
    output_path.write_text(output, encoding='utf-8')
    print(f'Completed processing {pdf_file.name} -> {output_path.name}')