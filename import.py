import os,csv,psycopg2

#Connect with database
DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

#Activate cursor
curr = conn.cursor()

#create table user
curr.execute("CREATE TABLE users (id serial PRIMARY KEY, \
                                    username VARCHAR ( 50 ) NOT NULL,\
                                    password VARCHAR ( 255 ) NOT NULL);")
print("users created")                                    

#create table gallery
curr.execute("CREATE TABLE gallery (id serial PRIMARY KEY, idphoto VARCHAR(255) NOT NULL, \
                                    location VARCHAR ( 50 ) NOT NULL,\
                                    URL VARCHAR ( 255 ) UNIQUE NOT NULL,\
                                    weather VARCHAR ( 50 ) NOT NULL,\
                                    landscape VARCHAR ( 50 ) NOT NULL);")
print("gallery created") 
#inser into table gallery                                   
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
#create table reviews
curr.execute("CREATE TABLE reviews (id SERIAL PRIMARY KEY, \
                                        timeDate TIMESTAMP NOT NULL, \
                                        username VARCHAR ( 255 ), \
                                        comment VARCHAR NOT NULL, \
                                        idphoto VARCHAR NOT NULL, \
					rating SMALLINT NOT NULL);")	
print("reviews!")	
#create table destinations
curr.execute("CREATE TABLE destinations (id SERIAL PRIMARY KEY, \
                                location VARCHAR ( 255 ), \
                                country VARCHAR (50), \
                                days SMALLINT NOT NULL);")	
print("reviews!")
#create table costs
curr.execute("CREATE TABLE costs (id SERIAL PRIMARY KEY, \
                                country VARCHAR (50), \
                                cost SMALLINT NOT NULL);")

#insert into table costs
curr.execute("INSERT INTO costs (country, cost) Values \
                                ('Switzerland',122.4), \
                                ('Norway',101.43), \
                                ('Iceland',100.48), \
                                ('Japan',83.35), \
                                ('Denmark',83), \
                                ('Bahamas',82.51), \
                                ('Luxembourg',81.89), \
                                ('Israel',81.15), \
                                ('Singapore',81.1), \
                                ('South Korea',78.18), \
                                ('Hong Kong',77.22), \
                                ('Barbados',76.02), \
                                ('Ireland',75.91), \
                                ('France',74.14), \
                                ('Netherlands',73.75),\
                                ('Australia',73.54),\
                                ('New Zealand',72.53),\
                                ('Belgium',71.78),\
                                ('Seychelles',71.59),\
                                ('United States',71.05),\
                                ('Austria',70.38),\
                                ('Finland',70.29),\
                                ('Sweden',69.85),\
                                ('Canada',67.62),\
                                ('Puerto Rico',67.54),\
                                ('Malta',67.46),\
                                ('United Kingdom',67.28),\
                                ('Italy',67.26),\
                                ('Germany',65.26),\
                                ('Macao',64.84),\
                                ('Qatar',64.04),\
                                ('United Arab Emirates',61.98),\
                                ('Taiwan',61.37),\
                                ('Lebanon',60.5),\
                                ('Bahrain',58.94),\
                                ('Cyprus',57.93),\
                                ('Jamaica',57.82),\
                                ('Greece',55.67),\
                                ('Zimbabwe',55.3),\
                                ('Palestinian Territory',54.54),\
                                ('Ethiopia',54.39),\
                                ('Panama',54.16),\
                                ('Costa Rica',53.98),\
                                ('Spain',53.77),\
                                ('Trinidad And Tobago',53.7),\
                                ('Jordan',53.67),\
                                ('Slovenia',53.43),\
                                ('Mauritius',53.04),\
                                ('Uruguay',51.04),\
                                ('Estonia',50.93),\
                                ('Kuwait',50.37),\
                                ('Thailand',49.77),\
                                ('Croatia',49.7),\
                                ('Portugal',49.52),\
                                ('Oman',49.28),\
                                ('Belize',49.23),\
                                ('Saudi Arabia',48.34),\
                                ('Latvia',47.94),\
                                ('Cambodia',47.49),\
                                ('Fiji',47.48),\
                                ('Czech Republic',46.15),\
                                ('El Salvador',45.57),\
                                ('Brunei',44.71),\
                                ('Nicaragua',44.56),\
                                ('Slovakia',44.46),\
                                ('Lithuania',44.28),\
                                ('Dominican Republic',44.06),\
                                ('Chile',43.62),\
                                ('Cuba',43.46),\
                                ('Suriname',43.14),\
                                ('Namibia',43.1),\
                                ('South Africa',42.87),\
                                ('Guatemala',42.7),\
                                ('Honduras',42.17),\
                                ('Myanmar',42.11),\
                                ('Ecuador',40.98),\
                                ('Hungary',40.85),\
                                ('Brazil',40.22),\
                                ('Kenya',40.21),\
                                ('China',40.04),\
                                ('Poland',40.04),\
                                ('Russia',39.21),\
                                ('Botswana',39.13),\
                                ('Malaysia',39.12),\
                                ('Iraq',39.04),\
                                ('Iran',39.01),\
                                ('Somalia',38.68),\
                                ('Peru',38.65),\
                                ('Vietnam',38.34),\
                                ('Montenegro',38.23),\
                                ('Ghana',37.65),\
                                ('Philippines',37.63),\
                                ('Indonesia',37.27),\
                                ('Bulgaria',36.7),\
                                ('Albania',36.39),\
                                ('Bosnia And Herzegovina',35.97),\
                                ('Mexico',35.72),\
                                ('Serbia',35.72),\
                                ('Romania',35.31),\
                                ('Tanzania',35.25),\
                                ('Belarus',34.7),\
                                ('Turkey',34.69),\
                                ('Bolivia',34.56),\
                                ('Morocco',34.32),\
                                ('Moldova',33.7),\
                                ('Rwanda',33.35),\
                                ('Ukraine',33.18),\
                                ('Argentina',32.95),\
                                ('Armenia',32.84),\
                                ('Bangladesh',32.25),\
                                ('Zambia',31.72),\
                                ('Sri Lanka',31.61),\
                                ('Macedonia',31.59),\
                                ('Paraguay',31.1),\
                                ('Nigeria',31),\
                                ('Colombia',30.66),\
                                ('Kazakhstan',30.64),\
                                ('Uganda',30.18),\
                                ('Algeria',30.1),\
                                ('Azerbaijan',29.92),\
                                ('Egypt',29.54),\
                                ('Nepal',29.05),\
                                ('Georgia',28.48),\
                                ('Kosovo',28.47),\
                                ('Venezuela',27.17),\
                                ('Tunisia',27.04),\
                                ('Kyrgyzstan',26.97),\
                                ('Uzbekistan',26.01),\
                                ('Syria',25.31),\
                                ('India',24.58),\
                                ('Afghanistan',24.24),\
                                ('Pakistan ',21.98)

#submit on database
conn.commit()
print("Insert Completed!")
