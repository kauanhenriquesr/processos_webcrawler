from datetime import date

str_data = str

def str_to_date(str_data) -> date:
    days = str_data[0:2]
    months = str_data[3:5]
    years = str_data[6:10]
    str_isoformat = years + '-' + months + '-' + days 
    try:
        converted_date = date.fromisoformat(str_isoformat)
        return converted_date
    except ValueError:
        raise ValueError("Invalid date")

def date_to_str(data) -> str:
    return data.strftime("%d/%m/%Y")

def get_today() -> date:
    return date.today()

def get_str_today() -> str:
    hoje = date_to_str(date.today())
    return hoje