import csv

#Handle Data: 
def loadCsv(filename):
	with open('Address Book.csv', 'r') as f:
    	lines = csv.reader(f)
		dataset = list(lines)
	for i in range(len(dataset)):
		dataset[i] = [float(x) for x in dataset[i]]
	return dataset
filename = 'data.csv'
dataset = loadCsv(filename)
print('Loaded data file {0} with {1} rows').format(filename, len(dataset))