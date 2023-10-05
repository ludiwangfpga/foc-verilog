import numpy as np

import time
class FOCController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.error_sum = 0
        self.prev_error = 0

    def pi_controller(self, error):
        self.error_sum += error
        return self.kp * error + self.ki * self.error_sum

    def clarke_transform(self, ia, ib):
        return np.array([ia, (1 / np.sqrt(3)) * (ia + 2 * ib)])

    def park_transform(self, alpha, beta, theta):
        return np.array([
            alpha * np.cos(theta) + beta * np.sin(theta),
            -alpha * np.sin(theta) + beta * np.cos(theta)
        ])

    def inverse_park_transform(self, d, q, theta):
        return np.array([
            d * np.cos(theta) - q * np.sin(theta),
            d * np.sin(theta) + q * np.cos(theta)
        ])

    def inverse_clarke_transform(self, alpha, beta):
        return np.array([
            alpha,
            (-alpha / 2 + np.sqrt(3) / 2 * beta)
        ])

    def compute(self, theta, iq_ref, id_ref):
        # Assuming ia, ib are obtained from your system
        ia, ib = 1.0, 1.0  # replace with actual values

        alpha_beta = self.clarke_transform(ia, ib)
        dq = self.park_transform(alpha_beta[0], alpha_beta[1], theta)

        error_q = iq_ref - dq[0]
        error_d = id_ref - dq[1]

        control_output_q = self.pi_controller(error_q)
        control_output_d = self.pi_controller(error_d)

        alpha_beta_inv = self.inverse_park_transform(control_output_d, control_output_q, theta)
        ia_ib_inv = self.inverse_clarke_transform(alpha_beta_inv[0], alpha_beta_inv[1])

        return ia_ib_inv, dq  # returning the inverse transformed current values and the dq values


# Usage:
foc_controller = FOCController(kp=1.0, ki=0.1, kd=1.0)
theta, iq_ref, id_ref = np.pi/4, 1.0, 1.11111111111111

start_time = time.time()
end_time = start_time + 10  # 1 minute later

# Create an empty list to store the computations per second
computations_per_second = []

while time.time() < end_time:
    iterations = 0
    check_time = time.time() + 1  # 1 second later
    while time.time() < check_time:
        ia_ib_ic, iq_id = foc_controller.compute(theta, iq_ref, id_ref)
        iterations += 1

        print(ia_ib_ic)
    # Append the number of computations in this second to the list
    computations_per_second.append(iterations)

# Convert the list to a numpy array if needed
computations_per_second_array = np.array(computations_per_second)
print(computations_per_second_array)
