import numpy as np

data = [(2, 50), (3.6667, 100), (5, 200), (7.2, 500), (10, 1000)]

for d in data:
    s, n = d
    s_float32 = np.float32(s)

    print("\n\n" + "#" * 64)
    print("s =", s, "; n =", n)

    dzeta_forward = 0.0
    eta_forward = 0.0

    dzeta_backward = 0.0
    eta_backward = 0.0

    dzeta_forward_float32 = np.float32(0.0)
    eta_forward_float32 = np.float32(0.0)

    dzeta_backward_float32 = np.float32(0.0)
    eta_backward_float32 = np.float32(0.0)

    # w przód
    for k in range(1, n + 1):
        dzeta_forward += 1 / (k ** s)
        dzeta_forward_float32 += np.float32(1 / np.float32(k ** s))

        eta_forward += (-1) ** (k - 1) / k ** s
        eta_forward_float32 += np.float32((-1) ** (k - 1) / np.float32(k ** s))

    # wstecz
    for k in range(n, 0, -1):
        dzeta_backward += 1 / (k ** s)
        dzeta_backward_float32 += np.float32(1 / np.float32(k ** s))

        eta_backward += (-1) ** (k - 1) / k ** s
        eta_backward_float32 += np.float32((-1) ** (k - 1) / np.float32(k ** s))

    print("float64 - dzeta w przód: ", dzeta_forward)
    print("float64 - eta w przód: ", eta_forward)
    print("float64 - dzeta wstecz: ", dzeta_backward)
    print("float64 - eta wstecz:", eta_backward)
    print("float64 - dzeta różnica w przód/wstecz: ", abs(dzeta_forward - dzeta_backward))
    print("float64 - eta różnica w przód/wstecz: ", abs(eta_forward - eta_backward))

    print("\nfloat32 - dzeta w przód: ", dzeta_forward_float32)
    print("float32 - eta w przód: ", eta_forward_float32)
    print("float32 - dzeta wstecz: ", dzeta_backward_float32)
    print("float32 - eta wstecz:", eta_backward_float32)
    print("float32 - dzeta różnica w przód/wstecz: ", abs(dzeta_forward_float32 - dzeta_backward_float32))
    print("float32 - eta różnica w przód/wstecz: ", abs(eta_forward_float32 - eta_backward_float32))

    print("\ndzeta w przód - różnica float32/float64: ", abs(dzeta_forward - dzeta_forward_float32))
    print("eta w przód - różnica float32/float64: ", abs(eta_forward - eta_forward_float32))
    print("dzeta wstecz - różnica float32/float64: ", abs(dzeta_backward - dzeta_backward_float32))
    print("eta wstecz - różnica float32/float64: ", abs(eta_backward - eta_backward_float32))
