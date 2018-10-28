#!/usr/bin/env python
# coding=utf-8
import codecs
import six


def noisyormodel():
	diag_code = []

	with codecs.open('../data/diag-set.out', 'r', encoding='utf-8') as raw_input:
		for line in raw_input.readlines():
			line = line.strip()
			diag_code.append(line)

	for code in range(0, len(diag_code)):
		diag_patient = []
		non_patient = []
		non_symp_dict = {}
		symp_dict = {}
		with codecs.open('../data/a-diag.out', 'r', encoding='utf-8') as raw_input:
			for line in raw_input.readlines():
				line = line.strip()
				text = line.split('@')
				if text[0] == diag_code[code]:
					diag_patient.append(text[1])

		with codecs.open('../data/patient-set.out', 'r', encoding='utf-8') as raw_input:
			for line in raw_input.readlines():
				line = line.strip()
				if line not in diag_patient:
					non_patient.append(line)

		with codecs.open('../data/b-symp1.out', 'r', encoding='utf-8') as raw_input:
			for line in raw_input.readlines():
				line = line.strip()
				text = line.split('@')
				if text[1] in diag_patient:
					if text[0] not in symp_dict:
						symp_dict[text[0]] = 1
					else:
						symp_dict[text[0]] = symp_dict[text[0]] + 1
				elif text[1] in non_patient:
					if text[0] not in non_symp_dict:
						non_symp_dict[text[0]] = 1
					else:
						non_symp_dict[text[0]] = non_symp_dict[text[0]] + 1

		# sorted(dict2list(symp_dict), key=lambda x: x[1], reverse=True)
		symp_dict = sorted(symp_dict.items(), key=lambda e: e[1], reverse=True)

		weight = {}
		for k, v in symp_dict:
			if v < 5:
				break

			# calculate the weight
			m = float(len(diag_patient) - v) / float(len(diag_patient))
			if k in non_symp_dict:
				if len(non_patient) - non_symp_dict[k] != 0:
					n = float(len(non_patient) - non_symp_dict[k]) / float(len(non_patient))
				else:  # laplace smoothing
					n = 1.0 / float(len(non_patient))
			else:
				n = 1.0
			weight[k] = m / n
			weight[k] = 1 - weight[k]

		# sort the weughts descently
		weight = sorted(weight.items(), key=lambda e: e[1], reverse=True)

		diag_name = ''
		with codecs.open('../data/top-diags.csv', 'r', encoding='utf-8') as raw_input:
			for line in raw_input.readlines():
				line = line.strip()
				line = line.split('@')
				if line[0] == diag_code[code]:
					diag_name = line[1]
					break
		filename = '../data/diag-symp-noisyor/' + diag_code[code] + '.out'
		if six.PY3:
			output = open(filename, 'w', encoding='utf-8')
		output = codecs.open(filename, 'w', encoding='utf-8')
		output.write('Desease | Symptom | Weight')
		output.write('\n')
		for k, v in weight:
			output.write(diag_code[code] + ':' + diag_name)
			output.write(' | ')
			output.write(k)
			output.write(' | ')
			output.write(str(v))
			output.write('\n')
	output.close()


noisyormodel()
