#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import codecs
import six
import math


def dict2list(dic:dict):
	''' dict-->list '''
	keys = dic.keys()
	vals = dic.values()
	lst = [(key, val) for key, val in zip(keys, vals)]
	return lst


def naivebayes():
	diag_code = []
	with codecs.open('../data/diag-set.out', 'r', encoding='utf-8') as raw_input:
		for line in raw_input.readlines():
			line = line.strip()
			diag_code.append(line)


	for code in range(0, len(diag_code)):
		diag_patient = []
		non_patient = []
		symp_dict = {}
		non_symp_dict = {}
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

			# calculate the weight, use log
			m = float(v) / float(len(diag_patient))
			if k in non_symp_dict:
				n = float(non_symp_dict[k]) / float(len(non_patient))
			else:  # Laplace smoothing
				n = 1.0 / float(len(non_patient))
			m = math.log(m)
			n = math.log(n)
			weight[k] = m - n

		# sort weights descently
		weight = sorted(weight.items(), key=lambda e: e[1], reverse=True)

		diag_name = ''
		with codecs.open('../data/top-diags.csv', 'r', encoding='utf-8') as raw_input:
			for line in raw_input.readlines():
				line = line.strip()
				line = line.split('@')
				if line[0] == diag_code[code]:
					diag_name = line[1]
					break
		filename = '../data/diag-symp-nb/' + diag_code[code] + '.out'
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


naivebayes()
