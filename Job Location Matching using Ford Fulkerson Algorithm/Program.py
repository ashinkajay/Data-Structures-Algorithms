import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import *
import tkinter.filedialog

class Graph:
    def __init__(self, graph):
        # residual graph
        self.graph = graph
        self.applicants = len(graph[:, 0])
        self.locations = len(graph[0, :])

    # A DFS based recursive function that returns true if a matching for vertex u is possible
    def searchMatch(self, u, matchings, visited):

        # Try every location one by one
        for v in range(self.locations):

            # If applicant u is interested in location v and v is not visited
            if self.graph[u, v] and visited[v] == False:

                # Mark v as visited
                visited[v] = True

                # If location 'v' is not assigned to an applicant OR previously assigned applicant for location v has an alternate location available.
                if matchings[v] == -1 or self.searchMatch(matchings[v], matchings, visited):
                    matchings[v] = u
                    return True
        return False

    # Returns maximum number of matching
    def maximumBipartiteMatching(self):

        # The value of matchings[i] is the applicant number assigned to location i, the value -1 indicates nobody is assigned.
        matchings = [-1] * self.locations

        # Number of applicants got allocated.
        result = 0

        for i in range(self.applicants):

            # Mark all locations as not visited for next applicant.
            visited = [False] * self.locations

            # Find if the applicant 'u' can get a location
            if self.searchMatch(i, matchings, visited):
                result += 1
        return (matchings, result)


def Jobmatching():

    # Duplicate of dataframe df to hold actual data.
    global df1
    #pd.set_option("display.max_rows", 11, "display.max_columns", None)
    df = pd.read_csv(filename)
    df1 = pd.read_csv(filename)

    applicants = list(df['Applicants'])
    applicants.sort()
    applicants = list(df1['Applicants'])
    applicants.sort()

    # Finding unique locations
    locations = set()
    locations.update(set(df['Location preference 1']))
    locations.update(set(df['Location preference 2']))
    locations.update(set(df['Location preference 3']))
    locations.update(set(df['Location preference 4']))
    locations.update(set(df['Location preference 5']))
    locations.update(set(df1['Location preference 1']))
    locations.update(set(df1['Location preference 2']))
    locations.update(set(df1['Location preference 3']))
    locations.update(set(df1['Location preference 4']))
    locations.update(set(df1['Location preference 5']))
    locations = list(locations)
    locations.sort()

    # Converting the Applicants and Location data into integer values.
    for i in range(len(applicants)):
        df["Applicants"] = df["Applicants"].replace(to_replace=applicants[i], value=i)

    for i in range(len(locations)):
        df["Location preference 1"] = df["Location preference 1"].replace(to_replace=locations[i], value=i)
        df["Location preference 2"] = df["Location preference 2"].replace(to_replace=locations[i], value=i)
        df["Location preference 3"] = df["Location preference 3"].replace(to_replace=locations[i], value=i)
        df["Location preference 4"] = df["Location preference 4"].replace(to_replace=locations[i], value=i)
        df["Location preference 5"] = df["Location preference 5"].replace(to_replace=locations[i], value=i)

    data = df.to_numpy()
    graph = np.zeros((len(applicants), len(locations)), dtype=int)
    #print("Converted to numpy array")
    #print(data)

    for i in range(len(applicants)):
        for j in range(1, 6):
            graph[i, data[i, j]] = 1
    # print("\nConverted to graph")
    # print(graph)

    g = Graph(graph)
    (matchings, result) = g.maximumBipartiteMatching()

    # Converting integers to text values.
    data = {'Applicant': matchings, 'Location': list(range(len(matchings)))}
    global dfMatchings
    dfMatchings = pd.DataFrame(data)
    for i in dfMatchings['Applicant']:
        dfMatchings["Applicant"] = dfMatchings["Applicant"].replace(to_replace=i, value=applicants[i])
    for i in dfMatchings['Location']:
        dfMatchings["Location"] = dfMatchings["Location"].replace(to_replace=i, value=locations[i])
    dfMatchings = dfMatchings.sort_values(by='Applicant')

    print(df1.head())
    print(dfMatchings.head())
    #dfMatchings.to_csv("output.csv")
    return result

def upload_file():
    # Getting the uploaded file path into filename.
    global filename
    f_types = [('CSV Files', '*.csv')]
    filename = tk.filedialog.askopenfilename(filetypes=f_types)
    res = ''
    res = Jobmatching()
    # Displaying the max number of matchings
    label2.config(text=f"Maximum number of applicants that got preferred location:{res}")


def applicant_details():

    #Fetching the text from Entry to Applicant_name variable
    Applicant_Name = E1.get()
    print(Applicant_Name)
    index_value = int(df1[df1['Applicants'] == Applicant_Name].index.values)
    # print(index_value)
    list_location = []
    list_location_1 = []
    # Fetching the applicant details from the data frame df1 to get the preferred locations
    for i in range(5):
        list_location.append(df1.iat[index_value, i + 1])
    print(list_location)
    pref = ','.join(list_location)
    # Fetching the applicant details from the data frame dfmatchings to get the allocated location
    for i in range(2):
        list_location_1.append(dfMatchings.iat[index_value, i])
    print(list_location_1)
    alloc = ' is '.join(list_location_1)
    label4.config(text=f"Preferred Locations:{pref}")
    label5.config(text=f"The Allocated Location of {alloc}")


#Creating a Window for user interface
root = Tk()
root.state('zoomed')
root.title('Job Applicant and Location Mapping')
scr_width = root.winfo_screenwidth()
scr_height = root.winfo_screenheight()
root.geometry(f"{scr_width}x{scr_height}+0+0")

#Creating frames
frame = tk.Frame(root, width=scr_width, height=scr_height, pady=50)
frame.pack(expand=YES, fill=BOTH)

frame1 = tk.Frame(root, width=scr_width, height=scr_height, )
frame1.pack(expand=YES, fill=BOTH)

frame2 = tk.Frame(root, width=scr_width, height=scr_height)
frame2.pack(expand=YES, fill=BOTH)

#Creating the labels
heading = tk.Label(frame,
                   text='Job Applicants and Location Mapping',
                   font=("Arial Bold", 20),
                   foreground="White",
                   background="Black",
                   width=50,
                   height=3)
heading.pack()

label1 = tk.Label(frame, text="Upload the Data file consisting of job applicants and their preferred locations:",
                  font=70)
B1 = tk.Button(frame,
               text='Click here to upload file!',
               font=70,
               width=20,
               foreground="White",
               background="Blue",
               command=lambda: upload_file())
label1.pack()
B1.pack()

label2 = tk.Label(frame,
                  text='',
                  font=("Arial", 16, "italic"),
                  foreground="Green"
                  )
label2.pack()

label3 = tk.Label(frame1, text='Enter the Applicant Name:')
E1 = tk.Entry(frame1, bd=5)
B2 = tk.Button(frame1,
               text='Click here to get details!',
               font=70,
               width=20,
               foreground="White",
               background="Blue",
               command=lambda: applicant_details())
label3.pack()
E1.pack()
B2.pack()

label4 = tk.Label(frame1,
                  text='',
                  font=("Arial", 16, "italic"),
                  foreground="Red"
                  )
label4.pack()

label5 = tk.Label(frame1,
                  text='',
                  font=("Arial Bold", 20),
                  foreground="Purple"
                  )
label5.pack()
root.mainloop()
