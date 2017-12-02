#######################################################
## TEAM BFP
## Sprint 2
## Team 1 - Tiffany D. & Apoorva T.
## Module 1
#######################################################

import pandas as pd
import numpy as np

# Create data frame from CSV_input_file with fields required
df = pd.read_csv('./assets/CSV_input_file.csv', usecols=['Employee SSN', 'Employee ID', 'Employee Last Name', 'Employee First Name', 'Employee Middle Initial', 'Employee Date of Birth', 'Street Address 1', 'Street Address 2', 'City', 'State', 'ZIP Code', 'Email Address', 'Phone Number', 'Department', 'Coverage Start Date', 'Coverage Indicator.7', 'Enrollment Status.14'])

# Initializing empty arrays for columns validated
rowLength = 0
employeeSSNArr = []
dobMonthArr = []
dobDayArr = []
dobYearArr = []
zipCodeArr = []
areaCodeArr = []
homePhoneArr = []
emailAddressArr = []
planTypeArr = []
statusArr = []
clientIDArr = []
deductMethodArr = []
primaryArr = []
productIDArr = []

# Employee SSN Validation
for row in df['Employee SSN']:
    if len(str(row)) >= 9:
        employeeSSNArr.append(np.int64(str(row)[:9]))
    rowLength += 1

# Employee DOB Validation
for row in df['Employee Date of Birth']:
    fullDOBSplit = row.split('/')
    dobMonthArr.append(fullDOBSplit[0])
    dobDayArr.append(fullDOBSplit[1])
    dobYearArr.append(fullDOBSplit[2])

# Employee Zip Code Validation
for row in df['ZIP Code']:
    if len(str(row)) >= 5:
        zipCodeArr.append(np.int64(str(row)[:5]))

# Employee Phone number processing
for row in df['Phone Number']:
    areaCodeArr.append(str(row)[:3])
    homePhoneArr.append(str(row)[-7:])

# Email Address validation
for row in df['Email Address']:
    if pd.isnull(row):
        emailAddressArr.append('ift540@asu.edu')
    else:
        emailAddressArr.append(row)

# Coverage Indicator processing
# Utilizes the mangle_dupe_columns(set true by default) index to grab the
# correct column
for row in df['Coverage Indicator.7']:
    if row == 1:
        planTypeArr.append('Individual')
    else:
        planTypeArr.append('Family')

# Hard coding static columns
for row in range(rowLength):
    statusArr.append('Add')
    clientIDArr.append('1495')
    deductMethodArr.append('Employer Payroll Deduction')
    primaryArr.append('Y')
    productIDArr.append('PAP')

#######################
# Write to file
#######################

# Creating new data frame based on validated/processed list objects
newDF = pd.DataFrame(np.column_stack([df['Coverage Start Date'], statusArr, clientIDArr, df['Employee ID'], df['Employee First Name'], df['Employee Middle Initial'], df['Employee Last Name'], employeeSSNArr, dobMonthArr, dobDayArr, dobYearArr, df['Street Address 1'], df['Street Address 2'], df['City'], df['State'], zipCodeArr, areaCodeArr, homePhoneArr, emailAddressArr, deductMethodArr, df['Department'], df['Enrollment Status.14'], primaryArr, df['Employee ID'], df['Employee ID'], planTypeArr, productIDArr]), columns=['Effective Date', 'Status', 'ClientID', 'EmployeeID', 'MemberFirstName', 'MemberMiddleInitial', 'MemberLastName', 'MemberSSN', 'DOB_Month', 'DOB_Day', 'DOB_Year', 'Address1', 'Address2', 'City', 'State', 'ZipCode', 'AreaCode', 'HomePhone', 'Email', 'Deduction Method', 'Customer_Defined', 'Relationship', 'Primary', 'FamilyID', 'UniqueID', 'Plan_Type', 'ProductID' ])

# Write to new CSV file
newDF.to_csv('./assets/enrollment_file.csv', encoding='utf-8')
