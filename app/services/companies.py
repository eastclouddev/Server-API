from models.companies import Companies

from logging import getLogger
logger = getLogger("uvicorn.app")

def create_companies_list(found_companies):

    companies_list = []

    for company in found_companies:
        one_company = {
            "company_id": company.id,
            "name": company.name,
            "prefecture": company.prefecture,
            "city": company.city,
            "town": company.town,
            "address": company.address,
            "postal_code": company.postal_code,
            "phone_number": company.phone_number,
            "email": company.email,
            "created_at": company.created_at.isoformat()
        }

        companies_list.append(one_company)

    return {"companies":companies_list}

def cereate_users_list(role, found_user):

    users_list = []

    for user in found_user:
        user_personal = {
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": role,
            "last_login": user.last_login.isoformat()
        }
        users_list.append(user_personal)
    
    return {"users": users_list}