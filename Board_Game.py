import random


def get_board_mapping():
    return {
        "ladders": {3: 16, 5: 7, 15: 25, 18: 20, 21: 32},
        "snakes": {12: 2, 14: 11, 17: 4, 31: 19, 35: 22}
    }


def roll_die():
    return random.randint(1, 6)


def move_player(position, ladders, snakes, ladder_chance=1.0, immune_snake_count=0):
    new_position = position + roll_die()
    snakes_hit = 0

    if new_position >= 36:
        return new_position, snakes_hit, immune_snake_count

    if new_position in ladders:
        if random.random() < ladder_chance:
            new_position = ladders[new_position]
    elif new_position in snakes:
        if immune_snake_count > 0:
            immune_snake_count -= 1
        else:
            new_position = snakes[new_position]
            snakes_hit = 1

    return new_position, snakes_hit, immune_snake_count


def q1_q2_simulation(simulations=10000):
    board = get_board_mapping()
    p1_wins = 0
    total_snakes = 0

    for _ in range(simulations):
        p1_pos = 1
        p2_pos = 1
        game_snakes = 0

        while True:
            p1_pos, s_hit, _ = move_player(p1_pos, board["ladders"], board["snakes"])
            game_snakes += s_hit
            if p1_pos >= 36:
                p1_wins += 1
                total_snakes += game_snakes
                break

            p2_pos, s_hit, _ = move_player(p2_pos, board["ladders"], board["snakes"])
            game_snakes += s_hit
            if p2_pos >= 36:
                total_snakes += game_snakes
                break

    return (p1_wins / simulations) * 100, total_snakes / simulations


def q3_simulation(simulations=10000):
    board = get_board_mapping()
    total_rolls = 0

    for _ in range(simulations):
        pos = 1
        rolls = 0

        while pos < 36:
            pos, _, _ = move_player(pos, board["ladders"], board["snakes"], ladder_chance=0.5)
            rolls += 1

        total_rolls += rolls

    return total_rolls / simulations


def q4_simulation(simulations=10000):
    board = get_board_mapping()
    best_start = 1
    closest_diff = 100

    for start_pos in range(1, 36):
        p1_wins = 0

        real_start_pos = start_pos
        if real_start_pos in board["ladders"]:
            real_start_pos = board["ladders"][real_start_pos]
        elif real_start_pos in board["snakes"]:
            real_start_pos = board["snakes"][real_start_pos]

        for _ in range(simulations):
            p1_pos = 1
            p2_pos = real_start_pos

            while True:
                p1_pos, _, _ = move_player(p1_pos, board["ladders"], board["snakes"])
                if p1_pos >= 36:
                    p1_wins += 1
                    break

                p2_pos, _, _ = move_player(p2_pos, board["ladders"], board["snakes"])
                if p2_pos >= 36:
                    break

        p1_win_rate = p1_wins / simulations
        diff = abs(p1_win_rate - 0.5)

        if diff < closest_diff:
            closest_diff = diff
            best_start = start_pos

    return best_start


def q5_simulation(simulations=10000):
    board = get_board_mapping()
    p1_wins = 0

    for _ in range(simulations):
        p1_pos = 1
        p2_pos = 1
        p2_immunity = 1

        while True:
            p1_pos, _, _ = move_player(p1_pos, board["ladders"], board["snakes"])
            if p1_pos >= 36:
                p1_wins += 1
                break

            p2_pos, _, p2_immunity = move_player(p2_pos, board["ladders"], board["snakes"],
                                                 immune_snake_count=p2_immunity)
            if p2_pos >= 36:
                break

    return (p1_wins / simulations) * 100


def run_all():
    q1_win, q2_snakes = q1_q2_simulation()
    q3_rolls = q3_simulation()
    q4_start = q4_simulation()
    q5_win = q5_simulation()

    print(f"Q1: {q1_win:.2f}%")
    print(f"Q2: {q2_snakes:.2f}")
    print(f"Q3: {q3_rolls:.2f}")
    print(f"Q4: Casa {q4_start}")
    print(f"Q5: {q5_win:.2f}%")


if __name__ == "__main__":
    run_all()