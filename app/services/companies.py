from models.companies import Companies

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