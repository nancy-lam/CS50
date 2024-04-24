-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Look at the crime_scene_reports that matches the date the CS50 Duck was stolen

SELECT *
FROM crime_scene_reports
WHERE year = 2023
AND month = 7
AND day = 28
AND street = 'Humphrey Street';

-- From the description, we know that there were witnesses so next we will look at the transcripts from the interviews table

SELECT name, transcript
FROM interviews
WHERE year = 2023
AND month = 7
AND day = 28
AND transcript LIKE '%bakery%';

-- Based on the transcript, the thieft got into a car, withdrew money from an ATM and planned to take the earliest flight tomorrow

-- Check the video footage to get name and phone number of car exiting out the parking lot around the time the duck was stolen

SELECT DISTINCT(name), phone_number, passport_number
FROM people
JOIN bakery_security_logs
ON bakery_security_logs.license_plate = people.license_plate
WHERE year = 2023
AND month = 7
AND day = 28
AND minute BETWEEN 10 AND 25;

-- After narrow down people from the videdo footage to 21 people, we will move forward with anothe clue from the transcript interview to find  alist of people withdrew money from the ATM

SELECT name
FROM people
JOIN bank_accounts
ON people.id = bank_accounts.person_id
JOIN atm_transactions
ON bank_accounts.account_number = atm_transactions.account_number
WHERE year = 2023
AND month = 7
AND day = 28
AND atm_location = 'Leggett Street'
AND transaction_type = 'withdraw';

-- Compare this list with the video footage list, we have 4 suspicious people: Bruce, Diana, Iman and Luca

-- Based on the third clue, the thieft called someone less than a minute

SELECT name FROM people
JOIN phone_calls
ON people.phone_number = phone_calls.caller
WHERE year = 2023
AND month = 7
AND day = 28
AND duration < 60;

-- We narrow down to Bruce and Diana. Next we will check the passengers for the flight out of Fiftyville tomorrow

SELECT name
FROM people
JOIN passengers
ON people.passport_number = passengers.passport_number
JOIN flights
ON passengers.flight_id = flights.id
JOIN airports
ON flights.origin_airport_id = airports.id
WHERE airports.city = 'Fiftyville'
AND year = 2023
AND month = 7
AND day = 29
ORDER BY hour, minute LIMIT 10;

-- We see Bruce on the list so the thieft is Bruce

SELECT city
FROM airports
JOIN flights
ON airports.id = destination_airport_id
JOIN passengers
ON flights.id = passengers.flight_id
JOIN people
ON passengers.passport_number = people.passport_number
WHERE people.name = 'Bruce';

-- Bruce escaped to New York City

-- To check for Who the thief’s accomplice is who helped Bruce escape, we will run the following codes:

SELECT name
FROM people
WHERE phone_number IN
(
    SELECT receiver
    FROM phone_calls
    WHERE year = 2023
    AND month = 7
    AND day = 28
    AND caller =
        (SELECT phone_number
        FROM people
        WHERE name = 'Bruce')
    AND duration < 60
);

And it's Robin









