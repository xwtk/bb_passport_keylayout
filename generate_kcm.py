import os
import csv
from collections import defaultdict

# Define physical layouts
PHYSICAL_LAYOUTS = {
    'QWERTY': {
        'key_mapping': {
            16: 'Q', 17: 'W', 18: 'E', 19: 'R', 20: 'T', 21: 'Y', 22: 'U', 23: 'I', 24: 'O', 25: 'P',
            30: 'A', 31: 'S', 32: 'D', 33: 'F', 34: 'G', 35: 'H', 36: 'J', 37: 'K', 38: 'L',
            44: 'Z', 45: 'X', 46: 'C', 47: 'V', 48: 'B', 49: 'N', 50: 'M'
        }
    },
    'AZERTY': {
        'key_mapping': {
            16: 'A', 17: 'Z', 18: 'E', 19: 'R', 20: 'T', 21: 'Y', 22: 'U', 23: 'I', 24: 'O', 25: 'P',
            30: 'Q', 31: 'S', 32: 'D', 33: 'F', 34: 'G', 35: 'H', 36: 'J', 37: 'K', 38: 'L',
            44: 'W', 45: 'X', 46: 'C', 47: 'V', 48: 'B', 49: 'N', 50: 'M'
        }
    },
    'QWERTZ': {
        'key_mapping': {
            16: 'Q', 17: 'W', 18: 'E', 19: 'R', 20: 'T', 21: 'Z', 22: 'U', 23: 'I', 24: 'O', 25: 'P',
            30: 'A', 31: 'S', 32: 'D', 33: 'F', 34: 'G', 35: 'H', 36: 'J', 37: 'K', 38: 'L',
            44: 'Y', 45: 'X', 46: 'C', 47: 'V', 48: 'B', 49: 'N', 50: 'M'
        }
    }
}

# Define row groupings for KCM structure
ROW_GROUPINGS = {
    'ROW1': [16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
    'ROW2': [30, 31, 32, 33, 34, 35, 36, 37, 38],
    'ROW3': [44, 45, 46, 47, 48, 49, 50]
}

# Language names for header
LANGUAGE_NAMES = {
    'zz': 'Alphabet', 'en_US': 'English (US)', 'en_GB': 'English (UK)', 'en_AU': 'English (Australia)',
    'en_CA': 'English (Canada)', 'en_IE': 'English (Ireland)', 'en_IN': 'English (India)',
    'en_NZ': 'English (New Zealand)', 'en_SG': 'English (Singapore)', 'en_ZA': 'English (South Africa)',
    'af': 'Afrikaans', 'az_AZ': 'Azerbaijani', 'bs': 'Bosnian', 'ca': 'Catalan',
    'cy': 'Welsh', 'da': 'Danish', 'es': 'Spanish', 'es_US': 'Spanish (US)', 'es_MX': 'Spanish (MX)',
    'es_419': 'Spanish (Latin America)', 'et_EE': 'Estonian', 'eu_ES': 'Basque', 'fi': 'Finnish',
    'fil': 'Filipino', 'ga': 'Irish', 'gl_ES': 'Galician', 'in': 'Indonesian', 'is': 'Icelandic',
    'it': 'Italian', 'nb': 'Norwegian Bokmål', 'nl': 'Dutch', 'pl': 'Polish', 'pt_BR': 'Portuguese (Brazil)',
    'pt_PT': 'Portuguese (Portugal)', 'ro': 'Romanian', 'sq': 'Albanian', 'su': 'Sundanese', 'sv': 'Swedish',
    'tr': 'Turkish', 'de': 'German', 'at': 'German (Austria)', 'ch-de': 'German (Switzerland)',
    'cs': 'Czech', 'sk': 'Slovak', 'hu': 'Hungarian', 'hr': 'Croatian', 'sl': 'Slovenian',
    'sr': 'Serbian', 'fr': 'French', 'fr_CA': 'French (Canada)', 'ja': 'Japanese',
    'zh_CN_stroke': 'Chinese (Simplified, Stroke)', 'zh_TW_zhuyin': 'Chinese (Traditional, Zhuyin)',
    'ar': 'Arabic', 'be': 'Belarusian', 'bg': 'Bulgarian', 'ru': 'Russian', 'ru_translit': 'Russian Translit',
    'uk': 'Ukrainian', 'el': 'Greek', 'iw': 'Hebrew', 'hy_AM': 'Armenian', 'bn_IN': 'Bengali (India)',
    'hi': 'Hindi', 'kn_IN': 'Kannada', 'ml_IN': 'Malayalam', 'mr_IN': 'Marathi', 'ta_IN': 'Tamil',
    'te_IN': 'Telugu', 'km_KH': 'Khmer', 'lo_LA': 'Lao', 'th': 'Thai', 'mn_MN': 'Mongolian',
    'ms_MY': 'Malay', 'ro_translit': 'Romanian Translit', 'vi': 'Vietnamese'
}

# Character mappings for non-Latin languages
CHARACTER_MAPPINGS = {
    'alt-sym': {
        'Q': ('0', '~'), 'W': ('1', '`'), 'E': ('2', '['), 'R': ('3', ']'), 'T': ('(', '{'),
        'Y': (')', '}'), 'U': ('_', '<'), 'I': ('1', '>'), 'O': ('"', '^'), 'P': ('&', '%'),
        'A': ('#', '_'), 'S': ('4', '+'), 'D': ('5', '-'), 'F': ('6', '='), 'G': ('/', '\\'),
        'H': (':', '|'), 'J': (';', '&'), 'K': ('@', '«'), 'L': (',', '»'),
        'Z': ('*', '¥'), 'X': ('7', '€'), 'C': ('8', '£'), 'V': ('9', '$'), 'B': ('!', '!'),
        'N': ('?', '?'), 'M': ('.', '.')
    },
    'ru': {  # Russian
        'Q': ('й', 'Й'), 'W': ('у', 'У'), 'E': ('к', 'К'), 'R': ('е', 'Е'), 'T': ('н', 'Н'),
        'Y': ('г', 'Г'), 'U': ('ш', 'Ш'), 'I': ('з', 'З'), 'O': ('х', 'Х'), 'P': ('ю', 'Ю'),
        'A': ('ф', 'Ф'), 'S': ('в', 'В'), 'D': ('а', 'А'), 'F': ('п', 'П'), 'G': ('р', 'Р'),
        'H': ('о', 'О'), 'J': ('л', 'Л'), 'K': ('д', 'Д'), 'L': ('ж', 'Ж'),
        'Z': ('я', 'Я'), 'X': ('с', 'С'), 'C': ('м', 'М'), 'V': ('и', 'И'), 'B': ('т', 'Т'),
        'N': ('ь', 'Ь'), 'M': ('б', 'Б')
    },
    'ru_translit': {  # Russian Translit
        'Q': ('я', 'Я'), 'W': ('ш', 'Ш'), 'E': ('е', 'Е'), 'R': ('р', 'Р'), 'T': ('т', 'Т'),
        'Y': ('ы', 'Ы'), 'U': ('у', 'У'), 'I': ('и', 'И'), 'O': ('о', 'О'), 'P': ('п', 'П'),
        'A': ('а', 'А'), 'S': ('с', 'С'), 'D': ('д', 'Д'), 'F': ('ф', 'Ф'), 'G': ('г', 'Г'),
        'H': ('х', 'Х'), 'J': ('й', 'Й'), 'K': ('к', 'К'), 'L': ('л', 'Л'),
        'Z': ('з', 'З'), 'X': ('ж', 'Ж'), 'C': ('ц', 'Ц'), 'V': ('в', 'В'), 'B': ('б', 'Б'),
        'N': ('н', 'Н'), 'M': ("м", "М")
    },
    'ar': {  # Arabic
        'Q': ('ض', 'ض'), 'W': ('ص', 'ص'), 'E': ('ث', 'ث'), 'R': ('ق', 'ق'), 'T': ('ف', 'ف'),
        'Y': ('غ', 'غ'), 'U': ('ع', 'ع'), 'I': ('ه', 'ه'), 'O': ('خ', 'خ'), 'P': ('ح', 'ح'),
        'A': ('ش', 'ش'), 'S': ('س', 'س'), 'D': ('ي', 'ي'), 'F': ('ب', 'ب'), 'G': ('ل', 'ل'),
        'H': ('ا', 'ا'), 'J': ('ت', 'ت'), 'K': ('ن', 'ن'), 'L': ('م', 'م'),
        'Z': ('ئ', 'ئ'), 'X': ('ء', 'ء'), 'C': ('ؤ', 'ؤ'), 'V': ('ر', 'ر'), 'B': ('لا', 'لا'),
        'N': ('ى', 'ى'), 'M': ('ة', 'ة')
    },
    'ja': {  # Japanese
        'Q': ('た', 'た'), 'W': ('て', 'て'), 'E': ('い', 'い'), 'R': ('す', 'す'), 'T': ('か', 'か'),
        'Y': ('ん', 'ん'), 'U': ('な', 'な'), 'I': ('に', 'に'), 'O': ('ら', 'ら'), 'P': ('せ', 'せ'),
        'A': ('ち', 'ち'), 'S': ('と', 'と'), 'D': ('し', 'し'), 'F': ('は', 'は'), 'G': ('き', 'き'),
        'H': ('く', 'く'), 'J': ('ま', 'ま'), 'K': ('の', 'の'), 'L': ('り', 'り'),
        'Z': ('つ', 'つ'), 'X': ('さ', 'さ'), 'C': ('そ', 'そ'), 'V': ('ひ', 'ひ'), 'B': ('こ', 'こ'),
        'N': ('み', 'み'), 'M': ('も', 'も')
    },
    'zh_CN_stroke': {  # Chinese STROKE
        'Q': ('一', '一'), 'W': ('丨', '丨'), 'E': ('丿', '丿'), 'R': ('丶', '丶'), 'T': ('乙', '乙'),
        'Y': ('亅', '亅'), 'U': ('二', '二'), 'I': ('八', '八'), 'O': ('冂', '冂'), 'P': ('亠', '亠'),
        'A': ('人', '人'), 'S': ('儿', '儿'), 'D': ('入', '入'), 'F': ('刀', '刀'), 'G': ('力', '力'),
        'H': ('勹', '勹'), 'J': ('匕', '匕'), 'K': ('匚', '匚'), 'L': ('十', '十'),
        'Z': ('口', '口'), 'X': ('囗', '囗'), 'C': ('土', '土'), 'V': ('士', '士'), 'B': ('夂', '夂'),
        'N': ('夊', '夊'), 'M': ('夕', '夕')
    },
    'zh_TW_zhuyin': {  # Zhuyin
        'Q': ('ㄅ', 'ㄅ'), 'W': ('ㄉ', 'ㄉ'), 'E': ('ˇ', 'ˇ'), 'R': ('ˋ', 'ˋ'), 'T': ('ㄓ', 'ㄓ'),
        'Y': ('ˊ', 'ˊ'), 'U': ('ㄕ', 'ㄕ'), 'I': ('ㄘ', 'ㄘ'), 'O': ('ㄟ', 'ㄟ'), 'P': ('ㄣ', 'ㄣ'),
        'A': ('ㄇ', 'ㄇ'), 'S': ('ㄊ', 'ㄊ'), 'D': ('ㄍ', 'ㄍ'), 'F': ('ㄐ', 'ㄐ'), 'G': ('ㄔ', 'ㄔ'),
        'H': ('ㄗ', 'ㄗ'), 'J': ('ㄧ', 'ㄧ'), 'K': ('ㄛ', 'ㄛ'), 'L': ('ㄨ', 'ㄨ'),
        'Z': ('ㄈ', 'ㄈ'), 'X': ('ㄌ', 'ㄌ'), 'C': ('ㄎ', 'ㄎ'), 'V': ('ㄑ', 'ㄑ'), 'B': ('ㄒ', 'ㄒ'),
        'N': ('ㄖ', 'ㄖ'), 'M': ('ㄙ', 'ㄙ')
    },
    'be': {  # Belarusian
        'Q': ('й', 'Й'), 'W': ('ц', 'Ц'), 'E': ('у', 'У'), 'R': ('к', 'К'), 'T': ('е', 'Е'),
        'Y': ('н', 'Н'), 'U': ('г', 'Г'), 'I': ('ш', 'Ш'), 'O': ('ў', 'Ў'), 'P': ('з', 'З'),
        'A': ('ф', 'Ф'), 'S': ('ы', 'Ы'), 'D': ('в', 'В'), 'F': ('а', 'А'), 'G': ('п', 'П'),
        'H': ('р', 'Р'), 'J': ('о', 'О'), 'K': ('л', 'Л'), 'L': ('д', 'Д'),
        'Z': ('я', 'Я'), 'X': ('ч', 'Ч'), 'C': ('с', 'С'), 'V': ('м', 'М'), 'B': ('і', 'І'),
        'N': ('т', 'Т'), 'M': ('ь', 'Ь')
    },
    'bg': {  # Bulgarian
        'Q': ('я', 'Я'), 'W': ('в', 'В'), 'E': ('е', 'Е'), 'R': ('р', 'Р'), 'T': ('т', 'Т'),
        'Y': ('ъ', 'Ъ'), 'U': ('у', 'У'), 'I': ('и', 'И'), 'O': ('о', 'О'), 'P': ('п', 'П'),
        'A': ('а', 'А'), 'S': ('с', 'С'), 'D': ('д', 'Д'), 'F': ('ф', 'Ф'), 'G': ('г', 'Г'),
        'H': ('х', 'Х'), 'J': ('й', 'Й'), 'K': ('к', 'К'), 'L': ('л', 'Л'),
        'Z': ('з', 'З'), 'X': ('ь', 'Ь'), 'C': ('ц', 'Ц'), 'V': ('ж', 'Ж'), 'B': ('б', 'Б'),
        'N': ('н', 'Н'), 'M': ('м', 'М')
    },
    'uk': {  # Ukrainian
        'Q': ('й', 'Й'), 'W': ('ц', 'Ц'), 'E': ('у', 'У'), 'R': ('к', 'К'), 'T': ('е', 'Е'),
        'Y': ('н', 'Н'), 'U': ('г', 'Г'), 'I': ('ш', 'Ш'), 'O': ('щ', 'Щ'), 'P': ('з', 'З'),
        'A': ('ф', 'Ф'), 'S': ('і', 'І'), 'D': ('в', 'В'), 'F': ('а', 'А'), 'G': ('п', 'П'),
        'H': ('р', 'Р'), 'J': ('о', 'О'), 'K': ('л', 'Л'), 'L': ('д', 'Д'),
        'Z': ('я', 'Я'), 'X': ('ч', 'Ч'), 'C': ('с', 'С'), 'V': ('м', 'М'), 'B': ('и', 'И'),
        'N': ('т', 'Т'), 'M': ('ь', 'Ь')
    },
    'el': {  # Greek
        'Q': (';', ';'), 'W': ('ς', 'ς'), 'E': ('ε', 'Ε'), 'R': ('ρ', 'Ρ'), 'T': ('τ', 'Τ'),
        'Y': ('υ', 'Υ'), 'U': ('θ', 'Θ'), 'I': ('ι', 'Ι'), 'O': ('ο', 'Ο'), 'P': ('π', 'Π'),
        'A': ('α', 'Α'), 'S': ('σ', 'Σ'), 'D': ('δ', 'Δ'), 'F': ('φ', 'Φ'), 'G': ('γ', 'Γ'),
        'H': ('η', 'Η'), 'J': ('ξ', 'Ξ'), 'K': ('κ', 'Κ'), 'L': ('λ', 'Λ'),
        'Z': ('ζ', 'Ζ'), 'X': ('χ', 'Χ'), 'C': ('ψ', 'Ψ'), 'V': ('ω', 'Ω'), 'B': ('β', 'Β'),
        'N': ('ν', 'Ν'), 'M': ('μ', 'Μ')
    },
    'iw': {  # Hebrew
        'Q': ('/', '/'), 'W': ("'", "'"), 'E': ('ק', 'ק'), 'R': ('ר', 'ר'), 'T': ('א', 'א'),
        'Y': ('ט', 'ט'), 'U': ('ו', 'ו'), 'I': ('ן', 'ן'), 'O': ('ם', 'ם'), 'P': ('פ', 'פ'),
        'A': ('ש', 'ש'), 'S': ('ד', 'ד'), 'D': ('ג', 'ג'), 'F': ('כ', 'כ'), 'G': ('ע', 'ע'),
        'H': ('י', 'י'), 'J': ('ח', 'ח'), 'K': ('ל', 'ל'), 'L': ('ך', 'ך'),
        'Z': ('ז', 'ז'), 'X': ('ס', 'ס'), 'C': ('ב', 'ב'), 'V': ('ה', 'ה'), 'B': ('נ', 'נ'),
        'N': ('מ', 'מ'), 'M': ('צ', 'צ')
    },
    'hy': {  # Armenian
        'Q': ('ք', 'Ք'), 'W': ('ո', 'Ո'), 'E': ('ե', 'Ե'), 'R': ('ռ', 'Ռ'), 'T': ('տ', 'Տ'),
        'Y': ('ը', 'Ը'), 'U': ('ւ', 'Ւ'), 'I': ('ի', 'Ի'), 'O': ('օ', 'Օ'), 'P': ('պ', 'Պ'),
        'A': ('ա', 'Ա'), 'S': ('ս', 'Ս'), 'D': ('դ', 'Դ'), 'F': ('ֆ', 'Ֆ'), 'G': ('գ', 'Գ'),
        'H': ('հ', 'Հ'), 'J': ('յ', 'Յ'), 'K': ('կ', 'Կ'), 'L': ('լ', 'Լ'),
        'Z': ('զ', 'Զ'), 'X': ('ղ', 'Ղ'), 'C': ('ց', 'Ց'), 'V': ('վ', 'Վ'), 'B': ('բ', 'Բ'),
        'N': ('ն', 'Ն'), 'M': ('մ', 'Մ')
    },
    'bn': {  # Bengali
        'Q': ('ৌ', 'ৌ'), 'W': ('ৈ', 'ৈ'), 'E': ('া', 'া'), 'R': ('ী', 'ী'), 'T': ('ূ', 'ূ'),
        'Y': ('ব', 'ব'), 'U': ('হ', 'হ'), 'I': ('গ', 'গ'), 'O': ('দ', 'দ'), 'P': ('জ', 'জ'),
        'A': ('ো', 'ো'), 'S': ('ে', 'ে'), 'D': ('ি', 'ি'), 'F': ('ু', 'ু'), 'G': ('প', 'প'),
        'H': ('র', 'র'), 'J': ('ক', 'ক'), 'K': ('ত', 'ত'), 'L': ('চ', 'চ'),
        'Z': ('ং', 'ং'), 'X': ('ম', 'ম'), 'C': ('ন', 'ন'), 'V': ('ল', 'ল'), 'B': ('স', 'স'),
        'N': ('ট', 'ট'), 'M': ('থ', 'থ')
    },
    'hi': {  # Hindi (Devanagari)
        'Q': ('ौ', 'ौ'), 'W': ('ै', 'ै'), 'E': ('ा', 'ा'), 'R': ('ी', 'ी'), 'T': ('ू', 'ू'),
        'Y': ('ब', 'ब'), 'U': ('ह', 'ह'), 'I': ('ग', 'ग'), 'O': ('द', 'द'), 'P': ('ज', 'ज'),
        'A': ('ो', 'ो'), 'S': ('े', 'े'), 'D': ('ि', 'ि'), 'F': ('ु', 'ु'), 'G': ('प', 'प'),
        'H': ('र', 'र'), 'J': ('क', 'क'), 'K': ('त', 'त'), 'L': ('च', 'च'),
        'Z': ('़', '़'), 'X': ('म', 'म'), 'C': ('न', 'न'), 'V': ('ल', 'ल'), 'B': ('स', 'स'),
        'N': ('ट', 'ट'), 'M': ('थ', 'थ')
    },
    'kn': {  # Kannada
        'Q': ('ೌ', 'ೌ'), 'W': ('ೆ', 'ೆ'), 'E': ('ಾ', 'ಾ'), 'R': ('ೀ', 'ೀ'), 'T': ('ೂ', 'ೂ'),
        'Y': ('ಬ', 'ಬ'), 'U': ('ಹ', 'ಹ'), 'I': ('ಗ', 'ಗ'), 'O': ('ದ', 'ದ'), 'P': ('ಜ', 'ಜ'),
        'A': ('ೊ', 'ೊ'), 'S': ('ೇ', 'ೇ'), 'D': ('ಿ', 'ಿ'), 'F': ('ು', 'ು'), 'G': ('ಪ', 'ಪ'),
        'H': ('ರ', 'ರ'), 'J': ('ಕ', 'ಕ'), 'K': ('ತ', 'ತ'), 'L': ('ಚ', 'ಚ'),
        'Z': ('ಃ', 'ಃ'), 'X': ('ಮ', 'ಮ'), 'C': ('ನ', 'ನ'), 'V': ('ಲ', 'ಲ'), 'B': ('ಸ', 'ಸ'),
        'N': ('ಟ', 'ಟ'), 'M': ('ಥ', 'ಥ')
    },
    'ml': {  # Malayalam
        'Q': ('ൌ', 'ൌ'), 'W': ('ൈ', 'ൈ'), 'E': ('ാ', 'ാ'), 'R': ('ീ', 'ീ'), 'T': ('ൂ', 'ൂ'),
        'Y': ('ബ', 'ബ'), 'U': ('ഹ', 'ഹ'), 'I': ('ഗ', 'ഗ'), 'O': ('ദ', 'ദ'), 'P': ('ജ', 'ജ'),
        'A': ('ോ', 'ോ'), 'S': ('േ', 'േ'), 'D': ('ി', 'ി'), 'F': ('ു', 'ു'), 'G': ('പ', 'പ'),
        'H': ('ര', 'ര'), 'J': ('ക', 'ക'), 'K': ('ത', 'ത'), 'L': ('ച', 'ച'),
        'Z': ('ഃ', 'ഃ'), 'X': ('മ', 'മ'), 'C': ('ന', 'ന'), 'V': ('ല', 'ല'), 'B': ('സ', 'സ'),
        'N': ('ട', 'ട'), 'M': ('ഥ', 'ഥ')
    },
    'mr': {  # Marathi
        'Q': ('ौ', 'ौ'), 'W': ('ै', 'ै'), 'E': ('ा', 'ा'), 'R': ('ी', 'ी'), 'T': ('ू', 'ू'),
        'Y': ('ब', 'ब'), 'U': ('ह', 'ह'), 'I': ('ग', 'ग'), 'O': ('द', 'द'), 'P': ('ज', 'ज'),
        'A': ('ो', 'ो'), 'S': ('े', 'े'), 'D': ('ि', 'ि'), 'F': ('ु', 'ु'), 'G': ('प', 'प'),
        'H': ('र', 'र'), 'J': ('क', 'क'), 'K': ('त', 'त'), 'L': ('च', 'च'),
        'Z': ('़', '़'), 'X': ('म', 'म'), 'C': ('न', 'न'), 'V': ('ल', 'ल'), 'B': ('स', 'स'),
        'N': ('ट', 'ट'), 'M': ('थ', 'थ')
    },
    'ta': {  # Tamil
        'Q': ('ஔ', 'ஔ'), 'W': ('ஐ', 'ஐ'), 'E': ('ஆ', 'ஆ'), 'R': ('ஈ', 'ஈ'), 'T': ('ஊ', 'ஊ'),
        'Y': ('ப', 'ப'), 'U': ('ஹ', 'ஹ'), 'I': ('க', 'க'), 'O': ('த', 'த'), 'P': ('ஜ', 'ஜ'),
        'A': ('ஓ', 'ஓ'), 'S': ('ஏ', 'ஏ'), 'D': ('இ', 'இ'), 'F': ('உ', 'உ'), 'G': ('ஞ', 'ஞ'),
        'H': ('ர', 'ர'), 'J': ('ா', 'ா'), 'K': ('ட', 'ட'), 'L': ('ச', 'ச'),
        'Z': ('ஃ', 'ஃ'), 'X': ('ம', 'ம'), 'C': ('ன', 'ன'), 'V': ('ல', 'ல'), 'B': ('ஸ', 'ஸ'),
        'N': ('ண', 'ண'), 'M': ('ந', 'ந')
    },
    'te': {  # Telugu
        'Q': ('ౌ', 'ౌ'), 'W': ('ై', 'ై'), 'E': ('ా', 'ా'), 'R': ('ీ', 'ీ'), 'T': ('ూ', 'ూ'),
        'Y': ('బ', 'బ'), 'U': ('హ', 'హ'), 'I': ('గ', 'గ'), 'O': ('ద', 'ద'), 'P': ('జ', 'జ'),
        'A': ('ో', 'ో'), 'S': ('ే', 'ే'), 'D': ('ి', 'ి'), 'F': ('ు', 'ు'), 'G': ('ప', 'ప'),
        'H': ('ర', 'ర'), 'J': ('క', 'క'), 'K': ('త', 'త'), 'L': ('చ', 'చ'),
        'Z': ('ః', 'ః'), 'X': ('మ', 'మ'), 'C': ('న', 'న'), 'V': ('ల', 'ల'), 'B': ('స', 'స'),
        'N': ('ట', 'ట'), 'M': ('థ', 'థ')
    },
    'km': {  # Khmer
        'Q': ('ឝ', 'ឝ'), 'W': ('ឞ', 'ឞ'), 'E': ('េ', 'េ'), 'R': ('ៀ', 'ៀ'), 'T': ('ំ', 'ំ'),
        'Y': ('ប', 'ប'), 'U': ('ហ', 'ហ'), 'I': ('ក', 'ក'), 'O': ('ដ', 'ដ'), 'P': ('ព', 'ព'),
        'A': ('ា', 'ា'), 'S': ('ស', 'ស'), 'D': ('ឌ', 'ឌ'), 'F': ('ថ', 'ថ'), 'G': ('ភ', 'ភ'),
        'H': ('រ', 'រ'), 'J': ('យ', 'យ'), 'K': ('ឡ', 'ឡ'), 'L': ('ល', 'ល'),
        'Z': ('ឆ', 'ឆ'), 'X': ('ខ', 'ខ'), 'C': ('ឈ', 'ឈ'), 'V': ('វ', 'វ'), 'B': ('អ', 'អ'),
        'N': ('ន', 'ន'), 'M': ('ម', 'ម')
    },
    'lo': {  # Lao
        'Q': ('ເ', 'ເ'), 'W': ('ແ', 'ແ'), 'E': ('ໍ', 'ໍ'), 'R': ('ຽ', 'ຽ'), 'T': ('໌', '໌'),
        'Y': ('ບ', 'ບ'), 'U': ('ຮ', 'ຮ'), 'I': ('ງ', 'ງ'), 'O': ('ດ', 'ດ'), 'P': ('ຈ', 'ຈ'),
        'A': ('າ', 'າ'), 'S': ('ສ', 'ສ'), 'D': ('ຄ', 'ຄ'), 'F': ('ຕ', 'ຕ'), 'G': ('ຜ', 'ຜ'),
        'H': ('ຣ', 'ຣ'), 'J': ('ຢ', 'ຢ'), 'K': ('ລ', 'ລ'), 'L': ('ວ', 'ວ'),
        'Z': ('ຊ', 'ຊ'), 'X': ('ຂ', 'ຂ'), 'C': ('ໜ', 'ໜ'), 'V': ('ໝ', 'ໝ'), 'B': ('ຫ', 'ຫ'),
        'N': ('ນ', 'ນ'), 'M': ('ມ', 'ມ')
    },
    'th': {  # Thai
        'Q': ('ๆ', 'ๆ'), 'W': ('ไ', 'ไ'), 'E': ('ำ', 'ำ'), 'R': ('พ', 'พ'), 'T': ('ะ', 'ะ'),
        'Y': ('ั', 'ั'), 'U': ('ี', 'ี'), 'I': ('ร', 'ร'), 'O': ('น', 'น'), 'P': ('ย', 'ย'),
        'A': ('ฟ', 'ฟ'), 'S': ('ห', 'ห'), 'D': ('ก', 'ก'), 'F': ('ด', 'ด'), 'G': ('เ', 'เ'),
        'H': ('้', '้'), 'J': ('่', '่'), 'K': ('า', 'า'), 'L': ('ส', 'ส'),
        'Z': ('ผ', 'ผ'), 'X': ('ป', 'ป'), 'C': ('แ', 'แ'), 'V': ('อ', 'อ'), 'B': ('ิ', 'ิ'),
        'N': ('ื', 'ื'), 'M': ('ท', 'ท')
    },
    'mn': {  # Mongolian (Cyrillic)
        'Q': ('й', 'Й'), 'W': ('ц', 'Ц'), 'E': ('у', 'У'), 'R': ('к', 'К'), 'T': ('е', 'Е'),
        'Y': ('н', 'Н'), 'U': ('г', 'Г'), 'I': ('ш', 'Ш'), 'O': ('ө', 'Ө'), 'P': ('з', 'З'),
        'A': ('ф', 'Ф'), 'S': ('ы', 'Ы'), 'D': ('в', 'В'), 'F': ('а', 'А'), 'G': ('п', 'П'),
        'H': ('р', 'Р'), 'J': ('о', 'О'), 'K': ('л', 'Л'), 'L': ('д', 'Д'),
        'Z': ('я', 'Я'), 'X': ('ч', 'Ч'), 'C': ('с', 'С'), 'V': ('м', 'М'), 'B': ('и', 'И'),
        'N': ('т', 'Т'), 'M': ('ь', 'Ь')
    },
    'ro_translit': {  # Romanian Translit
        'Q': ('â', 'Â'), 'W': ('w', 'W'), 'E': ('e', 'E'), 'R': ('r', 'R'), 'T': ('t', 'T'),
        'Y': ('y', 'Y'), 'U': ('u', 'U'), 'I': ('i', 'I'), 'O': ('o', 'O'), 'P': ('p', 'P'),
        'A': ('a', 'A'), 'S': ('s', 'S'), 'D': ('d', 'D'), 'F': ('f', 'F'), 'G': ('g', 'G'),
        'H': ('h', 'H'), 'J': ('j', 'J'), 'K': ('k', 'K'), 'L': ('l', 'L'),
        'Z': ('z', 'Z'), 'X': ('x', 'X'), 'C': ('c', 'C'), 'V': ('v', 'V'), 'B': ('b', 'B'),
        'N': ('n', 'N'), 'M': ('m', 'M')
    }
}

def unicode_escape(s):
    return ''.join(
        c if ord(c) < 128 else f'\\u{ord(c):04x}'
        for c in s
    )

def generate_kcm_file(locale, layout_type, kcm_filename, output_dir):
    # Get physical layout mapping, we assume base hardware layout is set to QWERTY in the system by QPNP keypad
    base_layout = PHYSICAL_LAYOUTS["QWERTY"]
    physical_layout = PHYSICAL_LAYOUTS[layout_type]
    
    # Get language name for header
    language_name = LANGUAGE_NAMES.get(locale, locale)
    
    # Create KCM content with proper header
    content = "#\n"
    content += "# {} for reduced physical keyboard\n".format(language_name)
    content += "# Gor Mirzoyan (xwtk.cloud).\n"
    content += "#\n\n"
    content += "type OVERLAY\n\n"
    
    # Process each row group
    for row_name, key_codes in ROW_GROUPINGS.items():
        content += "### {}\n".format(row_name)
        
        for key_code in key_codes:
            if key_code not in physical_layout['key_mapping']:
                continue
                
            base_key_label = base_layout['key_mapping'][key_code]
            key_label = physical_layout['key_mapping'][key_code]
            
            # Get character mapping, prioritize full locale
            if locale in CHARACTER_MAPPINGS and key_label in CHARACTER_MAPPINGS[locale]:
                base_char, shift_char = CHARACTER_MAPPINGS[locale][key_label]
                alt, sym = CHARACTER_MAPPINGS["alt-sym"][key_label]
            elif locale.split('_')[0] in CHARACTER_MAPPINGS and key_label in CHARACTER_MAPPINGS[locale.split('_')[0]]:
                base_char, shift_char = CHARACTER_MAPPINGS[locale.split('_')[0]][key_label]
                alt, sym = CHARACTER_MAPPINGS["alt-sym"][key_label]
            else:
                # Default to Latin mapping
                base_char = key_label.lower()
                shift_char = key_label.upper()
                alt, sym = CHARACTER_MAPPINGS["alt-sym"][key_label]
            
            # Apply Unicode escaping to non-ASCII characters
            escaped_base = unicode_escape(base_char)
            escaped_shift = unicode_escape(shift_char)
            
            escaped_alt = unicode_escape(alt)
            escaped_sym = unicode_escape(sym)
            
            # Create key entry
            content += "key {} {{\n".format(base_key_label)
            content += "    label: '{}'\n".format(base_key_label)
            content += "    base: '{}'\n".format(escaped_base)
            content += "    shift, capslock: '{}'\n".format(escaped_shift)
            content += "    lalt, alt: '{}'\n".format(alt)
            content += "    sym: '{}'\n".format(sym)
            content += "}\n\n"
    
    # Write to file
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, kcm_filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return output_path

def main(language_list_file, output_dir):
    # Read language list CSV
    with open(language_list_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        languages = list(reader)
    
    # Process each language entry
    for lang in languages:
        locale = lang['Locale']
        
        # Process QWERTY layout if specified
        if lang['QWERTY_KCM']:
            print("Generating QWERTY for {}: {}".format(locale, lang['QWERTY_KCM']))
            generate_kcm_file(locale, 'QWERTY', lang['QWERTY_KCM'], output_dir)
        
        # Process AZERTY layout if specified
        if lang['AZERTY_KCM']:
            print("Generating AZERTY for {}: {}".format(locale, lang['AZERTY_KCM']))
            generate_kcm_file(locale, 'AZERTY', lang['AZERTY_KCM'], output_dir)
        
        # Process QWERTZ layout if specified
        if lang['QWERTZ_KCM']:
            print("Generating QWERTZ for {}: {}".format(locale, lang['QWERTZ_KCM']))
            generate_kcm_file(locale, 'QWERTZ', lang['QWERTZ_KCM'], output_dir)
    
    print("\nGenerated {} KCM files in {}".format(
        sum(1 for lang in languages if any([lang['QWERTY_KCM'], lang['AZERTY_KCM'], lang['QWERTZ_KCM']])),
        output_dir
    ))

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate KCM files for keyboard layouts')
    parser.add_argument('language_list', help='CSV file containing language layouts')
    parser.add_argument('output_dir', help='Output directory for KCM files')
    
    args = parser.parse_args()
    
    main(args.language_list, args.output_dir)
