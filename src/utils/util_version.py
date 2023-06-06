import logging
import re

def versionCompare(v1, v2):
     
    # This will split both the versions by '.'
    arr1 = v1.split(".")
    arr2 = v2.split(".")
    n = len(arr1)
    m = len(arr2)
     
    # converts to integer from string
    arr1 = [int(i) for i in arr1]
    arr2 = [int(i) for i in arr2]
  
    # compares which list is bigger and fills
    # smaller list with zero (for unequal delimeters)
    if n>m:
      for i in range(m, n):
         arr2.append(0)
    elif m>n:
      for i in range(n, m):
         arr1.append(0)
     
    # returns 1 if version 1 is bigger and -1 if
    # version 2 is bigger and 0 if equal
    for i in range(len(arr1)):
      if arr1[i]>arr2[i]:
         return 1
      elif arr2[i]>arr1[i]:
         return -1
    return 0

def find_batch_version_update(records, serial):
    # print(records)
    for i in range(len(records)):
        if not ('Model' in records[i]['fields']):
            continue
        if(records[i]['fields']['Model'] in serial):
            return records[i]['fields']
    return False

def version_clean_compare_v1_fewer_v2(v1, v2):

    v1_filted=re.match(r'^(\d+\.\d+\.\d+)', v1)
    v2_filted=re.match(r'^(\d+\.\d+\.\d+)', v2)

    if not v1_filted:
        return False
    if not v2_filted:
        return False
    
    # print(type(v1_filted.group(1)))
    # print(versionCompare(v1_filted.group(1), v2_filted.group(1)))
    # if not versionCompare(v1_filted.group(1), v2_filted.group(1)) == -1:
    #    return False
    
    return versionCompare(v1_filted.group(1), v2_filted.group(1))
    
    # return True
