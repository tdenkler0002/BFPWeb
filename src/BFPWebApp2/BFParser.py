#######################################################
## TEAM BFP
## Sprint 2
## Team 1 - Tiffany D. & Apoorva T.
## Module 2
#######################################################

import pandas as pd
import numpy as np
import re

def PyParser(filename):
    # Create data frame from CSV_input_file
    pyFile = filename
    pyFileName = filename.name
    df = pd.read_csv(pyFile)
    orgColNames = df.columns.tolist()
    inputColNames = []
    dict_DOB = {1: 31, 2: [28, 29], 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    # Validation Methods

    def columnCheck(colNames):
        for colName in colNames:
            if re.match(r"(effective)", colName, re.IGNORECASE):
                colName = "Effective Date"
            if re.match(r"(status)", colName, re.IGNORECASE):
                colName = "Status"
            if re.match(r"(client|cid)", colName, re.IGNORECASE):
                colName = "ClientID"
            if re.match(r"(employee|eid)", colName, re.IGNORECASE):
                colName = "EmployeeID"
            if re.match(r"(first)", colName, re.IGNORECASE):
                colName = "MemberFirstName"
            if re.match(r"(middle)", colName, re.IGNORECASE):
                colName = "MemberMiddleName"
            if re.match(r"(last)", colName, re.IGNORECASE):
                colName = "MemberLastName"
            if re.match(r"(ssn)", colName, re.IGNORECASE):
                colName = "MemberSSN"
            if re.match(r"(dob[\s,_]?day)", colName, re.IGNORECASE):
                colName = "DOB_Day"
            if re.match(r"(dob[\s,_]?month)", colName, re.IGNORECASE):
                colName = "DOB_Month"
            if re.match(r"(dob[\s,_]?year)", colName, re.IGNORECASE):
                colName = "DOB_Year"
            if re.match(r"(address1|address_1|address\s1)", colName, re.IGNORECASE):
                colName = "Address1"
            if re.match(r"(address2|address_2|address\s2)", colName, re.IGNORECASE):
                colName = "Address2"
            if re.match(r"(city)", colName, re.IGNORECASE):
                colName = "City"
            if re.match(r"(state)", colName, re.IGNORECASE):
                colName = "State"
            if re.match(r"(zip)", colName, re.IGNORECASE):
                colName = "ZipCode"
            if re.match(r"(area[\s,_]?code)", colName, re.IGNORECASE):
                colName = "AreaCode"
            if re.match(r"(home[\s,_]?phone)", colName, re.IGNORECASE):
                colName = "HomePhone"
            if re.match(r"(email)", colName, re.IGNORECASE):
                colName = "Email"
            if re.match(r"(deduction)", colName, re.IGNORECASE):
                colName = "Deduction Method"
            if re.match(r"(customer)", colName, re.IGNORECASE):
                colName = "Customer_Defined"
            if re.match(r"(relationship|rel)", colName, re.IGNORECASE):
                colName = "Relationship"
            if re.match(r"(primary)", colName, re.IGNORECASE):
                colName = "Primary"
            if re.match(r"(family|fid)", colName, re.IGNORECASE):
                colName = "FamilyID"
            if re.match(r"(unique|uid)", colName, re.IGNORECASE):
                colName = "UniqueID"
            if re.match(r"(plan)", colName, re.IGNORECASE):
                colName = "Plan_Type"
            if re.match(r"(product|pid)", colName, re.IGNORECASE):
                colName = "ProductID"

            inputColNames.append(colName)

    def is_leap_year (year):
        return (year % 4 == 0) and (year % 100 != 0) or (year % 400 == 0)

    def validateDOB (dobDay, dobMonth, dobYear):
        dobvalid = False
        if len(str(dobYear)) == 4:
            if dobMonth in dict_DOB.keys():
                if dobMonth == 2:
                    if is_leap_year(dobYear) and dobDay in range(1, dict_DOB[dobMonth][-1]):
                        dobvalid = True
                    if not is_leap_year(dobYear) and dobDay in range(1, dict_DOB[dobMonth][0]):
                        dobvalid = True
                else:
                    if dobDay in range(1, dict_DOB[dobMonth]):
                        dobvalid = True
        return dobvalid

    def validateReln (relationDF):
        for index, familyID, relation, planType, primary in relationDF.itertuples():
            if relation in ['D', 'S', 'C'] and primary == 'Y':
                relationDF['Primary'].set_value(index, 'N')
            else:
                pass

    def alertReln (relationDF, familyDF):
        correctFamID = []
        incorrectFamID = []

        for familyID, relation, planType, primary in relationDF.itertuples(index=False):
            if relation != "P" and planType == "Individual":
                print("ALERT: Member with familyID  " + familyID + " is not compliant. Has a relationship " + relation + " with a plan type of " + planType)
            if relation in ['D', 'S', 'C']:
                for famID, reln in familyDF.itertuples(index=False):
                    if famID == familyID and reln == "P" and reln != relation:
                        correctFamID.append(famID)

        for familyID, relation, planType, primary in relationDF.itertuples(index=False):
            if relation != "P" and familyID not in correctFamID:
                print("ALERT: Member with familyID " + familyID + " does not have a correspoding Primary member. Please correct this.")

    def validateZIPLength (zipDF):
        for index, zipCode in zipDF.itertuples():
            zipDF['ZipCode'] = zipDF['ZipCode'].apply('{:0>5}'.format)

    def validateSSN (ssnDF):
        for index, ssn, empID in ssnDF.itertuples():
            if isinstance(ssn, str):
                ssnDF['MemberSSN'].set_value(index, (re.sub('[^0-9]','', ssn)))
            else:
                 if len(str(ssn)) == 9 and str(ssn).isdigit():
                     pass
                 else:
                     print("ALERT: Incorrect SSN format for employee " + empID)

    def validatePhone(phoneDF):
        for index, areaCode, homePhone in phoneDF.itertuples():
            if len(str(areaCode)) == 3 and len(str(homePhone)) == 7:
                pass

            if len(str(homePhone)) == 10:
                if len(str(areaCode)) == 3:
                    phoneDF['HomePhone'].set_value(index, str(homePhone)[3:])
                else:
                    phoneDF['AreaCode'].set_value(index, str(homePhone)[:3])
                    phoneDF['HomePhone'].set_value(index, str(homePhone)[3:])
            if re.match(r"(^\+?1\s\d{3}\s\d{7})", str(homePhone)):
                phoneDF['AreaCode'].set_value(index, str(homePhone)[3:5])
                phoneDF['HomePhone'].set_value(index, str(homePhone)[7:])

            if re.match(r"(^1\s\d{3}\s\d{7})", str(homePhone)):
                phoneDF['AreaCode'].set_value(index, str(homePhone)[2:4])
                phoneDF['HomePhone'].set_value(index, str(homePhone)[6:])

            if re.match(r"(^1\d{10})", str(homePhone)):
                phoneDF['AreaCode'].set_value(index, str(homePhone)[1:4])
                phoneDF['HomePhone'].set_value(index, str(homePhone)[4:])

    # Column Validation
    columnCheck(orgColNames)
    df.columns = inputColNames

    #Create data frames for validations
    dobDF = df[['DOB_Day', 'DOB_Month', 'DOB_Year', 'EmployeeID']]
    relationDF = df[['FamilyID', 'Relationship', 'Plan_Type', 'Primary']].copy()
    familyDF = df[['FamilyID', 'Relationship']].copy()
    zipDF = df[['ZipCode']].copy()
    ssnDF = df[['MemberSSN', 'EmployeeID']].copy()
    phoneDF = df[['AreaCode', 'HomePhone']].copy()

    # DOB Validation
    for dobDay, dobMonth, dobYear, empID in dobDF.itertuples(index=False):
        if validateDOB(dobDay, dobMonth, dobYear):
            pass
        else:
            print("ALERT: Employee ID " + empID + " does not have a valid date of birth. Please correct!")

    # Relationship Dependent Validation
    validateReln(relationDF)

    # Relationship Validation Alerts
    alertReln(relationDF, familyDF)

    # ZipCode Validation
    validateZIPLength(zipDF)

    # Validate SSN
    validateSSN(ssnDF)

    # Phone Validation
    validatePhone(phoneDF)

    #######################
    # Write to file
    #######################

    # Creating new data frame based on validated/processed list objects
    newDF = pd.DataFrame(np.column_stack([df['Effective Date'], df['Status'], df['ClientID'], df['EmployeeID'], df['MemberFirstName'], df['MemberMiddleName'], df['MemberLastName'], ssnDF['MemberSSN'], dobDF['DOB_Month'], dobDF['DOB_Day'], dobDF['DOB_Year'], df['Address1'], df['Address2'], df['City'], df['State'], zipDF['ZipCode'], phoneDF['AreaCode'], phoneDF['HomePhone'], df['Email'], df['Deduction Method'], df['Customer_Defined'], df['Relationship'], relationDF['Primary'], df['FamilyID'], df['UniqueID'], df['Plan_Type'], df['ProductID']]), columns=['Effective Date', 'Status', 'ClientID', 'EmployeeID', 'MemberFirstName', 'MemberMiddleInitial', 'MemberLastName', 'MemberSSN', 'DOB_Month', 'DOB_Day', 'DOB_Year', 'Address1', 'Address2', 'City', 'State', 'ZipCode', 'AreaCode', 'HomePhone', 'Email', 'Deduction Method', 'Customer_Defined', 'Relationship', 'Primary', 'FamilyID', 'UniqueID', 'Plan_Type', 'ProductID' ])

    newDF['Relationship'] = pd.Categorical(newDF['Relationship'], ['P', 'D', 'S', 'C'], ordered=True)
    newDF = newDF.sort_values(['Relationship'])

    newDF.to_csv('./media/documents/%s-Corrected' % pyFileName, encoding='utf-8')
