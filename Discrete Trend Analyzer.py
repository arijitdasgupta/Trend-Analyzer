#Parsing from the CSV data file
#and
#getting regions and points from a multivariate data set
#Author: Arijit Dasgupta
import sys
import getopt

filename = 'Data.csv'
text_row = 0
data_row_starts = 2
useful_columns_int = []
useful_columns_discrete = []
flag, flag1 = False, False
axis_div = 10

options = 'f:t:n:u:d:r:'
long_options = ['filename=','textrow=','numberrow=','ucolumn=','ducolumn=','reso=']

check_list = [('-f', '--filename'),('-t', '--textrow'),('-n', '--numberrow'),('-u', '--ucolumn'),('-d', '--ducolumn'),('-r','--reso')]
check_flags = [False for i in range(len(check_list))]
with_arg = False

try:
    arguments, remainder = getopt.getopt(sys.argv[1:],options,long_options)
    args = [x[0] for x in arguments]
    for i in args:
        for check_i,check in enumerate(check_list):
            if i in check:
                check_flags[check_i] = True
    if False in check_flags and check_flags != [False for i in range(len(check_list))]:
        raise Exception
    else:
        with_arg = True
except:
    print "You got the arguments wrong or incomplete!"
    raw_input('Press enter to continue!')
    exit()

for opt, val in arguments:
    if opt in ('-f', '--filename'):
        filename = val
    elif opt in ('-t', '--textrow'):
        text_row = int(val)
    elif opt in ('-n', '--numberrow'):
        data_row_starts = int(val)
    elif opt in ('-r', '--reso'):
        axis_div = int(val)
    elif opt in ('-u', '--ucolumn'):
        useful_columns_int.append(int(val))
        flag = True
    elif opt in ('-d', '--ducolumn'):
        useful_columns_discrete.append(int(val))
        flag1 = True
 
if not flag:
    useful_columns_int = [1,2,3,4]
if not flag1:
    useful_columns_discrete = [6]

norm_factor = 100

try:
    from numpy import std, mean
    from math import exp
    import csv
    import traceback
    from matplotlib import pyplot as plot
    import itertools

    ip_file = open(filename,'r')
    read_lines = csv.reader(ip_file)
    
    text_fields = []
    text_fields_discrete = []
    data = []
    discrete_data = []
        
    lines = []
    for i, vect in enumerate(read_lines):
        if i == text_row:
            text_row_line = vect
        elif i >= data_row_starts:
            lines.append(vect)

    for counter,i in enumerate(text_row_line):
        if counter in useful_columns_int:
            text_fields.append(i)
        elif counter in useful_columns_discrete:
            text_fields_discrete.append(i)
        counter = counter + 1
        
    print 'Fields/dimensions',text_fields
    print 'Discrete fields',text_fields_discrete
    
    for i in lines:
        data.append([])
        discrete_data.append([])
        for j, val in enumerate(i):
            if j in useful_columns_int:
                data[-1].append(float(val))
            elif j in useful_columns_discrete:
                discrete_data[-1].append(val)
    
    #Classification and quantification of discrete data
    discrete_list = []
    for i in range(len(discrete_data[0])):
        temp_list = [x[i] for x in discrete_data]
        discrete_list.append(temp_list)
    
    discrete_points = []
    for points in discrete_list:
        discrete_points.append([])
        for i in points:
            if i not in discrete_points[-1]:
                discrete_points[-1].append(i)
    
    discrete_points_numeric = []
    for points in discrete_points:
        discrete_points_numeric.append({})
        for i, val in enumerate(points):
            discrete_points_numeric[-1][val] = i + 1
    
    print 'Discrete data points',discrete_points_numeric
    
    discrete_data_numeric = []
    for a_point in discrete_data:
        discrete_data_numeric.append([])
        for i, pt in enumerate(a_point):
            discrete_data_numeric[-1].append(discrete_points_numeric[i][pt])
            
    data_final = []
    for x, y in zip(data, discrete_data_numeric):
        data_final.append(x + y)
    
    #Writing up the parsed data
    op_file = open('parsed_text.csv', 'w', True)
    csv_writer = csv.writer(op_file)
    for i in data_final:
        csv_writer.writerow(i)
    op_file.close()
        
    data_len = len(data_final[0])
    del data, data_final #Deleting previous resources
    
    #opening parsed data file
    ip_file = open('parsed_text.csv','r')
    data = []
    parameters = []
    for i in range(len(useful_columns_discrete)):
        parameters.append(data_len - i - 1)
    
    #Parsing all the data from the file
    csv_reader = csv.reader(ip_file)
    for i in csv_reader:
        params = []
        ips = []
        for index, val in enumerate(i):
            if index not in parameters:
                ips.append(float(val))
            else:
                params.append(int(val))
        data.append([tuple(ips),tuple(params)])
    #Data parsing done
    
    print "Data parsed!"
    
    #Normalizing the data field
    ranges = []
    for i in range(len(data[0][0])):
        x = [pt[0][i] for pt in data]
        mx = max(x)
        mn = min(x)
        rn = mx - mn
        ranges.append((rn, mn))
    
    print 'Value ranges are',ranges
    
    norm_data = []
    for i in data:
        norm_data.append([])
        x = []
        for index, val in enumerate(i[0]):
            x.append(((val - ranges[index][1])/ranges[index][0]) * norm_factor)
        norm_data[-1].append(tuple(x))
        norm_data[-1].append(i[1])
        
    print "Data normalized in the scale of 0 ->", norm_factor
    
    n_param = len(data[0][1])
    n_ips = len(data[0][0])
    
    #function to find distances
    def dist(pt1, pt2):
        temp_sum = 0
        for i in range(len(pt1)):
            temp_sum = temp_sum + (pt1[i] - pt2[i]) ** 2
        temp_sum = temp_sum ** 0.5
        return temp_sum
    
    def index_finder(i):
        location_coord = []
        rem = i
        for divisor in divisors:
            div = rem / divisor
            rem = rem % divisor
            location_coord.append(div)
        return tuple(location_coord)
    
    def index_definder(vector):
        temp = 0
        for i, val in enumerate(vector):
            temp += divisors[i] * val
        return temp
    
    point_matrix = []
    axis_len = norm_factor
    dimensions = len(norm_data[0][0])
    n_elements = axis_div ** dimensions
    divisors = [(n_elements/(axis_div**(i + 1))) for i in range(dimensions)]
    print 'We will be treatin ',n_elements,'points'
    for i in range(n_elements):
        point_matrix.append([((x * axis_len)/axis_div) for x in index_finder(i)])
    print 'Creation of point_matrix done'
    
    def gauss(point, mean, standard_deviation):
        exponent = 0
        for i, value in enumerate(mean):
            exponent += float((point[i] - mean[i])**2)/(2 * (standard_deviation ** 2))
        return exp(-exponent)
        
    def denorm(point):
        temp_point = []
        for i, val in enumerate(point):
            val = (ranges[i][0] * val)/norm_factor + ranges[i][1]
            temp_point.append(val)
        return temp_point
    
    def discrete_denorm(index, key):
        temp_dic = discrete_points_numeric[index]
        for i in temp_dic:
            if(temp_dic[i] == key):
                return i
            
    #Generating adjacence combinations
    adjacent_index = []
    combis = 3 ** dimensions
    numbs = [-1, 0, 1]
    divs = [(combis/(3**(i + 1))) for i in range(dimensions)]
    for i in range(combis):
        one_index = []
        rem = i
        for div_i in divs:
            div = rem / div_i
            rem = rem % div_i
            one_index.append(numbs[div])
        adjacent_index.append(one_index)
    
    n_points = len(norm_data)
    #Calculating values for each field property
    stan_dev = axis_len/axis_div
    for index, val in enumerate(text_fields_discrete):
        point_values = []
        print "Working for ",val
        invalid_index = []
        valid_points = []
        valid_point_index = []
        point_matrix_index = []
        discrete_numbers = []
        for point_index, point in enumerate(point_matrix):
            averaging_dic = {}
            point_matrix_index.append(index_finder(point_index))
            for data_point in norm_data:
                if data_point[1][index] not in discrete_numbers:
                    discrete_numbers.append(data_point[1][index])
                prob_val = gauss(point, data_point[0], stan_dev) * (axis_len - dist(point, data_point[0]))
                compare_str = str(data_point[1][index])
                if compare_str not in averaging_dic.keys():
                    averaging_dic[compare_str] = prob_val
                else:
                    averaging_dic[compare_str] += prob_val
            for key in averaging_dic:
                averaging_dic[key] /= n_points
            max_val = max(averaging_dic.values())
            max_key = None
            for key in averaging_dic:
                if averaging_dic[key] == max_val:
                    max_key = int(key)
            point_values.append(max_key)
            for data_pt in norm_data:
                if data_pt[1][index] == max_key and dist(data_pt[0], point) < (stan_dev * 2):
                    invalid_index.append(point_index)
        for point_index, point in enumerate(point_matrix):
            if point_index not in invalid_index:
                valid_points.append([denorm(point), point_values[point_index]])
                valid_point_index.append(point_matrix_index[point_index])
        for i in discrete_numbers:
            filename = val + ' ' + discrete_denorm(index, i) + '.csv'
            print "Writing",filename
            prospective_file = open(filename, 'w', True)
            csv_writer = csv.writer(prospective_file)
            csv_writer.writerow(text_fields + [val])
            for x in valid_points:
                if x[1] == i:
                    csv_writer.writerow(x[0] + [discrete_denorm(index, i)])
            prospective_file.close()
        checked_point_index = []
        interesting_points = []
        for index_value in valid_point_index:
            value_here = point_values[index_definder(index_value)]
            for adj in adjacent_index:
                test_index = []
                for i, vect_comp in enumerate(adj):
                    temp_i = index_value[i] + vect_comp
                    if temp_i >= 0 and temp_i < axis_div:
                        test_index.append(temp_i)
                    else:
                        test_index.append(0)
                temp_index = index_definder(test_index)
                interesting_flag = False
                if(point_values[temp_index] != value_here) and (temp_index not in checked_point_index):
                    interesting_flag = True
            if interesting_flag:
                interesting_points.append([denorm(point_matrix[index_definder(index_value)]),value_here])
            checked_point_index.append(index_definder(index_value))
        print "Almost done!"
        interesting_points.sort(key = lambda x: x[1])
        interesting_point_file = open('Interesting points ' + val + '.csv','w',True)
        print 'Writing interesting points for', val
        csv_writer = csv.writer(interesting_point_file)
        csv_writer.writerow(text_fields + [text_fields_discrete[index]])
        for i in interesting_points:
            csv_writer.writerow(i[0] + [discrete_denorm(index, i[1])])
        interesting_point_file.close()
        print "The program found",len(interesting_points),'interesting points'
        print "Plotting all the combinations of parameters"
        #Plot start with all the possible combinations
        for combi in itertools.combinations(text_fields, 2):
            index0, index1 = text_fields.index(combi[0]), text_fields.index(combi[1])
            plot.autoscale(tight = True)
            X = [denorm(i)[index0] for i in point_matrix]
            Y = [denorm(i)[index1] for i in point_matrix]
            col = [i for i in point_values]
            plot.scatter(X, Y, c = col, vmin = 0, vmax = len(discrete_numbers))
            #TODO: set a legend for the plot with discrete_denorm
            #TODO: Set x_label as text_fields[index0] and set y_label as text_fields[index1]
            #Each graph file name with axis and morphology
            file_name_string = 'Plot %s %s %s.png'%(val, text_fields[index0], text_fields[index1])
            plot.savefig(file_name_string)
            plot.clf()
        #Plot end
    if not with_arg:
        raw_input("Press enter to continue!")
except:
    print traceback.print_exc(file=sys.stdout)
    print 'Problem occured, please check you inputs!'
    raw_input("Press enter to continue!")
