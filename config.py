class Continent:

    world = {'width' : 0,
             'height' : 0,
             'lat_0' : 0,
             'lon_0' : 0,
             'lat_1' : 0,
             'lat_2' : 0,
             'llcrnrlon' : -180,
             'llcrnrlat' : -60,
             'urcrnrlon' : 180,
             'urcrnrlat' : 80,
             }
    europe = {'width' : 4000000,
              'height' : 4060000,
              'lat_0' : 55.5,
              'lon_0' : 14,
              'lat_1' : 5.,
              'lat_2' : 55,
              'llcrnrlon' : -9.5,
              'llcrnrlat' : 33.5,
              'urcrnrlon' : 61.5,
              'urcrnrlat' : 68.5,
             }

# European city coordinates (latitude, longitude)
# Format: 'City, Country': (latitude, longitude)
european_city_coords = {
    # Switzerland
    'Zurich, Switzerland': (47.3769, 8.5417),
    'Geneva, Switzerland': (46.2044, 6.1432),
    'Basel, Switzerland': (47.5596, 7.5886),
    'Lausanne, Switzerland': (46.5197, 6.6323),
    'Bern, Switzerland': (46.9480, 7.4474),
    'Lugano, Switzerland': (46.0037, 8.9511),

    # United Kingdom
    'London, United Kingdom': (51.5074, -0.1278),
    'Manchester, United Kingdom': (53.4808, -2.2426),
    'Birmingham, United Kingdom': (52.4862, -1.8904),
    'Edinburgh, United Kingdom': (55.9533, -3.1883),
    'Glasgow, United Kingdom': (55.8642, -4.2518),
    'Bristol, United Kingdom': (51.4545, -2.5879),
    'Liverpool, United Kingdom': (53.4084, -2.9916),
    'Leeds, United Kingdom': (53.8008, -1.5491),
    'Oxford, United Kingdom': (51.7520, -1.2577),
    'Cambridge, United Kingdom': (52.2053, 0.1218),
    'Brighton, United Kingdom': (50.8225, -0.1372),
    'Cardiff, United Kingdom': (51.4816, -3.1791),
    'Belfast, United Kingdom': (54.5973, -5.9301),
    'York, United Kingdom': (53.9600, -1.0873),
    'Southampton, United Kingdom': (50.9097, -1.4044),
    'Reading, United Kingdom': (51.4543, -0.9781),
    'Guildford, United Kingdom': (51.2362, -0.5704),
    'Coventry, United Kingdom': (52.4068, -1.5197),
    'Newcastle upon Tyne, United Kingdom': (54.9783, -1.6178),
    'Bournemouth, United Kingdom': (50.7192, -1.8808),
    'Milton Keynes, United Kingdom': (52.0406, -0.7594),
    'Sheffield, United Kingdom': (53.3811, -1.4701),
    'Nottingham, United Kingdom': (52.9548, -1.1581),

    # Norway
    'Oslo, Norway': (59.9139, 10.7522),
    'Bergen, Norway': (60.3913, 5.3221),
    'Trondheim, Norway': (63.4305, 10.3951),
    'Stavanger, Norway': (58.9700, 5.7331),

    # Denmark
    'Copenhagen, Denmark': (55.6761, 12.5683),
    'Aarhus, Denmark': (56.1629, 10.2039),
    'Odense, Denmark': (55.4038, 10.4024),
    'Aalborg, Denmark': (57.0488, 9.9217),

    # Sweden
    'Stockholm, Sweden': (59.3293, 18.0686),
    'Gothenburg, Sweden': (57.7089, 11.9746),
    'Malmo, Sweden': (55.6050, 13.0038),
    'Uppsala, Sweden': (59.8586, 17.6389),
    'Lund, Sweden': (55.7047, 13.1910),

    # Finland
    'Helsinki, Finland': (60.1695, 24.9354),
    'Espoo, Finland': (60.2055, 24.6559),
    'Turku, Finland': (60.4518, 22.2666),

    # Iceland
    'Reykjavik, Iceland': (64.1466, -21.9426),

    # Ireland
    'Dublin, Ireland': (53.3498, -6.2603),
    'Cork, Ireland': (51.8969, -8.4863),
    'Galway, Ireland': (53.2707, -9.0568),
    'Limerick, Ireland': (52.6638, -8.6267),

    # Netherlands
    'Amsterdam, Netherlands': (52.3676, 4.9041),
    'Rotterdam, Netherlands': (51.9225, 4.47917),
    'The Hague (Den Haag), Netherlands': (52.0705, 4.3007),
    'Utrecht, Netherlands': (52.0907, 5.1214),
    'Eindhoven, Netherlands': (51.4416, 5.4697),
    'Groningen, Netherlands': (53.2194, 6.5665),
    'Delft, Netherlands': (52.0116, 4.3571),
    'Leiden, Netherlands': (52.1601, 4.4970),
    'Haarlem, Netherlands': (52.3874, 4.6462),

    # Belgium
    'Brussels, Belgium': (50.8503, 4.3517),
    'Antwerp, Belgium': (51.2194, 4.4025),
    'Gent, Belgium': (51.0543, 3.7174),
    'Leuven, Belgium': (50.8798, 4.7005),

    # Luxembourg
    'Luxembourg, Luxembourg': (49.6116, 6.1319),

    # France
    'Paris, France': (48.8566, 2.3522),
    'Lyon, France': (45.7640, 4.8357),
    'Marseille, France': (43.2965, 5.3698),
    'Toulouse, France': (43.6047, 1.4442),
    'Nice, France': (43.7102, 7.2620),
    'Bordeaux, France': (44.8378, -0.5792),
    'Lille, France': (50.6292, 3.0573),
    'Strasbourg, France': (48.5734, 7.7521),
    'Montpellier, France': (43.6108, 3.8767),
    'Grenoble, France': (45.1885, 5.7245),

    # Germany
    'Berlin, Germany': (52.5200, 13.4050),
    'Munich, Germany': (48.1351, 11.5820),
    'Hamburg, Germany': (53.5511, 9.9937),
    'Frankfurt, Germany': (50.1109, 8.6821),
    'Cologne, Germany': (50.9375, 6.9603),
    'Stuttgart, Germany': (48.7758, 9.1829),
    'Dusseldorf, Germany': (51.2277, 6.7735),
    'Dortmund, Germany': (51.5136, 7.4653),
    'Essen, Germany': (51.4556, 7.0116),
    'Leipzig, Germany': (51.3397, 12.3731),
    'Bremen, Germany': (53.0793, 8.8017),
    'Dresden, Germany': (51.0504, 13.7373),
    'Hanover, Germany': (52.3759, 9.7320),
    'Nuremberg, Germany': (49.4521, 11.0767),
    'Heidelberg, Germany': (49.3988, 8.6724),
    'Karlsruhe, Germany': (49.0069, 8.4037),
    'Mannheim, Germany': (49.4875, 8.4660),
    'Augsburg, Germany': (48.3705, 10.8978),
    'Wiesbaden, Germany': (50.0826, 8.2400),
    'Bonn, Germany': (50.7374, 7.0982),
    'Darmstadt, Germany': (49.8728, 8.6512),
    'Erlangen, Germany': (49.5897, 11.0089),
    'Kiel, Germany': (54.3233, 10.1228),
    'Aachen, Germany': (50.7753, 6.0839),

    # Austria
    'Vienna, Austria': (48.2082, 16.3738),
    'Graz, Austria': (47.0707, 15.4395),

    # Poland
    'Warsaw, Poland': (52.2297, 21.0122),
    'Krakow, Poland': (50.0647, 19.9450),
    'Wroclaw, Poland': (51.1079, 17.0385),
    'Poznan, Poland': (52.4064, 16.9252),
    'Gdansk, Poland': (54.3520, 18.6466),
    'Lodz, Poland': (51.7592, 19.4560),
    'Katowice, Poland': (50.2649, 19.0238),
    'Szczecin, Poland': (53.4285, 14.5528),

    # Czech Republic
    'Prague, Czech Republic': (50.0755, 14.4378),
    'Brno, Czech Republic': (49.1951, 16.6068),
    'Ostrava, Czech Republic': (49.8209, 18.2625),
    'Plzen, Czech Republic': (49.7384, 13.3736),

    # Slovakia
    'Bratislava, Slovakia': (48.1486, 17.1077),
    'Kosice, Slovakia': (48.7164, 21.2611),

    # Hungary
    'Budapest, Hungary': (47.4979, 19.0402),
    'Debrecen, Hungary': (47.5316, 21.6273),
    'Pecs, Hungary': (46.0727, 18.2328),

    # Romania
    'Bucharest, Romania': (44.4268, 26.1025),
    'Cluj-Napoca, Romania': (46.7712, 23.6236),
    'Timisoara, Romania': (45.7489, 21.2087),
    'Iasi, Romania': (47.1585, 27.6014),
    'Brasov, Romania': (45.6579, 25.6012),
    'Constanta, Romania': (44.1598, 28.6348),
    'Craiova, Romania': (44.3302, 23.7949),
    'Sibiu, Romania': (45.7983, 24.1256),
    'Oradea, Romania': (47.0458, 21.9189),

    # Bulgaria
    'Sofia, Bulgaria': (42.6977, 23.3219),
    'Plovdiv, Bulgaria': (42.1354, 24.7453),
    'Varna, Bulgaria': (43.2141, 27.9147),
    'Burgas, Bulgaria': (42.5048, 27.4626),
    'Stara Zagora, Bulgaria': (42.4258, 25.6342),

    # Croatia
    'Zagreb, Croatia': (45.8150, 15.9819),
    'Split, Croatia': (43.5081, 16.4402),
    'Rijeka, Croatia': (45.3271, 14.4422),

    # Serbia
    'Belgrade, Serbia': (44.7866, 20.4489),
    'Novi Sad, Serbia': (45.2671, 19.8335),
    'Nis, Serbia': (43.3209, 21.8958),

    # Slovenia
    'Ljubljana, Slovenia': (46.0569, 14.5058),

    # Bosnia And Herzegovina
    'Sarajevo, Bosnia And Herzegovina': (43.8563, 18.4131),

    # Moldova
    'Chisinau, Moldova': (47.0105, 28.8638),

    # Montenegro
    'Podgorica, Montenegro': (42.4304, 19.2594),

    # Albania
    'Tirana, Albania': (41.3275, 19.8187),

    # North Macedonia
    'Skopje, North Macedonia': (41.9973, 21.4280),

    # Greece
    'Athens, Greece': (37.9838, 23.7275),
    'Thessaloniki, Greece': (40.6401, 22.9444),
    'Heraklion, Greece': (35.3387, 25.1442),

    # Italy
    'Rome, Italy': (41.9028, 12.4964),
    'Milan, Italy': (45.4642, 9.1900),
    'Naples, Italy': (40.8518, 14.2681),
    'Turin, Italy': (45.0703, 7.6869),
    'Florence, Italy': (43.7696, 11.2558),
    'Bologna, Italy': (44.4949, 11.3426),
    'Genoa, Italy': (44.4056, 8.9463),
    'Padova, Italy': (45.4064, 11.8768),
    'Trieste, Italy': (45.6495, 13.7768),
    'Brescia, Italy': (45.5416, 10.2118),
    'Bergamo, Italy': (45.6983, 9.6773),
    'Pisa, Italy': (43.7228, 10.4017),
    'Cagliari, Italy': (39.2238, 9.1217),
    'Bari, Italy': (41.1171, 16.8719),
    'Catania, Italy': (37.5079, 15.0830),
    'Bolzano-Bozen, Italy': (46.4983, 11.3548),
    'Trento, Italy': (46.0664, 11.1257),
    'Treviso, Italy': (45.6669, 12.2430),
    'Reggio Nell\'emilia, Italy': (44.6989, 10.6297),

    # Spain
    'Madrid, Spain': (40.4168, -3.7038),
    'Barcelona, Spain': (41.3851, 2.1734),
    'Valencia, Spain': (39.4699, -0.3763),
    'Seville (Sevilla), Spain': (37.3891, -5.9845),
    'Bilbao, Spain': (43.2630, -2.9350),
    'Malaga, Spain': (36.7213, -4.4214),
    'Alicante, Spain': (38.3452, -0.4810),
    'Palma de Mallorca, Spain': (39.5696, 2.6502),
    'Granada, Spain': (37.1773, -3.5986),
    'Oviedo, Spain': (43.3614, -5.8493),
    'Las Palmas de Gran Canaria, Spain': (28.1248, -15.4300),
    'Santa Cruz de Tenerife, Spain': (28.4636, -16.2518),

    # Portugal
    'Lisbon, Portugal': (38.7223, -9.1393),
    'Porto, Portugal': (41.1579, -8.6291),
    'Braga, Portugal': (41.5454, -8.4265),
    'Coimbra, Portugal': (40.2033, -8.4103),

    # Cyprus
    'Nicosia, Cyprus': (35.1856, 33.3823),
    'Limassol, Cyprus': (34.6841, 33.0384),
    'Larnaca, Cyprus': (34.9088, 33.6248),
    'Paphos, Cyprus': (34.7571, 32.4246),

    # Malta
    'Valletta, Malta': (35.8989, 14.5146),
    'Sliema, Malta': (35.9122, 14.5019),

    # Russia
    'Moscow, Russia': (55.7558, 37.6173),
    'Saint Petersburg, Russia': (59.9311, 30.3609),
    'Vladivostok, Russia': (43.1056, 131.8735),
    'Novosibirsk, Russia': (55.0084, 82.9357),
    'Yekaterinburg, Russia': (56.8389, 60.6057),
    'Kazan, Russia': (55.8304, 49.0661),
    'Nizhny Novgorod, Russia': (56.2965, 43.9361),
    'Samara, Russia': (53.1959, 50.1003),
    'Rostov-on-Don (Rostov-na-donu), Russia': (47.2357, 39.7015),
    'Ufa, Russia': (54.7388, 55.9721),
    'Krasnodar, Russia': (45.0328, 38.9769),
    'Tyumen, Russia': (57.1522, 65.5272),
    'Chelyabinsk, Russia': (55.1644, 61.4368),
    'Tomsk, Russia': (56.4977, 84.9744),
    'Kaliningrad, Russia': (54.7104, 20.4522),

    # Ukraine
    'Kyiv, Ukraine': (50.4501, 30.5234),
    'Kharkiv, Ukraine': (49.9935, 36.2304),
    'Odessa, Ukraine': (46.4825, 30.7233),
    'Dnipro, Ukraine': (48.4647, 35.0462),
    'Lviv, Ukraine': (49.8397, 24.0297),

    # Belarus
    'Minsk, Belarus': (53.9045, 27.5615),

    # Lithuania
    'Vilnius, Lithuania': (54.6872, 25.2797),
    'Kaunas, Lithuania': (54.8985, 23.9036),

    # Latvia
    'Riga, Latvia': (56.9496, 24.1052),

    # Estonia
    'Tallinn, Estonia': (59.4370, 24.7536),
    'Tartu, Estonia': (58.3780, 26.7290),

    # Turkey
    'Istanbul, Turkey': (41.0082, 28.9784),
    'Ankara, Turkey': (39.9334, 32.8597),
    'Izmir, Turkey': (38.4237, 27.1428),
    'Bursa, Turkey': (40.1826, 29.0665),
    'Antalya, Turkey': (36.8969, 30.7133),
    'Eskisehir, Turkey': (39.7767, 30.5206),
    'Mersin, Turkey': (36.8121, 34.6415),

    # Kosovo
    'Pristina, Kosovo (Disputed Territory)': (42.6629, 21.1655),
}