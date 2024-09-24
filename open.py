from Crypto.Cipher import AES
import io
from PyPDF2 import PdfReader, PdfWriter
import os
import tempfile
import threading
import time
import subprocess
import pikepdf
# 서버에서 받아온 p/w 로 복호화
# 복호화 된 파일 읽기전용으로 하나 만들기 (아직 구현 X)
# 파일 열람창 띄워주기


# pdf파일 복호화
def decrypt_pdf(file_path, key):
    reader = PdfReader(file_path)
    reader.decrypt(key)

    writer = PdfWriter()

    for page in range(len(reader.pages)):
        writer.add_page(reader.pages[page])

    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
        temp_file_name = temp_file.name
        writer.write(temp_file)

    return temp_file_name

def decrypt(encrypted_pdf_path, key, owner_password):
    with pikepdf.open(encrypted_pdf_path, password = key) as pdf:
        # PDF 파일 permission 설정
        permissions = pikepdf.Permissions(
            accessibility=True,
            extract=False,
            modify_annotation=False,
            modify_assembly=False,
            modify_form=False,
            modify_other=False,
            print_highres=False,
            print_lowres=False
        )
        # PDF 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file_path = tmp_file.name
            # PDF 파일을 저장하면서 소유자 비밀번호와 권한 설정
            pdf.save(tmp_file_path, encryption=pikepdf.Encryption(
                owner=owner_password,
                user='',
                allow=permissions
            ))
    # temp 파일을 생성하고 그 경로를 알려주는 코드임
    return tmp_file_path

# 일정 시간이 지난 후 파일 삭제
def delete_temp_file(file_path, delay):
    time.sleep(delay)
    try:
        os.remove(file_path)
        print(f"Temporary file {file_path} deleted.")
    except FileNotFoundError:
        print(f"File {file_path} already deleted.")

#------------------------------------------

encrypted_pdf_path = '/Users/macbook/Desktop/pdf1.8/enc.pdf'
key = '1234567890' # 파일의 비번
delete_delay = 10  # 초 단위로 설정, 임시파일 삭제 시간
owner_password = '0123456789'

#------------------------------------------
# 파일 복호화 한 후 임시파일로 생성하기
#temp_file_name = decrypt_pdf(encrypted_pdf_path, key)

temp_file_name = decrypt(encrypted_pdf_path, key, owner_password)

# 외부 뷰어에서 열기 Windows용
#os.startfile(temp_file_name)

# 외부 뷰어에서 열기 (macOS용)
subprocess.run(['open', temp_file_name])

# 임시파일 삭제하는 코드
threading.Thread(target=delete_temp_file, args=(temp_file_name, delete_delay)).start()