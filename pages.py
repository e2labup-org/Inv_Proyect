from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Introduction(Page):
    pass


class Vendedor(Page):
    """This page is only for P1
    P1 sends amount (all, some, or none) to P2
    This amount is tripled by experimenter,
    i.e if sent amount by P1 is 5, amount received by P2 is 15"""

    form_model = 'group'
    form_fields = ['monto_enviado']
    
    def is_displayed(self):
        return self.player.id_in_group == 1

class SendBackWaitPage(WaitPage):
    pass


class Comprador(Page):
    """This page is only for P2
    P2 sends back some amount (of the tripled amount received) to P1"""

    form_model = 'group'
    form_fields = ['monto_pago']
    
    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):

        return dict(
            monto_pago=self.monto_pago,
        )


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    """This page displays the earnings of each player"""


page_sequence = [
    Introduction,
    Vendedor,
    SendBackWaitPage,
    Comprador,
    ResultsWaitPage,
    Results,
]
