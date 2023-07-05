CREATE PROCEDURE get_reserves_for_months(IN _start_date date)
BEGIN
    select concat( ac.first_name,' ',ac.last_name) full_name, ac.document_number, ro.`number` nroom, rc.name category, 
	ar.category promotion, ar.start_date, ar.end_date, ap.name methods,ar.cost, ar.discount 
	from api_reservedatedetail ar
	join api_room ro on ro.id = ar.room_id
	join api_roomcategory rc on rc.id = ro.category_id 
	join api_reserve re on re.id = ar.reserve_id
	join api_clients ac on ac.id = re.client_id
	join api_paymentmethods ap on ap.id = re.payment_method_id ;
END