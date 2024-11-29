import os
import re


def convert_txt_to_html(txt_file, html_file):
    with open(txt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    name = str(os.path.basename(txt_file)).split('.')[0]
    name = re.sub(r"\d+", "", name, flags=re.UNICODE)
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <h>{name}</h>
    </head>
    <body>
        <pre>{content}</pre>
    </body>
    </html>
    """

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)


def convert_all_txt_to_html(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            txt_file_path = os.path.join(directory, filename)
            html_file_path = os.path.splitext(txt_file_path)[0] + '.html'
            convert_txt_to_html(txt_file_path, html_file_path)


def delete_txt_format(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            os.remove(os.path.join(directory,filename))


directory_path = 'html+'
convert_all_txt_to_html(directory_path)
delete_txt_format(directory_path)
