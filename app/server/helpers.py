def user_helper(user) -> dict:
    return {
        "UserId": user["UserId"],
        "FirstName": user["FirstName"],
        "LastName": user["LastName"],
        "Email": user["Email"],
        "Skills": [{skill["name"]: skill["year"]} for skill in user["Skills"]]
    }


def vacancy_helper(vacanty) -> dict:
    return {
        "VacancyId": vacanty["VacancyId"],
        "CompanyName": vacanty["CompanyName"],
        "PositionName": vacanty["PositionName"],
        "Salary": vacanty["Salary"],
        "Currency": vacanty["Currency"],
        "VacancyLink": vacanty["VacancyLink"],
        "RequiredSkills": vacanty["RequiredSkills"]
    }