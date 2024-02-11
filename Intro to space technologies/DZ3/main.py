from scipy.stats import norm

# mjerne jedinice su navedene kraj varijabli u komentarima

H = 417 # km
srednja_vrijednost = 400  # km
st_devijacija = 100  # km

TEC_S1 = 33  # TECU
TEC_S2 = 45  # TECU
TEC_S3 = 42  # TECU
TEC_S4 = 39  # TECU38,

Δ_x = 277  # km
Δ_y = 237  # km

x_min = 1185  # km
x_max = 1580  # km
y_min = 4995  # km
y_max = 5550  # km

frekvencija = 1176.45 * 10 ** 6  # Hz

# a)
postotak_sadrzaja_elektrona = 1 - norm(loc=srednja_vrijednost, scale=st_devijacija).cdf(H)
print("Postotak ukupnog sadržaja elektrona u ionosferi koji se nalazi iznad ISS2: {:.4f} %"
      .format(postotak_sadrzaja_elektrona * 100))

# b)
x_p = x_min + Δ_x  # km
y_p = y_min + Δ_y  # km
print("Koordinate točke P: {} km, {} km".format(x_p, y_p))

# c)
x_p_norm = (x_p - x_min) / (x_max - x_min)
y_p_norm = (y_p - y_min) / (y_max - y_min)

TEC = TEC_S1 * x_p_norm * y_p_norm + \
      TEC_S2 * (1 - x_p_norm) * y_p_norm + \
      TEC_S3 * (1 - x_p_norm) * (1-y_p_norm) + \
      TEC_S4 * x_p_norm * (1-y_p_norm)
print("Ukupni sadržaj elektrona u ionosferi izračunat za lokaciju P korištenjem "
      "ionosferskog modela sustava EGNOS: {:.4f} TECU".format(TEC))

# d)
Δ_I_T_P = 40.3 / (frekvencija ** 2 * 3 * 10 ** 8) * 10 ** 16 * TEC * 10 ** 9
print("Ionosfersko kašnjenje na lokaciji P (izračunato EGNOS-om) n"
      "a frekvenciji od f=1176.45 MHz: {:.4f} ns".format(Δ_I_T_P))

# e)
Δ_I_T_ISS2 = Δ_I_T_P * postotak_sadrzaja_elektrona
print("Ionosfersko kašnjenje signala s Galileo satelita "
      "koji se nalazi u zenitnom smjeru iznad ISS2: {:.4f} ns".format(Δ_I_T_ISS2))

# f)
Δ_I_S_ISS2 = Δ_I_T_ISS2 * 3 * 10 ** 8 * 10 ** -9
print("Pogreška procijenjene udaljenosti od tog Galileo satelita "
      "do ISS2 kada ju ne bismo kompenzirali: {:.4f} m".format(Δ_I_S_ISS2))
