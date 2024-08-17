import streamlit as st
import openai
import datetime
import json
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키를 환경 변수에서 가져옴
openai.api_key = os.getenv("OPENAI_API_KEY")

def calculate_life_path_number(birthdate):
    total = sum(int(digit) for digit in birthdate.strftime("%d%m%Y"))
    while total > 9:
        total = sum(int(digit) for digit in str(total))
    return total

def get_lucky_numbers(life_path_number, current_date):
    prompt = f"""
    당신은 숫자학 전문가입니다. 생명수 {life_path_number}인 사람을 위해 {current_date.strftime('%Y년 %m월 %d일')}에 해당하는 1부터 45 사이의 행운의 숫자 6개를 생성해주세요.
    다음 요소들을 고려해주세요:
    1. 생명수: {life_path_number}
    2. 현재 날짜: {current_date.strftime('%Y년 %m월 %d일')}
    3. 요일: {['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일'][current_date.weekday()]}
    4. 월: {current_date.strftime('%m월')}
    5. 계절: {get_season(current_date)}

    각 숫자에 대한 자세한 설명과 그 의미를 장문으로 제공해주세요. 또한, 왜 이 6개의 숫자가 선택되었는지에 대한 전체적인 설명도 포함해주세요.
    응답은 'numbers' (6개의 정수 리스트), 'explanations' (6개의 문자열 리스트), 'overall_explanation' (전체 설명을 위한 문자열) 키를 가진 JSON 객체 형식으로 작성해주세요.
    모든 설명은 한국어로 작성해주세요.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "당신은 세계적으로 예측을 가장 잘하는 수비학 전문 박사입니다. 생명수와 현재 날짜를 바탕으로 행운의 숫자를 생성하는 숙련된 수비학 전문가입니다."},
            {"role": "user", "content": prompt}
        ]
    )

    try:
        result = json.loads(response.choices[0].message.content)
        return result['numbers'], result['explanations'], result['overall_explanation']
    except json.JSONDecodeError:
        st.error("GPT-4의 응답을 해석하는 데 문제가 발생했습니다. 다시 시도해 주세요.")
        return [], [], ""

def get_season(date):
    month = date.month
    if 3 <= month <= 5:
        return "봄"
    elif 6 <= month <= 8:
        return "여름"
    elif 9 <= month <= 11:
        return "가을"
    else:
        return "겨울"

st.title("🔮 한국식 수비학 운세 풀이 앱")

st.write("이 앱은 여러분의 생년월일과 선택한 날짜를 바탕으로 수비학적 운세와 행운의 숫자를 제공합니다.")
st.write("⚠️ 주의: 양력 생년월일을 입력해 주세요.")

birthdate = st.date_input("양력 생년월일을 선택하세요", min_value=datetime.date(1900, 1, 1))
current_date = st.date_input("운세를 보고 싶은 날짜를 선택하세요", min_value=birthdate)

if st.button("🔮 운세 보기"):
    if not openai.api_key:
        st.error("OpenAI API 키가 설정되지 않았습니다. .env 파일을 확인해주세요.")
    else:
        with st.spinner("운세를 분석 중입니다..."):
            life_path_number = calculate_life_path_number(birthdate)
            st.write(f"🔢 당신의 생명수는 **{life_path_number}** 입니다.")

            lucky_numbers, explanations, overall_explanation = get_lucky_numbers(life_path_number, current_date)
            
            if lucky_numbers and explanations:
                st.subheader("🍀 오늘의 행운의 숫자")
                for num, explanation in zip(lucky_numbers, explanations):
                    st.write(f"**{num}**: {explanation}")

                st.subheader("✨ 숫자 선택 이유")
                st.write(overall_explanation)

                st.subheader("🎱 최종 행운의 숫자")
                st.write(" ".join(map(str, lucky_numbers)))

                st.balloons()
            else:
                st.warning("행운의 숫자를 생성하는 데 문제가 발생했습니다. 다시 시도해 주세요.")

st.write("---")
st.write("📌 참고: 이 앱은 오락 목적으로 제작되었습니다. 중요한 결정은 이 운세에 의존하지 마시고, 현실적인 판단을 해주세요.")