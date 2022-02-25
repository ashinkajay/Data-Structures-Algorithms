# Job Location Matching using Ford Fulkerson Algorithm

Problem Description:
There are a certain number of job applicants and each applicant likes a certain set of job locations. Each person can select only one job location and each job location have only one vacancy. The aim is to assign the job locations to applicants in such a manner that as many applicants as possible get their preferred location.

The program starts with adding Applicants and Job Locations as different parts of the bipartite graph. Then the problem is converted to a flow network adding a source and sink. Each edge is given a capacity of 1. Finally Ford-Fulkerson algorithm is used to find the maximum flow (here maximum number of matchings) and the matched location for each applicant.