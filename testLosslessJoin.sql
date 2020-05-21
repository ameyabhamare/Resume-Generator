/* Natural join MEMBER, SCHOOLING, HIGHER_EDUCATION, DEGREE_INFO, EXPERIENCE, JOB, PROJECTS, SKILLS, ACCOMPLISHMENTS to test for lossless decomposition */

USE CLIENT;

SELECT 
M.MEMBER_ID, M.NAME, M.BIO, M.ADDRESS, M.PHONE, M.EMAIL, 
S.NAME AS SCHOOL, S.LOCATION,
SCH.PASSING_LEVEL, SCH.PASSING_YEAR, SCH.STREAM, SCH.SCORE,
D.DEGREE, D.MAJOR,
H.UNIVERSITY, H.GPA,
J.EMPLOYER, J.LOCATION, J.TITLE, J.DESCRIPTION,
E.DURATION,
P.PROJECT_NAME, P.DESCRIPTION,
SK.SKILL_NAME, SK.EXPERIENCE_LEVEL,
A.ACCOMPLISHMENT_NAME, A.DESCRIPTION
FROM MEMBER M 
INNER JOIN SCHOOLING SCH ON M.MEMBER_ID = SCH.MEMBER_ID
	INNER JOIN SCHOOL S ON SCH.SCHOOL_ID = S.SCHOOL_ID 
INNER JOIN HIGHER_EDUCATION H ON M.MEMBER_ID = H.MEMBER_ID
	INNER JOIN DEGREE_INFO D ON H.DEGREE_ID = D.DEGREE_ID
INNER JOIN EXPERIENCE E ON M.MEMBER_ID = E.MEMBER_ID
	INNER JOIN JOB J ON E.JOB_ID = J.JOB_ID
INNER JOIN PROJECTS P ON M.MEMBER_ID = P.MEMBER_ID
INNER JOIN SKILLS SK ON M.MEMBER_ID = SK.MEMBER_ID
INNER JOIN ACCOMPLISHMENTS A ON M.MEMBER_ID = A.MEMBER_ID;