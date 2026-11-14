FROM odoo:18.0
COPY ./ventas_unicah /mnt/extra-addons/ventas_unicah
COPY ./tienda_unicah /mnt/extra-addons/tienda_unicah
COPY ./unicah_prestamo_equipo /mnt/extra-addons/unicah_prestamo_equipo

ENTRYPOINT []
CMD ["sh", "-c", "odoo --http-port=${PORT:-8069} --db_host=$HOST --db_port=5432 --db_user=$USER --db_password=$PASSWORD --db_sslmode=require -d neondb -i base --db-filter=^neondb$ --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons --workers=0 --max-cron-threads=0 --without-demo=all"]
