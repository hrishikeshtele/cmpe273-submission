import os
import glob
import sys
import heapq

# Merge sort
def sort(arr):
    if len(arr) > 1:
        left_array = arr[: len(arr) // 2]
        right_array = arr[len(arr) // 2 :]

        sort(left_array)
        sort(right_array)

        l_index = 0  # left array index
        r_index = 0  # right array index
        arr_index = 0  # final array index

        while l_index < len(left_array) and r_index < len(right_array):
            if left_array[l_index] < right_array[r_index]:
                arr[arr_index] = left_array[l_index]
                l_index += 1
                arr_index += 1
            else:
                arr[arr_index] = right_array[r_index]
                r_index += 1
                arr_index += 1
        while l_index < len(left_array):
            arr[arr_index] = left_array[l_index]
            l_index += 1
            arr_index += 1
        while r_index < len(right_array):
            arr[arr_index] = right_array[r_index]
            r_index += 1
            arr_index += 1


class Node:
    def __init__(self, data, file):
        self.data = data
        self.file = file

    def __lt__(self, other):
        return self.data < other.data


class Driver:
    def __init__(self):
        self.tempFiles = []

    # Read input files
    def readFiles(self):
        # list of input file names
        for input_file in glob.glob("input/unsorted_*.txt"):
            # check if file is of type txt format
            if input_file.endswith(".txt"):
                arr = self.readListFromFile(input_file)
                sort(arr)
                self.writeFile(arr, "".join([i for i in input_file if i.isdigit()]))

    # Read list from file
    def readListFromFile(self, file_name):
        arr = []
        with open(file_name) as f:
            elements = f.readlines()
            for element in elements:
                if element != "":
                    arr.append(int(element))
        return arr

    # Write list to the file
    def writeFile(self, arr, file_number):
        filename = "./output/sorted_" + file_number + ".txt"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        file = open(glob.glob("output/")[0] + "sorted_" + file_number + ".txt", "w+")
        file.write("\n".join(str(data) for data in arr))
        file.seek(0)
        self.tempFiles.append(file)

    # Merge sorted files
    def mergeSortedTempFiles(self):
        init_list = []

        # Each Element from temp files
        for tempFile in self.tempFiles:
            data = int(tempFile.readline().strip())
            init_list.append(Node(data, tempFile))
        # Create file to store final sorted array
        sorted_file = open(glob.glob("output/")[0] + "sorted.txt", "w")

        # Heapify the list to access minimum element in O(1) time complexity
        heapq.heapify(init_list)

        cnt = 0
        temp = []
        while True:
            min_heap_node = heapq.heappop(init_list)

            # Check if heap is empty
            if min_heap_node.data == sys.maxsize:
                break
            cnt += 1
            temp.append(min_heap_node.data)

            # Write data to final sorted file in chunks of 100 elements
            if cnt == 100:
                with open(glob.glob("output/sorted.txt")[0], "a") as f:
                    f.write("\n".join(str(data) for data in temp))
                    f.write("\n")
                cnt = 0
                temp = []
            # Increment file pointer to access next element
            filePointer = min_heap_node.file
            data = filePointer.readline().strip()

            # Set data to max size which will be used to break out of loop
            if not data:
                data = sys.maxsize
            else:
                data = int(data)
            heapq.heappush(init_list, Node(data, filePointer))
        # Close files
        sorted_file.close()
        for temp in self.tempFiles:
            temp.close()

    # Remove temp files from the system
    def removeTempFiles(self):
        for temp_file in glob.glob("output/sorted_*.txt"):
            os.remove(temp_file)


if __name__ == "__main__":

    driver = Driver()

    driver.readFiles()

    driver.mergeSortedTempFiles()

    driver.removeTempFiles()