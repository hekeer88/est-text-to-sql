class REPR_TYPE:
    CODE_REPRESENTATION = "SQL"
    TEXT_REPRESENTATION = "TEXT"
    OPENAI_DEMOSTRATION = "NUMBERSIGN"
    BASIC = "BASELINE"
    ALPACA_SFT = "INSTRUCTION"
    OPENAI_DEMOSTRATION_WFK = "NUMBERSIGNWFK"
    BASIC_WOFK = "BASELINEWOFK"
    TEXT_REPRESENTATION_WFK = "TEXTWFK"
    ALPACA_SFT_WFK = "INSTRUCTIONWFK"
    OPENAI_DEMOSTRATION_WORULE = "NUMBERSIGNWORULE"
    CODE_REPRESENTATION_WRULE = "SQLWRULE"
    ALPACA_SFT_WRULE = "INSTRUCTIONWRULE"
    TEXT_REPRESENTATION_WRULE = "TEXTWRULE"
    CODE_REPRESENTATION_COT = "SQLCOT"
    TEXT_REPRESENTATION_COT = "TEXTCOT"
    OPENAI_DEMOSTRATION_COT = "NUMBERSIGNCOT"
    ALPACA_SFT_COT = "INSTRUCTIONCOT"
    CBR = "CBR"

class EXAMPLE_TYPE:
    ONLY_SQL = "ONLYSQL"
    QA = "QA"
    COMPLETE = "COMPLETE"
    QAWRULE = "QAWRULE"
    OPENAI_DEMOSTRATION_QA = "NUMBERSIGNQA"
    BASIC_QA = "BASELINEQA"

class SELECTOR_TYPE:
    COS_SIMILAR = "COSSIMILAR"
    RANDOM = "RANDOM"
    EUC_DISTANCE = "EUCDISTANCE"
    EUC_DISTANCE_THRESHOLD = "EUCDISTANCETHRESHOLD"
    EUC_DISTANCE_SKELETON_SIMILARITY_THRESHOLD = "EUCDISSKLSIMTHR"
    EUC_DISTANCE_QUESTION_MASK = "EUCDISQUESTIONMASK"
    EUC_DISTANCE_PRE_SKELETON_SIMILARITY_THRESHOLD = "EUCDISPRESKLSIMTHR"
    EUC_DISTANCE_PRE_SKELETON_SIMILARITY_PLUS = "EUCDISPRESKLSIMPLUS"
    EUC_DISTANCE_MASK_PRE_SKELETON_SIMILARITY_THRESHOLD = "EUCDISMASKPRESKLSIMTHR"
    EUC_DISTANCE_MASK_PRE_SKELETON_SIMILARITY_THRESHOLD_SHIFT = "EUCDISMASKPRESKLSIMTHRSHIFT"


class LLM:
    # openai LLMs
    GPT_4 = "gpt-4"
    GPT_4o = "gpt-4o"
    GPT_4o_mini = "gpt-4o-mini"
    GPT_o3_mini = "o3-mini"

    # Gemini LLMs
    Gemini_PRO = "gemini-2.5-pro-preview-03-25"
    Gemini_PRO_exp = "gemini-2.5-pro-exp-03-25"
    Gemini_flash = "gemini-2.0-flash"
    Gemini_flash_light = "gemini-2.0-flash-lite"
    Gemini_PRO_1 = "gemini-1.5-pro"

    # DeepSeek LLMs
    DeepSeek_reasoner = "deepseek-reasoner"
    DeepSeek_chat = "deepseek-chat"

    GEMINI_MODELS = [
        Gemini_PRO,
        Gemini_PRO_1,
        Gemini_PRO_exp,
        Gemini_flash,
        Gemini_flash_light
    ]

    OPENAI_MODELS = [
        GPT_4,
        GPT_4o,
        GPT_4o_mini,
        GPT_o3_mini
    ]

    DEEPSEEK_MODELS = [
        DeepSeek_reasoner,
        DeepSeek_chat
    ]

    # LLMs that use openai chat api
    TASK_CHAT = [
        GPT_4,
        GPT_4o,
        GPT_4o_mini,
        GPT_o3_mini,
        Gemini_PRO,
        Gemini_PRO_1,
        Gemini_PRO_exp,
        Gemini_flash,
        Gemini_flash_light,
        DeepSeek_chat,
        DeepSeek_reasoner
    ]

    costs_per_thousand = {
        GPT_4: 0.03
    }
