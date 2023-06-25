CREATE PROCEDURE get_last_banners()
BEGIN 
     select ab.image from api_banners ab where ab.status = 1 order by created_at desc limit 10;
END