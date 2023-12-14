import datetime


def get_day_name(date: datetime.datetime):
    day_num = date.weekday()

    if day_num == 0:
        return "Lunes"
    elif day_num == 1:
        return "Martes"
    elif day_num == 2:
        return "Miercoles"
    elif day_num == 3:
        return "Jueves"
    elif day_num == 4:
        return "Viernes"
    elif day_num == 5:
        return "Sabado"
    else:
        return "Domingo"


def get_month_name(date: datetime.datetime):
    month_num = date.month
    if month_num == 1:
        return 'Enero'
    elif month_num == 2:
        return "Febrero"
    elif month_num == 3:
        return "Marzo"
    elif month_num == 4:
        return "Abril"
    elif month_num == 5:
        return "Mayo"
    elif month_num == 6:
        return "Junio"
    elif month_num == 7:
        return "Julio"
    elif month_num == 8:
        return "Agosto"
    elif month_num == 9:
        return "Septiembre"
    elif month_num == 10:
        return "Octubre"
    elif month_num == 11:
        return "Noviembre"
    else:
        return "Diciembre"


def calc_discount(percentage, total):
    return (float(total) / 100) * float(percentage)
