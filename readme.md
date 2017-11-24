#Test Data Engineer ContentSquare

I created a SQLite Database, and a table named "Users":

1|Andre|127.0.0.1|Charles|22

I run the python server using a virtualenv.

Needed command to launch :


#Endpoint 1 : /users/id

Returns a json with all the information about the selected user.
Returns an error if the user doesn't exists.

The API will aslo go search for the country in the excelfile.
It works also when the ip provided in the xlsx file is like this : 123.45.*.* it will match the ip of the user to the pattern in the xlsx


#EndPoint 2 : /add? with parameter id, lastname, ip, firstname, age.

Id, lastname and ip are mandatory. If those are missing it will return an error specifying which one is missing.


The two others are optional, the API won't update the missing value. For example if the age is missing, the API will update the others values and the age will remain the same as previous.

If the provided Id doesn't exist yet it will create a new user, otherwise it will update the existing user with the provided values
