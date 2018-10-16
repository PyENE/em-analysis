"""Stores oculometric data as pandas dataframe."""
from .config import DATA_PATH
import math
from openalea.sequence_analysis import Sequences
from openalea.sequence_analysis._sequence_analysis import _MarkovianSequences
import numpy as np
import os
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from unidecode import unidecode


class EyeMovementData:
    """Stores oculometric data as pandas dataframe."""

    def __init__(self, oculometric_file=os.path.join(DATA_PATH, 'HMM_feat_outfile_v6_165_166.xls'),
                 text_file=os.path.join(DATA_PATH, 'TextesLectureParis.xlsx'),
                 text_type_file=os.path.join(DATA_PATH, 'text-a-priori-clustering.csv'), index_as_ms=False):
        """Class constructor.Import and merge data in pandas dataframe."""
        if index_as_ms:
            raise NotImplementedError('Not implemented yet.')

        self._index_as_ms = index_as_ms
        self.dataframe = pd.read_excel(oculometric_file)

        if oculometric_file == os.path.join(DATA_PATH, 'HMM_feat_outfile_v6_165_166.xls'):
            self._init_old_data(text_file, text_type_file)
        elif oculometric_file == os.path.join(DATA_PATH, 'oculo_data_nov17.xlsx'):
            self._init_new_data()
        elif oculometric_file == os.path.join(DATA_PATH, 'preprocessed_data_nov17.xlsx'):
            self._init_preprocessed_data(os.path.join(DATA_PATH, 'preprocessed_data_nov17.xlsx'))
        elif oculometric_file == os.path.join(DATA_PATH, 'em-y35.xlsx'):
            self._init_preprocessed_data(os.path.join(DATA_PATH, 'em-y35.xlsx'))
        elif oculometric_file == os.path.join(DATA_PATH, 'em-y35-tmp2.xlsx'):
            self._init_preprocessed_data(os.path.join(DATA_PATH, 'em-y35-tmp2.xlsx'))
        elif oculometric_file == os.path.join(DATA_PATH, 'em-y35-fasttext.xlsx'):
            self._init_preprocessed_data(os.path.join(DATA_PATH, 'em-y35-fasttext.xlsx'))
        else:
            raise NotImplementedError('This data file is not supported yet.')

        self._input_sequence = None
        self._restored_data = None
        self._input_sequence_getter_optimizer = False

    @property
    def restored_data(self):
        """restored data getter."""
        return self._restored_data

    @restored_data.setter
    def restored_data(self, restored_data):
        """restored data setter."""
        self._restored_data = restored_data

    def _init_old_data(self, text_file, text_type_file):
        text_data = pd.read_excel(text_file, header=1, parse_cols=[1, 2, 3], encoding='latin1')
        text_type_data = pd.read_csv(text_type_file, sep=';')
        del self.dataframe['TYPE_TEXT']

        for i in xrange(1, text_data.shape[0] - 1, 2):
            text_data.iloc[i, 1] = text_data.values[i - 1, 1]

        self.dataframe = pd.merge(
            self.dataframe, text_data, left_on='TEXT',
            right_on='Nom des fichiers "image"', how='left')

        self.dataframe = pd.merge(
            self.dataframe, text_type_data, left_on='TEXT',
            right_on='TEXT', how='left')

        self.dataframe = self.dataframe.rename(columns=lambda x: unidecode(x))
        self.dataframe = self.dataframe.rename(columns={'Association semantique FORTE (AF)': 'TEXT_CONTENT'})

        self._compute_saccade_direction()
        self._recompute_saccade_amplitude()

    def _init_new_data(self):
        dfA = pd.read_excel(os.path.join(DATA_PATH, 'oculo_data_nov17.xlsx'), sheetname='A')
        dfM = pd.read_excel(os.path.join(DATA_PATH, 'oculo_data_nov17.xlsx'), sheetname='M')
        dfF = pd.read_excel(os.path.join(DATA_PATH, 'oculo_data_nov17.xlsx'), sheetname='F')
        self.dataframe = pd.concat([dfA, dfM, dfF], ignore_index=True)
        self.dataframe = self._drop_pathological_fixations()
        self.dataframe = self.dataframe[(self.dataframe.READMODE != '_TOBEREPLACED_') | (self.dataframe.ISLAST == 1)]
        self.dataframe = self.dataframe.reset_index(drop=True)
        self.dataframe = self.remove_scanpaths_with_more_than_x_missing_values(8)
        self.dataframe = self._fill_missing_values()
        self.dataframe = self._remove_scanpaths_shorter_than_x_fixations(4)
        # self.dataframe['READMODE'] = pd.Categorical.from_array(self.dataframe.READMODE).labels
        self.dataframe = self._recompute_readmode()
        self.dataframe = self._add_new_readmode_col()
        self._compute_saccade_direction()
        self._recompute_saccade_amplitude()

    def save_dataframe_to_xlsx(self, file_name, sheet_name):
        writer = pd.ExcelWriter(file_name)
        self.dataframe.to_excel(writer, sheet_name)
        writer.save()

    def _init_preprocessed_data(self, file):
        self.dataframe = pd.read_excel(file)

    def recompute_readmode(self, readmode_type=0):
        """
        :param readmode_type:
            0: {<-1 , -1 , 0, 1 , >1}
            1: {<-1, -1, 0, 1, 2, >2}
            2: {<-2, -2, -1, 0, 1, 2, >2}
            3: {<-2, -2, -1, {0, 1}, 2, >2}
            4: {<-2, -2, -1, {0, 1}, >1}
        :return: pandas.DataFrame
        """
        df = self.dataframe.copy()
        if readmode_type == 0:
            df.at[df.WINC > 1, 'READMODE'] = 4
            df.at[df.WINC == 1, 'READMODE'] = 3
            df.at[df.WINC == 0, 'READMODE'] = 2
            df.at[df.WINC == -1, 'READMODE'] = 1
            df.at[df.WINC < -1, 'READMODE'] = 0
        if readmode_type == 1:
            df['READMODE'] = 5
            df.at[df.WINC == 2, 'READMODE'] = 4
            df.at[df.WINC == 1, 'READMODE'] = 3
            df.at[df.WINC == 0, 'READMODE'] = 2
            df.at[df.WINC == -1, 'READMODE'] = 1
            df.at[df.WINC < -1, 'READMODE'] = 0
        elif readmode_type == 2:
            df['READMODE'] = 6
            df.at[df.WINC == 2, 'READMODE'] = 5
            df.at[df.WINC == 1, 'READMODE'] = 4
            df.at[df.WINC == 0, 'READMODE'] = 3
            df.at[df.WINC == -1, 'READMODE'] = 2
            df.at[df.WINC == -2, 'READMODE'] = 1
            df.at[df.WINC < -2, 'READMODE'] = 0
        elif readmode_type == 3:
            df['READMODE'] = 5
            df.at[df.WINC == 2, 'READMODE'] = 4
            df.at[df.WINC == 1, 'READMODE'] = 3
            df.at[df.WINC == 0, 'READMODE'] = 3
            df.at[df.WINC == -1, 'READMODE'] = 2
            df.at[df.WINC == -2, 'READMODE'] = 1
            df.at[df.WINC < -2, 'READMODE'] = 0
        elif readmode_type == 4:
            df['READMODE'] = 4
            df.at[df.WINC == 1, 'READMODE'] = 3
            df.at[df.WINC == 0, 'READMODE'] = 3
            df.at[df.WINC == -1, 'READMODE'] = 2
            df.at[df.WINC == -2, 'READMODE'] = 1
            df.at[df.WINC < -2, 'READMODE'] = 0
        else:
            raise UserWarning('invalid readmode readmode_type.\n'
                              '0: {<-1 , -1 , 0, 1 , >1}\n'
                              '1: {<-1, -1, 0, 1, 2, >2}\n'
                              '2: {<-2, -2, -1, 0, 1, 2, >2}\n'
                              '3: {<-2, -2, -1, {0, 1}, 2, >2}\n'
                              '4: {<-2, -2, -1, {0, 1}, >1}')
        df['READMODE'] = pd.Categorical.from_array(df.READMODE).labels
        return df

    def _drop_pathological_fixations(self):
        df = self.dataframe.copy()
        set_is_last = []
        # in case the fixations before the last one also have wfreq < 0
        for i in df.index[(df.OFF_DUR == 1) & (df.ISLAST == 1)]:
            j = i - 1
            while df.at[j, 'OFF_DUR'] == 1:
                j -= 1
            set_is_last.append(j)

        set_is_first = []
        for i in df.index[(df.OFF_DUR == 1) & (df.ISFIRST == 1)]:
            j = i + 1
            while df.at[j, 'OFF_DUR'] == 1:
                j += 1
            set_is_first.append(j)

        df.at[set_is_last, 'ISLAST'] = 1
        df.at[set_is_first, 'ISFIRST'] = 1
        df = df[df.OFF_DUR == 0]
        df = df.reset_index(drop=True)
        return df

    def remove_scanpaths_with_more_than_x_missing_values(self, x):
        df = self.dataframe.copy()
        gb = df.groupby(['SUBJ_NAME', 'TEXT'])['CINC'].apply(lambda x: pd.isnull(x).sum()) >= x
        for i in gb.index:
            if gb[i]:
                idx_to_drop = df[(df['SUBJ_NAME'] == i[0]) & (df['TEXT'] == i[1])].index
                df = df.drop(idx_to_drop)
        df = df.reset_index(drop=True)
        return df

    def _compute_saccade_direction(self):
        """Compute saccade direction."""
        self.dataframe['SACDIR'] = 'forward'
        for i in self.dataframe.index:
            if self.dataframe.at[i, 'ISLAST'] == 0:
                diff_x = self.dataframe.at[i + 1, 'X'] - self.dataframe.at[i, 'X']
                diff_y = self.dataframe.at[i + 1, 'Y'] - self.dataframe.at[i, 'Y']
                if diff_y > 30:
                    self.dataframe.at[i, 'SACDIR'] = 'downward'
                elif diff_y < -30:
                    self.dataframe.at[i, 'SACDIR'] = 'upward'
                elif diff_x < 0:
                    self.dataframe.at[i, 'SACDIR'] = 'backward'
            else:
                self.dataframe.at[i, 'SACDIR'] = 'last'

    def _recompute_saccade_amplitude(self):
        """Set saccade amplitude to -1 for line breaks and last outgoing saccade"""
        self.dataframe['SACAMP'] = abs(self.dataframe['SACAMP'])
        for i in self.dataframe.index:
            if self.dataframe.at[i, 'ISLAST'] == 1:
                self.dataframe.at[i, 'SACAMP'] = -1
            elif self.dataframe.at[i + 1, 'ISLAST'] != 1:
                i += 1
                diff_y = self.dataframe.at[i + 1, 'Y'] - self.dataframe.at[i, 'Y']
                a = math.sqrt((self.dataframe.at[i + 1, 'X'] - self.dataframe.at[i, 'X']) ** 2
                              + (self.dataframe.at[i + 1, 'Y'] - self.dataframe.at[i, 'Y']) ** 2)
                b = math.sqrt((self.dataframe.at[i + 1, 'X'] - self.dataframe.at[i - 1, 'X']) ** 2
                              + (self.dataframe.at[i + 1, 'Y'] - self.dataframe.at[i - 1, 'Y']) ** 2)
                c = math.sqrt((self.dataframe.at[i - 1, 'X'] - self.dataframe.at[i, 'X']) ** 2
                              + (self.dataframe.at[i - 1, 'Y'] - self.dataframe.at[i, 'Y']) ** 2)
                angle = math.acos((a ** 2 + c ** 2 - b ** 2) / (2 * a * c)) * (180. / math.pi)
                if diff_y > 30 and angle < 20:  # go to next line
                    self.dataframe.at[i, 'SACAMP'] = -1

    def _dataframe_to_sequence(self, col_names='READMODE'):
        """Extract the pandas dataframe as a Sequence."""
        if isinstance(col_names, str):
            assert(col_names in self.dataframe.columns)
        elif all(isinstance(item, str) for item in col_names):
            for col_name in col_names:
                assert(col_name in self.dataframe.columns)
        else:
            raise ValueError('Forbidden call.')
        data = []
        is_last = self.dataframe['ISLAST'] == 1
        scanpath_start_index = 0
        for i in self.dataframe.index[is_last]:
            data.append(self.dataframe.loc[range(scanpath_start_index, i+1), col_names].values.tolist())
            scanpath_start_index = i+1
        return data

    def drop_negative_wfreq_fixations(self):
        is_last = self.dataframe['ISLAST'] == 1
        neg_wfreq = self.dataframe['WFREQ'] < 0
        set_is_last = []
        # in case the fixations before the last one also have wfreq < 0
        for i in self.dataframe.index[is_last & neg_wfreq]:
            j = i-1
            while self.dataframe.loc[j, 'WFREQ'] < 0:
                j -= 1
            set_is_last.append(j)

        self.dataframe.loc[set_is_last, 'ISLAST'] = 1
        self.dataframe = self.dataframe.drop(self.dataframe.index[neg_wfreq])
        self.dataframe = self.dataframe.reset_index(drop=True)
        self.dataframe = self.dataframe.drop(9947)  # wtf ?
        self.dataframe = self.dataframe.reset_index(drop=True)

    def _remove_scanpaths_shorter_than_x_fixations(self, x):
        df = self.dataframe.copy()
        gb = df.groupby(['SUBJ_NAME', 'TEXT'], as_index=False).size() < x
        for i in gb.index:
            if gb[i]:
                idx_to_drop = df[(df['SUBJ_NAME'] == i[0]) & (df['TEXT'] == i[1])].index
                df = df.drop(idx_to_drop)
        df = df.reset_index(drop=True)
        return df

    def _fill_missing_values(self):
        df = self.dataframe
        missing_values = df.loc[df.READMODE.isnull() | ((df.READMODE == "_TOBEREPLACED_"))]
        not_missing_values = df.loc[~df.index.isin(missing_values.index)]
        mlpr = MLPRegressor(solver='lbfgs',  # lbfgs is an optimizer in the family of quasi-Newton methods.
                            hidden_layer_sizes=(100,),
                            # sets large amount of neurons which will be (quasi)-removed using penalization.
                            alpha=0.00000029,  # L2 penalty (regularization term) parameter.
                            tol=1e-4,  # once tol is reached, stops the optimization algorithm.
                            learning_rate='constant',  # constant learning rate given by learning_rate_init.
                            )
        scaler = StandardScaler()
        scaler.fit(not_missing_values[['SACAMP', 'SACOR']])
        Xtrain = scaler.transform(not_missing_values[['SACAMP', 'SACOR']])
        Xpop = scaler.transform(missing_values[['SACAMP', 'SACOR']])
        Ytrain = not_missing_values[['CINC', 'WINC']]
        mlpr.fit(Xtrain, Ytrain)
        predicted_NAs = mlpr.predict(Xpop).round()
        predicted_NAs
        df.loc[missing_values.index, 'CINC'] = predicted_NAs[:, 0]
        df.loc[missing_values.index, 'WINC'] = predicted_NAs[:, 1]
        return df

    def drop_na_fixations(self):
        df = self.dataframe.copy()
        index_to_drop = df.READMODE.isnull() | (df.READMODE == "_TOBEREPLACED_")
        set_is_last = []
        # in case the fixations before the last one also have wfreq < 0
        for i in df.index[index_to_drop & (df.ISLAST == 1)]:
            j = i - 1
            while pd.isnull(df.at[j, 'READMODE']) | (df.at[j, 'READMODE'] == '_TOBEREPLACED_'):
                j -= 1
            set_is_last.append(j)

        set_is_first = []
        for i in df.index[index_to_drop & (df.ISFIRST == 1)]:
            j = i + 1
            while pd.isnull(df.at[j, 'READMODE']) | (df.at[j, 'READMODE'] == '_TOBEREPLACED_'):
                j += 1
            set_is_first.append(j)

        df.at[set_is_last, 'ISLAST'] = 1
        df.at[set_is_first, 'ISFIRST'] = 1
        df = df[~index_to_drop]
        df = df.reset_index(drop=True)
        return df

    def _add_fixated_word_column(self):
        i = self.dataframe.index[self.dataframe['ISLAST'] == 1]
        i += 1
        i = np.insert(i, 0, 0)
        self.dataframe['WINC_CUMSUM'] = np.concatenate([np.cumsum(self.dataframe.WINC[i[x]:i[x+1]]) for x in xrange(0, len(i)-1)])
        # current fixated word
        cfw = np.array(self.dataframe.WINC_CUMSUM)
        cfw[self.dataframe['ISLAST'] == 1] = 0
        cfw = np.insert(cfw, 0, 0)
        cfw = cfw[0:-1]
        # self.dataframe['NEXT_FIXATED_WORD'] = [self.dataframe.TEXT_CONTENT[i].split(' ')[self.dataframe.WINC_CUMSUM[i]] for i in self.dataframe.index]
        self.dataframe['FIXATED_WORD'] = [self.dataframe.TEXT_CONTENT[x].split(' ')[cfw[x]] for x in self.dataframe.index]
        """
        cmax = [np.max(self.dataframe.WINC_CUMSUM[i[x]:i[x + 1]]) for x in xrange(0, len(i) - 1)]
        wmax = [len(self.dataframe.TEXT_CONTENT[i[x]].split(' ')) for x in xrange(0, len(i) - 1)]
        for x in xrange(0, len(cmax)):
            print 'ind:' + str(x) + ', cmax:' + str(cmax[x]) + ', wmax:' + str(wmax[x])
        self.dataframe[(self.dataframe.SUBJ == 21) & (self.dataframe.TEXT_NO == 50)].WINC
        from png_plot import PlotScanPath
        PlotScanPath('../share/data/HMM_feat_outfile_v6_165_166_viterbi_states.xls',
                     '../share/data/MaterielParagrapheGrisPNG-F', 21, 50)
        """

    def input_sequence(self, col_names="READMODE"):
        """initial probabilities getter."""
        if not self._input_sequence_getter_optimizer:
            self._input_sequence_getter_optimizer = True
            self._input_sequence = _MarkovianSequences(Sequences(self._dataframe_to_sequence(col_names)))
        return self._input_sequence

    def test_data_authentification(self):
        df = self.dataframe
        print('ISFIRST: ', (df.ISFIRST == 1).sum())
        print('ISLAST: ', (df.ISLAST == 1).sum())
        print('SUBJ_NAME/TEXT: ', df.groupby(['SUBJ_NAME', 'TEXT']).count().shape[0])
        assert (df.ISFIRST == 1).sum() == (df.ISLAST == 1).sum() == df.groupby(['SUBJ_NAME', 'TEXT']).count().shape[0]
