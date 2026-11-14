from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    prestamo_ids = fields.One2many(
        "unicah.prestamo", "solicitante_id", string="Préstamos de equipo"
    )
    total_prestamos = fields.Integer(
        string="Total préstamos", compute="_compute_total_prestamos"
    )

    def _compute_total_prestamos(self):
        for partner in self:
            partner.total_prestamos = len(partner.prestamo_ids)
