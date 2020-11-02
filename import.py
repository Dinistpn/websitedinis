import os,csv,psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

curr = conn.cursor()

curr.execute("CREATE TABLE users (id serial PRIMARY KEY, \
                                    username VARCHAR ( 50 ) NOT NULL,\
                                    password VARCHAR ( 50 ) NOT NULL);")
print("users created")                                    


curr.execute("CREATE TABLE gallery (id serial PRIMARY KEY, idphoto VARCHAR(255) NOT NULL, \
                                    location VARCHAR ( 50 ) NOT NULL,\
                                    URL VARCHAR ( 255 ) UNIQUE NOT NULL,\
                                    weather VARCHAR ( 50 ) NOT NULL,\
                                    landscape VARCHAR ( 50 ) NOT NULL);")
print("gallery created")                                    
curr.execute("INSERT INTO gallery (idphoto,location, URL, weather, landscape) Values \
        ('50130740836','Krakow','flickr.com/photos/189372031@N02/50130740836/in/dateposted-public/','Rain','City'),\
        ('50130966512','Krakow','flickr.com/photos/189372031@N02/50130966512/in/dateposted-public/','Rain','City'),\
        ('50130966617','Krakow','flickr.com/photos/189372031@N02/50130966617/in/dateposted-public/','Rain','City'),\
        ('50130172563','Budapest','flickr.com/photos/189372031@N02/50130172563/in/dateposted-public/','Rain','River'),\
        ('50130966802','Budapest','flickr.com/photos/189372031@N02/50130966802/in/dateposted-public/','Rain','River'),\
        ('50130741131','Budapest','flickr.com/photos/189372031@N02/50130741131/in/dateposted-public/','Rain','River'),\
        ('50130741146','Budapest','flickr.com/photos/189372031@N02/50130741146/in/dateposted-public/','Rain','River'),\
        ('50130966997','Budapest','flickr.com/photos/189372031@N02/50130966997/in/dateposted-public/','Rain','River'),\
        ('50130741296','Budapest','flickr.com/photos/189372031@N02/50130741296/in/dateposted-public/','Rain','River'),\
        ('50130966987','Budapest','flickr.com/photos/189372031@N02/50130966987/in/dateposted-public/','Rain','River'),\
        ('50130172743','Zakopane','flickr.com/photos/189372031@N02/50130172743/in/dateposted-public/','Snow','Montains'),\
        ('50130966977','Zakopane','flickr.com/photos/189372031@N02/50130966977/in/dateposted-public/','Snow','Montains'),\
        ('50130741386','Zakopane','flickr.com/photos/189372031@N02/50130741386/in/dateposted-public/','Snow','Montains'),\
        ('50130741461','Zakopane','flickr.com/photos/189372031@N02/50130741461/in/dateposted-public/','Snow','Montains'),\
        ('50130741481','Zakopane','flickr.com/photos/189372031@N02/50130741481/in/dateposted-public/','Snow','Montains'),\
        ('50284703658','Venice','flickr.com/photos/189372031@N02/50284703658/in/dateposted-public/','Sunny','Lagoon'),\
        ('50285536782','Venice','flickr.com/photos/189372031@N02/50285536782/in/dateposted-public/','Sunny','Lagoon'),\
        ('50285380946','Venice','flickr.com/photos/189372031@N02/50285380946/in/dateposted-public/','Sunny','Lagoon'),\
        ('50285381011','Venice','flickr.com/photos/189372031@N02/50285381011/in/dateposted-public/','Sunny','Lagoon'),\
        ('50285381221','Venice','flickr.com/photos/189372031@N02/50285381221/in/dateposted-public/','Sunny','Lagoon'),\
        ('50284702408','Budapest','flickr.com/photos/189372031@N02/50284702408/in/dateposted-public/','Rainy','City'),\
        ('50285535572','Budapest','flickr.com/photos/189372031@N02/50285535572/in/dateposted-public/','Rainy','City'),\
        ('50284702493','Budapest','flickr.com/photos/189372031@N02/50284702493/in/dateposted-public/','Rainy','City'),\
        ('50285535617','Budapest','flickr.com/photos/189372031@N02/50285535617/in/dateposted-public/','Rainy','City'),\
        ('50285530987','Bournemouth','flickr.com/photos/189372031@N02/50285530987/in/dateposted-public/','Rainy','City'),\
        ('50284697513','Bournemouth','flickr.com/photos/189372031@N02/50284697513/in/dateposted-public/','Rainy','City'),\
        ('50284697573','Bournemouth','flickr.com/photos/189372031@N02/50284697573/in/dateposted-public/','Rainy','City'),\
        ('50284697648','Bournemouth','flickr.com/photos/189372031@N02/50284697648/in/dateposted-public/','Rainy','City'),\
        ('50285529912','Aveiro','flickr.com/photos/189372031@N02/50285529912/in/dateposted-public/','Sun','Sea'),\
        ('50285529942','Aveiro','flickr.com/photos/189372031@N02/50285529942/in/dateposted-public/','Sun','Sea'),\
        ('50285530012','Aveiro','flickr.com/photos/189372031@N02/50285530012/in/dateposted-public/','Sun','Sea'),\
        ('50285530027','Aveiro','flickr.com/photos/189372031@N02/50285530027/in/dateposted-public/','Sun','Sea'),\
        ('50513399783','Gdansk','flickr.com/photos/189372031@N02/50513399783/in/dateposted-public/','Sun','Baltic Sea'),\
        ('50514110721','Vienna','flickr.com/photos/189372031@N02/50514110721/in/dateposted-public/','Clouds','Culture'),\
        ('50514110626','Vienna','flickr.com/photos/189372031@N02/50514110626/in/dateposted-public/','Clouds','Culture'),\
        ('50514110791','Vienna','flickr.com/photos/189372031@N02/50514110791/in/dateposted-public/','Clouds','Culture'),\
        ('50514110726','Vienna','flickr.com/photos/189372031@N02/50514110726/in/dateposted-public/','Clouds','Culture'),\
        ('50514278137','Vienna','flickr.com/photos/189372031@N02/50514278137/in/dateposted-public/','Clouds','Culture'),\
        ('50513399323','Vienna','flickr.com/photos/189372031@N02/50513399323/in/dateposted-public/','Clouds','Culture'),\
        ('50513399193','Vienna','flickr.com/photos/189372031@N02/50513399193/in/dateposted-public/','Clouds','Culture'),\
        ('50514277812','Vienna','flickr.com/photos/189372031@N02/50514277812/in/dateposted-public/','Clouds','Culture'),\
        ('50514110171','Gdansk','flickr.com/photos/189372031@N02/50514110171/in/dateposted-public/','Sun','Baltic Sea'),\
        ('50514109671','Malbork','flickr.com/photos/189372031@N02/50514109671/in/dateposted-public/','Rain','Castle'),\
        ('50514277722','Malbork','flickr.com/photos/189372031@N02/50514277722/in/dateposted-public/','Rain','Castle'),\
        ('50514109651','Aveiro','flickr.com/photos/189372031@N02/50514109651/in/dateposted-public/','Sun','River'),\
        ('50514109696','Venice','flickr.com/photos/189372031@N02/50514109696/in/dateposted-public/','Sun','Lagoon'),\
        ('50513398573','Budapest','flickr.com/photos/189372031@N02/50513398573/in/dateposted-public/','Rain','Culture'),\
        ('50513398533','Budapest','flickr.com/photos/189372031@N02/50513398533/in/dateposted-public/','Rain','Culture'),\
        ('50513398528','Budapest','flickr.com/photos/189372031@N02/50513398528/in/dateposted-public/','Rain','Culture'),\
        ('50514277077','Budapest','flickr.com/photos/189372031@N02/50514277077/in/dateposted-public/','Rain','Culture'),\
        ('50513398513','Zakopane','flickr.com/photos/189372031@N02/50513398513/in/dateposted-public/','Rain','Montains');")

print("gallery update")    

curr.execute("CREATE TABLE reviews (id SERIAL PRIMARY KEY, \
                                   timeDate TIMESTAMP NOT NULL, \
                                   username VARCHAR ( 255 ), \
								   comment VARCHAR NOT NULL, \
                                   idphoto VARCHAR NOT NULL, \
								   rating SMALLINT NOT NULL);")	
print("reviews!")	
curr.execute("CREATE TABLE destinations (id SERIAL PRIMARY KEY, \
                                location VARCHAR ( 255 ), \
                                days SMALLINT NOT NULL);")	
print("reviews!")						   						  
conn.commit()
print("Insert Completed!")
