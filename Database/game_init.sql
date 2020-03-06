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
`imageSource` VARCHAR(50),
PRIMARY KEY (`buildingId`)
);

CREATE TABLE IF NOT EXISTS Task(
`taskId` INT AUTO_INCREMENT NOT NULL,
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
UNIQUE(`teamId`, `taskId`)
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

-- CLUE DETAILS --
    
CREATE OR REPLACE VIEW usedclues AS

SELECT T2.clueId, T1.buildingId, T1.clueLevel, T2.teamId FROM
	(SELECT * FROM BuildingClue) AS T1
		JOIN
	(SELECT * FROM Used) AS T2
	ON  T1.clueId = T2.clueId;

-- VISITED --

CREATE OR REPLACE VIEW visited AS

SELECT T1.buildingId, T1.teamId, T2.buildingName, T1.time, T2.imageSource FROM
	(SELECT * FROM VisitBuilding) AS T1
		JOIN
	(SELECT buildingName, buildingId, imageSource FROM Building) AS T2
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

SELECT r.pathId, b.buildingName, r.stopNo FROM
	(SELECT * FROM Route) AS r
		JOIN
	(SELECT bl.buildingId, bl.buildingName FROM Building bl) AS b
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
(NULL, 'group','o', 'groupO@exeter.ac.uk', 'root', '4813494d137e1631bba301d5acab6e7bb7aa74ce1185d456565ef51d737677b2');

INSERT INTO Building VALUES
(NULL, 'Devonshire House', 'code1', 'devonshirehouse.png'),
(NULL, 'Queens', 'code2', 'queens.png'),
(NULL, 'Harrison', 'code3', 'harrison.png'),
(NULL, 'Innovation Centre', 'code4', 'innovation-grey.png'),
(NULL, 'Streatham Court', 'code5', 'streathamcourt.png'),
(NULL, 'Forum', 'code6', 'forum-grey.jpg');

INSERT INTO Task VALUES
(NULL, 150, 'Find Devonshire House', 1, 1),
(NULL, 75, 'Grab a seat in The Loft', 1, 0),
(NULL, 75, 'Find the hot water point in DH2', 1, 0),
(NULL, 25, 'Locate the drama room', 1, 0),
(NULL, 25, 'Find the Pieminister truck', 1, 0),
(NULL, 50, 'Order curly fries at The Ram', 1, 0),
(NULL, 150, 'Locate Queens', 2, 1),
(NULL, 75, 'Locate LT2', 2, 0),
(NULL, 50, 'Buy a coffee at Costa', 2, 0),
(NULL, 25, 'Find a place to study', 2, 0),
(NULL, 200, 'Locate Harrison', 3, 1),
(NULL, 75, 'Visit the Harrison Info Point', 3, 0),
(NULL, 75, 'Find the microwave and hot water point', 3, 0),
(NULL, 50, 'Buy a pasty at cafe', 3, 0),
(NULL, 250, 'Locate The Innovation Centre', 4, 1),
(NULL, 100, 'Visit the Lovelace and Babbage rooms', 4, 0),
(NULL, 50, 'Login to a Linux machine', 4, 0),
(NULL, 100, 'Visit Ronaldo Menezes office', 4, 0),
(NULL, 100, 'Locate Streatham Court', 5, 1),
(NULL, 50, 'Visit the fountain', 5, 0),
(NULL, 25, 'Find a place to study', 5, 0),
(NULL, 100, 'Locate The Forum', 6, 1),
(NULL, 50, 'Locate the SID desk', 6, 0),
(NULL, 100, 'Checkout a computer science book from the library', 6, 0),
(NULL, 50, 'Find the cheapest coffee', 6, 0),
(NULL, 25, 'Visit the Study Zone', 6, 0);

INSERT INTO Clue VALUES
(NULL, 'Full marks', 0),
(NULL, 'Click here for a text clue', 10),
(NULL, 'Click here for an image clue', 20),
(NULL, 'Click here for a clue on the map', 30);

INSERT INTO BuildingClue VALUES
(NULL,'Where you’d grab a pint and meet with the Guild President (attached to the Forum)', 1, 2),
(NULL,'Next to the Student’s Guild, full of classrooms', 2, 2),
(NULL,'Walk up Forum hill and turn right down North Park Road', 3, 2),
(NULL,'Up the hill from Harrison, big white building', 4, 2),
(NULL,'Near the main entrance to the University. Off of Rennes Drive', 5, 2),
(NULL,'Center of campus, up the steep hill from the campus main entrance', 6, 2),
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
