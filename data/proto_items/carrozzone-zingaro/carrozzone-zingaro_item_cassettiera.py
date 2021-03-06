# -*- coding: utf-8 -*-

"""
E' un sistema che emula, in maniera volutamente confusionaria, l'alternanza di
3 cassetti in una cassettiera.
"""


#= IMPORT ======================================================================

from src.database import database
from src.log    import log


#= FUNZIONI ====================================================================

def after_closed(entity, cassettiera, reverse_target, container_only, behavioured):
    if not entity:
        log.bug("entity non è un parametro valido: %r" % entity)
        return

    if not cassettiera:
        log.bug("cassettiera non è un parametro valido: %r" % cassettiera)
        return

    # -------------------------------------------------------------------------

    # Se non trova lo special apposito allora crea tutte le cassettiere in una
    # volta sola e le lega tra loro come in una catena circolare
    if "next_cassetto" in cassettiera.specials:
        cassettiera2 = cassettiera.specials["next_cassetto"]
    else:
        cassettiera2 = cassettiera.CONSTRUCTOR(cassettiera.prototype.code)
        cassettiera2.area = entity.area

        cassettiera3 = cassettiera.CONSTRUCTOR(cassettiera.prototype.code)
        cassettiera3.area = entity.area

        database[cassettiera2.ACCESS_ATTR][cassettiera2.code] = cassettiera2
        database[cassettiera3.ACCESS_ATTR][cassettiera3.code] = cassettiera3
        cassettiera.specials["next_cassetto"]  = cassettiera2
        cassettiera2.specials["next_cassetto"] = cassettiera3
        cassettiera3.specials["next_cassetto"] = cassettiera

    # Rimuove la cassettiera originale e inserisce quella del cassetto
    # successivo nello stesso posto in cui si trova colui che ha chiuso
    cassettiera = cassettiera.from_location(1)
    cassettiera.area = entity.area
    cassettiera2.to_location(entity.location)
#- Fine Funzione -


def on_booting(cassettiera):
    """
    Poiché lo special next_cassetto al caricamento è una stringa, e nel
    gamescript invece viene utilizzato, per comodità, come riferimento lo
    deve cercare nel database e reinizializzarlo.
    """
    if not cassettiera:
        log.bug("cassettiera non è un parametro valido: %r" % cassettiera)
        return

    if "next_cassetto" in cassettiera.specials and cassettiera.specials["next_cassetto"]:
        code = cassettiera.specials["next_cassetto"]
        if code in database["items"]:
            cassettiera.specials["next_cassetto"] = database["items"][code]
        else:
            log.bug("Impossibile trovare il codice %s tra gli oggetti (la persistenza è stata cancellata?)" % code)
            return
#- Fine Funzione -


def on_shutdown(cassettiera):
    """
    Poiché lo special next_cassetto è un riferimento lo deve convertire in
    stringa prima di poter essere salvato nella persistenza.
    """
    if not cassettiera:
        log.bug("cassettiera non è un parametro valido: %r" % cassettiera)
        return

    if "next_cassetto" in cassettiera.specials:
        cassettiera.specials["next_cassetto"] = cassettiera.specials["next_cassetto"].code
#- Fine Funzione -
