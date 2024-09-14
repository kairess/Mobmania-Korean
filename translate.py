import csv
import anthropic
import time
from tqdm import tqdm

client = anthropic.Anthropic(api_key="YOUR_API_KEY")

input_file = 'e_desc.csv'
output_file = 'overrides\\e_desc.csv'

# CSV 파일 읽기
with open(input_file, 'r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    all_rows = list(reader)

# 스킬 인덱스별로 그룹화
skill_groups = {}
for row in all_rows:
    skill_index = row[0]
    if skill_index not in skill_groups:
        skill_groups[skill_index] = []
    skill_groups[skill_index].append(row)

system_prompt = """당신은 게임 번역 전문가입니다. 게임 스킬 설명을 한국어로 번역해주세요. 
번역 시 다음 지침을 따라주세요:
1. 게임 용어는 일관성 있게 번역하세요.
2. 게임 세계관에 맞는 자연스러운 표현을 사용하세요.
3. 숫자와 단위는 원문 그대로 유지하세요.
4. 기술적인 용어는 가능한 한 한국어로 의역하되, 필요시 원어를 괄호 안에 병기하세요.
5. 플레이어의 몰입감을 높이는 문체를 사용하세요.
6. 반드시 한국어 스킬 설명만 반환하세요. 스킬레벨별로 엔터로 구분하세요.

다음과 같은 형식으로 번역 결과를 반환해주세요:
100 데미지를 주는 펀치 12개 발사 (공격 속도 7.5) (쿨다운 2.5초). 4번째 펀치마다 대시.
+4 펀치 (16개).
"""

for skill_index, skill_rows in tqdm(skill_groups.items()):
    user_message = "원문:\n"
    for row in skill_rows:
        user_message += f"{','.join(row[:3])}\n"
    
    user_message += "\n번역:"

    print(user_message)

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1500,
        temperature=0.2,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": [{
                "type": "text",
                "text": user_message
            }]
        }],
    )

    translations = message.content[0].text.strip().split('\n')

    print(translations)

    i = 0
    for translation in translations:
        if translation:
            try:
                skill_groups[skill_index][i][3] = translation.strip()
            except:
                skill_groups[skill_index][i].append(translation.strip())
            i+=1
    
    time.sleep(1)  # API 요청 간 간격

# 번역 결과를 원래 순서대로 정렬
translated_rows = []
for row in all_rows:
    skill_index = row[0]
    level = row[1]
    for skill_row in skill_groups[skill_index]:
        if skill_row[1] == level:
            translated_rows.append(skill_row)
            break

# 결과를 CSV 파일로 저장
with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(translated_rows)

