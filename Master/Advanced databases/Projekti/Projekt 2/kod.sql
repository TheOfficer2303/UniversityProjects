create or replace view regija1 as
select 
row_number() over() as id,
	st_union(array[zupanija1.geom, zupanija2.geom, zupanija2.geom, zupanija3.geom, zupanija4.geom, zupanija5.geom, zupanija6.geom]) as geom
from hrv_adm1 zupanija1, hrv_adm1 zupanija2, hrv_adm1 zupanija3, hrv_adm1 zupanija4, hrv_adm1 zupanija5, hrv_adm1 zupanija6
where zupanija1.name_1 = 'Brodsko-Posavska'
and zupanija2.name_1 = 'Požeško-Slavonska'
and zupanija3.name_1 = 'Vukovarsko-Srijemska'
and zupanija4.name_1 = 'Osjecko-Baranjska'
and zupanija5.name_1 = 'Viroviticko-Podravska'
and zupanija6.name_1 = 'Bjelovarska-Bilogorska';

create or replace view regija2 as
select
	row_number() over() as id,
	st_union(array[zupanija1.geom, zupanija2.geom, zupanija2.geom, zupanija3.geom, zupanija4.geom, zupanija5.geom, zupanija6.geom, zupanija7.geom]) as geom
from hrv_adm1 zupanija1, hrv_adm1 zupanija2, hrv_adm1 zupanija3, hrv_adm1 zupanija4, hrv_adm1 zupanija5, hrv_adm1 zupanija6, hrv_adm1 zupanija7
where zupanija1.name_1 = 'Sisacko-Moslavacka'
and zupanija2.name_1 = 'Varaždinska'
and zupanija3.name_1 = 'Krapinsko-Zagorska'
and zupanija4.name_1 = 'Koprivničko-Križevačka'
and zupanija5.name_1 = 'Medimurska'
and zupanija6.name_1 = 'Grad Zagreb'
and zupanija7.name_1 = 'Zagrebačka';


create or replace view regija3 as
select
	row_number() over() as id,
	st_union(array[zupanija1.geom, zupanija2.geom, zupanija2.geom, zupanija3.geom, zupanija4.geom]) as geom
from hrv_adm1 zupanija1, hrv_adm1 zupanija2, hrv_adm1 zupanija3, hrv_adm1 zupanija4
where zupanija1.name_1 = 'Karlovacka'
and zupanija2.name_1 = 'Primorsko-Goranska'
and zupanija3.name_1 = 'Licko-Senjska'
and zupanija4.name_1 = 'Istarska';

create or replace view regija4 as
select
	row_number() over() as id,
	st_union(array[zupanija1.geom, zupanija2.geom, zupanija2.geom, zupanija3.geom, zupanija4.geom]) as geom
from hrv_adm1 zupanija1, hrv_adm1 zupanija2, hrv_adm1 zupanija3, hrv_adm1 zupanija4
where zupanija1.name_1 = 'Zadarska'
and zupanija2.name_1 = 'Šibensko-Kninska'
and zupanija3.name_1 = 'Splitsko-Dalmatinska'
and zupanija4.name_1 = 'Dubrovacko-Neretvanska';


--sava
create or replace view sava_view as
SELECT
     ROW_NUMBER() OVER () AS id, name,
     ST_Union(waterways.geom) as geom
FROM waterways
where lower(name) = 'sava' 
GROUP BY name

select st_length(st_intersection(st_transform(r1.geom, 3765), s.geom)) as duljina_regija1,
st_length(st_intersection(st_transform(r2.geom, 3765), s.geom)) as duljina_regija2
from regija1 r1, regija2 r2, sava s


--buffer 
create view sava_buildings_dist as
select
  buildings.gid,
	st_distance(
        sava.geom, 
        buildings.geom
) as dist
from sava, buildings;

select min(dist) from sava_buildings_dist

311207

create view sava_buffer as
select row_number() over() as id, st_buffer(sava.geom::geography, 54.25106896336527) as buf
from sava


Šibensko-Kninska 
Zadarska 
Splitsko-Dalmatinska 
Osjecko-Baranjska 
Dubrovacko-Neretvans 
Medimurska 
Vukovarsko-Srijemska 
Krapinsko-Zagorska 
Bjelovarska-Bilogorska 
Varaždinska 
Brodsko-Posavska 
Koprivničko-Križevačka 
Zagrebačka 
Viroviticko-Podravska 
Licko-Senjska 
Grad Zagreb 
Sisacko-Moslavacka 
Istarska 
Požeško-Slavonska
Karlovacka 
Primorsko-Goranska
1.5662699192947704 
11.03687841758118 
14.313572968571146 
20.999950670515037 
22 60673244608809 
24.170516843312146 
27 71325999950725 
30.786028724895797 
32.30789546344744 
34.12044765030092 
34.5023628296255 
36.222791357417236 
36.586619850733854 
36.67999710653002 
38.89848843332051 
40.498773341562874 
49.347390117132214 
51.48326856657408 
53.810894744036744 
58.939075968925714 
60.53

CREATE TABLE tableName 
(
    name	varchar(75),
    area	double_precision
);

INSERT INTO forests2 (name_1, area) VALUES ('Šibensko-Kninska', '1.5662699192947704 ');
INSERT INTO forests2 (name_1, area) VALUES ('Zadarska', '11.03687841758118 ');
INSERT INTO forests2 (name_1, area) VALUES ('Splitsko-Dalmatinska', '14.313572968571146 ');
INSERT INTO forests2 (name_1, area) VALUES ('Osjecko-Baranjska', '20.999950670515037 ');
INSERT INTO forests2 (name_1, area) VALUES ('Dubrovacko-Neretvanska', '22 60673244608809 ');
INSERT INTO forests2 (name_1, area) VALUES ('Medimurska', '24.170516843312146 ');
INSERT INTO forests2 (name_1, area) VALUES ('Vukovarsko-Srijemska', '27 71325999950725');
INSERT INTO forests2 (name_1, area) VALUES ('Krapinsko-Zagorska', '30.786028724895797');
INSERT INTO forests2 (name_1, area) VALUES ('Bjelovarska-Bilogorska', '32.30789546344744');
INSERT INTO forests2 (name_1, area) VALUES ('Varaždinska', '34.12044765030092');
INSERT INTO forests2 (name_1, area) VALUES ('Brodsko-Posavska', '34.5023628296255');
INSERT INTO forests2 (name_1, area) VALUES ('Koprivničko-Križevačka', '36.222791357417236');
INSERT INTO forests2 (name_1, area) VALUES ('Zagrebačka', '36.586619850733854');
INSERT INTO forests2 (name_1, area) VALUES ('Viroviticko-Podravska', '36.67999710653002');
INSERT INTO forests2 (name_1, area) VALUES ('Licko-Senjska', '38.89848843332051');
INSERT INTO forests2 (name_1, area) VALUES ('Grad Zagreb', '40.498773341562874');
INSERT INTO forests2 (name_1, area) VALUES ('Sisacko-Moslavacka', '49.347390117132214');
INSERT INTO forests2 (name_1, area) VALUES ('Istarska', '51.48326856657408');
INSERT INTO forests2 (name_1, area) VALUES ('Požeško-Slavonska', '53.810894744036744');
INSERT INTO forests2 (name_1, area) VALUES ('Karlovacka', '58.939075968925714');
INSERT INTO forests2 (name_1, area) VALUES ('Primorsko-Goranska', '60.53');

 SELECT hrv_adm1.name_1,
    forests2.area,
    hrv_adm1.geom
   FROM hrv_adm1
     JOIN forests2 USING (name_1);
