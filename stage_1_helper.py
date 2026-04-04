import docx2txt

# extract text
text = docx2txt.process("data/computer.docx")

# extract text and write images in /tmp/img_dir
# text = docx2txt.process("file.docx", "/tmp/img_dir")
print(" ".join(text.split()))
