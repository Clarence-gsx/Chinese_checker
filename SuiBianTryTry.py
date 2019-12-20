def feature_eval2(self, state):
    evaluate = 0
    player = state[0]
    board = state[1]
    agent_pos = board.getPlayerPiecePositions(state[0])
    opponent_pos = board.getPlayerPiecePositions(3 - state[0])

    myDistanceWin = 0
    herDistanceWin = 0
    myDistanceCenter = 0
    average_row = 0
    myLooseness = 0
    rightsideness = 0

    for position in agent_pos:
        myDistanceWin += position[0]
        myDistanceCenter += abs(position[1] - board.getColNum(position[0]) / 2)
        average_row += position[0] / 10.0

    for position in opponent_pos:
        herDistanceWin += 20 - position[0]

    for position in agent_pos:
        myLooseness += abs(position[0] - average_row)

    """
    Moving distances summing up
    """
    actions = self.game.actions(state)
    last = actions[0][0]
    f = {}
    stepping = 0

    for action in actions:
        if action[0] in f.keys():
            if (action[0][0] - action[1][0]) < f[action[0]]:
                f[action[0]] = (action[0][0] - action[1][0])
        else:
            f[action[0]] = (action[0][0] - action[1][0])

    for i in f.keys():
        stepping += f[i]
    stepping = -stepping
    print("stepping", stepping, " myLooseness", myLooseness, " mhdis", (myDistanceWin - herDistanceWin))
    # stepping = sum([action[0][0] - action[1][0] for action in actions])

    evaluate = 2.1 * (myDistanceWin - herDistanceWin) + 0.34 * (-myDistanceCenter) + 0.7 * stepping - 0.35 * myLooseness
    return evaluate