import time
import bluetooth_tech
import uSGP30
import sys
import machine

# Définition du cablage (input SGP30) :

# I2C Data (SDA) = GPIO 18 :
I2C_SCL_GPIO = const(18)

# I2C Clock (SCL) = GPIO 19 :
I2C_SDA_GPIO = const(19)

# Fréquence :
I2C_FREQ = const(400000)


i2c = machine.SoftI2C(
    scl=machine.Pin(I2C_SCL_GPIO, machine.Pin.OUT),
    sda=machine.Pin(I2C_SDA_GPIO, machine.Pin.OUT),
    freq=I2C_FREQ
)


# Définition du raccourci de fonction de capteur :
sgp30 = uSGP30.SGP30(i2c)


# Définition du cablage (input LEDs) :
# Rouge :
I2C_RED_GPIO = const(13)
pRED = machine.Pin(I2C_RED_GPIO, machine.Pin.OUT)
pRED.value(0)

# Jaune :
I2C_YELLOW_GPIO = const(12)
pYELLOW = machine.Pin(I2C_YELLOW_GPIO, machine.Pin.OUT)
pYELLOW.value(0)

# Vert :
I2C_GREEN_GPIO = const(14)
pGREEN = machine.Pin(I2C_GREEN_GPIO, machine.Pin.OUT)
pGREEN.value(0)

# Bleu :
I2C_BLUE_GPIO = const(27)
pBLUE = machine.Pin(I2C_BLUE_GPIO, machine.Pin.OUT)
pBLUE.value(0)

# Définition du port valeur du buzzer :
I2C_BUZZ_GPIO = const(25)
pBUZZ = machine.Pin(I2C_BUZZ_GPIO, machine.Pin.OUT)
pBUZZ.value(0)

# Définition du réseau Bluetooth Low Energy :
#try :
#    ble = bluetooth_tech.ESP32_BLE('TEST BLUETOOTH')
#    time.sleep(60*5)
#except :
#    pass


# Fonction pour envoyer des données :
def envoi(val_tx):
#    ble.send(str(val_tx))  
    print("Donnée mesurée : ", val_tx," ppm.")

print("Le capteur se calibre, patientez s'il vous plaît...\n")
sgp30.set_absolute_humidity(62)
sgp30.measure_iaq()
time.sleep(18)
print("10 % ...\n")
sgp30.measure_iaq()
time.sleep(18)
print("20 % ...\n")
sgp30.measure_iaq()
time.sleep(18)
print("30 % ...\n")
sgp30.measure_iaq()
time.sleep(18)
print("40 % ...\n")
sgp30.measure_iaq()
time.sleep(18)
print("50 % ...\n")
sgp30.measure_iaq()
time.sleep(18)
print("60 % ...\n")
sgp30.measure_iaq()
time.sleep(18)
print("70 % ...\n")
sgp30.measure_iaq()
time.sleep(18)
print("80 % ...\n")
sgp30.measure_iaq()
time.sleep(18)
print("90 % ...\n")
sgp30.measure_iaq()
time.sleep(18)
print("100 % ...\n")
sgp30.measure_iaq()
time.sleep(2)
print("Calibrage complété avec succès !\n\n")

runtime = 120 # Change here the value, to control the runtime of the loop of measurement

timecode = "Temps en secondes;"
val_lst_co2 = "Valeurs mésurées d'équivalent CO₂ (en ppm) :;"
val_lst_tvoc = "Composés organiques volatils totaux (en ppb) :;"
checktime = 0

while checktime < runtime:
    co2eq_ppm, tvoc_ppb = sgp30.measure_iaq()
    envoi(co2eq_ppm)
    val_lst_co2 += str(co2eq_ppm)+";"
    val_lst_tvoc += str(tvoc_ppb)+";"
    timecode += str(checktime)+";"
    if co2eq_ppm >= 1000 :
        pYELLOW.value(0)
        pGREEN.value(0)
        pBLUE.value(0)
        pRED.value(1)
        pBUZZ.value(1)
    if 999 >= co2eq_ppm >= 800 :
        pGREEN.value(0)
        pBLUE.value(0)
        pRED.value(0)
        pBUZZ.value(0)
        pYELLOW.value(1)
    if 799 >= co2eq_ppm >= 600 :
        pBLUE.value(0)
        pRED.value(0)
        pYELLOW.value(0)
        pBUZZ.value(0)
        pGREEN.value(1)
    if 599 >= co2eq_ppm :
        pRED.value(0)
        pYELLOW.value(0)
        pGREEN.value(0)
        pBUZZ.value(0)
        pBLUE.value(1)
    checktime += 2
    time.sleep(2)
    
file = open("rapport.txt", "w")
file.write(timecode+"\n")
file.write(val_lst_co2+"\n")
file.write(val_lst_tvoc+"\n")
file.close() 