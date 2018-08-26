def convert():
    report = []
    parameters = []
    drop_downs = []

    #parameters.properties
    profileSQLParameters = []

    profileSQL = open('uploads/profile.sql', 'r')

    for line in profileSQL:
        if "insert into TEAMS_RPT_PROFILE_PARAMETER".lower() in line.lower():
            param = line[line.lower().index("values") : len(line)]
            param = param[param.index("(")+1 : param.index(")")]
            param = param.replace("'", "")
            param = param.strip()

            profileSQLParameters.append(param)

    for line in profileSQLParameters:
        param = line.split(",")
        param = param[1 : len(param)]

        temp = []
        for p in param:
            p = p.strip(" ")
            temp.append(p)

        parameters.append(temp)

    parametersProperties = open('downloads/parameters.properties', 'w')

    for param in parameters:
        temp = ""
        for p in param:
            temp += p + "|"
        temp = temp[0 : len(temp)-1]
        parametersProperties.write(temp + "\n")

    print("* created parameters.properties")


    #drop_down.properties
    profileSQLDropDowns = []

    profileSQL = open('uploads/profile.sql', 'r')

    for line in profileSQL:
        if "insert into TEAMS_RPT_PROF_PARAM_LIST_ITEM".lower() in line.lower():
            dropdown = line[line.lower().index("values") : len(line)]
            dropdown = dropdown[dropdown.index("(")+1 : dropdown.index(")")]
            #dropdown = dropdown.replace("'", "")
            dropdown = dropdown.strip()

            profileSQLDropDowns.append(dropdown)

    for line in profileSQLDropDowns:
        dropdown = line.split("',")
        dropdown = dropdown[1 : len(dropdown)]

        temp = []
        for d in dropdown:
            d = d.strip(" ").strip("'")
            temp.append(d)

        drop_downs.append(temp)

    dropDownProperties = open('downloads/drop_down.properties', 'w')

    for dropdown in drop_downs:
        temp = ""
        for d in dropdown:
            temp += d + "|"
        temp = temp[0 : len(temp)-1]
        dropDownProperties.write(temp + "\n")

    print("* created drop_down.properties")


    #report.properties
    cleanSQLReportProps = {}
    output_types = []

    ##Report Properties
    cleanSQL = open('uploads/clean.sql', 'r')

    for line in cleanSQL:
        if "insert into RFDS_TEAMS_RPT_PROFILE".lower() in line.lower():
            prop = line[line.lower().index("values") : len(line)]
            prop = prop[prop.index("(")+1 : prop.index(")")]
            prop = prop.replace("'", "")

            temp = prop.split(", ")

            cleanSQLReportProps["report_title"] = temp[0]
            cleanSQLReportProps["can_schedule"] = temp[1]
            cleanSQLReportProps["file_name"]    = temp[2]
            cleanSQLReportProps["note"]         = temp[3]
            cleanSQLReportProps["sort_order"]   = temp[4]
            cleanSQLReportProps["sys_owned"]    = temp[5]
            cleanSQLReportProps["subcategory"]  = temp[6]
            cleanSQLReportProps["preprocessor"] = temp[7]
            cleanSQLReportProps["conn_type"]    = temp[8]
            cleanSQLReportProps["active_flag"]  = temp[9]

    #Output Type
    cleanSQL = open('uploads/clean.sql', 'r')

    for line in cleanSQL:
        if "insert into TEAMS_REPORT_PROF_OUTPUT_TYPE".lower() in line.lower():
            prop = line[line.lower().index("values") : len(line)]
            prop = prop[prop.index("(")+1 : len(prop.strip())-1]
            prop = prop.replace("'", "")

            temp = prop.split(", ")
            output_types.append(temp[1])

    temp = ""
    for type in output_types:
        temp = type + "|"
    cleanSQLReportProps["output_type"] = temp[0: len(temp)-1]


    #RPT to JRXML
    cleanSQLReportProps["file_name"] = cleanSQLReportProps["file_name"].replace(".rpt", ".jrxml")

    reportProperties = open("downloads/report.properties", "w")

    reportProperties.write("Report_Name=\""      +cleanSQLReportProps["report_title"]+ "\"\n")
    reportProperties.write("Can_Be_Scheduled=\"" +cleanSQLReportProps["can_schedule"]+ "\"\n")
    reportProperties.write("Report=\""           +cleanSQLReportProps["file_name"]+    "\"\n")
    reportProperties.write("Note=\""             +cleanSQLReportProps["note"]+         "\"\n")
    reportProperties.write("System_Owned=\""     +cleanSQLReportProps["sys_owned"]+    "\"\n")
    reportProperties.write("Subcategory=\""      +cleanSQLReportProps["subcategory"]+  "\"\n")
    reportProperties.write("Active_Flag=\""      +cleanSQLReportProps["active_flag"]+  "\"\n")
    reportProperties.write("Connection_Type=\""  +cleanSQLReportProps["conn_type"]+    "\"\n")
    reportProperties.write("Report_Type=\"jasper\"\n")
    reportProperties.write("Output_Type=\""      +cleanSQLReportProps["output_type"]+ "\"\n")
    reportProperties.write("Sub_Reports=\"""\"\n")
    reportProperties.write("Report_DDL_Dependencies=\"ddl.sql\"\n")
    reportProperties.write("parameter_file=\"parameters.properties\"\n")
    reportProperties.write("drop_down_file=\"drop_down.properties\"\n")
    reportProperties.write("PreProcessor=\""     +cleanSQLReportProps["preprocessor"]+ "\"\n")

    print("* created report.properties")
