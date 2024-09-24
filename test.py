import tempfile
import shutil
import os
import platform
import subprocess

# PDF 파일 생성 함수
def create_pdf(file_path):
    pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Count 1 /Kids [3 0 R] >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>
endobj
4 0 obj
<< /Length 44 >>
stream
BT
/F1 24 Tf
100 700 Td
(Hello, PDF!) Tj
ET
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f 
0000000010 00000 n 
0000000079 00000 n 
0000000178 00000 n 
0000000293 00000 n 
0000000380 00000 n 
trailer
<< /Root 1 0 R /Size 6 >>
startxref
467
%%EOF"""
    with open(file_path, 'wb') as f:
        f.write(pdf_content)

# PDF 열기 함수
def open_pdf(pdf_path):
    # 파일 경로가 절대 경로인지 확인하고, 절대 경로로 변환
    pdf_path = os.path.abspath(pdf_path)
    
    # 파일이 존재하는지 확인
    if not os.path.isfile(pdf_path):
        print(f"파일이 존재하지 않습니다: {pdf_path}")
        return
    
    if platform.system() == 'Darwin':  # macOS
        try:
            # open 명령어와 함께 -a 옵션으로 'Preview' 지정
            subprocess.run(['open', '-a', 'Preview', pdf_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"PDF 열기 오류: {e}")
    else:
        print('이 스크립트는 macOS에서만 작동합니다.')

# 임시 디렉토리 생성 (RAM에 저장하는 것처럼 사용)
ram_directory = tempfile.mkdtemp()

# PDF 파일 경로 정의
pdf_file_path = os.path.join(ram_directory, 'sample.pdf')

# PDF 파일 생성
create_pdf(pdf_file_path)

# PDF 파일이 생성되었는지 확인
if os.path.isfile(pdf_file_path):
    print(f"PDF 파일이 생성되었습니다: {pdf_file_path}")
    # PDF 파일 열기
    open_pdf(pdf_file_path)
else:
    print(f"PDF 파일 생성 실패: {pdf_file_path}")

# 임시 디렉토리 정리
#shutil.rmtree(ram_directory)