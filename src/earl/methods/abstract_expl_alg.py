import time

import pandas as pd
from tqdm import tqdm


class ExplAlgAbstract:

    def __init__(self, env, bb_model, params, transition_model):
        pass

    def generate_explanation(self, facts, outcome, eval_path=''):
        # select only facts corresponding to fact_ids
        result_data = []
        objs = self.obj.objectives
        constraints = self.obj.constraints

        # generate explanations for each fact
        for i, f in tqdm(enumerate(facts)):
            start = time.time()
            cfs = self.get_best_cf(f, outcome.target_action)
            end = time.time()

            # collect results
            for cf in cfs:
                rew = cf.reward_dict
                item = ([i, list(cf.fact.forward_state), list(cf.cf), cf.recourse] +
                        [rew[o] for o in objs] + [rew[c] for c in constraints] +
                        [end-start])
                result_data.append(item)

        columns = ['Fact_id', 'Fact', 'Explanation', 'Recourse'] + objs + constraints + ['gen_time']
        res_df = pd.DataFrame(result_data, columns=columns)

        return res_df

    def get_best_cf(self, fact, target):
        return []