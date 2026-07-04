import random
from cfg.cfg_conf import *

labels = len(CFG_CONF_ENTRY)


class GreedWeight:
    def __init__(self, min_epsilon=0.05, decay_rate=0.995):
        self.path = []
        self.position = []
        self.label_times = {i: 0 for i in range(labels)}
        self.R = {}
        self.M = [i + 1 for i in range(labels)]
        self.min_epsilon = min_epsilon
        self.time_step = -1
        self.initial_epsilon = 1.0
        self.decay_rate = decay_rate
        for policy in self.M:
            self.R[policy] = {'success_count': 0, 'usage_count': 0}

    def empty_policy(self):
        for policy in self.M:
            self.R[policy] = {'success_count': 0, 'usage_count': 0}

    def add_path(self, policy):
        self.path.append(policy)

    def empty_path(self):
        self.path = []

    def add_position(self, position):
        self.position.append(position)

    def empty_position(self):
        self.position = []

    def add_time_step(self):
        self.time_step += 1

    def get_label_times(self):
        return self.label_times

    def add_label_times(self, item):
        self.label_times[item] += 1

    def get_rank(self):
        sorted_keys = sorted(self.label_times, key=self.label_times.get, reverse=True)
        return sorted_keys

    def experience_based_guide(self, policies):
        epsilon = max(self.min_epsilon, self.initial_epsilon * (self.decay_rate ** self.time_step))
        if random.random() < epsilon:
            total_usage_count = [self.R[policy]['usage_count'] for policy in policies]
            unused_policies = [policy for policy, count in zip(policies, total_usage_count) if count == 0]
            if unused_policies:
                selected_policy = random.choice(unused_policies)
            else:
                selected_policy = random.choice(policies)  # 如果没有未使用的策略，随机选择
        else:
            if len(policies) == 1:
                return random.choice(policies)
            selection_probabilities = self.calculate_weights(policies)
            selected_policy = random.choices(policies, weights=selection_probabilities, k=1)[0]

        return selected_policy

    def calculate_weights(self, policies):
        total_usage_count = max(sum(self.get_usage_count(policy) for policy in policies), 1)
        weights = []
        for policy in policies:
            base_weight = self.R[policy]['success_count']

            penalty = 1 - (self.R[policy]['usage_count'] / total_usage_count)

            final_weight = base_weight * penalty

            weights.append(final_weight)

        total_weight = max(sum(weights), 1)
        selection_probabilities = [weight / total_weight for weight in weights]
        return selection_probabilities

    def get_success_count(self, policy):
        return self.R[policy]['success_count']

    def get_usage_count(self, policy):
        return self.R[policy]['usage_count']

    def update_ranking(self, policy, success):
        if policy not in self.R:
            self.R[policy] = {'success_count': 0, 'usage_count': 0}  # 初始化策略

        self.R[policy]['usage_count'] += 1

        if success:
            self.R[policy]['success_count'] += 1

        self.R = dict(sorted(self.R.items(), key=lambda item: self.get_success_count(item[0]), reverse=True))

    def print_R(self):
        result = []
        for policy, stats in self.R.items():
            success_count = stats['success_count']
            usage_count = stats['usage_count']

            success_rate = success_count / usage_count if usage_count > 0 else 0.0
            result.append(
                f"Policy {policy}: Success Count = {success_count}, Usage Count = {usage_count}, "
                f"Success Rate = {success_rate:.4f}")

        return "\n".join(result)
