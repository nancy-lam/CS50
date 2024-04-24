-- In 13.sql, write a SQL query to list the names of all people who starred in a movie in which Kevin Bacon also starred.

SELECT DISTINCT people.name FROM people
JOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id
JOIN stars AS s2 ON movies.id = s2.movie_id
JOIN people AS p2 ON s2.person_id = p2.id
WHERE p2.name = 'Kevin Bacon' AND p2.birth = 1958 AND people.name != 'Kevin Bacon';

