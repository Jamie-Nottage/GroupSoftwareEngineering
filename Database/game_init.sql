DROP SCHEMA IF EXISTS GAME_DATABASE;
CREATE SCHEMA GAME_DATABASE;
USE GAME_DATABASE;

CREATE TABLE IF NOT EXISTS Tutor(
`tutorId` INT AUTO_INCREMENT NOT NULL,
`title` VARCHAR(4) NOT NULL,
`fName` VARCHAR(50) NOT NULL,
`lName` VARCHAR(50) NOT NULL,
PRIMARY KEY (`tutorId`),
UNIQUE (`title`,`fName`,`lName`)
);

CREATE TABLE IF NOT EXISTS Paths(
`pathId` INT AUTO_INCREMENT NOT NULL,
`noOfBuildings` INT NOT NULL,
PRIMARY KEY (`pathId`)
);

CREATE TABLE IF NOT EXISTS Team(
`teamId` INT AUTO_INCREMENT NOT NULL,
`teamName` VARCHAR(50) NOT NULL,
`tutorId` INT NOT NULL,
`pathId`INT NOT NULL,
PRIMARY KEY (`teamId`),
FOREIGN KEY (`tutorId`) REFERENCES Tutor(`tutorId`),
FOREIGN KEY (`pathId`) REFERENCES Paths(`pathId`)
);

CREATE TABLE IF NOT EXISTS Users(
`userId` INT AUTO_INCREMENT NOT NULL,
`fName` VARCHAR(50) NOT NULL,
`lName` VARCHAR(50) NOT NULL,
`emailAddress` VARCHAR(255) NOT NULL,
`username` VARCHAR(50) NOT NULL UNIQUE,
`password` VARCHAR(255) NOT NULL,
`tutorId` INT NOT NULL,
`teamId` INT NOT NULL,
PRIMARY KEY (`userID`),
FOREIGN KEY (`tutorId`) REFERENCES Tutor(`tutorId`),
FOREIGN KEY (`teamId`) REFERENCES Team(`teamId`),
UNIQUE (`fName`, `lName`, `emailAddress`)
);

CREATE TABLE IF NOT EXISTS Gamekeeper(
`gamekeeperId` INT AUTO_INCREMENT NOT NULL,
`fName` VARCHAR(50) NOT NULL,
`lName` VARCHAR(50) NOT NULL,
`emailAddress` VARCHAR(255) NOT NULL,
`username` VARCHAR(50) NOT NULL UNIQUE,
`password` VARCHAR(255) NOT NULL,
PRIMARY KEY (`gamekeeperId`),
UNIQUE (`fName`, `lName`, `emailAddress`)
);

CREATE TABLE IF NOT EXISTS Building(
`buildingId` INT AUTO_INCREMENT NOT NULL,
`buildingName` VARCHAR(100) NOT NULL,
`verificationCode` VARCHAR(100) NOT NULL UNIQUE,
`imageSource` VARCHAR(50) NOT NULL,
`latitude` VARCHAR(50) NOT NULL,
`longitude` VARCHAR(50) NOT NULL,
PRIMARY KEY (`buildingId`),
UNIQUE(`longitude`, `latitude` )
);

CREATE TABLE IF NOT EXISTS Task(
`taskId` INT AUTO_INCREMENT NOT NULL,
`title` VARCHAR(50) NOT NULL,
`points` INT NOT NULL,
`description` VARCHAR(255) NOT NULL,
`buildingId` INT NOT NULL,
`required` TINYINT NOT NULL,
PRIMARY KEY (`taskId`),
FOREIGN KEY (`buildingId`) REFERENCES Building(`buildingId`)
);

CREATE TABLE IF NOT EXISTS Clue(
`clueLevel` INT AUTO_INCREMENT NOT NULL,
`description` VARCHAR(255) NOT NULL,
`pointsDeducted` INT NOT NULL,
PRIMARY KEY (`clueLevel`)
);

CREATE TABLE IF NOT EXISTS Score(
`scoreId` INT AUTO_INCREMENT NOT NULL,
`clueLevel` INT DEFAULT 1,
`taskId` INT NOT NULL,
`teamId` INT NOT NULL,
FOREIGN KEY (`clueLevel`) REFERENCES Clue(`clueLevel`),
FOREIGN KEY (`taskId`) REFERENCES Task(`taskId`),
FOREIGN KEY (`teamId`) REFERENCES Team(`teamId`),
PRIMARY KEY (`scoreId`),
UNIQUE(`teamId`, `taskId`,`clueLevel`)
);

CREATE TABLE IF NOT EXISTS UsersScore(
`userscoreId` INT AUTO_INCREMENT NOT NULL,
`clueLevel` INT DEFAULT 1,
`completed` INT NOT NULL DEFAULT 0,
`taskId` INT NOT NULL,
`userId` INT NOT NULL,
FOREIGN KEY (`clueLevel`) REFERENCES Clue(`clueLevel`),
FOREIGN KEY (`taskId`) REFERENCES Task(`taskId`),
FOREIGN KEY (`userId`) REFERENCES Users(`userId`),
PRIMARY KEY (`userscoreId`),
UNIQUE(`userscoreId`, `userId`,`clueLevel`)
);

CREATE TABLE IF NOT EXISTS BuildingClue(
`clueId` INT AUTO_INCREMENT NOT NULL,
`clue` VARCHAR(255) NOT NULL, 
`buildingId` INT NOT NULL,
`clueLevel` INT NOT NULL,
PRIMARY KEY (`clueId`),
FOREIGN KEY (`buildingId`) REFERENCES Building(`buildingId`),
FOREIGN KEY (`clueLevel`) REFERENCES Clue(`clueLevel`),
UNIQUE(`clueLevel`, `buildingId`)
);

CREATE TABLE IF NOT EXISTS Used(
`clueId` INT NOT NULL, 
`teamId` INT NOT NULL, 
PRIMARY KEY (`clueId`, `teamId`),
FOREIGN KEY (`clueId`) REFERENCES BuildingClue(`clueId`),
FOREIGN KEY (`teamId`) REFERENCES Team(`teamId`),
UNIQUE(`clueId`, `teamId`)
);

CREATE TABLE IF NOT EXISTS Answers(
`taskId` INT NOT NULL,
`answer` VARCHAR(50) NOT NULL,
`correct` INT NOT NULL,
PRIMARY KEY(`taskId`, `answer`),
UNIQUE(`taskId`, `answer`, `correct`)
);

-- RELATIONSHIP ATTRICBUTES --
CREATE TABLE IF NOT EXISTS VisitBuilding(
`buildingId` INT NOT NULL,
`teamId` INT NOT NULL,
`time` DATETIME NOT NULL,
PRIMARY KEY(`buildingId`, `teamId`, `time`),
FOREIGN KEY (`buildingId`) REFERENCES Building(`buildingId`),
FOREIGN KEY (`teamId`) REFERENCES Team(`teamId`)
);

CREATE TABLE IF NOT EXISTS Route(
`pathId` INT NOT NULL,
`buildingId` INT NOT NULL,
`stopNo` INT NOT NULL,
PRIMARY KEY(`buildingId`, `pathId`,`stopNo`),
FOREIGN KEY (`buildingId`) REFERENCES Building(`buildingId`),
FOREIGN KEY (`pathId`) REFERENCES Paths(`pathId`)
);

-- CREATING VIEWS --

-- ACHIEVEMENT DETAILS --

CREATE OR REPLACE VIEW achievementdetails AS

SELECT T1.taskId, T1.answer, T1.correct, T2.description, T2.points, T2.buildingId FROM 
(SELECT * FROM Answers) AS T1
	JOIN
(SELECT * FROM Task) AS T2
ON T1.taskId=T2.taskId;

-- INDIVIDUAL SCORE --

CREATE OR REPLACE VIEW individualLeaderboard AS

SELECT DISTINCT username, sum(totalPoints) AS score FROM
(SELECT users.username, users.pointsDeducted, tasks.points, (SELECT tasks.points - users.pointsDeducted) AS totalPoints FROM 
(SELECT clues.pointsDeducted, clues.taskId, u.username FROM
	(SELECT c.clueLevel,c.pointsDeducted, s.taskId, s.userId FROM
		(SELECT cl.clueLevel, cl.pointsDeducted FROM Clue cl) AS c
			JOIN
		(SELECT sc.taskId, sc.userId, sc.clueLevel FROM UsersScore sc) AS s
			ON c.clueLevel=s.clueLevel) AS clues
				JOIN
			(SELECT us.userId, us.username FROM Users us) AS u
				ON u.userId=clues.userId) AS users
					JOIN
				(SELECT ts.taskId, ts.points FROM Task ts) AS tasks
                ON tasks.taskId=users.taskId) AS score
GROUP BY username
ORDER BY score DESC;

-- CLUE DETAILS --
    
CREATE OR REPLACE VIEW usedclues AS

SELECT T2.clueId, T1.buildingId, T1.clueLevel, T2.teamId FROM
	(SELECT * FROM BuildingClue) AS T1
		JOIN
	(SELECT * FROM Used) AS T2
	ON  T1.clueId = T2.clueId;

-- VISITED --

CREATE OR REPLACE VIEW visited AS

SELECT T1.buildingId, T1.teamId, T2.buildingName, T2.latitude, T2.longitude, T1.time, T2.imageSource FROM
	(SELECT * FROM VisitBuilding) AS T1
		JOIN
	(SELECT buildingName, buildingId, imageSource, latitude, longitude FROM Building) AS T2
ON T1.BuildingId=T2.BuildingId
ORDER BY time DESC;

-- LEADERBORD --

CREATE OR REPLACE VIEW leaderboard AS

SELECT DISTINCT teamName, sum(totalPoints) AS score FROM
(SELECT teams.teamName, teams.pointsDeducted, tasks.points, (SELECT tasks.points - teams.pointsDeducted) AS totalPoints FROM 
(SELECT clues.pointsDeducted, clues.taskId, t.teamName FROM
	(SELECT c.clueLevel,c.pointsDeducted, s.taskId, s.teamId FROM
		(SELECT cl.clueLevel, cl.pointsDeducted FROM Clue cl) AS c
			JOIN
		(SELECT sc.taskId, sc.teamId, sc.clueLevel FROM Score sc) AS s
			ON c.clueLevel=s.clueLevel) AS clues
				JOIN
			(SELECT tm.teamId, tm.teamName FROM Team tm) AS t
				ON t.teamId=clues.teamId) AS teams
					JOIN
				(SELECT ts.taskId, ts.points FROM Task ts) AS tasks
                ON tasks.taskId=teams.taskId) AS score
GROUP BY teamName
ORDER BY score DESC;

-- ROUTES --

CREATE OR REPLACE VIEW Routes AS

SELECT r.pathId, b.buildingName, r.stopNo, b.latitude, b.longitude FROM
	(SELECT * FROM Route) AS r
		JOIN
	(SELECT bl.buildingId, bl.buildingName, bl.latitude, bl.longitude FROM Building bl) AS b
	ON b.buildingId=r.buildingId;

    
-- FULL TASKS AND DESCRIPTIONS --

CREATE OR REPLACE VIEW TaskDescriptions AS

SELECT tasks. description, tasks.points, buildings.buildingName, tasks.required  FROM 
	(SELECT t.taskId, t.points, t.description, t.buildingId, t.required FROM Task t) AS tasks
		JOIN
	(SELECT b.buildingId, b.buildingName FROM Building b) AS buildings
	ON buildings.buildingId=tasks.buildingId;
    
-- DISPLAY --

CREATE OR REPLACE VIEW display AS

SELECT addclue.teamId, addclue.buildingName, addclue.time, addclue.imageSource, (SELECT addclue.points - clues.pointsDeducted) AS pointsEarned FROM
	(SELECT addtask.clueLevel, addtask.taskId, addtask.teamId, addtask.buildingName, addtask.time, addtask.imageSource, points.points FROM
		(SELECT score.clueLevel, score.taskId, score.teamId, visit.buildingName, visit.time, visit.imageSource FROM
			(SELECT * FROM Score) as score
			JOIN
			(SELECT * FROM visited) as visit
			ON score.teamId = visit.teamId) AS addtask
		JOIN
		(SELECT taskId, points FROM Task) as points 
		ON points.taskId=addtask.taskId) addclue
	JOIN
	(SELECT * FROM Clue) as clues
	ON clues.clueLevel=addclue.clueLevel
ORDER BY addclue.time DESC;

-- INSERTING DATA --

INSERT INTO Tutor VALUES
(NULL, 'Dr', 'Matthew', 'Collison'),
(NULL, 'Prof', 'Jonathon', 'Fieldsend'),
(NULL, 'Prof', 'Ronaldo', 'Menezes'),
(NULL, 'Dr', 'David', 'Wakeling');

INSERT INTO Paths VALUES
(NULL, 6),
(NULL, 6),
(NULL, 6),
(NULL, 6);

INSERT INTO Team VALUES
(NULL, 'Team Matthew Collison', 1, 1),
(NULL, 'Team Jonathon Fieldsend', 2, 2),
(NULL, 'Team Ronaldo Meenezes', 3, 3),
(NULL, 'Team David Wakeling', 4, 4);

INSERT INTO Users VALUES
(NULL, 'Name1', 'Surname1', 'email1', 'username1', 'password1', 1, 1),
(NULL, 'Name2', 'Surname2', 'email2', 'username2', 'password2', 1, 1),
(NULL, 'Name3', 'Surname3', 'email3', 'username3', 'password3', 2, 2),
(NULL, 'Name4', 'Surname4', 'email4', 'username4', 'password4', 3, 3);

INSERT INTO Gamekeeper VALUES
(NULL, 'Admin','Admin', 'admin@exeter.ac.uk', 'admin', '$5$rounds=535000$3IcTOWDMczSjIhYl$5cS5hqZ8zQzfN3zMzBpSuBIg0I242UJ8qmFMZNmFPb9');

INSERT INTO Building VALUES
(NULL, 'Devonshire House', 'code1', 'devonshirehouse.png', '50.735167', '-3.534269'),
(NULL, 'Queens', 'code2', 'queens.png', '50.734044', '-3.535082'),
(NULL, 'Harrison', 'code3', 'harrison.png', '50.737739', '-3.532628'),
(NULL, 'Innovation Centre', 'code4', 'innovation-grey.png', '50.738506', '-3.531004'),
(NULL, 'Streatham Court', 'code5', 'streathamcourt.png', '50.73567', '-3.530897'),
(NULL, 'Forum', 'code6', 'forum-grey.jpg', '50.735459', '-3.533207');

INSERT INTO Task VALUES
(NULL, 'N/A', 150, 'Find Devonshire House', 1, 1),
(NULL, 'Bye, bye Miss Exeter Pie ', 75, 'Which is NOT a flavour of pie at the Pieminister truck?', 1, 0),
(NULL, 'HOW MUCH ???', 50, 'How much do curly fries cost at The Ram?', 1, 0),
(NULL, 'Study Heaven', 50, 'Which Floor is The Loft located on?', 1, 0),
(NULL, 'N/A', 150, 'Locate Queens', 2, 1),
(NULL, 'Boujie Student', 75, 'What’s the price of a large cappuccino from Camper coffee in Queens?', 2, 0),
(NULL, 'N/A', 200, 'Locate Harrison', 3, 1),
(NULL, 'Listen to me I am cultured', 50, 'How much is a Cornish pasty at the Harrison café?', 3, 0),
(NULL, 'Im just getting a drink', 75, 'What floor is the cold water only bottle filler onin Harrison? ', 3, 0),
(NULL, 'Dont put a spoon in the works', 50, 'There is a microwave and hot water point around the corner from the Harrison café.', 3, 0),
(NULL, 'N/A', 250, 'Locate The Innovation Centre', 4, 1),
(NULL, 'Lovelace would be proud', 50, 'What colour seat cushions do the chairs in the Lovelace computer lab have?', 4, 0),
(NULL, 'Onde?', 75, 'What is the room number of Ronaldo Menezes’s office?', 4, 0),
(NULL, 'N/A', 150, 'Locate Streatham Court', 5, 1),
(NULL, '011001101', 50, 'What is the room number of Lecture Theatre A in Streatham Court?', 5, 0),
(NULL, 'N/A', 100, 'Locate The Forum', 6, 1),
(NULL, 'Book Worm', 75, 'What is the title of the book with identifier 001.6425 COC?', 6, 0),
(NULL, 'Student Budget', 50, 'How much is cheapest coffee from the Marketplace?', 6, 0),
(NULL, 'WhErE?', 50, 'Where is the Study Zone?', 6, 0);

INSERT INTO Clue VALUES
(NULL, 'Full marks', 0),
(NULL, 'Click here for a text clue', 25),
(NULL, 'Click here for an image clue', 75),
(NULL, 'Click here for a clue on the map', 100),
(NULL, 'achievement try 1', 20),
(NULL, 'achievement try 2', 40);

INSERT INTO Answers VALUES
(2, 'Heidi', 0),
(2, 'Ollie', 1),
(2, 'Kevin', 0),
(3, '£2.25', 1),
(3, '£2.50', 0),
(3, '£2.15', 0),
(4, 'First Floor', 0),
(4, 'Third Floor', 1),
(4, 'Second Floor', 0),
(6, '£2.20', 0),
(6, '£2.60', 0),
(6, '£2.80', 1),
(8, '£2.60', 0),
(8, '£2.35', 1),
(8, '£3.00', 0),
(9, 'Ground Floor', 0),
(9, 'First Floor', 0),
(9, 'Second Floor', 1),
(10, 'True', 1),
(10, 'False', 0),
(12, 'Red', 0),
(12, 'Blue', 1),
(12, 'Green', 0),
(13, 'B1C', 1),
(13, 'A1A', 0),
(13, 'B1B', 0),
(15, '0.02', 0),
(15, '0.04', 0),
(15, '0.01', 1),
(17, 'Software Development in C++', 0),
(17, 'Agile Software Development', 1),
(17, 'Software Engineering Principles', 0),
(18, '£1', 1),
(18, '£1.20', 0),
(18, '£1.50', 0),
(19, 'The basement', 0),
(19, 'The top floor', 0),
(19, 'Behind the SID', 1);

INSERT INTO BuildingClue VALUES
(NULL,'Attached to the Forum, make your way to where the Guild President works', 1, 2),
(NULL,'Next to the Student’s Guild, full of classrooms, you’re looking for Lecture Theatre 2', 2, 2),
(NULL,'Walk up Forum hill and turn right down North Park Road, find the front desk at the main entrance', 3, 2),
(NULL,'Up the hill from Harrison, big white building. Walk across the bridge and find the computer labs', 4, 2),
(NULL,'Near the main entrance to the University, off of Rennes Drive. Find a water fountain', 5, 2),
(NULL,'Center of campus, up the steep hill from the campus main entrance. Locate the big white desk on the main floor', 6, 2),
(NULL, 'devonshirehouse.png', 1, 3),
(NULL, 'queens.png', 2, 3),
(NULL, 'harrison.png', 3, 3),
(NULL, 'innovation-grey.png', 4, 3),
(NULL, 'streathamcourt.png', 5, 3),
(NULL, 'forum-grey.jpg', 6, 3);

INSERT INTO Route VALUES
(1,6,1),
(1,1,2),
(1,2,3),
(1,3,4),
(1,4,5),
(1,5,6),
-- route 2
(2,6,1),
(2,5,2),
(2,4,3),
(2,3,4),
(2,2,5),
(2,1,6),
-- route 3
(3,6,1),
(3,5,2),
(3,2,3),
(3,1,4),
(3,3,5),
(3,4,6),
-- route 4
(4,6,1),
(4,2,2),
(4,5,3),
(4,4,4),
(4,3,5),
(4,2,6);

select pathId from Paths order by pathId DESC LIMIT 1