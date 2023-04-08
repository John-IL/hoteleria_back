CREATE PROCEDURE `get_data_user_for_email`(
            in _email varchar(255)
            )
BEGIN
    
    declare _user_id int;
            
    SELECT id into _user_id from api_userprofile up  where email = _email;
            
                        SELECT up.id user_id,
                        up.is_active,
                        up.role_id,
                        up.document_type_id,
                        up.document_number,
                        up.phone,
                        up.is_staff,
                        concat(up.first_name, ' ', up.last_name) full_name,
                        if(up.is_staff = 1, 'ADMIN', r.name) role_name,
                        mo.arrModuls arr_modules,
                        us2.arrSections arr_sections,
                        up.email,
                        up.first_name,
                        up.last_name
                        FROM api_userprofile up
                        LEFT JOIN
                        (SELECT um.user_id, 
                             json_arrayagg(json_object('id_module', um.id, 'module_name', um.name , 'icons', um.icons, 'route_name',um.route_name)) arrModuls from 
                             api_userprofile u 
                             left join (select DISTINCT  m.id id, m.name name, m.icons icons, m.route route_name, us.user_id user_id from api_usersections us
                             left join api_modulesections ms on ms.id = us.module_section_id
                             left join api_modules m on m.id = ms.module_id 
                             where us.user_id =_user_id GROUP by 1 ) um on um.user_id = u.id
                             WHERE u.id=_user_id
                             GROUP by 1) mo
                        ON mo.user_id = up.id
                        LEFT JOIN
                        (SELECT ms2.user_id, 
                             json_arrayagg(json_object('section_id', ms2.section_id, 'title', ms2.name ,'route',ms2.route, 'icon',ms2.icon, 'is_new', ms2.is_new,'module_id', ms2.module_id,'user_id', ms2.user_id)) arrSections from 
                             api_userprofile u 
                             left join (select DISTINCT ms.section_id section_id, s.name, CONCAT(m.route,"-",s.route) route,s.icon icon, s.is_new is_new, ms.module_id module_id, us.user_id user_id FROM api_usersections us
                             left join api_modulesections ms on ms.id = us.module_section_id
                             left join api_modules m on m.id = ms.module_id
                             LEFT join api_sections s on s.id = ms.section_id
                             where us.user_id =_user_id ORDER BY 1) ms2 on ms2.user_id = u.id
                             WHERE u.id=_user_id
                         GROUP by 1) us2
                        ON mo.user_id = up.id
                        LEFT JOIN api_roles r
                        ON r.id = up.role_id
                        WHERE email = _email;
end
