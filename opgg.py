import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')

login = ""
password = ""



def UpdateButton(matches, where_msg, check_who, message_number):
    driver = webdriver.Chrome(options=options)

    # Inicjalizacja przeglądarki
    if check_who == 1:
        driver.get("https://www.op.gg/summoners/eune/Czeba%C4%87%20Jarnuchow")
    elif check_who == 2:
        driver.get("https://www.op.gg/summoners/eune/QBYST")
    elif check_who == 3:
        driver.get("https://www.op.gg/summoners/eune/DeporS")
    elif check_who == 4:
        driver.get("https://www.op.gg/summoners/eune/Wok3k3")
    elif check_who == 11:
        driver.get("https://www.op.gg/summoners/eune/1player%204apes")


    # Poczekaj na załadowanie strony
    time.sleep(5)

    try:
        # Zamknij baner
        close_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]/span')))
        close_button.click()
        time.sleep(1)

        # Czekaj maksymalnie 10 sekund, aż przycisk będzie widoczny na stronie i kliknij go
        button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content-header"]/div[1]/div/div[1]/div[2]/div[5]/button[1]')))
        button.click()
        time.sleep(20)

        # Pobierz zawartość strony po aktualizacji
        html = driver.page_source
        GetStats(html, matches, where_msg, check_who, message_number, driver)

    finally:
        # Zamknij przeglądarkę
        driver.quit()

def GetStats(html, matches_amount, where_msg, check_who, message_number, driver):
    soup = BeautifulSoup(html, 'html.parser')

    # Zebranie info o wszystkich meczach
    matches = soup.find('div', {'class': 'css-164r41r e1r5v5160'})

    # kazdy mecz po kolei
    match = matches.find_all('li', {'class': 'css-1qq23jn e1iiyghw3'})

    counter = 0
    stat_sum = 0
    cs_sum = 0
    ward_sum = 0
    kp_sum = 0
    kills = 0
    deaths = 0
    assists = 0
    won = 0
    lost = 0
    remake = 0
    for game in match:
        result = game.find('div', {'class': 'result'})
        kda = game.find('div', {'class': 'ratio'})
        cs = game.find('div', {'class': 'cs'})
        ward = game.find('div', {'class': 'ward'})
        kill_participation = game.find('div', {'class': 'p-kill'})
        k_d_a = game.find('div', {'class': 'k-d-a'})

        # WYNIK MECZU
        if result.text == "Victory":
            won += 1
        elif result.text == "Defeat":
            lost +=1
        else:
            remake += 1
        

        # CS
        creepy = cs.text
        cs_split = creepy.split(' ')[-1].strip('()')
        cs_sum += float(cs_split)

        # KONTROLKI
        wardy = ward.text
        ward_split = wardy.split()[-1]
        ward_sum += float(ward_split)

        # KILL PARTICIPATION
        kille = kill_participation.text
        kp_split = kille.split()[1][:-1]
        kp_sum += float(kp_split)

        # K D A
        killsy = k_d_a.text
        kills_split = killsy.split("/")
        stat_list = [int(x) for x in kills_split]
        kills += stat_list[0]
        deaths += stat_list[1]
        assists += stat_list[2]

        # KDA
        stat = kda.text
        if stat == "Perfect KDA":
            stat_split = stat_list[0] + stat_list[2]
        else:
            stat_split = stat.split(':')[0]
        stat_sum += float(stat_split)

        # 5 OSTATNICH MECZY
        counter += 1
        if counter == matches_amount:
            break


    stat_avg = round(stat_sum / (matches_amount - remake), 2)
    cs_avg = round(cs_sum / (matches_amount - remake), 1)
    ward_avg = round(ward_sum / (matches_amount - remake), 1)
    kp_avg = round(kp_sum / (matches_amount - remake))

    if deaths == 0:
        deaths = 1

    kda_sum = round((kills + assists) / deaths, 2)

    #print(stat_avg)
    #print(cs_avg)
    #print(ward_avg)
    #print(kp_avg)

    if check_who == 1:
        nick = "Markowar"
    elif check_who == 2:
        nick = "QBYST"
    elif check_who == 3:
        nick = "DeporS"
    elif check_who == 4:
        nick = "Wok3k3"
    elif check_who == 11:
        nick = ""



    if remake == 0:
        if message_number == 1:
            final_message = nick + " w ostatnich " + str(matches_amount) + " meczach: \nWygrał: " + str(won) + "\nPrzegrał: " + str(lost) + "\nŁączne statystyki: " + str(kills) + "/" + str(deaths) + "/" + str(assists) + " (" + str(kda_sum) + ")" + "\nŚrednie kda: " + str(stat_avg) + "\nŚredni cs: " + str(cs_avg) + "/min\nŚrednio control wardów na mecz: " + str(ward_avg) + "\nŚrednie KPA: " + str(kp_avg) + "%\nCzekamy na poprawę!\nWiadomosc wygenerowana automatycznie przez Depor Inc."
        else:
            final_message = nick + " w ostatnich " + str(matches_amount) + " meczach wygrał: " + str(won) + ", przegrał: " + str(lost) + ", łączne statystyki: " + str(kills) + "/" + str(deaths) + "/" + str(assists) + " (" + str(kda_sum) + ")" + ", jego średnie kda wynosiło: " + str(stat_avg) + ", średni cs: " + str(cs_avg) + "/min, control wardów stawiał średnio: " + str(ward_avg) + ", średnie KPA: " + str(kp_avg) + "%. Czekamy na poprawę!\nWiadomosc wygenerowana automatycznie przez Depor Inc."
    else:
        if message_number == 1:
            final_message = nick + " w ostatnich " + str(matches_amount) + " meczach: \nWygrał: " + str(won) + "\nPrzegrał: " + str(lost) + "\nRemake: " + str(remake) + "\nŁączne statystyki: " + str(kills) + "/" + str(deaths) + "/" + str(assists) + " (" + str(kda_sum) + ")" + "\nŚrednie kda: " + str(stat_avg) + "\nŚredni cs: " + str(cs_avg) + "/min\nŚrednio control wardów na mecz: " + str(ward_avg) + "\nŚrednie KPA: " + str(kp_avg) + "%\nCzekamy na poprawę!\nWiadomosc wygenerowana automatycznie przez Depor Inc."
        else:
            final_message = nick + " w ostatnich " + str(matches_amount) + " meczach wygrał: " + str(won) + ", przegrał: " + str(lost) + ", remake: " + str(remake) + ", łączne statystyki: " + str(kills) + "/" + str(deaths) + "/" + str(assists) + " (" + str(kda_sum) + ")" + ", jego średnie kda wynosiło: " + str(stat_avg) + ", średni cs: " + str(cs_avg) + "/min, control wardów stawiał średnio: " + str(ward_avg) + ", średnie KPA: " + str(kp_avg) + "%. Czekamy na poprawę!\nWiadomosc wygenerowana automatycznie przez Depor Inc."

    #print(final_message)10
    SendMessage(final_message, where_msg, driver)

def SendMessage(message, where_msg, driver):
    if where_msg == 1:
        driver.get("https://www.messenger.com/t/100003832263349")
    elif where_msg == 2:
        driver.get("https://www.messenger.com/t/3641227279261053")
    time.sleep(5)
    
    # Zamknij baner
    close_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div/div/div/div[4]/button[2]')))
    close_button.click()
    time.sleep(5)

    # Wpisz Login
    element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div/div[1]/div[1]/div/div[3]/div/div/form/div/input[7]')))
    element.send_keys(login)
    
    # Wpisz Haslo
    element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div/div[1]/div[1]/div/div[3]/div/div/form/div/input[8]')))
    element.send_keys(password)

    # Przycisk logowania
    button = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[1]/div[1]/div/div[3]/div/div/form/div/div[1]/button')))
    button.click()
    time.sleep(5)
    
    # Wpisanie wiadomosci
    element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[4]/div[2]/div/div/div[1]/p')))
    element.send_keys(message)

    # Wyslanie wiadomosci
    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/span[2]/div')))
    button.click()
    time.sleep(3)

    driver.quit()
    






print("Wybierz ilosc meczy (1-20): ")
matches = int(input())
print("Do kogo ma isc wiadomosc?")
print("1. Depor")
print("2. Grupka")
where_msg = int(input())
print("Czyje staty mam sprawdzic?")
print("1. Kupis")
print("2. Alan")
print("3. Depor")
print("4. Wok3k")
print("10. Wszyscy")
check_who = int(input())
print("W jakiej formie?")
print("1. Wiele wiadomosci")
print("2. Jedna wiadomosc")
message_number = int(input())
print("Podaj numer: ")
login = input()
print("Podaj hasło: ")
password = input()
UpdateButton(matches, where_msg, check_who, message_number)
#SendMessage("elo")