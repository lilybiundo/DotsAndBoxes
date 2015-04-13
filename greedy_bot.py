def think(state, quip):

	moves = state.get_moves()

	best_move = moves[0]
	best_expectation = float('-inf')

	me = state.get_whos_turn()

	def outcome(score):
		if me == 'red':
			return score['red'] - score['blue']
		else:
			return score['blue'] - score['red']

	for move in moves:

		rollout_state = state.copy()

		rollout_state.apply_move(move)

		score = outcome(rollout_state.get_score())

		if score > best_expectation:
			best_expectation = score
			best_move = move


	return best_move