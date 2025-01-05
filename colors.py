def determine_blanket_color(temperature: float) -> str:
    if temperature <= -10:
        return "Szary kamień 8465 / Morski 9018"
    elif -9 <= temperature <= -5:
        return "Dzins 6235"
    elif -4 <= temperature <= 0:
        return "Błęktiny 9027"
    elif 1 <= temperature <= 5:
        return "Mgła 9032"
    elif 6 <= temperature <= 10:
        return "Zielona szałwia 9029"
    elif 11 <= temperature <= 15:
        return "Oliwka 0705"
    elif 16 <= temperature <= 20:
        return "Ochra 2923"
    elif 21 <= temperature <= 25:
        return "Rdza 0707"
    elif 26 <= temperature <= 30:
        return "Czerowny 3609"
    elif temperature >= 31:
        return "Bordowy 9025"
