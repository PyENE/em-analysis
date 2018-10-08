"""Stores a HSMM model and its parameters."""
from config import MODELS_PATH
import initial_probabilities
import logging
import model_parameters
import numpy as np
import observation_distribution
import occupancy_distribution
from openalea.sequence_analysis import Estimate
from openalea.sequence_analysis import HiddenSemiMarkov
from openalea.sequence_analysis import Sequences
import os
import output_process
import random
import shutil
import tempfile
import transition_probabilities


class Model(object):
    """Stores a HSMM model and its parameters."""

    def __init__(self, eye_movement_data, model_type='HIDDEN_SEMI-MARKOV_CHAIN',
                 output_process_name='READMODE', init_hsmc_file=None,
                 k=None, random_init=False, n_init=None, n_random_seq=None,
                 n_iter_init=None):
        """Model constructor."""

        self.parameters = None
        self._criterion = dict()
        self._log_likelihood = []
        self._bic = []
        self._nb_parameters = []
        self._eye_movement_data = eye_movement_data
        self._model_type = model_type
        self._output_process_name = output_process_name
        self._init_hsmc_file = init_hsmc_file
        self._k = k
        self._random_init = random_init
        self._n_init = n_init
        self._n_random_seq = n_random_seq
        self._n_iter_init = n_iter_init

        self._tmp_path = tempfile.mkdtemp(prefix='ema-tmp-dir-')
        self._model_id = self._tmp_path[-6:]
        self._n_iter = 0
        self._hsmc_file = os.path.join(MODELS_PATH, self._model_id + '.hsmc')

        # init with hsmc file
        if init_hsmc_file is not None and not random_init and \
                all(item is None for item in
                    [k, n_init, n_random_seq, n_iter_init]):
            if '.' not in init_hsmc_file:
                raise ValueError('Mal-formated init_hsmc_file name.')
            shutil.copyfile(self._init_hsmc_file, self._hsmc_file)
            self.secure_probabilities_sum(self._hsmc_file)
            self.hsmm = HiddenSemiMarkov(self._hsmc_file)
            self.update_parameters()

        # simple init without hsmc file
        elif (not random_init and
                  all(item is None for item in [n_init, n_random_seq, n_iter_init])
              and k is not None):
            self._n_iter = 10
            self.hsmm = Estimate(self._eye_movement_data.input_sequence(self._output_process_name),
                                 'HIDDEN_SEMI-MARKOV', 'Ordinary', self._k, 'Irreducible',
                                 OccupancyMean='Estimated', NbIteration=self._n_iter,
                                 Estimator='CompleteLikelihood', StateSequences='Viterbi', Counting=False)
            self.hsmm.save(self._hsmc_file)
            self.secure_probabilities_sum(self._hsmc_file)
            self.update_parameters()
            self.update_restored_data()

        # random init
        elif (random_init and init_hsmc_file is None and
                  all(item is not None for item in
                      [k, n_init, n_random_seq, n_iter_init])):

            max_likelihood = float("-inf")
            best_model = Estimate(
                self._eye_movement_data.input_sequence(self._output_process_name), 'HIDDEN_SEMI-MARKOV', 'Ordinary', self._k,
                'Irreducible', OccupancyMean='Estimated',
                NbIteration=n_iter_init, Estimator='CompleteLikelihood',
                StateSequences='Viterbi', Counting=False)
            current_likelihood = best_model.get_likelihood()

            for _ in xrange(0, n_init):
                attempt_number = 0
                while attempt_number <= 50:
                    try:
                        random_sequences = Sequences(self.generate_random_sequences(n_random_seq))
                        semi_markov_model = Estimate(random_sequences, "SEMI-MARKOV", 'Ordinary')
                        semi_markov_model.write_hidden_semi_markov_init_file(os.path.join(MODELS_PATH, 'temp.hsmc'))
                        hidden_semi_markov_model = HiddenSemiMarkov(os.path.join(MODELS_PATH, 'temp.hsmc'))
                        hidden_semi_markov_model = Estimate(
                            self._eye_movement_data.input_sequence(self._output_process_name), "HIDDEN_SEMI-MARKOV",
                            hidden_semi_markov_model, NbIteration=n_iter_init)
                        current_likelihood = hidden_semi_markov_model.get_likelihood()
                        # current_likelihood = hidden_semi_markov_model.get_nb_param_vector()[-1]  # to comment
                        if current_likelihood > max_likelihood:
                            max_likelihood = current_likelihood
                            best_model = hidden_semi_markov_model
                            self._log_likelihood = hidden_semi_markov_model.get_likelihood_vector()
                            self._bic = hidden_semi_markov_model.get_bic_vector()
                            self._nb_parameters = hidden_semi_markov_model.get_nb_param_vector()
                        break
                    except Exception as e:
                        logging.warning(e)
                if attempt_number >= 20:
                    raise DeprecationWarning(
                        'The random initialization seems to be taking'
                        'too much time.'
                        'You should consider changing the hyperparameter :'
                        'n_random_seq')
            self.hsmm = best_model
            self.hsmm.save(self._hsmc_file)
            self.secure_probabilities_sum(self._hsmc_file)
            self._n_iter = n_iter_init
            self.update_parameters()
            self.update_restored_data()

        else:
            raise ValueError('Forbidden call.')

    def update_hsmc_file(self):
        """Update hsmc_file after manual modification of parameters."""

        try:
            with open(self._hsmc_file, 'w') as f:
                f.write(self._model_type)
                f.write('\n\n')
                f.write(str(self._k))
                f.write(' STATES\n\n')
                f.write('INITIAL_PROBABILITIES\n')
                for i in xrange(0, self._k):
                    f.write(str(self.parameters.initial_probabilities.initial_probabilities[i]))
                    if i != self._k - 1:
                        f.write('     ')
                f.write('\n\n')
                f.write('TRANSITION_PROBABILITIES\n')
                for i in xrange(0, self._k):
                    for j in xrange(0, self._k):
                        f.write(str(self.parameters.transition_probabilities.transition_probabilities[i, j]))
                        if j != self._k - 1:
                            f.write('     ')
                    f.write('\n')
                f.write('\n\n')
                for occupancy_distribution in self.parameters.occupancy_distributions:
                    if occupancy_distribution.state_type != 'ABSORBING':
                        f.write('STATE ')
                        f.write(str(occupancy_distribution.state_number))
                        f.write(' OCCUPANCY_DISTRIBUTION\n')
                        if occupancy_distribution.state_type != 'ABSORBING':
                            f.write(occupancy_distribution.distribution_name)
                            f.write('   INF_BOUND : ')
                            f.write(str(occupancy_distribution.lower_bound))
                            if occupancy_distribution.distribution_name == 'BINOMIAL':
                                f.write('   SUP_BOUND : ')
                                f.write(str(occupancy_distribution.upper_bound))
                            if occupancy_distribution.distribution_name == 'NEGATIVE_BINOMIAL' or \
                                    occupancy_distribution.distribution_name == 'POISSON':
                                f.write('   PARAMETER : ')
                                f.write(str(occupancy_distribution.parameter))
                            if occupancy_distribution.distribution_name == 'NEGATIVE_BINOMIAL' or \
                                    occupancy_distribution.distribution_name == 'BINOMIAL':
                                f.write('   PROBABILITY : ')
                                f.write(str(occupancy_distribution.probability))
                            f.write('\n\n')
                f.write(str(len(self.parameters.output_processes)))
                if len(self.parameters.output_processes) > 1:
                    f.write(' OUTPUT_PROCESSES\n\n')
                else:
                    f.write(' OUTPUT_PROCESS\n\n')
                for output_process in self.parameters.output_processes:
                    f.write('OUTPUT_PROCESS ')
                    f.write(str(output_process.output_process_number))
                    f.write(' : ')
                    f.write(output_process.output_process_type)
                    f.write('\n\n')
                    for observation_distribution in output_process.observation_distributions:
                        f.write('STATE ')
                        f.write(str(observation_distribution.observation_distribution_number))
                        f.write(' OBSERVATION_DISTRIBUTION\n')
                        for i in xrange(0, len(observation_distribution.outputs)):
                            f.write('OUTPUT ')
                            f.write(str(i))
                            f.write(' : ')
                            f.write(str(observation_distribution.outputs[i]))
                            f.write('\n')
                        f.write('\n')
                if bool(self._criterion):
                    f.write('# cumulative length: ')
                    f.write(str(self._criterion['cumulative_length']))
                    f.write('\n')
                    f.write('# information of the sequences in the iid case: ')
                    f.write(str(self._criterion['seq_information_iid_case']))
                    f.write('\n')
                    f.write('# log-likelihood of the state sequences: ')
                    f.write(str(self._criterion['ll_state_seq']))
                    f.write('\n')
                    f.write('# state sequence entropy: ')
                    f.write(str(self._criterion['state_seq_entropy']))
                    f.write('\n')
                    f.write('# log-likelihood of the observed sequences: ')
                    f.write(str(self._criterion['ll_observed_seq']))
                    f.write('\n')
                    f.write('# ')
                    f.write(str(self._criterion['free_parameters']))
                    f.write(' free parameters   2 * penalyzed log-likelihood'
                            '(AIC): ')
                    f.write(str(self._criterion['AIC']))
                    f.write('\n')
                    f.write('# ')
                    f.write(str(self._criterion['free_parameters']))
                    f.write(' free parameters   2 * penalyzed log-likelihood'
                            '(BIC): ')
                    f.write(str(self._criterion['BIC']))
                    f.write('\n')
                    f.write('# ')
                    f.write(str(self._criterion['free_parameters']))
                    f.write(' free parameters   2 * penalyzed log-likelihood'
                            '(ICL): ')
                    f.write(str(self._criterion['ICL']))
                    f.write('\n')
            self.hsmm = HiddenSemiMarkov(self._hsmc_file)
        except TypeError:
            with open(self._hsmc_file, 'w') as f:
                f.write(
                    'File could not be created. There might be an error\n'
                    'related to recent changes using model parameters\n'
                    'setters. Check out the user warnings.\n')

    def update_parameters(self):
        """Update model parameters after running estimate."""
        with open(self._hsmc_file, 'r') as f:
            while True:
                l = f.readline()
                if not l:
                    break
                if '#' in l:
                    pass
                if 'HIDDEN_SEMI-MARKOV_CHAIN' in l:
                    self._model_type = l.split()[0]
                if 'STATES' in l:
                    self._k = int(l.split()[0])
                if 'INITIAL_PROBABILITIES' in l:
                    l = f.readline()
                    row = map(float, l.split())
                    assert (len(row) == self._k)
                    init_p = initial_probabilities.InitialProbabilities(
                        self, row)
                if 'TRANSITION_PROBABILITIES' in l:
                    trans_p = np.zeros(
                        shape=(self._k, self._k))
                    for i in xrange(0, self._k):
                        l = f.readline()
                        row = map(float, l.split())
                        trans_p[i, :] = row
                    trans_p = transition_probabilities.TransitionProbabilities(
                        self, trans_p)
                    # absorbing states
                    occupancy_d = []
                    absorbing_states = []
                    for i in xrange(0, self._k):
                        if trans_p.transition_probabilities[i, i] == 1:
                            absorbing_states.append(i)
                    for absorbing_state in absorbing_states:
                        occupancy_d.append(
                            occupancy_distribution.OccupancyDistribution(
                                self, absorbing_state, 'ABSORBING'))
                if 'OCCUPANCY_DISTRIBUTION' in l:
                    state_number = int(l.split()[1])
                    l = f.readline()
                    state_type = 'RECURRENT'
                    distribution_name = l.split()[0]
                    if distribution_name == 'NEGATIVE_BINOMIAL':
                        lower_bound = int(l.split()[3])
                        parameter = float(l.split()[6])
                        probability = float(l.split()[9])
                        occupancy_d.append(
                            occupancy_distribution.OccupancyDistribution(
                                self, state_number, state_type,
                                distribution_name=distribution_name,
                                lower_bound=lower_bound, parameter=parameter,
                                probability=probability))
                    elif distribution_name == 'BINOMIAL':
                        lower_bound = int(l.split()[3])
                        upper_bound = int(l.split()[6])
                        probability = float(l.split()[9])
                        occupancy_d.append(
                            occupancy_distribution.OccupancyDistribution(
                                self, state_number, state_type,
                                distribution_name=distribution_name,
                                lower_bound=lower_bound,
                                upper_bound=upper_bound,
                                probability=probability))
                    elif distribution_name == 'POISSON':
                        lower_bound = int(l.split()[3])
                        parameter = float(l.split()[6])
                        occupancy_d.append(
                            occupancy_distribution.OccupancyDistribution(
                                self, state_number, state_type,
                                distribution_name=distribution_name,
                                lower_bound=lower_bound, parameter=parameter))
                    else:
                        raise IOError(
                            'Mal-formated file. Incorrect distribution name.')
                if 'OUTPUT_PROCESS' in l:
                    try:
                        number_of_output_processes = int(l.split()[0])
                        output_p = []
                    except ValueError:
                        pass
                if 'OUTPUT_PROCESS' in l and 'CATEGORICAL' in l:  # if 'OBSERVATION_DISTRIBUTION' in l:
                    output_process_number = int(l.split()[1])
                    output_process_type = l.split()[3]
                    observation_d = []
                    for _ in xrange(0, self._k):
                        while 'OBSERVATION_DISTRIBUTION' not in l:
                            l = f.readline()
                        observation_distribution_number = int(l.split()[1])
                        size_of_output_process = 0
                        last_position = f.tell()
                        l = f.readline()
                        while (not l) or ('OUTPUT_PROCESS' in l and 'CATEGORICAL' in l):
                            if 'OUTPUT ' in l:
                                if size_of_output_process < int(l.split()[1]):
                                    size_of_output_process = int(l.split()[1])
                            l = f.readline()
                        f.seek(last_position)
                        output_numbers = []
                        outputs = []
                        l = f.readline()
                        while 'OUTPUT ' in l:
                            output_numbers.append(int(l.split()[1]))
                            outputs.append(float(l.split()[3]))
                            l = f.readline()
                        if len(output_numbers) != size_of_output_process:
                            for i in xrange(0, size_of_output_process):
                                if i not in output_numbers:
                                    outputs.insert(i, 0.)
                        observation_d.append(
                            observation_distribution.ObservationDistribution(
                                self, observation_distribution_number, outputs))
                        if observation_distribution_number == self._k - 1:
                            output_p.append(
                                output_process.OutputProcess(
                                    self, output_process_number,
                                    output_process_type, observation_d))
                if 'cumulative length' in l:
                    self._criterion['cumulative_length'] = int(l.split()[3])
                if 'information of the sequences in the iid case' in l:
                    self._criterion['seq_information_iid_case'] = \
                        float(l.split()[9])
                if 'log-likelihood of the state sequences' in l:
                    self._criterion['ll_state_seq'] = float(l.split()[6])
                if 'state sequence entropy' in l:
                    self._criterion['state_seq_entropy'] = float(l.split()[4])
                if 'log-likelihood of the observed sequences' in l:
                    self._criterion['ll_observed_seq'] = float(l.split()[6])
                if '(AIC)' in l:
                    self._criterion['AIC'] = float(l.split()[9])
                if '(BIC)' in l:
                    self._criterion['BIC'] = float(l.split()[9])
                if '(ICL)' in l:
                    self._criterion['ICL'] = float(l.split()[9])
                if 'free parameters' in l:
                    self._criterion['free_parameters'] = int(l.split()[1])

            self.parameters = model_parameters.ModelParameters(
                self, init_p, trans_p, output_p, occupancy_d)

    def iterate_em(self, n_iter):
        """Iterate EM for n_iter steps."""
        if n_iter < 1:
            raise ValueError('n_iter must be > 0.')
        self.hsmm = HiddenSemiMarkov(self._hsmc_file)
        self.hsmm = Estimate(self._eye_movement_data.input_sequence(self._output_process_name),
                             "HIDDEN_SEMI-MARKOV", self.hsmm, NbIteration=n_iter)
        self.hsmm.save(self._hsmc_file)
        self.secure_probabilities_sum(self._hsmc_file)
        self._n_iter += n_iter
        self.update_parameters()
        self.update_restored_data()
        self._log_likelihood = self._log_likelihood + self.hsmm.get_likelihood_vector()
        self._bic = self._bic + self.hsmm.get_bic_vector()
        self._nb_parameters = self._nb_parameters + self.hsmm.get_nb_param_vector()

    def update_restored_data(self):
        """Update restaured data after running estimate."""
        restored_data = self.hsmm.extract_data()
        self.eye_movement_data.restored_data = self.eye_movement_data.dataframe.assign(
            STATES=[fixation[0] for text_reading in restored_data for fixation in text_reading])
        self.eye_movement_data.restored_data['PHASE'] = self.eye_movement_data.restored_data.STATES
        self.eye_movement_data.restored_data.at[self.eye_movement_data.restored_data.PHASE < 2, 'PHASE'] = 0
        self.eye_movement_data.restored_data.at[self.eye_movement_data.restored_data.PHASE == 2, 'PHASE'] = 1
        self.eye_movement_data.restored_data.at[self.eye_movement_data.restored_data.PHASE == 3, 'PHASE'] = 2
        self.eye_movement_data.restored_data.at[self.eye_movement_data.restored_data.PHASE == 4, 'PHASE'] = 3

    def print_hsmc_file(self, verbose=True):
        """Print the content inside hsmc_file on the stdout."""
        with open(self._hsmc_file, 'r') as f:
            for l in f:
                if (verbose or ('#' not in l and l != '\n')) and bool(l):
                    print(l)

    def generate_random_sequences(self, number_of_sequences_to_generate=100):
        """Generate random sequences.

        Select a random observed sequence of in self.input_sequence
        ('READMODE' by default) and generate a corresponding
        random hidden sequence.

        :param number_of_sequences_to_generate: an integer, the number of
        sequences to be generated
        :return: a list of list of list containing [the generated sequence,
        the output processes]

        :Example:

        >>> model.generate_random_sequences(100)
        """

        def generate_any_random_sequences(random_sequences, number_of_sequences_left):
            iseq = self.eye_movement_data.input_sequence(self._output_process_name)
 
            rseq = random_sequences
            n_output_processes = len(iseq[0][0])

            for _ in xrange(0, number_of_sequences_left):
                sequence_number = random.randint(0, len(iseq) - 1)
                random_sequence = []
                sequence_length = len(iseq[sequence_number])
                number_of_transitions = random.randint(1, min(sequence_length - 1, 3))  # min(sequence_length-1, 7)
                # tirage uniforme sans remise
                transition_instants = sorted(random.sample(np.arange(sequence_length) + 1, number_of_transitions))
                # tirage uniforme avec remise
                # mais pas deux fois le meme qui se suit
                random_sequence = iseq[sequence_number][:]
                current_hidden_state = random.sample(range(0, self._k), 1)[0]
                random_sequence[0].insert(0, current_hidden_state)
                for i in xrange(1, sequence_length):
                    if i in transition_instants:
                        possible_new_state = range(0, self._k)
                        possible_new_state.remove(current_hidden_state)
                        current_hidden_state = random.sample(possible_new_state, 1)[0]
                    random_sequence[i].insert(0, current_hidden_state)

                logging.debug('*generate_any_random_sequences* ', random_sequence)


                """
                random_hidden_states = [random.randint(0, self._k - 1)]
                current_hidden_state = random_hidden_states[0]
                for _ in xrange(0, number_of_transitions):
                    previous_hidden_state = current_hidden_state
                    while True:
                        random_hidden_states.append(
                            random.randint(0, self._k - 1))
                        current_hidden_state = random_hidden_states[-1]
                        if previous_hidden_state != current_hidden_state:
                            break
                        else:
                            random_hidden_states.pop()
                i = 0
                for j in xrange(0, len(random_hidden_states) - 1):
                    for _ in xrange(i, transition_instants[j]):
                        random_sequence.append([random_hidden_states[j]])
                        i += 1
                for _ in xrange(i, sequence_length):
                    random_sequence.append([random_hidden_states[-1]])
                    i += 1
                i = 0
                for fixation in iseq[sequence_number]:
                    for observation in fixation:
                        random_sequence[i].append(observation)
                    i += 1
                """
                rseq.append(random_sequence)
            return rseq

        def remove_invalid_sequences(random_sequences):
            # check that censured freq are always smaller than freq
            # initialization of freq tables
            iseq = self.eye_movement_data.input_sequence(self._output_process_name)
            max_seq_len = -1
            for text_reading in iseq:
                if len(text_reading) > max_seq_len:
                    max_seq_len = len(text_reading)
            single_run = dict(
                [(key, [0] * max_seq_len) for key in xrange(0, self._k)])
            initial_run = dict(
                [(key, [0] * max_seq_len) for key in xrange(0, self._k)])
            final_run = dict(
                [(key, [0] * max_seq_len) for key in xrange(0, self._k)])
            frequency = dict(
                [(key, [0] * max_seq_len) for key in xrange(0, self._k)])
            # build freq tables
            for i in xrange(0, len(random_sequences)):
                initial_run_bool = True
                current_state = random_sequences[i][0][0]
                it = 0
                global_it = 0
                for j in xrange(0, len(random_sequences[i])):
                    it += 1
                    global_it += 1
                    previous_state = current_state
                    current_state = random_sequences[i][j][0]
                    if previous_state != current_state:
                        if initial_run_bool:
                            initial_run_bool = False
                            initial_run[previous_state][it] += 1
                        else:
                            frequency[previous_state][it] += 1
                        it = 0
                    elif it == len(random_sequences[i]):
                        single_run[previous_state][it] += 1
                    elif global_it == len(random_sequences[i]):
                        final_run[current_state][it] += 1
            # max freq for non censored sojourn time
            max_seq_len_per_hidden_space = []
            for i in xrange(0, self._k):
                for j in range(max_seq_len - 1, 0, -1):
                    if frequency[i][j] != 0:
                        max_seq_len_per_hidden_space.append(j)
                        break
                if len(max_seq_len_per_hidden_space) <= i:
                    max_seq_len_per_hidden_space.append(0)

            # seq to be removed
            # (which have censored time longer than non censored time)
            pop_list = []
            for i in xrange(0, len(random_sequences)):
                initial_run_bool = True
                current_state = random_sequences[i][0][0]
                it = 0
                global_it = 0
                for j in xrange(0, len(random_sequences[i])):
                    it += 1
                    global_it += 1
                    previous_state = current_state
                    current_state = random_sequences[i][j][0]
                    if previous_state != current_state:
                        if initial_run_bool:
                            initial_run_bool = False
                            initial_run[previous_state][it] += 1
                            if it >= max_seq_len_per_hidden_space[previous_state]:
                                pop_list.append(i)
                                break
                        else:
                            frequency[previous_state][it] += 1
                        it = 0
                    elif it == len(random_sequences[i]):
                        single_run[previous_state][it] += 1
                        if it >= max_seq_len_per_hidden_space[previous_state]:
                            pop_list.append(i)
                            break
                    elif global_it == len(random_sequences[i]):
                        final_run[current_state][it] += 1
                        if it >= max_seq_len_per_hidden_space[previous_state]:
                            pop_list.append(i)
                            break
            pop_list.sort()
            for _ in range(len(pop_list), 0, -1):
                random_sequences.pop(pop_list.pop())
            return random_sequences

        random_sequences = []
        i = 0
        while len(random_sequences) < number_of_sequences_to_generate:
            i += 1
            logging.debug('iter: %d, number of sequences to generate: %d, current length: %d', i,
                          number_of_sequences_to_generate, len(random_sequences))
            random_sequences = generate_any_random_sequences(
                random_sequences,
                number_of_sequences_to_generate - len(random_sequences))
            logging.debug('number of seq after generation at iter %d: %d', i, len(random_sequences))
            random_sequences = remove_invalid_sequences(random_sequences)
            logging.debug('number of seq after remove invalid seq at iter %d: %d', i, len(random_sequences))
        return random_sequences

    @property
    def criterion(self):
        """criterion getter."""
        return self._criterion

    @property
    def model_type(self):
        """model_type getter."""
        return self._model_type

    @property
    def model_id(self):
        return self._model_id

    @property
    def k(self):
        return self._k

    @property
    def hsmc_file(self):
        return self._hsmc_file

    @property
    def eye_movement_data(self):
        return self._eye_movement_data

    @model_type.setter
    def model_type(self, value):
        """model_type setter."""
        model_list = ['HIDDEN_SEMI-MARKOV_CHAIN', 'SEMI-MARKOV_CHAIN']
        if value not in model_list:
            raise UserWarning('model_type not supported. Try:', model_list)
        self._model_type = value
        self.update_hsmc_file()

    @staticmethod
    def secure_probabilities_sum(hsmc_file):
        """Ensure init_p and trans_p probs sum to one (resp.) in hsmc_file."""

        def truncate(f, n):
            """Truncate/pad a float f to n decimal places without rounding.

            source : http://stackoverflow.com/questions/783897/truncating-floats-in-python
            """
            s = '{}'.format(f)
            if 'e' in s or 'E' in s:
                return '{0:.{1}f}'.format(f, n)
            i, p, d = s.partition('.')
            return float('.'.join([i, (d + '0' * n)[:n]]))

        with open(hsmc_file, 'r') as f:
            while True:
                l = f.readline()
                if not l:
                    break
                if '#' in l:
                    pass
                if 'STATES' in l:
                    k = int(l.split()[0])
                if 'INITIAL_PROBABILITIES' in l:
                    l = f.readline()
                    initial_probabilities = map(float, l.split())
                    assert (len(initial_probabilities) == k)
                    initial_probabilities = np.array(initial_probabilities)
                if 'TRANSITION_PROBABILITIES' in l:
                    transition_probabilities = np.zeros(
                        shape=(k, k))
                    for i in xrange(0, k):
                        l = f.readline()
                        row = map(float, l.split())
                        transition_probabilities[i, :] = row
                    break

        prob_sum = 0
        for i in xrange(0, k - 1):
            initial_probabilities[i] = truncate(initial_probabilities[i], 6)
            prob_sum += initial_probabilities[i]
        initial_probabilities[k - 1] = 1 - prob_sum
        for i in xrange(0, k - 1):
            prob_sum = 0
            for j in xrange(0, k - 1):
                transition_probabilities[i, j] = truncate(
                    transition_probabilities[i, j], 6)
                prob_sum += transition_probabilities[i, j]
            transition_probabilities[i, k - 1] = 1 - prob_sum
        prob_sum = 0
        for j in xrange(1, k):
            prob_sum += transition_probabilities[k - 1, j]
        transition_probabilities[k - 1, 0] = 1 - prob_sum

        fh, temp_file_path = tempfile.mkstemp()
        with open(temp_file_path, 'w') as temp_file:
            with open(hsmc_file, 'r') as old_file:
                while True:
                    l = old_file.readline()
                    if not l:
                        break
                    elif 'INITIAL_PROBABILITIES' in l:
                        temp_file.write('INITIAL_PROBABILITIES\n')
                        old_file.readline()
                        for i in xrange(0, k):
                            temp_file.write(str(initial_probabilities[i]))
                            if i != k - 1:
                                temp_file.write('     ')
                        temp_file.write('\n')
                    elif 'TRANSITION_PROBABILITIES' in l:
                        temp_file.write('TRANSITION_PROBABILITIES\n')
                        old_file.readline()
                        for i in xrange(0, k):
                            old_file.readline()
                            for j in xrange(0, k):
                                temp_file.write(
                                    str(transition_probabilities[i, j]))
                                if j != k - 1:
                                    temp_file.write('     ')
                            temp_file.write('\n')
                        temp_file.write('\n')
                    else:
                        temp_file.write(l)
        os.close(fh)
        os.remove(hsmc_file)
        shutil.move(temp_file_path, hsmc_file)
