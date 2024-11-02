import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from typing import Literal

def create_filter(fs, fc, ws, rp=0.2, rs=60, filter_type: Literal["butter", "cheby1", "cheby2", "ellip"]= "butter"):
    fs = fs
    fc = fc
    wp = fc / (fs / 2)
    ws = ws / (fs / 2)
    rp = rp
    rs = rs
    if filter_type == "butter":
        N_min, wn = signal.buttord(wp, ws, rp, rs, fs=fs)
        print(f"wn {wn}")
        b, a = signal.butter(N_min, wn, btype="low", output='ba')
        print(f"ordre du filtre {filter_type}: {N_min}")
    elif filter_type == "cheby1":
        N_min, wn = signal.cheb1ord(wp, ws, rp, rs, fs=fs)
        b, a = signal.cheby1(N_min, rp, wn, btype="low", output='ba')
        print(f"ordre du filtre {filter_type}: {N_min}")

    elif filter_type == "cheby2":
        N_min, wn = signal.cheb2ord(wp, ws, rp, rs, fs=fs)
        b, a = signal.cheby2(N_min, rp, wn, btype="low", output='ba')
        print(f"ordre du filtre {filter_type}: {N_min}")

    elif filter_type == "ellip":
        N_min, wn = signal.ellipord(wp, ws, rp, rs, fs=fs)
        b, a = signal.ellip(N_min, rp, rs, wn, btype="low", output='ba')
        print(f"ordre du filtre {filter_type}: {N_min}")


    zeroes = np.roots(b)
    poles = np.roots(a)

    # w, H = signal.freqz(b, a, fs)
    # H_db = 20 * np.log10(np.abs(H))
    # phase = np.angle(H)
    # # Transforme freq normalise sur pi en Hz
    # freq_Hz = w * fs/(2*np.pi)
    #
    #
    #
    # match filter_type:
    #     case "butter":
    #         filter_type_name = "Butterworth"
    #     case "cheby1":
    #         filter_type_name = "Chebyshev Type I"
    #     case "cheby2":
    #         filter_type_name = "Chebyshev Type II"
    #     case "ellip":
    #         filter_type_name = "Elliptic"
    #     case _: filter_type_name = "Butterworth"
    #
    # zp.zplane(b, a, plot_title=f"Plan Complexe du filtre de type {filter_type_name}")
    #
    # fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
    #
    # ax1.plot(freq_Hz, H_db)
    # ax1.set_title(f"Réponse fréquentielle du filtre passe-bas de type {filter_type_name}")
    # ax1.set_xlabel("Fréquence (Hz)")
    # ax1.set_ylabel("Amplitude (dB)")
    # ax1.grid()
    #
    # ax2.plot(freq_Hz, np.unwrap(phase))
    # ax2.set_xlabel("Fréquence (Hz)")
    # ax2.set_ylabel("Phase (radians)")
    # ax2.grid()
    #
    # plt.tight_layout()
    # plt.show()

    # print(f"ordre min: {N_min}")
    # print(f"zeroes: {zeroes}")
    # print(f"poles: {poles}")

    return b, a

def filter_data(data, b, a):
    return signal.lfilter(b, a, data)

def averaged_input(input, array):
    new_avg = (sum(array) + input) / (len(array) + 1)
    return new_avg

def push_to_data_array(input, array, max_length):
    if len(array) < max_length:
        array.append(input)
    else:
        array.pop(0)
        array.append(input)

def create_fake_measurements(min=20, max=100, min_error=5, max_error=150, length=1000, num_errors=50):
    smooth_data = np.linspace(min, max, length)

    error_indices = np.random.choice(len(smooth_data), num_errors, replace=False)
    for idx in error_indices:
        # Random errors between min error and max error to simulate sonar misreadings
        smooth_data[idx] = np.random.uniform(min_error, max_error)

    # Convert to a list for easy viewing/manipulation
    fake_measurements = smooth_data.tolist()
    return fake_measurements

def test_floating_average(input_min_value=20, input_max_value=100, input_min_error=5,
                          input_max_error=150, fake_input_length=1000, num_errors=50, max_length=10):
    fake_measurements = create_fake_measurements(input_min_value, input_max_value, input_min_error,
                                                 input_max_error, fake_input_length, num_errors)
    data = fake_measurements[:max_length]
    for input in fake_measurements[max_length:]:
        print("==========================")
        print(f"Valeur en entree: {input}")
        push_to_data_array(input, data, max_length)
        output = averaged_input(input, data)
        print(f"Valeur en sortie: {output}")

    print(f"longueur des donnees retenu: {len(data)}")

def test_filter():
    fake_measurements = create_fake_measurements(length=50)
    b, a = create_filter(8, 3, 4)
    output_data = fake_measurements[:10]
    for input in fake_measurements[10:]:
        print("==========================")
        print(f"Valeur en entree: {input}")
        output_data = np.append(output_data, input)
        output_data = filter_data(output_data, b, a)
        output = output_data[-1]
        print(f"Valeur en sortie: {output}")




if __name__ == '__main__':
    fe = 1 / 0.125
    fc = fe / 2

    test = [2, 2, 2, 2]
    test_floating_average()
    # test_filter()





