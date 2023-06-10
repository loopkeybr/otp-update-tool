from datetime import datetime, timedelta

def time_current():
    curruent_date = datetime.now()

    # Formate a data atual no formato desejado
    format_date = curruent_date.strftime("%Y-%m-%dT%H:00:00")
    return format_date

def time_increment(initial_time, days):
    
    data_datetime = datetime.strptime(initial_time, "%Y-%m-%dT%H:00:00")

    # Some 10 dias à data inicial
    final_date = data_datetime + timedelta(days)

    format_date = final_date.strftime("%Y-%m-%dT%H:%M:%S")
    # Exiba a data final
    return format_date