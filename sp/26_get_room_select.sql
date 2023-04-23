CREATE PROCEDURE get_rooms_select(
)

BEGIN

	select r.id , r.`number` from api_room r;

EN