from translate import IPA2KOR

vlp_dict = {
    "gæp": "갭", "kæt": "캣", "bʊk": "북",
    "æpt": "앱트", "setbæk": "셋백", "ækt": "액트",
    "stæmp": "스탬프", "keɪp": "케이프", "nest": "네스트", "pαːt": "파트", "desk": "데스크",
    "meɪk": "메이크", "æpl": "애플", "mætris": "매트리스", "ʧipmʌŋk": "치프멍크", "siknis": "시크니스"
}

vdp_dict = {
    "bʌlb": "벌브", "lænd": "랜드", "zigzæg": "지그재그",
    "lɔbstə": "로브스터", "kidnæp": "키드냅", "signəl": "시그널"
}

fricative_dict = {
    "mαːsk": "마스크", "dʒæz": "재즈", "græf": "그래프", "ɔliv": "올리브", "θril": "스릴", "beið": "베이드",
    "flæʃ": "플래시", "ʃrʌb": "슈러브", "ʃαːk": "샤크", "ʃæŋk": "섕크", "fæʃən": "패션", "ʃerif": "셰리프", "ʃɔpiŋ": "쇼핑",
    "ʃuː": "슈", "ʃim": "심", "mirαːʒ": "미라지", "viʒən": "비전"
}

affricate_dict = {
    "kiːʦ": "키츠", "ɔʣ": "오즈", "swiʧ": "스위치", "briʤ": "브리지",
    "piʦbəːg": "피츠버그", "hiʧhaik": "히치하이크", "ʧαːt": "차트", "vəːʤin": "버진"
}

nasal_dict = {
    "stiːm": "스팀", "kɔːn": "콘", "riŋ": "링", "læmp": "램프",
    "hint": "힌트", "iŋk": "잉크", "hæŋiŋ": "행잉", "lɔŋiŋ": "롱잉"
}

liquid_dict = {
    "hoʊtel": "호텔", "pʌlp": "펄프", "slaid": "슬라이드", "film": "필름",
    "helm": "헬름", "swouln": "스월른", "hæmlit": "햄릿", "henli": "헨리"
}

long_vowel_dict = {"tiːm": "팀", "ruːt": "루트"}

middle_vowel_dict = {"taɪm": "타임", "haʊs": "하우스", "skeɪt": "스케이트", "ɔɪl": "오일", "boʊt": "보트", "taʊə": "타워"}

semi_vowel_dict = {
        "wəːd": "워드", "wɔnt": "원트", "wou": "워", "wαndə": "완더",
        "wæg": "왜그", "west": "웨스트", "wiʧ": "위치", "wul": "울",
        "swiŋ": "스윙", "twist": "트위스트", "peŋgwin": "펭귄", "hwisl": "휘슬", "kwɔːtə": "쿼터",
        "jαːd": "야드", "jæŋk": "얭크", "jəːn": "연", "jeloʊ": "옐로", "jɔːn": "욘",
        "juː": "유", "jiə": "이어", "indjən": "인디언", "bətæljən": "버탤리언", "juːnjən": "유니언"
}

compound_dict = {"kʌplaik": "컵라이크", "bukend": "북엔드", "hedlait": "헤드라이트", "tʌʧwud": "터치우드", "sitin": "싯인",
                 "bukmeikə": "북메이커", "flæʃgʌn": "플래시건", "tɔpnɔt": "톱놋", "lɔsæləmous": "로스앨러모스", "tɔpklæs": "톱클래스"}

# 표기의 기본 원칙
# 1. 외래어는 국어의 현용 24 자모만으로 적는다.
# 2. 외래어의 1 음운은 원칙적으로 1 기호로 적는다.
# 3. 받침에는 ‘ㄱ, ㄴ, ㄹ, ㅁ, ㅂ, ㅅ, ㅇ’만을 쓴다.
# 4. 파열음 표기에는 된소리를 쓰지 않는 것을 원칙으로 한다.
# 5. 이미 굳어진 외래어는 관용을 존중하되, 그 범위와 용례는 따로 정한다.

translator = IPA2KOR()
translator.evaluate_performance(vlp_dict)
translator.evaluate_performance(vdp_dict)
translator.evaluate_performance(fricative_dict) #재즈 해결
translator.evaluate_performance(affricate_dict)
translator.evaluate_performance(nasal_dict)
translator.evaluate_performance(liquid_dict)
translator.evaluate_performance(long_vowel_dict)
translator.evaluate_performance(middle_vowel_dict)
translator.evaluate_performance(semi_vowel_dict)
#translator.evaluate_performance(compound_dict) #받침 구분