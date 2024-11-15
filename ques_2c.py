import numpy as np

class Alice:
    def __init__(self):
        self.past_play_styles = np.array([1, 1])
        self.results = np.array([1, 0])
        self.opp_play_styles = np.array([1, 1])
        self.points = 1

    def play_move(self):
        """
        Decide Alice's play style for the current round.
        
        Returns: 
            0 : attack
            1 : balanced
            2 : defence

        """
        n_b = Bob().points
        n_a = self.points
        if self.opp_play_styles[-1] == 2:
            return 1
        elif self.opp_play_styles[-1] == 1:
            return 0
        else:
            if n_b >= 1.2 * n_a:
                return 0
            else:
                return 2

    def observe_result(self, own_style, opp_style, result):
        """
        Update Alice's knowledge after each round based on the observed results.
        
        Returns:
            None
        """
        self.past_play_styles = np.append(self.past_play_styles, own_style)
        self.results = np.append(self.results, result)
        self.opp_play_styles = np.append(self.opp_play_styles, opp_style)
        self.points += result


class Bob:
    def __init__(self):
        self.past_play_styles = np.array([1, 1])
        self.results = np.array([0, 1])
        self.opp_play_styles = np.array([1, 1])
        self.points = 1

    def play_move(self):
        """
        Decide Bob's play style for the current round.

        Returns: 
            0 : attack
            1 : balanced
            2 : defence
        
        """
        if self.results[-1] == 1:
            return 2
        elif self.results[-1] == 0.5:
            return 1
        else:
            return 0

    def observe_result(self, own_style, opp_style, result):
        """
        Update Bob's knowledge after each round based on the observed results.
        
        Returns:
            None
        """
        self.past_play_styles = np.append(self.past_play_styles, own_style)
        self.results = np.append(self.results, result)
        self.opp_play_styles = np.append(self.opp_play_styles, opp_style)
        self.points += result

def simulate_round(alice, bob, payoff_matrix):
    """
    Simulates a single round of the game between Alice and Bob.
    
    Returns:
        None
    """
    m1 = alice.play_move()
    m2 = bob.play_move()
    n_a = alice.points
    n_b = bob.points

    res1, draw, res2 = payoff_matrix[m1][m2]

    if callable(res1):
        res1 = res1(n_a, n_b)

    random_val = np.random.random()

    if random_val < draw:
        result = (0.5, 0.5)
    elif random_val < draw + res1:
        result = (1, 0)
    else:
        result = (0, 1)

    alice.observe_result(m1, m2, result[0])
    bob.observe_result(m2, m1, result[1])

    return result[0]  # Returning Alice's round result

def estimate_tau(T):
    """
    Estimate the expected value of the number of rounds taken for Alice to win 'T' rounds.
    Your total number of simulations must not exceed 10^5.

    Returns:
        Float: estimated value of E[tau]
    """
    payoff_matrix = np.array([[(lambda n_a, n_b: n_b / (n_a + n_b), 0, lambda n_a, n_b: n_a / (n_a + n_b)),
                              (7 / 10, 0, 3 / 10),
                              (5 / 10, 0, 6 / 11)],
                              [(3 / 10, 0, 7 / 10),
                               (1 / 3, 1 / 3, 1 / 3),
                               (3 / 10, 1 / 2, 1 / 5)],
                              [(6 / 11, 0, 5 / 11),
                               (1 / 5, 1 / 2, 3 / 10),
                               (1 / 10, 4 / 5, 1 / 10)]])

    t = []

    for _ in range(10**5):
        a = Alice()
        b = Bob()
        rounds = 2
        while a.points < T:
            simulate_round(a, b, payoff_matrix)
            rounds += 1
        t.append(rounds)

    return np.mean(t)
entry_num = "2023MT60677"
print(f'E(τ) for T = 77 : {estimate_tau(17)}')
