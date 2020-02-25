USE GAME_DATABASE;


-- next stop
SELECT buildingName FROM Building
	WHERE buildingId = (SELECT buildingId FROM Route 
		WHERE stopNo=
			(SELECT stopNo FROM Route 
			WHERE pathId=(SELECT teamId FROM visited WHERE teamId=1 LIMIT 1) 
			AND buildingId=(SELECT buildingId FROM visited WHERE teamId=1 LIMIT 1))+1
		AND pathId=(SELECT teamId FROM visited WHERE teamId=1 LIMIT 1));

-- qr code

SELECT verificationCode FROM Building
WHERE buildingId = (SELECT buildingId FROM Route 
		WHERE stopNo=
			(SELECT stopNo FROM Route 
			WHERE pathId=(SELECT teamId FROM visited WHERE teamId=1 LIMIT 1) 
			AND buildingId=(SELECT buildingId FROM visited WHERE teamId=1 LIMIT 1))+1
		AND pathId=(SELECT teamId FROM visited WHERE teamId=1 LIMIT 1));
    
INSERT INTO VisitBuilding VALUES 
((SELECT buildingId FROM Building WHERE verificationCode='code3'), /*teamId*/1, NOW());

-- leaderboard

SELECT * FROM leaderboard;

-- image for visited

SELECT buildingId, buildingName, time FROM visited;

-- display point earnt from building    

SELECT * FROM display;

SELECT DISTINCT teamId FROM display;

    
-- 


                
                 