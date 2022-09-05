from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Сategory, Income, Spending
from django.db.models import Sum


def index(request):

    if request.method == 'POST':

        opr_type = request.POST.get("type")
        amount = request.POST.get("amount")
        cat_id = request.POST.get("category")

        if opr_type == "income":
            record = Income(amount=amount, category_id=Сategory.objects.get(id=cat_id))

        elif opr_type == "spending":
            record = Spending(amount=amount, category_id=Сategory.objects.get(id=cat_id))

        date_input = request.POST.get("date")
        if date_input:
            record.create_date = date_input

        record.save()
        message = f"Запис з новою операцією успішно додано"
        return render(request, 'countfin/messages.html', {"message": message})

    categories_list = Сategory.objects.order_by('name')

    return render(request, 'countfin/index.html', {"category_list": categories_list})

def edit(request):
    if request.method == 'POST':

        new_cat = request.POST.get("category_name")
        if new_cat:
            if not Сategory.objects.filter(name=new_cat):
                new_category = Сategory(name=new_cat)
                new_category.save()
                #message = f"Категорія успішно додана"
                #return render(request, 'countfin/messages.html', {"message": message})
                return redirect("edit")
        
        cat_id = request.POST.get("category")
        if cat_id:
            Сategory.objects.filter(id=cat_id).delete()
            return redirect("edit")
            #message = f"Категорія успішно видалена"
            #return render(request, 'countfin/messages.html', {"message": message})
        

    categories_list = Сategory.objects.order_by('name')

    return render(request, 'countfin/edit-categories.html', {"category_list": categories_list})

def report(request):

    inc_id = request.GET.get('record_income')
    if inc_id:
        Income.objects.filter(id=inc_id).delete()
        return redirect('report')

    spd_id = request.GET.get('record_spend')
    if spd_id:
        Spending.objects.filter(id=spd_id).delete()
        return redirect('report')
    
    categories_list = Сategory.objects.order_by('name')

    income = Income.objects.order_by("amount")
    spending = Spending.objects.order_by("amount")

    sum_inc = income.aggregate(amount = Sum('amount'))["amount"]
    sum_inc = sum_inc if sum_inc else 0

    sum_spend = spending.aggregate(amount = Sum('amount'))["amount"]
    sum_spend  = sum_spend if sum_spend else 0

    balance = sum_inc - sum_spend

    if request.method == 'POST':
        start_date = request.POST.get("from_date")
        end_date = request.POST.get("to_date")

        #if cat_id:
            #res = Income.objects.filter(category_id=cat_id).order_by("amount")
            #res = ' ,'.join(res)
            #return HttpResponse(f"{cat_id }")
            #income_cat = Income.objects.filter(category_id=cat_id).order_by("amount")
            #spending_cat = Spending.objects.filter(category_id=cat_id).order_by("amount")
    

        if start_date and end_date:
            income = income.filter(create_date__range=(start_date, end_date)).order_by("amount")
            spending = spending.filter(create_date__range=(start_date, end_date)).order_by("amount")

            sum_inc = Income.objects.filter(create_date__range=(start_date, end_date)).aggregate(amount = Sum('amount'))["amount"]
            sum_inc = sum_inc if sum_inc else 0
            
            sum_spend = Spending.objects.filter(create_date__range=(start_date, end_date)).aggregate(amount = Sum('amount'))["amount"]
            sum_spend  = sum_spend if sum_spend else 0

            balance = sum_inc - sum_spend
         
    values = {  
                "category_list": categories_list,
                "income": income, 
                "spending": spending,
                "sum_inc": sum_inc, 
                "sum_spend": sum_spend,
                "balance": balance
            }
 
    return render(request, 'countfin/report.html', values)

def messages(request):
    message = "Empty"
    return render(request, 'countfin/messages.html', {"message": message})








