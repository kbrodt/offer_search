import itertools
from collections import namedtuple

"""Data sampler for slotfilling as Cartesian product of slots.
"""


__all__ = [
    'PhraseSlot',
    'make_samples'
]


class PhraseSlot(namedtuple('PhraseSlot', ['phrase', 'slot'])):
    """
    This class represents named tuple with two records: phrase and slot.
    This wrapper over namedtuple is needed only for initialization with default values.
    """
    
    __slots__ = ()
    def __new__(self, phrase, slot=None):
        assert type(phrase) is str, f'{phrase} must be of type `str`, got {type(phrase)}'
        phrase = phrase.strip()
        assert '' != phrase, f'phrase must be non empty'
        if slot is not None:
            assert type(slot) is str, f'{slot} must be of type `str`, got {type(slot)}'
            slot = slot.strip()
            assert '' != slot, f'slot must be non empty'
        
        return super(PhraseSlot, self).__new__(self, phrase, slot)


def make_slot(phrase_slots, sep=' '):
    """
    Makes pair of phrase and list of slots, where phrase is string and
    slot is dict with the following structure:
    
        {'start': start position of slot,
         'end': end position of slot,
         'len': length of slot value # actually redundant key
         'title': name of slot,
         'text': slot value}
    
    inputs:
        phrase_slots: list of PhraseSlot
        sep: separator between phrases when concatenating
    outputs: pair of text and slots
    """
    
    current_length = 0
    slots = list()
    for phrase, slot in phrase_slots:
        start_position = current_length
        current_length += len(phrase) + len(sep)
        if slot is not None:
            slot_dict = dict()
            slot_dict['start'] = start_position
            slot_dict['end'] = start_position + len(phrase)
            slot_dict['len'] = slot_dict['end'] - slot_dict['start']
            slot_dict['title'] = slot
            slot_dict['text'] = phrase
            slots.append(slot_dict)
            
    return sep.join([phrase for phrase, _ in phrase_slots]), slots


def make_samples(*phrase_slots):
    """
    Makes list of samples for slotfilling from lists *phrase_slots as descartes product

    Example usage:
        begin_phrases = [PhraseSlot(phrase='я хочу купить'),
                    PhraseSlot(phrase='где купить')]
        slots = [PhraseSlot(phrase='велик', slot='Item'),
                PhraseSlot(phrase='велосипед', slot='Item')]
        prices = [PhraseSlot(phrase='60к', slot='Price')]

        samples = make_samples(begin_phrases, slots, prices)
    """
    
    return [make_slot(phrase_slot) for phrase_slot in itertools.product(*phrase_slots)]