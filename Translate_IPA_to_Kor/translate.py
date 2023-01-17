from hangul_utils import join_jamos


class IPA2KOR:
    def __init__(self):
        self.VOWEL = "vowel"
        self.CONSONANT = "consonant"
        self.SHORT_VOWEL = "short-vowel"
        self.SEMI_VOWEL = "semi-vowel"
        self.MIDDLE_VOWEL = "middle-vowel"
        self.dict = {
            # 모음
            self.VOWEL: {
                "i": "ㅇㅣ", "y": "ㅇㅟ", "e": "ㅇㅔ", "ø": "ㅇㅚ", "ɛ": "ㅇㅒ", "œ": "ㅇㅚ", "æ": "ㅇㅐ", "a": "ㅇㅏ",
                "α": "ㅇㅏ", "ʌ": "ㅇㅓ", "ɔ": "ㅇㅗ", "o": "ㅇㅗ", "u": "ㅇㅜ", "ə": "ㅇㅓ", "ɚ": "ㅇㅓ", "ɪ": "ㅇㅣ", "ʊ": "ㅇㅜ"
            },
            # 자음 : [모음 앞, 자음 앞 또는 어말]
            self.CONSONANT: {
                "p": ["ㅍ", ["ㅂ", "ㅍㅡ"]], "t": ["ㅌ", ["ㅅ", "ㅌㅡ"]], "k": ["ㅋ", ["ㄱ", "ㅋㅡ"]],
                "b": ["ㅂ", "ㅂㅡ"], "d": ["ㄷ", "ㄷㅡ"], "g": ["ㄱ", "ㄱㅡ"],
                "s": ["ㅅ", "ㅅㅡ"], "z": ["ㅈ", "ㅈㅡ"], "f": ["ㅍ", "ㅍㅡ"], "v": ["ㅂ", "ㅂㅡ"], "θ": ["ㅅ", "ㅅㅡ"], "ð": ["ㄷ", "ㄷㅡ"], "ʃ": ["ㅅㅣ", ["ㅅㅠ", "ㅅㅣ"]], "ʒ": ["ㅈ", "ㅈㅣ"],
                "ʦ": ["ㅊ", "ㅊㅡ"], "ʣ": ["ㅈ", "ㅈㅡ"], "ʧ": ["ㅊ", "ㅊㅣ"], "ʤ": ["ㅈ", "ㅈㅣ"],
                "m": "ㅁ", "n": "ㄴ", "ŋ": "ㅇ",
                "l": [["ㄹ", "ㄹㄹ"], "ㄹ"],
                "ɲ": ["ㄴㅣ", "ㄴㅠ"], "r": ["ㄹ", "ㄹㅡ"], "h": ["ㅎ", "ㅎㅡ"], "ç": ["ㅎ", "ㅎㅣ"], "x": ["ㅎ", "ㅎㅡ"]
            },
            # 단모음
            self.SHORT_VOWEL: ["ɪ", "ʊ", "i", "e", "æ", "a", "α", "ʌ", "ɔ", "o", "u", "ə", "ɚ"],
            # 반모음
            self.SEMI_VOWEL: {"j": "ㅇㅣ", "ɥ": "ㅇㅟ", "w": ["ㅇㅗ", "ㅇㅜ"]},
            # 중모음
            self.MIDDLE_VOWEL: {"ai": "ㅇㅏㅇㅣ", "au": "ㅇㅏㅇㅜ", "ei": "ㅇㅔㅇㅣ", "ɔi": "ㅇㅗㅇㅣ", "ou": "ㅇㅗ", "oʊ": "ㅇㅗ", "auə": "ㅇㅏㅇㅝ"}
        }

    def pronunciation_classification(self, word):
        for idx, (key, alpha) in enumerate(self.dict.items()):
            if word in alpha:
                return key

    def vowel_classification(self, word, idx):
        vowel = ""
        for i in word[::-1][len(word)-idx:]:
            if self.pronunciation_classification(i) == self.CONSONANT:
                break
            else:
                vowel += i
        return vowel[::-1]

    def translate(self, word):
        hangul = ""
        idx = 0
        while idx < len(word):
            pron = self.pronunciation_classification(word[idx])
            kor = ""
            # 모음
            if pron == self.VOWEL:
                idx, kor = self.Vowel(word, idx)
            # 자음[모음 앞/어말 or 자음 앞] = 0/1
            elif pron == self.CONSONANT:
                idx, kor = self.Consonant(word, idx)
            # 반모음
            elif pron == self.SEMI_VOWEL:
                idx, kor = self.SemiVowel(word, idx)
            hangul += kor
            idx += 1
        return join_jamos(hangul)

    def Vowel(self, word, idx):
        front = word[idx - 1] if idx > 0 else None
        if front is not None:
            if front == "ŋ":
                return idx, self.NasalSound(word[idx - 2] if idx > 1 else None, word[idx])
            else:
                front = self.pronunciation_classification(front)
                if len(word) - idx >= 3 and word[idx:idx+3] == "aʊə":
                    return idx+2, 'ㅏ워' if front == self.CONSONANT else '아워'
                elif len(word) - idx >= 2 and word[idx:idx+2] == "oʊ":
                    return idx+1, 'ㅗ' if front == self.CONSONANT else '오'
                else:
                    return idx, self.dict[self.VOWEL][word[idx]][1:] if front == self.CONSONANT else self.dict[self.VOWEL][word[idx]]
        else:
            return idx, self.dict[self.VOWEL][word[idx]]

    def Consonant(self, word, idx):
        # [모음 앞 / 자음 앞 or 반모음 앞 or 어말]
        kor = self.dict[self.CONSONANT][word[idx]]
        # 앞 단어(없을 경우 None)
        front = word[idx - 1] if idx > 0 else None
        # 뒤 단어(없을 경우 None)
        rear = word[idx + 1] if idx < len(word) - 1 else None
        # 첫 단어인 경우 True 나머지 False
        start = True if idx == 0 else False
        # 마지막 단어인 경우 True 나머지 False
        end = True if idx == len(word) - 1 else False

        if word[idx] in ['g', 'h', 'k'] and rear == 'w':
            return idx, ""
        # 제1항 무성 파열음([p], [t], [k])
        elif word[idx] in ['p', 't', 'k']:
            return idx, self.VoicelessPlosive(self.vowel_classification(word, idx), kor, rear, end)
        # 제3항 마찰음([s], [z], [f], [v], [θ], [ð], [ʃ], [ʒ])
        elif word[idx] in ["s", "z", "f", "v", "θ", "ð", "ʃ", "ʒ"]:
            return self.Fricative(idx, word)
        # 제5항 비음([m], [n], [ŋ])
        elif word[idx] in ['m', 'n', 'ŋ']:
            return idx, kor
        # 제6항 유음([l])
        elif word[idx] == 'l':
            return idx, self.Liquid(front, kor, rear, start, end)
        # 제2항 유성 파열음([b], [d], [g])
        # 제4항 파찰음([ʦ], [ʣ], [ʧ], [ʤ])
        # 나머지 자음([ɲ], [r], [h], [ç], [x])
        else:
            return idx, kor[0] if (not end and rear in self.dict[self.VOWEL].keys()) or (word[idx:idx+3] == 'djə') else kor[1]

    # 제1항 무성 파열음([p], [t], [k])
    # p : [모음 앞 : ㅍ / 자음 앞 or 반모음 앞 or 어말 : ㅂ, 프]
    # t : [모음 앞 : ㅌ / 자음 앞 or 반모음 앞 or 어말 : ㅅ, 트]
    # k : [모음 앞 : ㅋ / 자음 앞 or 반모음 앞 or 어말 : ㄱ, 크]
    def VoicelessPlosive(self, front, word, rear, end):
        # 1. 짧은 모음 다음의 어말 무성 파열음([p], [t], [k])은 받침으로 적는다.
        # 2. 짧은 모음과 유음·비음([l], [r], [m], [n]) 이외의 자음 사이에 오는 무성 파열음([p], [t], [k])은 받침으로 적는다.
        if front in self.dict[self.SHORT_VOWEL] and (end or rear in list(set(self.dict[self.CONSONANT].keys()) - {'l', 'r', 'm', 'n'})):
            return word[1][0]
        elif not end and rear in self.dict[self.VOWEL].keys():
            return word[0]
        # 3. 위 경우 이외의 어말과 자음 앞의 [p], [t], [k]는 '으'를 붙여 적는다.
        else:
            return word[1][1]

    # 제3항 마찰음([s], [z], [f], [v], [θ], [ð], [ʃ], [ʒ])
    # s : [모음 앞 : ㅅ / 자음 앞 or 반모음 앞 or 어말 : 스]
    # z : [모음 앞 : ㅈ / 자음 앞 or 반모음 앞 or 어말 : 즈]
    # f : [모음 앞 : ㅍ / 자음 앞 or 반모음 앞 or 어말 : 프]
    # v : [모음 앞 : ㅂ / 자음 앞 or 반모음 앞 or 어말 : 브]
    # θ : [모음 앞 : ㅅ / 자음 앞 or 반모음 앞 or 어말 : 스]
    # ð : [모음 앞 : ㄷ / 자음 앞 or 반모음 앞 or 어말 : 드]
    # ʃ : [모음 앞 : 시 / 자음 앞 or 반모음 앞 or 어말 : 슈, 시]
    # ʒ : [모음 앞 : ㅈ / 자음 앞 or 반모음 앞 or 어말 : 지]
    def Fricative(self, idx, word):
        dictionary = {"ʃα": 'ㅅㅑ', "ʃæ": 'ㅅㅒ', "ʃə": 'ㅅㅕ', "ʃe": 'ㅅㅖ', "ʃɔ": 'ㅅㅛ', "ʃu": 'ㅅㅠ', "ʃi": 'ㅅㅣ'}
        kor = self.dict[self.CONSONANT][word[idx]]
        rear = word[idx + 1] if idx < len(word) - 1 else None
        end = True if idx == len(word) - 1 else False
        # 1. 어말 또는 자음 앞의 [s], [z], [f], [v], [θ], [ð]는 '으'를 붙여 적는다.
        # 3. 어말 또는 자음 앞의 [ʒ]는 '지'로 적고, 모음 앞의 [ʒ]는 'ㅈ'으로 적는다.
        if word[idx] != 'ʃ':
            if not end and rear in self.dict[self.VOWEL].keys():
                return idx, kor[0]
            else:
                return idx, kor[1]
        # 2. 어말의 [ʃ]는 '시'로 적고, 자음 앞의 [ʃ]는 '슈'로, 모음 앞의 [ʃ]는 뒤따르는 모음에 따라 '샤', '섀', '셔', '셰', '쇼', '슈', '시'로 적는다.
        else:
            if end or rear in self.dict[self.SEMI_VOWEL]:
                return idx, kor[1][1]
            elif rear in self.dict[self.CONSONANT].keys():
                return idx, kor[1][0]
            else:
                return idx+1, dictionary[word[idx]+rear] if word[idx] + rear in dictionary.keys() else kor[0][0]

    # 제5항 비음([m], [n], [ŋ])
    # m : [모음 앞 : ㅁ / 자음 앞 or 반모음 앞 or 어말 : ㅁ]
    # n : [모음 앞 : ㄴ / 자음 앞 or 반모음 앞 or 어말 : ㄴ]
    # ŋ : [모음 앞 : ㅇ / 자음 앞 or 반모음 앞 or 어말 : ㅇ]
    # 1. 어말 또는 자음 앞의 비음은 모두 받침으로 적는다.
    def NasalSound(self, front, rear):
        # 2. 모음과 모음 사이의 [ŋ]은 앞 음절의 받침 'ㅇ'으로 적는다.
        if front is not None and self.pronunciation_classification(front) == self.VOWEL:
            return self.dict[self.VOWEL][rear]
        else:
            return self.dict[self.VOWEL][rear][1:]

    # 제6항 유음([l])
    # l : [모음 앞 : ㄹ, ㄹㄹ / 자음 앞 or 반모음 앞 or 어말 : ㄹ]
    def Liquid(self, front, word, rear, start, end):
        # 1. 어말 또는 자음 앞의 [l]은 받침으로 적는다.
        if end or rear in list(set(self.dict[self.CONSONANT].keys()) - {'m', 'n'}):
            return word[1]
        # 다만, 비음([m], [n]) 뒤의 [l]은 모음 앞에 오더라도 'ㄹ'로 적는다.
        elif front in ['m', 'n']:
            return word[0][0]
        # 2. 어중의 [l]이 모음 앞에 오거나, 모음이 따르지 않는 비음([m], [n]) 앞에 올 때에는 'ㄹㄹ'로 적는다.
        elif not start and rear in list(set(self.dict[self.VOWEL].keys()) | set(self.dict[self.SEMI_VOWEL].keys())):
            return word[0][1]
        elif not start and rear in ['m', 'n']:
            return word[0][1] + 'ㅡ'
        # 첫단어가 유음이고 뒤에 모음 or ['m', 'n']이 나오는 경우/ 어중의 l 뒤에 반모음이 나오는 경우
        else:
            return word[0][0]

    def SemiVowel(self, word, idx):
        dictionary = {
            # 반모음('w')
            "wə": "ㅇㅝ", "wɔ": "ㅇㅝ", "wou": "ㅇㅝ", "wα": "ㅇㅘ", "wæ": "ㅇㅙ", "we": "ㅇㅞ", "wi": "ㅇㅟ", "wu": "ㅇㅜ",
            # 반모음('j')
            "jα": "ㅇㅑ", "jæ": "ㅇㅒ", "jə": ["ㅇㅕ", "ㅣㅇㅓ"], "je": "ㅇㅖ", "jɔ": "ㅇㅛ", "ju": "ㅇㅠ", "ji": "ㅇㅣ"
        }
        front = word[idx - 1] if idx > 0 else None
        if word[idx] == 'w':
            if len(word) - idx >= 3 and word[idx:idx+3] == 'wou':
                return idx+2, self.dict[self.CONSONANT][front][0] + dictionary["wou"][1:] if front in ['g', 'h', 'k'] else dictionary["wou"]
            elif len(word) - idx >= 2 and word[idx:idx+2] in dictionary:
                return idx+1, self.dict[self.CONSONANT][front][0] + dictionary[word[idx:idx+2]][1:] if front in ['g', 'h', 'k'] else dictionary[word[idx:idx+2]]
            else:
                return idx, self.dict[self.SEMI_VOWEL][word[idx]][0]
        elif word[idx] == 'j' and len(word) - idx >= 2:
            if front in ['d', 'l', 'n'] and word[idx:idx+2] == 'jə':
                return idx + 1, dictionary[word[idx:idx+2]][1]
            elif word[idx:idx+2] == 'jə':
                return idx + 1, dictionary[word[idx:idx+2]][0]
            elif word[idx:idx+2] in dictionary:
                return idx + 1, dictionary[word[idx:idx+2]]
        return idx, self.dict[self.SEMI_VOWEL][word[idx]]

    def evaluate_performance(self, dictionary):
        print(f"전체 : {len(dictionary)}")
        score = 0
        for i in dictionary.keys():
            kor = self.translate(i)
            if dictionary[i] == kor:
                score += 1
            print(f"번역 : {kor}, 정답 : {dictionary[i]}, 정답 : {True if dictionary[i] == kor else False}")
        print(f"정답 : {score}")
        print(f"Accuracy : {score / len(dictionary)}")
