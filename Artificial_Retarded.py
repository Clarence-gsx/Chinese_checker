class Artificial_Retarded(Agent):
    def getAction(self, state):
        legal_actions = self.game.actions(state)
        self.action = random.choice(legal_actions)
        player = self.game.player(state)
        ### START CODE HERE ###
        move = None
        agent_pos = state[1].getPlayerPiecePositions(player)
        opponent_pos = state[1].getPlayerPiecePositions(3 - player)
        aghead, agrear = self.get_head_rear(agent_pos, player)
        ophead, oprear = self.get_head_rear(opponent_pos, 3 - player)

        if self.stage_end(agrear,oprear,player):
            # end stage
            move = random.choice(self.greedy(legal_actions, player))
        elif self.stage_mid(aghead,ophead,player):
            # mid stage
            move = self.max_layer(state, 2, -float('inf'), float('inf'))[1]
        else:
            # start stage
            move = random.choice(self.greedy(legal_actions, player))
        self.action = move

    def greedy(self,legal_actions,player):
        if player == 1:
            max_vertical_advance_one_step = max([action[0][0] - action[1][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if
                           action[0][0] - action[1][0] == max_vertical_advance_one_step]
        else:
            max_vertical_advance_one_step = max([action[1][0] - action[0][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if
                           action[1][0] - action[0][0] == max_vertical_advance_one_step]
        return max_actions

    def get_head_rear(self, pos, player):
        if player == 1:
            head = pos[0][0]
            rear = pos[0][0]
            for position in pos:
                if position[0] < head:
                    head = position[0]
                if position[0] > rear:
                    rear = position[0]
        else:
            head = pos[0][0]
            rear = pos[0][0]
            for position in pos:
                if position[0] > head:
                    head = position[0]
                if position[0] < rear:
                    rear = position[0]

        return head, rear

    def stage_mid(self, aghead, ophead, player):
        if player == 1:
            return ophead - aghead >= 2
        else:
            return aghead - ophead >= 2

    def stage_end(self, agrear, oprear, player):
        if player == 1:
            return agrear <= oprear
        else:
            return oprear <= agrear

    def feature_eval(self, state):
        player = state[0]
        board = state[1]
        ag_pos = board.getPlayerPiecePositions(state[0])
        op_pos = board.getPlayerPiecePositions(3 - state[0])
        a1 = 0
        a2 = 0
        b1 = 0
        c1 = 0
        d1 = 0
        if player == 1:
            for position in ag_pos:
                a1 += 20 - position[0]
                b1 += abs(position[1] - board.getColNum(position[0]) / 2)
                c1 += position[0] / 10
        else:
            for position in ag_pos:
                a1 += position[0]
                b1 += abs(position[1] - board.getColNum(position[0]) / 2)
                c1 += position[0] / 10
        if player == 1:
            for position in op_pos:
                a2 += position[0]
        else:
            for position in op_pos:
                a2 += 20 - position[0]
        for position in ag_pos:
            d1 += abs(position[0] - c1)
        actions = self.game.actions(state)
        vertical_ad = {}
        advance = 0
        if player == 1:
            for action in actions:
                if action[0] in vertical_ad.keys():
                    if (action[0][0] - action[1][0]) > vertical_ad[action[0]]:
                        vertical_ad[action[0]] = action[0][0] - action[1][0]
                else:
                    vertical_ad[action[0]] = action[0][0] - action[1][0]
        else:
            for action in actions:
                if action[0] in vertical_ad.keys():
                    if (action[0][0] - action[1][0]) < vertical_ad[action[0]]:
                        vertical_ad[action[0]] = (action[0][0] - action[1][0])
                else:
                    vertical_ad[action[0]] = action[0][0] - action[1][0]
        for i in vertical_ad.keys():
            advance += vertical_ad[i]
        if player == 2:
            advance = -advance
        eval = 2.153 * (a1 - a2) + 0.343 * (-b1) + 0.712 * advance - 0.351 * d1
        return eval

    def ad_order(self, action):
        return action[1][0] - action[0][0]

    def max_layer(self, state, n, alpha, beta):
        if n == 0:
            return self.feature_eval(state)
        value = -float('inf')
        best_action = None
        actions = self.game.actions(state)
        if state[0] == 1:
            actions.sort(key=self.ad_order)
        else:
            actions.sort(key=self.ad_order)
            actions = actions[::-1]
        for action in actions:
            if state[0] == 1:
                if action[0][0] - action[1][0] < -1 or action[0][0] <= 4:
                    continue
            else:
                if action[0][0] - action[1][0] > 1 or action[0][0] >= 16:
                    continue
            if state[0] == 1:
                if value > 0:
                    value = max(value, self.min_layer(self.game.succ(state, action), n-1, alpha, beta) / (0.06 * (21 - action[0][0])))
                else:
                    value = max(value, self.min_layer(self.game.succ(state, action), n-1, alpha, beta) * (0.06 * (21 - action[0][0])))
            else:
                if value < 0:
                    value = max(value, self.min_layer(self.game.succ(state, action), n-1, alpha, beta) * ((0.06 * action[0][0])))
                else:
                    value = max(value, self.min_layer(self.game.succ(state, action), n-1, alpha, beta) / ((0.06 * action[0][0])))
            if value >= beta:
                if n == 2:
                    return value, action
                else:
                    return value
            if value > alpha:
                alpha = value
                if n == 2:
                    self.action = action
                best_action = action
        if n == 2:
            return value, best_action
        else:
            return value

    def min_layer(self, state, n, alpha, beta):
        value = float('inf')
        actions = self.game.actions(state)
        if state[0] == 2:
            actions.sort(key=self.ad_order)
            actions = actions[::-1]
        else:
            actions.sort(key=self.ad_order)
        for action in actions:
            if state[0] == 2:
                if action[0][0] - action[1][0] > 1 or action[0][0] >= 16:
                    continue
            else:
                if action[0][0] - action[1][0] < -1 or action[0][0] <= 4:
                    continue
            successor = self.game.succ(state, action)
            value = min(value, self.max_layer(successor, n-1, alpha, beta))
            if value <= alpha:
                return value
            beta = min(value, beta)
        return value

