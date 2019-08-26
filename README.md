# README

## HOW TO DEPLOY APP:

### 1. login to server using ssh (e.g. putty) 
ip: 
84.201.158.146  
creds:  
entrant  
8f0b7205d4f42975164b318a8a717f26221e94f0ad06d039bfac2e04637358ab  


### 2. install mysql: 

sudo apt update  
sudo apt install mysql-server  
sudo mysql  
mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';   
mysql> FLUSH PRIVILEGES;  
mysql> exit  

sudo mysql  

create database MyDB;  
use MyDB;  
CREATE TABLE `imports` (  
  `import_id` int(11) NOT NULL AUTO_INCREMENT,  
  PRIMARY KEY (`import_id`)  
) ;  

CREATE TABLE `persons` (  
  `person_id` int(11) NOT NULL AUTO_INCREMENT,  
  `import_id` int(11) DEFAULT NULL,  
  `citizen_id` int(11) DEFAULT NULL,  
  `town` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,  
  `street` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,  
  `building` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,  
  `apartment` int(11) DEFAULT NULL,  
  `name` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,  
  `birth_date` date DEFAULT NULL,  
  `gender` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,  
  `relatives` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,  
  PRIMARY KEY (`person_id`)  
) ;  

CREATE TABLE `relatives` (  
  `relatives_id` int(11) NOT NULL AUTO_INCREMENT,  
  `import_id` int(11) DEFAULT NULL,  
  `citizen_id` int(11) DEFAULT NULL,  
  `relative` int(11) DEFAULT NULL,  
  PRIMARY KEY (`relatives_id`)  
) ;  

mysql> exit  

### 3. place files into empty dir. in my case it is app dir in home directory  
c:\pscp C:\py\rest\app.py entrant@84.201.158.146:/home/entrant/app/app.py  
c:\pscp C:\py\rest\tests_for_app.py entrant@84.201.158.146:/home/entrant/app/tests_for_app.py  

### 4. run app
cd app   
sudo python3 app.py  

### 5. check requests  

post request:  


curl -X POST \
  http://0.0.0.0:8080/imports \
  -H 'Content-Type: application/json' \
  -d '{
    "citizens": [
        {
            "citizen_id": 2,
            "town": "Москва",
            "street": "Льва Толстого",
            "building": "16к7стр5",
            "apartment": 7,
            "name": "Иванов Сергей Иванович",
            "birth_date": "01.04.1997",
            "gender": "male",
            "relatives": [
                3,
                4
            ]
        },
        {
            "citizen_id": 3,
            "town": "Керчь",
            "street": "Иосифа Бродского",
            "building": "2",
            "apartment": 11,
            "name": "Романова Мария Леонидовна",
            "birth_date": "23.11.1986",
            "gender": "female",
            "relatives": [
                2,
                3,
                4
            ]
        },
        {
            "citizen_id": 4,
            "town": "Керчь",
            "street": "Иосифа Бродского",
            "building": "2",
            "apartment": 11,
            "name": "Романова Мария Леонидовна",
            "birth_date": "23.11.1986",
            "gender": "female",
            "relatives": [
                2,
                3
            ]
        }
    ]
}'

get request:

curl -X GET \
  http://0.0.0.0:8080/imports/5/citizens \
  -H 'Content-Type: application/json' 


patch request:

curl -X PATCH \
  http://0.0.0.0:8080/imports/5/citizens/2 \
  -H 'Content-Type: application/json' \
  -d '
        {

            "town": "London",
            "name": "masha",
            "birth_date": "12.11.2017",
            "relatives": [2,3]
        }'

birth request:

curl -X GET \
  http://0.0.0.0:8080/imports/5/citizens/birthdays \
  -H 'Content-Type: application/json' 





