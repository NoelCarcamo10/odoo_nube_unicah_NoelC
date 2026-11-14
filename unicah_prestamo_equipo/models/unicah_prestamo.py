from odoo import api, fields, models
from odoo.exceptions import ValidationError


class UnicahPrestamo(models.Model):
    _name = "unicah.prestamo"
    _description = "Préstamo de Equipo Universitario"

    name = fields.Char(string="Código / Referencia", required=True, default="PREST-001")
    solicitante_id = fields.Many2one("res.partner", string="Solicitante", required=True)
    tipo_solicitante = fields.Selection(
        related="solicitante_id.tipo_cliente",
        string="Tipo de solicitante",
        readonly=True,
    )
    equipo = fields.Selection(
        [
            ("proyector", "Proyector Multimedia"),
            ("laptop", "Laptop Institucional"),
            ("adaptador", "Adaptador HDMI / VGA"),
            ("parlante", "Sistema de Audio"),
        ],
        string="Equipo",
        required=True,
        default="proyector",
    )
    aula_destino = fields.Char(string="Aula / Laboratorio", required=True)
    fecha_prestamo = fields.Date(
        string="Fecha de préstamo",
        required=True,
        default=fields.Date.context_today,
    )
    fecha_devolucion = fields.Date(string="Fecha de devolución", required=True)
    dias_prestamo = fields.Integer(
        string="Días solicitados",
        compute="_compute_dias_prestamo",
        store=True,
    )
    estado = fields.Selection(
        [
            ("borrador", "Solicitado"),
            ("prestado", "Entregado"),
            ("devuelto", "Devuelto"),
        ],
        string="Estado",
        default="borrador",
        required=True,
    )

    @api.depends("fecha_prestamo", "fecha_devolucion")
    def _compute_dias_prestamo(self):
        for rec in self:
            if rec.fecha_prestamo and rec.fecha_devolucion:
                diferencia = (rec.fecha_devolucion - rec.fecha_prestamo).days
                rec.dias_prestamo = max(diferencia, 0)
            else:
                rec.dias_prestamo = 0

    @api.constrains("fecha_prestamo", "fecha_devolucion", "solicitante_id")
    def _check_reglas_prestamo(self):
        for rec in self:
            if rec.solicitante_id.tipo_cliente == "externo":
                raise ValidationError(
                    "Los usuarios externos no tienen autorizado el préstamo de equipo institucional."
                )
            if (
                rec.fecha_devolucion
                and rec.fecha_prestamo
                and rec.fecha_devolucion < rec.fecha_prestamo
            ):
                raise ValidationError(
                    "La fecha de devolución no puede ser anterior a la fecha de préstamo."
                )

    def action_entregar(self):
        for rec in self:
            rec.estado = "prestado"

    def action_devolver(self):
        for rec in self:
            rec.estado = "devuelto"
