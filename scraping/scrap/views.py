from django.shortcuts import render
import certifi
from django.http import JsonResponse
from bs4 import BeautifulSoup
import requests as r
import json
def content(request):
    response = r.get("https://hprera.nic.in/PublicDashboard/GetFilteredProjectsPV?DistrictList%5B0%5D.Selected=false&DistrictList%5B0%5D.Value=18&DistrictList%5B1%5D.Selected=false&DistrictList%5B1%5D.Value=24&DistrictList%5B2%5D.Selected=false&DistrictList%5B2%5D.Value=20&DistrictList%5B3%5D.Selected=false&DistrictList%5B3%5D.Value=23&DistrictList%5B4%5D.Selected=false&DistrictList%5B4%5D.Value=25&DistrictList%5B5%5D.Selected=false&DistrictList%5B5%5D.Value=22&DistrictList%5B6%5D.Selected=false&DistrictList%5B6%5D.Value=26&DistrictList%5B7%5D.Selected=false&DistrictList%5B7%5D.Value=21&DistrictList%5B8%5D.Selected=false&DistrictList%5B8%5D.Value=15&DistrictList%5B9%5D.Selected=false&DistrictList%5B9%5D.Value=17&DistrictList%5B10%5D.Selected=false&DistrictList%5B10%5D.Value=16&DistrictList%5B11%5D.Selected=false&DistrictList%5B11%5D.Value=19&PlottedTypeList%5B0%5D.Selected=false&PlottedTypeList%5B0%5D.Value=P&PlottedTypeList%5B1%5D.Selected=false&PlottedTypeList%5B1%5D.Value=F&PlottedTypeList%5B2%5D.Selected=false&PlottedTypeList%5B2%5D.Value=M&ResidentialTypeList%5B0%5D.Selected=false&ResidentialTypeList%5B0%5D.Value=R&ResidentialTypeList%5B1%5D.Selected=false&ResidentialTypeList%5B1%5D.Value=C&ResidentialTypeList%5B2%5D.Selected=false&ResidentialTypeList%5B2%5D.Value=M&AreaFrom=&AreaUpto=&SearchText=", verify=False) 
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.select('div[class="col-lg-6"]')[:6]
    details = list()
    for i in data:
         project_name = i.find('span', class_='font-lg fw-600').text
         rera_number = i.find('a').text
         project_type = i.find_all('span')[1].text.strip() 
         phone_number = i.find('i', class_='fa-mobile-alt').find_next('span').text.strip()
         email = i.find('i', class_='fa-at').find_next('span').text.strip()
         address = i.find('i', class_='fa-map-marker-alt').find_next('span').text.strip()
         valid_upto = i.find('div', class_='text-right font-xxs').find('span', class_='text-orange').text.strip()
         data_qs = i.find('a')['data-qs']
         details.append({
             'project_name': project_name,
             'rera_no': rera_number,
             'project_type': project_type,
             'phone_no':phone_number,
             'email': email,
             'address':address,
             'valid_upto': valid_upto,
             'qs': data_qs
         })

    return render(request, 'contents/content.html', {'details':details}) 


def detail(request, qs):
    response = r.get(f"https://hprera.nic.in/Project/ProjectRegistration/PromotorDetails_PreviewPV?qs={qs}", verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    name = soup.find('td', text='Name').find_next_sibling('td').text.strip()
    pan_no = soup.find('td', text='PAN No.').find_next_sibling('td').text.strip()
    gstin_no = soup.find('td', text='GSTIN No.').find_next_sibling('td').find('span').text.strip()
    permanent_address = soup.find('td', text='Permanent Address').find_next_sibling('td').text.strip()
    return render(request, 'contents/detailview.html', {'name':name, 'pan_no':pan_no, 'gstin_no': gstin_no, 'address':permanent_address})

# https://hprera.nic.in/Project/ProjectRegistration/PromotorDetails_PreviewPV?qs=