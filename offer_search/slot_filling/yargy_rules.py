import yargy
from yargy.tokenizer import MorphTokenizer
from yargy import Parser, rule, and_, or_, not_
from yargy.predicates import gram, dictionary, custom, true
from yargy.pipelines import morph_pipeline

#проверка на то, число ли это
def is_number(string):
    for c in string:
        if((ord(c) < 48 or ord(c) > 57)):
            return False
    return True
	
is_number_ = custom(is_number)
#правило понимает дроби
NUMBER_RULE = rule(
    or_(
        gram("NUMR"),
        is_number_
    )
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
        "от",
        "дороже"
    ]),
    NUMBER_RULE.repeatable(),
    MONEY_PIPE.optional().repeatable()
)
#верхнюю границу
PRICE_TO = rule(
    morph_pipeline([
        "до",
        "дешевле",
        "дешевле чем",
        "дешевле, чем"
    ]),
    NUMBER_RULE.repeatable(),
    MONEY_PIPE.optional().repeatable()
)
#точное значение
PRICE_VALUE = rule(
    NUMBER_RULE.repeatable(),
    not_(
        dictionary({
            "%",
            "процент",
            "процентов"
        })
    ),
    MONEY_PIPE.optional().repeatable()
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
TRUE =rule(
    true
)
ATTRIBUTE = rule(
    #TRUE.optional().repeatable(),
    MEANING.optional().repeatable(),
    #TRUE.repeatable(),
    gram("NOUN").repeatable(),
    #TRUE.optional().repeatable()
)
#поиск упоминаний процентов или денежных обозначений
MONEY_PERCENT = rule(
    or_(
    rule(
        morph_pipeline([
            "процент",
            "%"
        ]).optional(),
        MONEY_PIPE.repeatable()
        ),
    rule(
        morph_pipeline([
            "процент",
            "%"
        ]),
        MONEY_PIPE.optional().repeatable()
    )
    )
)
#значение кэшбека
CASHBACK_VALUE = rule(
    NUMBER_RULE,
    MONEY_PERCENT.optional()
)
#упоминание о кэшбеке вместе с числовым значением
CASHBACK_PIPE = morph_pipeline([
        "кэшбек",
        "кэшбэк",
        "кешбек",
        "кешбэк",
        "кэшбека",
        "кэшбэка",
        "кешбека",
        "кешбэка",
        "cb",
        "кб",
        "кэш",
        "cashback",
        "кэшбеком",
        "кэшбэком",
        "кешбеком",
        "кешбэком"
])
CASHBACK_AFTER = rule(
    CASHBACK_PIPE,
    dictionary({
        "от"
    }).optional(),
    NUMBER_RULE.optional().repeatable(),
    MONEY_PERCENT.optional()
)
CASHBACK_BEFORE = rule(
    dictionary({
        "от"
    }).optional(),
    NUMBER_RULE.optional().repeatable(),
    MONEY_PERCENT.optional(),
    CASHBACK_PIPE
)
#число + обозначение процентов
PERCENT_RULE = rule(
    NUMBER_RULE,
    morph_pipeline([
        "%",
        "процент"
    ])
)
MONEY_RULE = rule(
    NUMBER_RULE.repeatable(),
    MONEY_PIPE.optional()
)