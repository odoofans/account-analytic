##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import Warning
import logging
_logger = logging.getLogger(__name__)


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    is_distribution = fields.Boolean(
    )
    distribution_line_ids = fields.One2many(
        'account.analytic.account.distribution_line',
        'distribution_analytic_id',
        'Distribution Line',
    )

    @api.one
    @api.constrains('distribution_line_ids', 'is_distribution')
    def check_distribution_lines(self):
        difference = self.company_id.currency_id.round(sum(
            self.distribution_line_ids.mapped('percentage')) - 100.0)
        if self.is_distribution and difference:
            raise Warning(_(
                'Lines of the analytic distribuion account "%s" must '
                'sum 100') % self.name)


class AccountAnalyticAccountDistribution(models.Model):
    _name = "account.analytic.account.distribution_line"

    distribution_analytic_id = fields.Many2one(
        'account.analytic.account',
        'Distribution Account',
        required=True,
        ondelete='cascade',
    )
    account_analytic_id = fields.Many2one(
        'account.analytic.account',
        'Analytic Account',
        required=True,
    )
    percentage = fields.Float(
        'Percentage',
        required=True,
    )
