#JWT 토큰 Verify
#인증용 토큰을 DB와 대조해 해당 P/W 찾기 -> dict.py랑 협업해서 작동할꺼임 ㅎ
import jwt
import pickle


def verify_jwt_token(jwt_token, secret_key):
    try:
        # JWT 토큰 디코딩
        decoded_token = jwt.decode(jwt_token, secret_key, algorithms=['HS256'])
        return True, decoded_token
    except jwt.ExpiredSignatureError:
        return False, "JWT Token is expired."
    except jwt.InvalidTokenError as e:
        return False, f"Invalid JWT Token: {e}"
    
    

#-------------------------------------------------------

jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwZGZfaGFzaCI6IjlkNjMyYjM1NDU0OTA5MTg5Y2Q4ZmJlNTg4YTk4OTkyNGU4YTY0MGVkZTRmMjdjYTVjMGE3OTVmNTkyMWM4ZjIiLCJyYW5kb21fc3RyaW5nIjoiO1R5fVM5Mjhla1RKU3wlVDNCfSk-TXBhKWQ2fmNSIn0.TNAmy81lh7Z4hZY5xGvgriQRYSXDqiyOAtNeOjc6ctE'
secret_key = '(e1:Ub-)+|(Yyf8(zSwR~!OQ*_:WU&'

#-------------------------------------------------------

# JWT 토큰 검증
is_valid, result = verify_jwt_token(jwt_token, secret_key)

if is_valid:
    print("JWT Token is valid.")
    print(f"Decoded Token: {result}")
else:
    print("JWT Token verification failed.")
    print(f"Error: {result}")



# ------------------------------------------------------------------