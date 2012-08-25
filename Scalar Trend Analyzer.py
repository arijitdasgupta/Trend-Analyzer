#Import modules
import math
import csv
import itertools
import sys
import getopt
import traceback
#Get the constants ready, such as resolutions, parameter columns, scalar columns
filename = 'Data.csv'
text_row = 0 
number_row = 2 
Reso = 10
norm_factor = 100 #Normalization factor
parameter_columns = []
scalar_columns = []

short_opts = 'f:t:n:p:s:r:'
long_opts = ['filename=', 'textrow=', 'numberrow=', 'parameter=', 'scalar=', 'resolution=']
arg_flag = [False for i in range(len(long_opts))]

parsed_options, remainder = getopt.getopt(sys.argv[1:], short_opts, long_opts)
try:
    for opt in parsed_options:
        if opt[0] in ('-f', '--filename'):
            filename = opt[1]
            arg_flag[0] = True
        if opt[0] in ('-t', '--textrow'):
            text_row = int(opt[1])
            arg_flag[1] = True
        if opt[0] in ('-n', '--numberrow'):
            number_row = int(opt[1])
            arg_flag[2] = True
        if opt[0] in ('-p', '--parameter'):
            parameter_columns.append(int(opt[1]))
            arg_flag[3] = True
        if opt[0] in ('-s', '--scalar'):
            scalar_columns.append(int(opt[1]))
            arg_flag[4] = True
        if opt[0] in ('-r', '--resolution'):
            Reso = int(opt[1])
            arg_flag[5] = True
    if False in arg_flag and arg_flag != [False for i in range(len(long_opts))]:
        print 'Arguments not entered correctly'
        raise BaseException
except:
    print 'Arguments entered wrong, please check'
    raw_input('Enter any key to continue')
    exit(0)

try:
    if parameter_columns == []:
        parameter_columns = [1, 2]#Parameter columnse
    if scalar_columns == []:
        scalar_columns = [3, 4] #Scalar columns

    data_file = open(filename, 'r')
    csv_read = csv.reader(data_file)
    parameter_fields = [] #Text field for parameters
    scalar_fields = [] #Text field for scalars
    parameters = [] #Parameters
    scalars = [] #Scalars
    for index, val in enumerate(csv_read):
        if index == text_row:
            for i, v in enumerate(val):
                if i in parameter_columns:
                    parameter_fields.append(v)
                elif i in scalar_columns:
                    scalar_fields.append(v)
        elif index >= number_row:
            param = []
            scale = []
            for i, v in enumerate(val):
                if i in parameter_columns:
                    param.append(float(v))
                elif i in scalar_columns:
                    scale.append(float(v))
            parameters.append(tuple(param))
            scalars.append(tuple(scale))
    data_file.close()
    #Reading of data file done!
    #Text fields parameter_fields, scalar_fields
    #data contained in parameters, scalars
    #Generate the point_matrix...
    #Point matrix
    #Calculate values for all the points in point matrix
    point_matrix = []
    dimensions = len(parameter_fields)
    divisors = [Reso**i for i in range(dimensions)]
    divisors.reverse()
    for i in range(Reso**dimensions):
        rem = i
        index = []
        for divisor in divisors:
            div = rem/divisor
            rem = rem % divisor
            index.append(div)
        point_matrix.append(tuple(index))
     
    #Normalize all the parameters except
    #Find the ranges
    ranges = []
    for i in range(len(parameter_fields)):
       mx = max([x[i] for x in parameters])
       mn = min([x[i] for x in parameters])
       ranges.append((mn, mx - mn))
    #ranges list format (minimum, difference)
    #Normalize all the parameters => parameters_norm with ranges = []
    norm_parameters = []
    for i in parameters:
        norm_parameters.append([])
        for f, val in enumerate(i):
            temp_val = ((val - ranges[f][0]) * norm_factor / ranges[f][1]) #Normalizing
            norm_parameters[-1].append(temp_val)
    #values are normalized
    #Add a Gaussian function distribution for N dimensions
    def gauss(mean, point, stanDev):
        temp = 0
        for i in range(len(mean)):
            temp += ((point[i] - mean[i]) ** 2)/(2*(stanDev**2))
        val = math.exp(-temp)
        return val
    #Add a distance function
    def dist(point1, point2):
        temp = 0
        for i in range(len(point1)):
            temp += (point1[i] - point2[i]) ** 2
        return temp ** 0.5
    #de-normalization function
    def denorm(point):
        temp_lst = []
        for index, val in enumerate(point):
            temp_val = (val * ranges[index][1])/norm_factor + ranges[index][0]
            temp_lst.append(temp_val)
        return tuple(temp_lst)
    #Calculate all the values for all the points for each scalar value fields
    stanDev = norm_factor/Reso
    minDev = norm_factor/Reso
    for scalar_value_index, scalar_field in enumerate(scalar_fields):
        print 'Working for', scalar_field
        point_values = []
        for point in point_matrix:
            val = 0
            r_point = [x * minDev for x in point]
            for point_index, mean in enumerate(norm_parameters):
                val += gauss(mean, r_point, stanDev) * scalars[point_index][scalar_value_index]
            point_values.append(val)
        #Sort the list after normalization
        point_max = max(point_values)
        point_values_norm = [(x * norm_factor) / point_max for x in point_values]
        vals = zip(point_matrix, point_values_norm)
        vals.sort(key = lambda x: x[1])
        op_filename = 'Prediction %s.csv'%(scalar_field)
        op_file = file(op_filename, 'w', True)
        #Write to a CSV file
        writer = csv.writer(op_file)
        writer.writerow(list(parameter_fields) + [scalar_field])
        for val in vals:
            near_flag = False
            other_point = [x * minDev for x in val[0]]
            for i in norm_parameters:
                if(dist(other_point,i) < 2 * minDev):
                    near_flag = True
            if not near_flag:
                writer.writerow(list(denorm(other_point)) + [val[1]])
        op_file.close()
except:
    traceback.print_exc(file = sys.stdout)
    print "Some problem occured, please check everything!"
    raw_input("Press enter to continue")
