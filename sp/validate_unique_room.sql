CREATE PROCEDURE validate_unique_room(in _room int)
BEGIN
    select exists( select id from api_room r where r.number  = _room) not_unique;
END