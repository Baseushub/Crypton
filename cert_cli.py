import re
import os
import requests
import json

# 메타데이터에서 JWT 추출 extract_jwt_from_binary
# JWT 서버로 보내기 send_token_receive_password
# 서버에서 준 JWT로 교체 modify_jwt_in_pdf

def extract_jwt_from_binary(input_pdf):
    jwt_token = None
    try:
        with open(input_pdf, 'rb') as file:
            content = file.read().decode('latin1')  # 바이너리 데이터를 문자열로 변환
            print("File content read and decoded.")

            # 정규 표현식을 사용하여 /Info 객체 찾기
            info_pattern = re.compile(r'/Info\s+(\d+)\s+0\s+R')
            match = info_pattern.search(content)
            if match:
                info_obj_num = match.group(1)
                print(f"/Info object found: {info_obj_num}")

                obj_pattern = re.compile(r'\b{}\s+0\s+obj\b(.*?)\bendobj\b'.format(info_obj_num), re.DOTALL)
                obj_match = obj_pattern.search(content)
                if obj_match:
                    info_content = obj_match.group(1)
                    print("/Info object content found.")
                    #print("Info content:", info_content)  # /Info 객체 내용 출력

                    # JWT 토큰 키-값 쌍 추출
                    jwt_pattern = re.compile(r'/JWT\s*\<([^)]*?)\>')
                    jwt_match = jwt_pattern.search(info_content)
                    if jwt_match:
                        jwt_token = jwt_match.group(1)
                        #print(f"JWT Token found: {jwt_token}")
                    else:
                        print("No JWT token found in /Info object.")
            else:
                print("No /Info object found.")
    except Exception as e:
        print(f"Failed to extract JWT token: {e}")
    return jwt_token

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

# JWT 토큰 서버로 보내고 비번 받아오기
def send_token_receive_password(extracted_jwt_token):
    try:
        jwt_token = extracted_jwt_token
        if jwt_token:
            # 서버로 JWT 토큰 전송
            headers = {'Content-Type': 'application/json'}
            data = {'jwt_token': jwt_token}
            
            response = requests.post(server_url, headers=headers, data=json.dumps(data))

            # 서버 응답 처리
            if response.status_code == 200:
                response_data = response.json()
                new_token = response_data.get('new_token')
                old_userpass = response_data.get('old_userpass')
                old_ownerpass = response_data.get('old_ownerpass')

                print(f"Received new token: {new_token}")
                print(f"Received old userpass: {old_userpass}")
                print(f"Received old ownerpass: {old_ownerpass}")

                return old_userpass, old_ownerpass
            else:
                print(f"Failed to get password: {response.status_code}")
                print(f"Server response: {response.text}")
                return None
        else:
            print("No JWT token extracted or failed to open the PDF.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return None



#-------------------------------------------------------
# 암호화된 pdf 경로
encrypted_pdf_path = "여기에 경로 입력"
# JWT 토큰값
jwt_token = f'여기에 JWT토큰 입력'

# 서버 URL 설정
server_url = 'http://localhost:5000/password_pdf'

#-------------------------------------------------------


# JWT 토큰 추출
extracted_jwt_token = extract_jwt_from_binary(encrypted_pdf_path)

if extracted_jwt_token:
    print(f"Extracted JWT Token: {extracted_jwt_token}")
else:
    print("No JWT token extracted or failed to open the PDF.")

# 서버로 JWT 토큰 보내고 비밀번호 받아오기

result = send_token_receive_password(extracted_jwt_token)
if result:
    userpass, ownerpass = result
    print("Successfully received the passwords.")
    print(f"User password: {userpass}")
    print(f"Owner password: {ownerpass}")
else:
    print("Failed to receive the passwords.")


# JWT 토큰 변경
modify_jwt_in_pdf(encrypted_pdf_path, jwt_token)