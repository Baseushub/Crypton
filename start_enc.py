import jwt
import hashlib
import re
import secrets
import pikepdf
from pikepdf import Encryption
import datetime
import string

# pdf 암호화
# 해시 및 인증용 토큰을 담은 JWT 토큰 생성

# 해쉬값 생성 파트
def generate_pdf_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as pdf_file:
        buf = pdf_file.read()
        
        # 여기다 이 코드를 넣으면 시간에 따라 해시값이 다름.
        current_time = int(datetime.datetime.now().timestamp() * 1000)%1000
        current_time = current_time.to_bytes(2, byteorder='big')
        buf = buf + current_time
        hasher.update(buf)
    return hasher.hexdigest()

# 해쉬값을 바탕으로 JWT 토큰 생성
def create_jwt_token(pdf_hash, random_string_token, secret_key):
    payload = {
        'pdf_hash': pdf_hash,
        'random_string': random_string_token
        #'exp': datetime.datetime.now() + datetime.timedelta(days=1)  # 토큰 만료 시간 설정
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token
#/*해쉬값에 대한 랜덤 문자열 추가해야됨*/

# 안전한 랜덤 문자열 생성
def generate_secure_random_string(length):
    # 사용할 문자 집합 정의 (대문자, 소문자, 숫자, 특수 문자 포함)
    characters = string.ascii_letters + string.digits + string.punctuation
    # 랜덤한 문자열 생성
    secure_random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return secure_random_string

# PDF 파일 암호화
def encrypt_pdf(input_pdf, output_pdf, user_password, owner_password):
    # PDF 파일 열기
    with pikepdf.open(input_pdf) as pdf:
        # 보안 옵션 설정 및 암호화
        pdf.save(output_pdf, encryption=Encryption(
            user=user_password,
            owner=owner_password,
            R=6,  # AES-256
            aes=True,
            metadata=False
        ))

def modify_jwt_in_pdf(file_path, jwt_token):
    # 1. 파일을 바이트 단위로 읽기
    with open(file_path, 'rb') as file:
        byte_content = file.read()

    # 2. 바이트 데이터를 'latin1' 인코딩으로 문자열로 변환
    text_content = byte_content.decode('latin1')

    # 3. /JWT로 시작하는 줄 찾기 및 수정
    pattern = re.compile(r'/JWT\s+<([^>]*)>')

    def replace_jwt_content(match):
        old_content = match.group(1)
        new_content = jwt_token  # 원하는 문자열로 변경
        return f'/JWT <{new_content}>'

    modified_text = pattern.sub(replace_jwt_content, text_content)

    # 4. 수정된 문자열을 다시 바이트로 변환하여 파일에 쓰기
    modified_byte_content = modified_text.encode('latin1')

    with open(file_path, 'wb') as file:
        file.write(modified_byte_content)

def add_jwt_seat_to_metadata(input_pdf):
    with pikepdf.open(input_pdf, allow_overwriting_input=True) as pdf:
        pdf.docinfo['/JWT'] = 'TEST'
        pdf.save(input_pdf)

#-------------------------------------------------------
# PDF 파일 경로 설정
pdf_path = "/Users/macbook/Documents/사업/pdf1.8/testPDF.pdf"
encrypted_pdf_path = "/Users/macbook/Documents/사업/pdf1.8/ENC_testPDF.pdf"

# 32바이트 키 생성
userpass = '1234567890'#os.urandom(32) # os의 랜덤 바이트 생성 기능
ownerpass = '123456789'#os.urandom(32) #스트링으로 넣기~

#-------------------------------------------------------

# PDF 에 대한 해쉬값 생성
pdf_hash = generate_pdf_hash(pdf_path)

# JWT 토큰 들어갈 자리 메타데이터에 만들기
add_jwt_seat_to_metadata(pdf_path)

# JWT 토큰에 들어갈 랜덤 문자열
random_string_token = generate_secure_random_string(30)

#랜덤 문자열 만들어주고, 그걸 secret_key로 사용
secret_key = generate_secure_random_string(30) # 나중에 빠져도 됨. JWT token의 secret key는 하나만 존재해야 서버 부하 낮음

# JWT 토큰 생성
jwt_token = create_jwt_token(pdf_hash, random_string_token, secret_key)

# PDF 파일 암호화하고 보안옵션 설정 후 저장
encrypt_pdf(pdf_path, encrypted_pdf_path, userpass, ownerpass)

# JWT 토큰 넣기
modify_jwt_in_pdf(encrypted_pdf_path, jwt_token)