import csv
from googletrans import Translator

def translate_csv():
    translator = Translator()
    
    with open('overrides/e_name.csv', 'r', encoding='utf-8') as input_file, \
         open('overrides/e_name_translated.csv', 'w', newline='', encoding='utf-8') as output_file:
        
        reader = csv.reader(input_file)
        writer = csv.writer(output_file)
        
        # 헤더 추가
        writer.writerow(['ID', 'English Name', 'Korean Name'])
        
        for row in reader:
            id, name = row
            # 영어 이름을 한국어로 번역
            korean_name = translator.translate(name, src='en', dest='ko').text
            # 새 행에 ID, 영어 이름, 한국어 이름 추가
            writer.writerow([id, name, korean_name])

    print("번역이 완료되었습니다. 결과는 'overrides/e_name_translated.csv' 파일에 저장되었습니다.")

if __name__ == "__main__":
    translate_csv()
