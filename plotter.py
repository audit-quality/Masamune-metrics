import matplotlib.pyplot as plt
import argparse
import csv

def parse_args():
	parser = argparse.ArgumentParser(description="sothis plotting tool: visualize blockchain data the easy way")
	parser.add_argument("-i", "--input_file",
						help="CSV input file", default="results.csv")
	# parser.add_argument("-d", "--debug", action="store_true",
	# 					help="Print parsed x and y values")
	return parser.parse_args()

# def debug(debug_mode: bool, print_msg: str):
# 	if(debug_mode):
# 		print(print_msg)

def plot_data(csv_file: str):
	all_data = []
	with open(csv_file, newline='') as csvfile:
		csv_data = csv.reader(csvfile, delimiter=',')
		for row in csv_data:
			all_data.append(row)
	
	audit_names = []
	crits = []
	highs = []
	total = []
	crits_avg = []
	highs_avg = []
	lows_avg = []
	infos_avg = []
	total_avg = []
	for i in range(len(all_data)):
		if i == 0:
			continue
		audit_names.append(all_data[i][0])
		crits.append(float(all_data[i][1]))
		highs.append(float(all_data[i][1]))
		total.append(float(all_data[i][9]))
		crits_avg.append(float(all_data[i][12]))
		highs_avg.append(float(all_data[i][13]))
		lows_avg.append(float(all_data[i][15]))
		infos_avg.append(float(all_data[i][17]))
		total_avg.append(float(all_data[i][20]))

	# Plot the data

	# Plot overall total
	plt.subplot(231)
	plt.bar(audit_names, total)
	plt.ylabel('Findings')
	plt.title('Total Findings')
	# Plot average crits
	plt.subplot(232)
	plt.bar(audit_names, crits_avg)
	plt.ylabel('Average Criticals')
	plt.title('Average Critical Findings Per Report')
	# Plot average highs
	plt.subplot(233)
	plt.bar(audit_names, highs_avg)
	plt.ylabel('Average Highs')
	plt.title('Average High Findings Per Report')
	# Plot average low findings
	plt.subplot(234)
	plt.bar(audit_names, lows_avg)
	plt.ylabel('Average Lows')
	plt.title('Average Low Findings Per Report')
	# Plot average info findings
	plt.subplot(235)
	plt.bar(audit_names, infos_avg)
	plt.ylabel('Average Infos')
	plt.title('Average Info Findings Per Report')
	# Plot average total findings
	plt.subplot(236)
	plt.bar(audit_names, total_avg)
	plt.ylabel('Average Findings')
	plt.title('Average Total Findings Per Report')
	plt.show()

if __name__ == "__main__":

	# Parse input arguments
	args = parse_args()
	plot_data(args.input_file)
