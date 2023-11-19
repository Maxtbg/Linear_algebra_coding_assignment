def check_matrix_format(input_matrix): #function to check if a matrix is either square or singular, making it not invertible (edit: square check is redundant now as in the input the user is now only able to input square matrices, still leaving it in in case i might need it at some point)
    if len(input_matrix) != len(input_matrix[0]): #check if matrix is square
        print("Input Matrix is not square!", "\n")
    elif calculate_determinante(input_matrix) == 0: #check if matrix is singular by calculating the determinant
        print("This Matrix is singular!", "\n")
    else:
        return True # returns that the check passed


def take_user_input_matrix():
    rows = int(input("Please enter the number of rows in your desired matrix: ")) # the user has to say how big he wants his matrix to be
    columns = rows # as the matrix has to be square we can just say the rows are the same size as columns
    matrix = []
    print("Enter every value rowwise and then press enter: ")
    for i in range(rows):          # loop for row entries
        row_entries = []
        for j in range(columns):      # loop for column entries
             row_entries.append(int(input()))
        matrix.append(row_entries)
    return matrix


def take_user_input_vector(input_matrix): # function to take a users input and convert it to a vector, later used to solve  a system of equasions after these variables 
    rows = int(len(input_matrix)) # as the matrix is square we dont need to worry that we get the column numbers as the are the same size as the rows anyway
    vector = []
    print("Enter number values correspnding to the size of your matrix and then press enter: ")
    for i in range(rows):          # loop which iterates for the same length as the matrix
        try:
            vector.append(int(input())) #converts the entry to an integer and appends it to our vector
        except:
            raise ValueError
    return vector # gives out the vector
    

def create_identity_matrix(input_matrix): # function to create an identity matrix in size of the given square matrix
    identity_matrix = [] # creates an empty matrix

    number_columns = len(input_matrix[0]) #creates a number of the size of the amount of columns as it reads the length of the first lists (rows)
    number_rows = len(input_matrix) # #creates a number of the size of the amount of rows as it reads the length of whole list

    for i in range(number_rows): # loop that iterates over the number of rows
        row = []
        for j in range(number_columns): # loop that iterates over every single row
            if i == j: # when the column and row index is the same, it appends a 1 at that position
                row.append(1)
            else: # else it just appends a 0
                row.append(0)
        identity_matrix.append(row) # now appends the filled row to the final matrix
    
    return identity_matrix # returns the finished identity matrix 


def create_matrix(input_matrix, index): # function used in the calculation of the determinante, to create a new matrix, with deleting a certain column 
    if len(input_matrix) == 2: # if the input matrix's length is 2, we can just return the 2x2 matrix as the determinant is now easily calculated
        return input_matrix
    else:
        new_matrix = [] # creates an empty new matrix
        for row in input_matrix[1:]: # iterates over the matrix's length without the first row , as it starts reading from index 1
            new_row = row[:index] + row[index + 1:] # creates a new row completely the same with all values from before, but now without a certain value 
            new_matrix.append(new_row) # appends this new row to the matrix
        return new_matrix # returns the new matrix without the first row and a certain index


def calculate_determinante(input_matrix): # function to calculate determinante
# https://amalrkrishna596.medium.com/determinant-of-a-matrix-without-numpy-653aac58c121
    if len(input_matrix) == 2: # formula to simnply calculate determinante as it only is a 2x2 matrix
        return (input_matrix[0][0] * input_matrix[1][1]) - (input_matrix[1][0] * input_matrix[0][1]) # returns determinante after simple calculation
    elif len(input_matrix) == 1: # returns determinantes input from a 1x1 matrix
        return input_matrix[0][0]

    else: # calculates determinante in every other case
        determinante = 0 # creates a variable for the determinante
        for i in range(len(input_matrix[0])): # iterates over the length of the matrix's columns 
            determinante += ((-1)**i)*input_matrix[0][i]*calculate_determinante(create_matrix(input_matrix, i)) # recursively calculates the determinante by adding it on top of the result from before. (further comments next line)
# (-1) to the power of i is to ensure that the current value is to be added or substracted, input_matrix[0][i] ensures that every column values "submatrices until 2x2" are properly calculated, then recall function to split the matrix further down
    return determinante # returns determinante for singularity checks


def gaussian_elemination(input_matrix, identity_matrix): #Concept used by: https://steemit.com/hive-181430/@sheham-sh/siz-tutorial-or-or-gauss-jordan-method-in-python-without-numpy-or-or-20-to-siz-official-or-or-by-sheham-sh

    if check_matrix_format(input_matrix): #checks the matrix's format

        number_columns = len(input_matrix[0]) # gets the matrix's columns
        number_rows = len(input_matrix) # gets the matrix's rows

        # comment from later in the program development, the differencation betwenn row and column size is redundant now, also still leaving it in the program in case that i might need it at some point again

        for column in range(number_columns): # iterates through the matrix's columns

            pivot_element = input_matrix[column][column] # gets the pivot element

            for i in range(number_columns): # iterates over the matrix's column values
                input_matrix[column][i] /= pivot_element # makes the columns diagonal values to 1
                identity_matrix[column][i] /= pivot_element # does the same operation with the pivot with the identity matrix to transform it

            for row in range(number_rows): # iterates amount of number of rows times 
                if row != column: # check that we don't manipulate valies on the diagonal
                    scalar = input_matrix[row][column] # reads the scalar in every other position
                    for j in range(number_columns): # and now changes the values depending on the scalar before, to eleminate them and to perform the same operation on the identity matrix, this and the next two lines written with the help from chatgpt
                        input_matrix[row][j] -= scalar * input_matrix[column][j] # eleminates the value
                        identity_matrix[row][j] -= scalar * identity_matrix[column][j] # does the same with the identyty matrix and thereby creating the inverse
        return identity_matrix # returns the inverted matrix
    

def row_calculation(input_listA, input_listB): # calculates the values when one multiplies one row with a column
    result = 0
    for index, entry in enumerate(input_listA):
        result += entry*input_listB[index] # adds up all the multiplied values from the lists
    return result # returns the result


def solve_system_of_equasion(input_matrix, input_vector): # just a function to perform the solution of the system of equasions with before given values

    A = gaussian_elemination(input_matrix, create_identity_matrix(input_matrix)) # gives the inversed matrix
    x = [] # empty list for later results
    local_result = 0 

    for index, row in enumerate(A): # iterates over every row in the left matrix
         local_result = row_calculation(row, input_vector) # the result now is the result of the calculation from the row with the column
         x.append(round(local_result, 5)) # ads the result to the list

    
    return x


def print_matrix(input_matrix): # functiuon to beautiful print matrices
    for row in input_matrix:
        print(row)
    print("\n")


def print_equation_solutions(input_matrix):
    for index, entry in enumerate(input_matrix):
        print(f' x{index + 1} = {entry}\n ')


test_matrices = [  # Bottom 5 invertible, Top 5 singular!
    

    [[1, 2, 3, 4], 
     [0, 0, 0, 0], 
     [1, 2, 3, 4], 
     [2, 4, 6, 8]],


    [[1, 2, 3, 4, 5], 
     [2, 4, 6, 8, 10], 
     [3, 6, 9, 12, 15], 
     [4, 8, 12, 16, 20], 
     [5, 10, 15, 20, 25]],


    [[1, 2], 
     [2, 4]],


    [[1, 2, 3], 
     [4, 5, 6], 
     [7, 8, 9]],


    [[1, 2, 3, 4, 5, 6], 
     [0, 0, 0, 0, 0, 0], 
     [1, 2, 3, 4, 5, 6], 
     [2, 4, 6, 8, 10, 12], 
     [3, 6, 9, 12, 15, 18], 
     [4, 8, 12, 16, 20, 24]],


    [[1, 2], 
     [3, 4]],


    [[1, 2, 3], 
     [0, 1, 4], 
     [5, 6, 0]],


    [[1, 2, 3, 4], 
     [0, 1, 0, 4], 
     [0, 0, 1, 0], 
     [0, 0, 0, 1]],


    [[1, 2, 0, 0, 0], 
     [0, 1, 2, 0, 0], 
     [0, 0, 1, 3, 0], 
     [0, 0, 0, 1, 4], 
     [0, 0, 0, 0, 1]],


    [[1, 2, 0, 0, 0, 0], 
     [0, 1, 2, 0, 0, 0], 
     [0, 0, 1, 3, 0, 0], 
     [0, 0, 0, 1, 4, 0], 
     [0, 0, 0, 0, 1, 5], 
     [0, 0, 0, 0, 0, 1]]

    ]


task_2_A = [[1, -3, -7], [-1, 5, 6], [-1, 3, 10]]

task_2_b = [10,-21,-7]

task_3 = [[1,2,3], [0,1,4],[5,6,0]]


def main():
    
    program_shutdown = False
    while program_shutdown == False:
        user_input = str(input("Press 1 if you want to get the inverse of a matrix, 2 if you want to solve a system of equasions, 3 if you want to run the test matrices, 4 if you want to see the midtermsheet's solutions or 5 if you want to end the program: "))
        if user_input == "1":
            user_matrix = take_user_input_matrix()
            print_matrix(gaussian_elemination(user_matrix, create_identity_matrix(user_matrix)))

        elif user_input == "2":
            user_matrix = take_user_input_matrix()
            user_vector = take_user_input_vector(user_matrix)
            print_equation_solutions(solve_system_of_equasion(user_matrix, user_vector))

        elif user_input == "3":
            for matrix in test_matrices:
                try:
                    print_matrix(gaussian_elemination(matrix, create_identity_matrix(matrix)))
                except:
                    pass

        elif user_input == "4":
            print("Task 2: ")
            print_equation_solutions(solve_system_of_equasion(task_2_A, task_2_b))
            print("Task 3: ")
            print_matrix(gaussian_elemination(task_3, create_identity_matrix(task_3)))
        elif user_input == "5":
            program_shutdown = True
        else:
            pass


main()
