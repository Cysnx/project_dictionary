from datetime import datetime
import pandas as pd

def power_law(c_response,w_response,datetime_last_c_response): ## bunu çalışmam gerek
    k = w_response / (1 + c_response)
    today = datetime.now()

    if (
        datetime_last_c_response is None
        or datetime_last_c_response == ""
        or datetime_last_c_response == ''
        or pd.isna(datetime_last_c_response)
        or datetime_last_c_response == 'N/A'
    ):
        return 0.0

    if isinstance(datetime_last_c_response, str):
        last_c = datetime.fromisoformat(datetime_last_c_response)
    else:
        last_c = pd.to_datetime(datetime_last_c_response).to_pydatetime()

    delta = (today - last_c).total_seconds()/86400

    return round((1 + delta) ** (-k),4)