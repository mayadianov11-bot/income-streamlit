import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Прогноз дохода", layout="centered")

# Загружаем модель
model = joblib.load("model.pkl")

# ---------- ШАПКА ----------
st.title("Гениальное приложение по предсказыванию среднего дохода")
st.write("Заполните форму ниже и узнайте можете ли вы зарабатывать больше 50к.")
st.markdown("---")

# ============================================================
#                  БЛОК 1. ЧИСЛОВЫЕ ПРИЗНАКИ
# ============================================================

st.header("Немного цифр о вас")

col1, col2 = st.columns(2)

with col1:
    age = st.slider(
        "Сколько вам полных лет?",
        min_value=17,
        max_value=90,
        value=0,
        help="Возраст респондента на момент опроса"
    )

    fnlwgt = st.number_input(
        "Вес наблюдения",
        min_value=19302,
        max_value=1484705,
        value=19302,
        help="Технический коэффициент. "
             "Если не знаете, оставьте значение по умолчанию."
    )

    hours_per_week = st.slider(
        "Сколько часов в неделю вы обычно работаете?",
        min_value=1,
        max_value=99,
        value=1,
        help="Среднее количество рабочих часов в неделю"
    )

with col2:
    capital_gain = st.slider(
        "Доход от инвестиций за год",
        min_value=0,
        max_value=99999,
        value=0,
        help="Прибыль от капитальных вложений. "
             "Если инвестиций не было, оставьте 0."
    )

    capital_loss = st.slider(
        "Убытки от инвестиций за год",
        min_value=0,
        max_value=3900,
        value=0,
        help="Фиксированные убытки от инвестиций. "
             "Если убытков не было, оставьте 0."
    )

st.markdown("---")


# ============================================================
#                БЛОК 2. КАТЕГОРИАЛЬНЫЕ ПРИЗНАКИ
# ============================================================

st.header("И немного о вас в категориях")

# --------- EDUCATION ---------
education_map = {
    "Детский сад": "Preschool",
    "1–4 классы школы": "1st-4th",
    "5–6 классы школы": "5th-6th",
    "7–8 классы школы": "7th-8th",
    "9 классов школы": "9th",
    "10 классов школы": "10th",
    "11 классов школы": "11th",
    "12 классов школы": "12th",
    "Школьный аттестат (полное среднее)": "HS-grad",
    "Некоторое время в колледже/вузе": "Some-college",
    "Колледж (профессиональный диплом)": "Assoc-voc",
    "Колледж (академический диплом)": "Assoc-acdm",
    "Бакалавр": "Bachelors",
    "Магистр": "Masters",
    "Профессиональная школа (мед, юр и т.п.)": "Prof-school",
    "Докторская степень": "Doctorate"
}

education_to_num = {
    "Preschool": 1, "1st-4th": 2, "5th-6th": 3, "7th-8th": 4, "9th": 5,
    "10th": 6, "11th": 7, "12th": 8, "HS-grad": 9, "Some-college": 10,
    "Assoc-voc": 11, "Assoc-acdm": 12, "Bachelors": 13,
    "Masters": 14, "Prof-school": 15, "Doctorate": 16
}

col1, col2 = st.columns(2)


education_ru = st.selectbox(
    "Какой у вас максимальный завершённый уровень образования?",
    list(education_map.keys()),
    help="Выберите самый высокий уровень образования, который вы полностью завершили"
)
education = education_map[education_ru]
education_num = education_to_num[education]

# --------- WORKCLASS & MARITAL ---------
with col2:
    workclass_map = {
        "Частный сектор": "Private",
        "Самозанятый (без регистрации компании)": "Self-emp-not-inc",
        "Самозанятый (как зарегистрированная компания)": "Self-emp-inc",
        "Местное правительство (город/район)": "Local-gov",
        "Правительство штата": "State-gov",
        "Федеральное правительство": "Federal-gov",
        "Работа без оплаты (волонтёрство и т.п.)": "Without-pay"
    }

    marital_map = {
        "Никогда не был(а) в официальном браке": "Never-married",
        "В официальном браке, живу с партнёром": "Married-civ-spouse",
        "В браке (военная служба AF-spouse)": "Married-AF-spouse",
        "В браке, но супруг(а) сейчас не живёт со мной": "Married-spouse-absent",
        "Временно живём отдельно": "Separated",
        "Разведён(а)": "Divorced",
        "Вдова/вдовец": "Widowed"
    }

workclass = workclass_map[st.selectbox(
    "Какой у вас тип занятости?",
    list(workclass_map.keys()),
    help="Определите свою форму занятости: частный сектор, самозанятость, госслужба и др."

)]

marital = marital_map[st.selectbox(
    "Ваше текущее семейное положение?",
    list(marital_map.keys()),
    help="Выберите вариант, который наиболее точно описывает вашу семейную ситуацию."
)]


# --------- occupation / relationship / race / sex ---------

occupation_map = {
    "Административная работа (офис, clerical)": "Adm-clerical",
    "Вооружённые силы": "Armed-Forces",
    "Ремесло / ремонт, рабочие специальности": "Craft-repair",
    "Руководитель / управление": "Exec-managerial",
    "Сельское хозяйство / рыбалка": "Farming-fishing",
    "Уборка / неквалифицированный физический труд": "Handlers-cleaners",
    "Оператор машин и оборудования": "Machine-op-inspct",
    "Сфера услуг (обслуживание клиентов, сервис)": "Other-service",
    "Домашний персонал (няни, домработники и т.п.)": "Priv-house-serv",
    "Профессиональные специальности (врачи, юристы и др.)": "Prof-specialty",
    "Охрана / безопасность": "Protective-serv",
    "Продажи (розничные, оптовые и т.п.)": "Sales",
    "Техническая поддержка (IT и др.)": "Tech-support",
    "Транспорт / логистика": "Transport-moving"
}

occupation = occupation_map[st.selectbox(
    "Чем вы в основном занимаетесь на работе?",
    list(occupation_map.keys()),
    help="Тип вашей основной работы или профессиональной деятельности."
)]

relationship_map = {
    "Живу с супругом/супругой, я основной добытчик": "Husband",
    "Живу с супругом/супругой, основной добытчик — партнёр": "Wife",
    "Я живу с родителями/опекунами как ребёнок": "Own-child",
    "Живу отдельно, без семьи": "Not-in-family",
    "Живу с другими родственниками": "Other-relative",
    "Не состою в официальном браке, живу один/одна": "Unmarried"
}

relationship = relationship_map[st.selectbox(
    "С кем вы в основном живёте сейчас?",
    list(relationship_map.keys()),
    help="Выберите вариант, который наиболее точно вам подходит."
)]

colA, colB = st.columns(2)

with colA:
    race_map = {
        "Белые": "White",
        "Чёрные": "Black",
        "Азиаты/тихоокеанцы": "Asian-Pac-Islander",
        "Индейцы/эскимосы": "Amer-Indian-Eskimo",
        "Другая / смешанная": "Other"
    }

    race = race_map[st.selectbox(
        "К какой расовой группе вы себя относите?",
        list(race_map.keys()),
        help="Выберите вариант, который вам наиболее подходит."
    )]

with colB:


    sex_choice = st.radio(
        "Укажите ваш пол:",
        ["Женский", "Мужской"],
        help="Выберите вариант, который вам наиболее подходит."
    )
    sex = "Male" if sex_choice == "Мужской" else "Female"

st.markdown("---")
# ============================================================
#                   ПРЕДСКАЗАНИЕ
# ============================================================

if st.button("Предсказать доход"):

    # 1. Числа
    data_input = {
        "age": age,
        "fnlwgt": fnlwgt,
        "education-num": education_num,
        "capital-gain": capital_gain,
        "capital-loss": capital_loss,
        "hours-per-week": hours_per_week,
    }

    # 2. Дамми
    dummy_columns = [
        'workclass_Local-gov','workclass_Private','workclass_Self-emp-inc',
        'workclass_Self-emp-not-inc','workclass_State-gov','workclass_Without-pay',

        'education_11th','education_12th','education_1st-4th','education_5th-6th',
        'education_7th-8th','education_9th','education_Assoc-acdm','education_Assoc-voc',
        'education_Bachelors','education_Doctorate','education_HS-grad','education_Masters',
        'education_Preschool','education_Prof-school','education_Some-college',

        'marital-status_Married-AF-spouse','marital-status_Married-civ-spouse',
        'marital-status_Married-spouse-absent','marital-status_Never-married',
        'marital-status_Separated','marital-status_Widowed',

        'occupation_Armed-Forces','occupation_Craft-repair','occupation_Exec-managerial',
        'occupation_Farming-fishing','occupation_Handlers-cleaners','occupation_Machine-op-inspct',
        'occupation_Other-service','occupation_Priv-house-serv','occupation_Prof-specialty',
        'occupation_Protective-serv','occupation_Sales','occupation_Tech-support',
        'occupation_Transport-moving',

        'relationship_Not-in-family','relationship_Other-relative','relationship_Own-child',
        'relationship_Unmarried','relationship_Wife',

        'race_Asian-Pac-Islander','race_Black','race_Other','race_White',
        'sex_Male'
    ]

    for col in dummy_columns:
        data_input[col] = 0

    mapping = {
        f"workclass_{workclass}": workclass,
        f"education_{education}": education,
        f"marital-status_{marital}": marital,
        f"occupation_{occupation}": occupation,
        f"relationship_{relationship}": relationship,
        f"race_{race}": race
    }

    for col in mapping:
        if col in dummy_columns:
            data_input[col] = 1

    if sex == "Male":
        data_input["sex_Male"] = 1

    X_input = pd.DataFrame([data_input])

    pred = model.predict(X_input)[0]
    prob = model.predict_proba(X_input)[0][1]

    # ---------- ПРЕДСКАЗАНИЕ ----------
    st.subheader("Результат прогноза")

    pred = model.predict(X_input)[0]
    prob = model.predict_proba(X_input)[0][1]

    # ---------- CSS для анимации ----------
    st.markdown(
        """
        <style>
        @keyframes fadeSlide {
            0% {opacity: 0; transform: translateY(20px);}
            100% {opacity: 1; transform: translateY(0);}
        }
        .result-card {
            animation: fadeSlide 0.8s ease-out forwards;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Если доход > 50K
    if pred == 1:
        st.markdown(
            f"""
            <div class="result-card" style="
                padding: 20px;
                border-radius: 12px;
                background-color: #0f3d21;
                border: 2px solid #4ade80;
                color: #d1ffe8;
                font-size: 18px;
                margin-top: 20px;
            ">
                <h3 style="color: #86ffb3; margin-top: 0;">
                    Доход выше 50K
                </h3>
                <p>Модель прогнозирует, что ваш годовой доход, вероятно, превышает 50K.</p>
                <p><b>Оценка вероятности, что доход превышает 50к: {prob*100:.2f}%</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Если доход ≤ 50K
    else:
        st.markdown(
            f"""
            <div class="result-card" style="
                padding: 20px;
                border-radius: 12px;
                background-color: #3a0d0d;
                border: 2px solid #ff6b6b;
                color: #ffecec;
                font-size: 18px;
                margin-top: 20px;
            ">
                <h3 style="color: #ffb3b3; margin-top: 0;">
                    Доход не превышает 50K
                </h3>
                <p>Модель считает, что ваш годовой доход скорее всего не превышает 50K.</p>
                <p><b>Оценка вероятности, что доход превышает 50к: {prob*100:.2f}%</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )