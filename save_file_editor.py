import base64
import json
import os
import shutil

# 파일 경로
file_path = r"c:\Users\kaire\AppData\Local\Mobmania\profile.enc"

def decrypt_profile(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Steam ID (17자)와 암호화된 데이터 분리
    steam_id = content[:17]
    encrypted_data = content[17:]

    # Base64 디코딩
    decoded_data = base64.b64decode(encrypted_data)

    # JSON으로 파싱
    try:
        json_data = json.loads(decoded_data)
        return steam_id, json_data
    except json.JSONDecodeError:
        print("JSON 파싱 오류. 데이터가 올바른 JSON 형식이 아닙니다.")
        return steam_id, decoded_data.decode('utf-8', errors='ignore')

def encrypt_profile(steam_id, data):
    json_data = json.dumps(data)
    encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
    return steam_id + encoded_data

# 원본 파일 백업
backup_path = file_path + '.backup'
shutil.copy2(file_path, backup_path)
print(f"\n원본 파일이 {backup_path}로 백업되었습니다.")

# 복호화 실행
steam_id, decrypted_data = decrypt_profile(file_path)

print(f"Steam ID: {steam_id}")
# print("원본 복호화된 데이터:")
# print(json.dumps(decrypted_data, indent=2, ensure_ascii=False))

# ch_coins 값을 100으로 변경
decrypted_data['ch_coins'] = 1000
decrypted_data['coins'] = 1283971

decrypted_data['cardsOwned'] = [
    0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0,
    100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 108.0,

    1000.0, 1001.0, 1002.0, 1003.0, 1004.0, 1005.0, 1006.0, 1007.0, 1008.0, 1009.0, 1010.0, 1011.0, 1012.0, 1013.0, 1014.0, 1015.0, 1016.0, 1017.0, 1018.0, 1019.0,
    1100.0, 1101.0, 1102.0, 1103.0, 1104.0, 1105.0, 1106.0, 1107.0, 1108.0,

    2000.0, 2001.0, 2002.0, 2003.0, 2004.0, 2005.0, 2006.0, 2007.0, 2008.0, 2009.0, 2010.0, 2011.0, 2012.0, 2013.0, 2014.0, 2015.0, 2016.0, 2017.0, 2018.0, 2019.0,
    2100.0, 2101.0, 2102.0, 2103.0, 2104.0, 2105.0, 2106.0, 2107.0, 2108.0,

    3000.0, 3001.0, 3002.0, 3003.0, 3004.0, 3005.0, 3006.0, 3007.0, 3008.0, 3009.0, 3010.0, 3011.0, 3012.0, 3013.0, 3014.0, 3015.0, 3016.0, 3017.0, 3018.0, 3019.0,
    3100.0, 3101.0, 3102.0, 3103.0, 3104.0, 3105.0, 3106.0, 3107.0, 3108.0,
]
# exit()

# print("\n수정된 데이터:")
# print(json.dumps(decrypted_data, indent=2, ensure_ascii=False))

# 수정된 데이터를 암호화하여 원본 파일에 덮어쓰기
encrypted_data = encrypt_profile(steam_id, decrypted_data)
with open(file_path, 'w') as file:
    file.write(encrypted_data)

print(f"수정된 데이터가 {file_path}에 저장되었습니다.")

# 복호화된 데이터를 JSON 파일로 저장 (선택사항)
with open('decrypted.json', 'w', encoding='utf-8') as json_file:
    json.dump(decrypted_data, json_file, indent=2, ensure_ascii=False)

print("수정된 복호화 데이터가 'decrypted.json' 파일로 저장되었습니다.")
