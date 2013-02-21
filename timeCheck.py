def checkTimeString(string_time):
    try:
        split_string = string_time.split(":")
    except:
        print "Wrong format, must be a string"
        return None          
    if len(split_string) == 3 and 0 < len(split_string[0]) < 3 and len(split_string[1]) == 2 and len(split_string[2]) == 2:
        #check 'string' hour
        if  int(split_string[0]) <0 or int(split_string[0])> 23:
            print "Wrong format, hour must be between 0 and 23"
            return None
        if len(split_string[0]) == 1:
            split_string[0] = "0" + split_string[0]
        #check 'string' minute
        if int(split_string[1]) <0 or int(split_string[1])> 59:
            print "Wrong format, minute must be between 0 and 59"
            return None
        #check 'string' minute
        if int(split_string[2]) <0 or int(split_string[2])> 59:
            print "Wrong format, second must be between 0 and 59"
            return None
    else:
        print "string must be in format 'HH:MM:SS'"
        return None
    return split_string[0] + ":" + split_string[1] + ":" + split_string[2]
