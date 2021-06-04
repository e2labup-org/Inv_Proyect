from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    pass


class Send(Page):
    """This page is only for P1
    P1 sends amount (all, some, or none) to P2
    This amount is tripled by experimenter,
    i.e if sent amount by P1 is 5, amount received by P2 is 15"""

    form_model = 'group'
    form_fields = ['sent_amount' if i==0 else 'sent_amount_'+str(i) for i in range(4)]
    
    def is_displayed(self):
        return self.player.id_in_group == 1
    
    
class SendBackWaitPage(WaitPage):
    pass


class SendBack(Page):
    """This page is only for P2
    P2 sends back some amount (of the tripled amount received) to P1"""

    form_model = 'group'
    form_fields = ['sent_back_amount']
    #form_fields = ['sent_back_amount' if i==0 else 'sent_back_amount_'+str(i) for i in range(4)]

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        tripled_amount = self.group.sent_amount * Constants.multiplier
        tripled_amount_1 = self.group.sent_amount_1 * Constants.multiplier
        tripled_amount_2 = self.group.sent_amount_2 * Constants.multiplier
        tripled_amount_3 = self.group.sent_amount_3 * Constants.multiplier

        return dict(
            tripled_amount=tripled_amount,
            tripled_amount_1=tripled_amount_1,
            tripled_amount_2=tripled_amount_2,
            tripled_amount_3=tripled_amount_3
        )


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    """This page displays the earnings of each player"""

    def vars_for_template(self):
        return dict(tripled_amount=self.group.sent_amount * Constants.multiplier)


page_sequence = [
    Introduction,
    Send,
    SendBackWaitPage,
    SendBack,
    ResultsWaitPage,
    Results,
]
