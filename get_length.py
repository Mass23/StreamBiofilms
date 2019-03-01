import glob
import os
from Bio import SeqIO
import pandas as pd
import matplotlib.pyplot as plt
from multiprocessing import Pool

n_cores = 24
data_inputs = glob.glob('*')
data_inputs = [i for i in data_inputs if os.path.isdir(i) == True]

def ProcessProject(project):
    samples_list = glob.glob(project + '/*')

    with open(project + '/' + project + '_stats.tsv', 'w') as out:
        out.write('SampleID\tSequenceID\tLength\n')

        for sample in samples_list:
            sample_name = sample.split('/')[-1]

            with open(project + '/' + sample_name + '/' + sample_name + '.fna') as fasta:
                for record in SeqIO.parse(fasta, "fasta"):
                    sequence_name = record.id.split(' ')[0].replace('>','')

                    out.write('\t'.join([sample_name, sequence_name, str(len(record.seq))]) + '\n')

    with open(project + '/' + project + '_stats.tsv') as file:
        col_names = ['SampleID', 'SequenceID', 'Length']
        data = pd.read_csv(file, sep='\t', header=1, names = col_names, na_values = 'NA', dtype={'SampleID': str, 'SequenceID': str, 'Length': int})

        plt.figure()
        plt.hist(data['Length'])
        plt.savefig(project + '/' + project + '_Length.png')
        plt.close()

        print('Project: ', project, ' done!')

pool = Pool(n_cores)
pool.map(ProcessProject, data_inputs)
pool.close()
pool.join()
