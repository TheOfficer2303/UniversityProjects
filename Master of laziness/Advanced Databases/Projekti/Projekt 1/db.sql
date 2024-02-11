-- ZD 1
CREATE TABLE reviews(
  title VARCHAR(200)
  summary VARCHAR(200)
  text VARCHAR(5000)
);

CREATE INDEX index1 ON reviews(text, summary, title)

-- ZD 2
CREATE TEXT SEARCH CONFIGURATION bs52494(
  PARSER = pg_catalog.default
);

ALTER TEXT SEARCH CONFIGURATION bs52494
ADD MAPPING FOR asciiword, word, numword, asciihword, hword, numhword, hword_asciipart, hword_part, hword_numpart, email, protocol, url, host, url_path, file, sfloat, float, int, uint, version, tag, entity, blank
WITH pg_catalog.simple



select *
from
ts_debug('bs52494', 'THIS GAME ROCKS!! First of all this game has been delayed like a MILLION times so lots of people are waiting for it to come out. The things that make this game ROCK are She gets new outfits she still has a wetsuit but it looks different. There is a another person you can play his name is Kurtis Trent and he wants REVENGE on the dude who KILLED his father. It is on the PS2. There are better graphics. It has a better storyline. She has HAND TO HAND COMBAT in it AND SHE LOOKS SO COOL AND SEXY!!! BUT DO NOT BUT IT AT AMAZON.COM IT COMES OUT JUNE 18 AT THE FRISCO MALL BUY IT THERE!BECAUSE IT COMES OUT JUNE 20 AT AMAZON.COM THIS GAME ROCKS!!!!!!!!!!!THIS GAME ROCKS!! First of all this game has been delayed like a MILLION times so lots of people are waiting for it to come out. The things that make this game ROCK are She gets new outfits she still has a wetsuit but it looks different. There is a another person you can play his name is Kurtis Trent and he wants REVENGE on the dude who KILLED his father. It is on the PS2. There are better graphics. It has a better storyline. She has HAND TO HAND COMBAT in it AND SHE LOOKS SO COOL AND SEXY!!! BUT DO NOT BUT IT AT AMAZON.COM IT COMES OUT JUNE 18 AT THE FRISCO MALL BUY IT THERE!BECAUSE IT COMES OUT JUNE 20 AT AMAZON.COM THIS GAME ROCKS!!!!!!!!!!!')
where alias <> 'blank'
order by alias

-- ZD 3
ALTER TEXT SEARCH CONFIGURATION bs52494
ALTER MAPPING FOR asciiword, word
WITH english_stem, pg_catalog.simple

SELECT *
FROM
ts_debug('bs52494', 'Hello Blaž, this are the words')
WHERE alias <> 'blank'

--ZD 4
CREATE TEXT SEARCH DICTIONARY bs52494Syn
  (TEMPLATE = synonym,
  SYNONYMS = bs52494Syn);

--ZD 5
ALTER TEXT SEARCH CONFIGURATION bs52494
ALTER MAPPING FOR asciiword, word
WITH bs52494Syn, english_stem, pg_catalog.simple

SELECT *
FROM
ts_debug('bs52494', '"Očito" means "obvious" in Croatian')
WHERE alias <> 'blank'

--ZD 6
SELECT * from reviews
WHERE TO_tsVector('bs52494', summary)
@@
plainTO_tsquery('bs52494', 'Playing game was an enjoyment');;

Iz rezultata ovog upita (prvi dio na priloženom screenshotu) vidljivo je da su pronađene riječi koje imaju isti normalizirani oblik kao one u upitu, ali nisu iste riječi (enjoyable, play).

SELECT * from reviews
WHERE TO_tsVector('bs52494', text)
@@
phraseto_tsquery('bs52494', 'very nice game');

Drugi dio priloženog screenshota pokazuje pronađen rezultat u pretraživanju fraze "very nice game".

SELECT * from reviews
WHERE TO_tsVector('bs52494', text)
@@
to_tsQuery('bs52494', 'overall <4> experience')

U zadnjem dijelu screenshota vidi se pronađen rezultat gdje su tražene riječi međusobno udaljene za N mjesta.

--ZD 7
ALTER TABLE reviews
ADD allTSV varchar

UPDATE reviews
SET allTSV = setweight(to_tsvector('english', title), 'A') ||
             setweight(to_tsvector('english', summary), 'B') ||
             setweight(to_tsvector('english', text), 'C')

SELECT ts_rank(TO_tsVector(summary), query) AS rank, title, summary, text
FROM reviews, plainTo_tsquery('Grand theft auto') query
WHERE query @@ TO_tsVector(summary)
ORDER BY rank DESC
LIMIT 10;

SELECT ts_rank(TO_tsVector(title), query) AS rank, title, summary, text
FROM reviews, plainTo_tsquery('Grand theft auto') query
WHERE query @@ TO_tsVector(title)
ORDER BY rank DESC
LIMIT 10;

--ZD 8
SELECT ts_rank(to_tsvector('Grand Theft Auto: The Trilogy (Grand Theft Auto / Grand Theft Auto: Vice City / Grand Theft Auto: San Andreas)'),
to_tsquery('grand & theft'));

SELECT ts_rank(to_tsvector('Grand Theft Auto IV'),
to_tsquery('grand & theft'));

SELECT ts_rank(to_tsvector('Grand Theft Auto: The Trilogy (Grand Theft Auto / Grand Theft Auto: Vice City / Grand Theft Auto: San Andreas)'),
to_tsquery('grand & theft'), 2);

SELECT ts_rank(to_tsvector('Grand Theft Auto IV'),
to_tsquery('grand & theft'), 2);


--ZD 10

CREATE INDEX text_trigram_idx ON reviews USING gist(text gist_trgm_ops); 

EXPLAIN ANALYZE
    SELECT * from reviews
	WHERE TO_tsVector('english', text)
	@@www
	plainTO_tsquery('english', 'Excellent and very nice video game');