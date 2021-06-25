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
import random

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
    num_rounds = 3

    instructions_template = 'trust/instructions.html'

    # Initial amount allocated to each player
    endowment_vendedor = c(20)
    endowment_comprador = c(20)

class Subsession(BaseSubsession):
    def creating_session(self):

        num = random.random()

        defectuoso = 1 if num >0.5 else 0
        asset = c(5) if random.random() > 0.5 else c(15)

        self.group.asset_value = asset

class Group(BaseGroup):
    monto_enviado = models.CurrencyField(
        min=0,
        max=c(50),
        doc="""Amount sent by P1""",
        label="Monto a VENDER por el activo, sabiendo que el precio de mercado es 10"
    )

    monto_pago = models.CurrencyField(doc="""Amount sent back by P2""",
        min=c(0),
        max=Constants.endowment_comprador,
        label="Monto a PAGAR por el activo (indicar un monto si deseas adquirirlo, 0 de otro modo)"
    )
    
    asset_value = models.CurrencyField()

    def sent_back_amount_max(self):
        return self.sent_amount 
    
    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.payoff = Constants.endowment_vendedor - self.asset_value + self.monto_enviado #Utilidad del Vendedor
        p2.payoff =  Constants.endowment_comprador + self.asset_value - self. monto_pago #Utilidad del comprador


class Player(BasePlayer):
    pass

