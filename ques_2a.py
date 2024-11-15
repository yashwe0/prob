import numpy as np

class Alice:
    def __init__(self):
        self.past_play_styles = np.array([1, 1])
        self.results = np.array([1, 0])
        self.opp_play_styles = np.array([1, 1])
        self.points = 1

    def play_move(self):
        """
        Decide Alice's play style for the current round. Implement your strategy for 2a here.

        Returns:
            0 : attack
            1 : balanced
            2 : defence
        """
        n_a = self.points
        if self.results[-1] == 0:
            return 1
        elif self.results[-1] == 0.5:
            return 0
        else:
            n_b = len(self.results) - n_a
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
        # Initialize lists to store Bob's past play styles, results, and opponent's play styles
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

    choices = [1,0.5,0]

    res1, draw, res2 = payoff_matrix[m1][m2]
    
    if callable(res1):
        res1 = res1(n_a, n_b)

    if callable(res2):
        res2 = res2(n_a, n_b)
    weights = [res1, draw, res2]
    
    random_value = np.random.choice(choices, p = weights)


    if(random_value == 0.5):
        result = (0.5,0.5)
    elif random_value ==1:
        result = (1,0)
    else:
        result = (0,1)

    alice.observe_result(m1, m2, result[0])
    bob.observe_result(m2, m1, result[1])

def monte_carlo(num_rounds):
    """
    Runs a Monte Carlo simulation of the game for a specified number of rounds.

    Returns:
        None
    """
    payoff_matrix = np.array([[(lambda n_a, n_b: n_b / (n_a + n_b), 0, lambda n_a, n_b: n_a / (n_a + n_b)),
                              (7/10, 0, 3/10),
                              (5/11, 0, 6/11)],
                              [(3/10, 0, 7/10),
                               (1/3, 1/3, 1/3),
                               (3/10, 1/2, 1/5)],
                              [(6/11, 0, 5/11),
                               (1/5, 1/2, 3/10),
                               (1/10, 4/5, 1/10)]])

    a = Alice()
    b = Bob()

    for _ in range(num_rounds-2):
        simulate_round(a, b, payoff_matrix)

    print(f"Alice's final points: {int(a.points)}")
    print(f"Bob's final points: {int(b.points)}")

# Run Monte Carlo simulation with a specified number of rounds
if __name__ == "__main__":
    monte_carlo(num_rounds=10**5)

