import yargy
from yargy.tokenizer import MorphTokenizer
from yargy import Parser, rule, and_, or_, not_
from yargy.predicates import gram, dictionary, custom, true
from yargy.pipelines import morph_pipeline

#проверка на то, число ли это
def is_number(string):
    for c in string:
        if((ord(c) < 48 or ord(c) > 57) and not (c == "." or c == ",")):
            return False
    return True
	
is_number_ = custom(is_number)
#правило понимает дроби
NUMBER_RULE = rule(
    or_(
        gram("NUMR"),
        is_number_
    ),
    morph_pipeline([
        ",",
        "."
    ]).optional(),
    or_(
        gram("NUMR"),
        is_number_
    ).optional()
)
#все приставки, означающие денки:
MONEY_PIPE = morph_pipeline([
        "тыс",
        "к",
        "k",
        "м",
        "руб",
        "рублей",
        "тысяч"
])
#поиск токенов, означающих цену
#нижнюю границу
PRICE_FROM = rule(
    morph_pipeline([
        "от"
    ]),
    NUMBER_RULE,
    MONEY_PIPE.optional()
)
#верхнюю границу
PRICE_TO = rule(
    morph_pipeline([
        "до"
    ]),
    NUMBER_RULE,
    MONEY_PIPE.optional()
)
#точное значение
PRICE_VALUE = rule(
    NUMBER_RULE,
    not_(
        dictionary({
            "%",
            "процент",
            "процентов"
        })
    ),
    MONEY_PIPE.optional()
)
#поиск атрибутов.
#Note: в строку атрибутов входит название самого товара
MEANING = rule(
    not_(
        or_(
            or_(
                gram("INFN"),
                gram("VERB")
            ),
            or_(
                or_(
                    gram("PREP"), gram("CONJ")
                ),
                or_(
                    gram("PRCL"), gram("ADVB")
                )
            )
        )
    )
)
ATTRIBUTE = rule(
    MEANING.optional().repeatable(),
    gram("NOUN").repeatable()
)
#поиск упоминаний процентов или денежных обозначений
MONEY_PERCENT = rule(
    or_(
    rule(
        morph_pipeline([
            "процент",
            "%"
        ]).optional(),
        MONEY_PIPE
        ),
    rule(
        morph_pipeline([
            "процент",
            "%"
        ]),
        MONEY_PIPE.optional()
    )
    )
)
#значение кэшбека
CASHBACK_VALUE = rule(
    NUMBER_RULE,
    MONEY_PERCENT.optional()
)
#упоминание о кэшбеке вместе с числовым значением
CASHBACK = rule(
    NUMBER_RULE.optional().repeatable(),
    MONEY_PERCENT.optional(),
    morph_pipeline([
        "кэшбек",
        "кэшбэк",
        "cb",
        "кб",
        "кэш"
    ]),
    dictionary({
        "от"
    }).optional(),
    NUMBER_RULE.optional().repeatable(),
    MONEY_PERCENT.optional()
)
#число + обозначение процентов
PERCENT_RULE = rule(
    NUMBER_RULE,
    morph_pipeline([
        "%",
        "процент"
    ])
)
