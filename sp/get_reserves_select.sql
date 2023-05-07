CREATE PROCEDURE get_reserves_select(
)

BEGIN

select ar.id  from api_reserve ar;

END