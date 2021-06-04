from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


doc = """
This is a standard 2-player trust game where the amount sent by player 1 gets
tripled. The trust game was first proposed by
<a href="http://econweb.ucsd.edu/~jandreon/Econ264/papers/Berg%20et%20al%20GEB%201995.pdf" target="_blank">
    Berg, Dickhaut, and McCabe (1995)
</a>.
"""


class Constants(BaseConstants):
    name_in_url = 'trust'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'trust/instructions.html'

    # Initial amount allocated to each player
    endowment = c(5)
    multiplier = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    sent_amount = models.CurrencyField(
        min=0,
        max=Constants.endowment,
        doc="""Amount sent by P1""",
        label="Si fueras el jugador A, ¿cuánto enviarías al jugador B?"
    )
    sent_amount_1 = models.CurrencyField(
        min=0,
        max=Constants.endowment,
        doc="""Amount sent by P1""",
        label="Si fueras el jugador B y recibieras 3 puntos, ¿cuánto enviarías de vuelta al jugador A?"
    )
    sent_amount_2 = models.CurrencyField(
        min=0,
        max=Constants.endowment,
        doc="""Amount sent by P1""",
        label="Si fueras el jugador B y recibieras 6 puntos, ¿cuánto enviarías de vuelta al jugador A?"
    )
    sent_amount_3 = models.CurrencyField(
        min=0,
        max=Constants.endowment,
        doc="""Amount sent by P1""",
        label="Si fueras el jugador B y recibieras 9 puntos, ¿cuánto enviarías de vuelta al jugador A?"
    )

    sent_back_amount = models.CurrencyField(doc="""Amount sent back by P2""",min=c(0),label="")
    #sent_back_amount_1 = models.CurrencyField(doc="""Amount sent back by P2""",min=c(0),label="hola1")
    ##sent_back_amount_2 = models.CurrencyField(doc="""Amount sent back by P2""",min=c(0),label="hola2")
    #sent_back_amount_3 = models.CurrencyField(doc="""Amount sent back by P2""",min=c(0),label="hola3")

    def sent_back_amount_max(self):
        return self.sent_amount * Constants.multiplier
    
    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.payoff = Constants.endowment - self.sent_amount + self.sent_back_amount
        p2.payoff = self.sent_amount * Constants.multiplier - self.sent_back_amount


class Player(BasePlayer):
    pass