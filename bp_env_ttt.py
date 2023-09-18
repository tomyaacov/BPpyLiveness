from bp_env_mask import BPEnvMask


class BPEnvTTT(BPEnvMask):
    def reset(self, seed=None):
        super().reset(seed)
        while all([x.name.startswith("X") and x.name != "XWin" for x in self.bprogram.event_selection_strategy.selectable_events(self.bprogram.tickets)]):
            self.bprogram.advance_bthreads(self.bprogram.tickets, self.bprogram.event_selection_strategy.select(self.bprogram.tickets))
        state = self.state_to_gym_space(True)
        self.hot_states = [False] * len(self.bprogram.tickets)
        self.last_state = state
        return state, None

    def step(self, action):
        s, r, done, a, b = super().step(action)
        if done:
            return s, r, done, a, b
        while all([x.name.startswith("X") and x.name != "XWin"  for x in self.bprogram.event_selection_strategy.selectable_events(self.bprogram.tickets)]):
            self.bprogram.advance_bthreads(self.bprogram.tickets, self.bprogram.event_selection_strategy.select(self.bprogram.tickets))
        new_state = self.state_to_gym_space(False)
        return new_state, r, done, a, b