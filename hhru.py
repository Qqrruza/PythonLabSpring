import requests
import json

def fetch_jobs():
    
    api_url = "https://api.hh.ru/vacancies"
    
    request_params = {
        'area': 2,
        'text': '1С',
        'per_page': 7,
        'period': 30
    }
    
    try:
        req = requests.get(api_url, params=request_params)
        result = req.json()
    except:
        print("не удалось получить данные")
        return
    
    all_jobs = result.get('items', [])
    total = result.get('found', 0)
    
    print(f"всего нашлось вакансий: {total}")
    print(f"показываем: {len(all_jobs)}")
    print("=" * 60)
    
    job_list = []
    
    for index, job in enumerate(all_jobs, 1):
        print(f"\n--- ВАКАНСИЯ #{index} ---")
        print(f"{job['name']}")
        print(f"{job['employer']['name']} | {job['area']['name']}")
        
        salary_info = job.get('salary')
        salary_text = "не указана"
        
        if salary_info:
            salary_from = salary_info.get('from')
            salary_to = salary_info.get('to')
            salary_cur = salary_info.get('currency', 'rub')
            
            if salary_from and salary_to:
                salary_text = f"{salary_from} - {salary_to} {salary_cur}"
            elif salary_from:
                salary_text = f"от {salary_from} {salary_cur}"
            elif salary_to:
                salary_text = f"до {salary_to} {salary_cur}"
        
        print(f"зарплата: {salary_text}")
        print(f"требуемый опыт: {job['experience']['name']}")
        print(f"график: {job['employment']['name']}")
        print(f"подробнее: {job['alternate_url']}")
        
        job_item = {
            'position': job['name'],
            'company_name': job['employer']['name'],
            'location': job['area']['name'],
            'payment': salary_text,
            'experience_level': job['experience']['name'],
            'work_type': job['employment']['name'],
            'job_link': job['alternate_url']
        }
        job_list.append(job_item)
    
    final_data = {
        'date': 'сегодня',
        'search': '1С',
        'results_count': total,
        'jobs': job_list
    }
    
    with open('jobs.json', 'w', encoding='utf-8') as file:
        json.dump(final_data, file, ensure_ascii=False, indent=4)
    
    print(f"\nготово! данные сохранены в jobs.json")


if __name__ == "__main__":
    fetch_jobs()