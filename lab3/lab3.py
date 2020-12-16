import plot as my_plots
import pandas as pd
from sklearn.linear_model import LinearRegression

areas = ["Івано-Франківська", "Волинська", "Вінницька", "Дніпропетровська",
         "Донецька", "Житомирська", "Закарпатська", "Запорізька", "Київська",
         "Кіровоградська", "Луганська", "Львівська", "Миколаївська", "Одеська",
         "Полтавська", "Рівненська", "Сумська", "Тернопільська", "Харківська",
         "Херсонська", "Хмельницька", "Черкаська", "Чернівецька", "Чернігівська",
         "м. Київ"]
commands = ["show raw correlation", "show lag correlation",
                 "predict cases for area by leader", "predict cases for area by 3 leaders"]


def get_command(text, vals):
    print(text, end='')
    c = int(input())
    while c not in vals:
        print(text, end='')
        c = int(input())
    return c


def show_options(options):
    n = len(options)
    for i in range(n):
        print(i + 1, "-", options[i])


def parse_data(csv):
    data = pd.read_csv(csv)
    data = data[["zvit_date", "registration_area", "active_confirm"]]
    data = data.groupby(["zvit_date", "registration_area"]).sum().reset_index()
    return data


def format_data(data):
    unique_area = data["registration_area"].unique()
    unique_date = data["zvit_date"].unique()
    res = pd.DataFrame({"zvit_date": unique_date})
    for area in unique_area:
        right = data[data["registration_area"] == area]
        right = right.drop(columns=["registration_area"])
        right = right.rename(columns={"active_confirm": area})
        res = res.merge(right, how="left", on="zvit_date")
    return res


def lag_and_corr(area1, area2, T):
    lag_max, corr_max = 0.0, 0.0
    df_shifted = covid[[area1, area2]].copy()
    df_shifted[area2] = df_shifted[area2].shift(-T - 1)
    for lag_curr in range(-T, T + 1):
        df_shifted[area2] = df_shifted[area2].shift(1)
        df_shifted[area2].dropna()
        curr_corr = df_shifted[area1].corr(df_shifted[area2])
        if curr_corr > corr_max:
            lag_max, corr_max = lag_curr, curr_corr
    return lag_max, corr_max


def lag_df(T=50):
    areas = covid.columns[1:]
    df_lag = pd.DataFrame(columns=areas, index=areas, dtype="float64")
    df_corr = pd.DataFrame(columns=areas, index=areas, dtype="float64")
    for i in range(len(areas)):
        a1 = areas[i]
        for j in range(len(areas)):
            a2 = areas[j]
            if i == j:
                df_lag.at[a1, a2] = 0
                df_corr.at[a1, a2] = 1.0
            else:
                lag_a1_a2, corr_a1_a1 = lag_and_corr(a1, a2, T)
                df_lag.at[a1, a2] = lag_a1_a2
                df_corr.at[a1, a2] = corr_a1_a1
    return df_lag, df_corr


def get_leaders(area, number):
    areas = covid.columns[1:]
    corrs = pd.Series(index=areas, dtype="int64")
    for i in areas:
        if i == area:
            corrs.loc[i] = 0
        else:
            lag_curr, corr_curr = lag_and_corr(area, i, 50)
            corrs.loc[i] = corr_curr
    print(corrs)
    res = corrs.nlargest(number).index
    return res


def predict_cases(area_to_predict, leaders):
    # датасет з лідеруючою областю і тією, яку вибрали
    train = pd.DataFrame()
    predict = pd.DataFrame()
    train[area_to_predict] = covid[area_to_predict].copy()
    for leader in leaders:
        lag_for_leader = lag_and_corr(area_to_predict, leader, 50)[0]
        train[leader] = covid[leader].copy()
        train[leader] = train[leader].shift(lag_for_leader)
    # групуємо дані на тестові та навчальні
    train = train.dropna()
    x_test = train[leaders].tail(7)
    y_test = train[area_to_predict].tail(7)
    x_train = train[leaders].head(-7)
    y_train = train[area_to_predict].head(-7)
    # лінійна регесія дя тестових і навчаьних даних (нормалізуємо дані ще)
    reg = LinearRegression(normalize=True).fit(x_train, y_train)
    print("Train score:", reg.score(x_train, y_train))
    print("Test score:", reg.score(x_test, y_test))
    # прогноз для активних хворих по області
    x = x_train.append(x_test).reset_index()[leaders]
    predict["prediction"] = reg.predict(x)
    y = y_train.append(y_test).reset_index()[area_to_predict]
    predict[area_to_predict] = y
    # додаємо дату
    dates = covid[["zvit_date", area_to_predict]].dropna()
    predict = predict.merge(dates, how="left", on=area_to_predict)
    predict = predict.set_index("zvit_date")
    return predict


covid = parse_data('covid19_by_area_type_hosp_dynamics.csv')
covid = format_data(covid)
loop = True
while loop:
    print()
    show_options(commands)
    print("5 - exit")
    com = get_command("Command: ", range(len(commands) + 1))
    if com == 1:
        my_plots.plot_correlation(covid)
    elif com == 2:
        ldf, cdf = lag_df()
        my_plots.plot_lag_correlation(ldf, cdf, 50)
    elif com == 3:
        show_options(areas)
        area = get_command("Area for prediciton: ", range(1, len(areas) + 1))
        leaders = get_leaders(areas[area - 1], 1)
        print("Leader: ", *list(leaders))
        pr = predict_cases(areas[area - 1], leaders)
        my_plots.plot_prediction(pr, areas[area - 1])
    elif com == 4:
        show_options(areas)
        area = get_command("Area for prediciton: ", range(1, len(areas) + 1))
        leaders = get_leaders(areas[area - 1], 3)
        print("Leaders: ", *list(leaders))
        pr = predict_cases(areas[area - 1], leaders)
        my_plots.plot_prediction(pr, areas[area - 1])
    else:
        loop = False
