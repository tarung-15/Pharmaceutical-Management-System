from django.shortcuts import render,redirect
from .models import Medicine, Bill
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from .models import Medicine
from django.contrib import messages
from django.utils import timezone 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone  #  Required for date tracking
from .models import Medicine, Bill
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Bill
from django.utils.timezone import localtime
import traceback  # For debugging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Medicine, Bill, BillItem
from django.db import transaction
from django.utils.timezone import localtime
from django.http import HttpResponse
import traceback
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Bill
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from .models import Medicine, Bill, BillItem
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Bill
# Create your views here.
def home(request):
    return render(request, 'core/home.html')

# Signup
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form =CustomUserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

# Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

# Logout
@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

def home(request):
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good Morning"
    elif current_hour < 17:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    return render(request, 'core/home.html', {'greeting': greeting})

#edit
def edit_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        medicine.name = request.POST.get('name')
        medicine.description = request.POST.get('description')
        medicine.quantity = request.POST.get('quantity')
        medicine.price = request.POST.get('price')
        medicine.save()
        return redirect('inventory')
    return render(request, 'core/edit_medicine.html', {'medicine': medicine})

# Add Medicine
def add_medicine(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        Medicine.objects.create(
            name=name,
            description=description,
            quantity=quantity,
            price=price
        )
        return redirect('inventory')
    return render(request, 'core/add_medicine.html')


# Delete Medicine
def delete_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    medicine.delete()
    return redirect('inventory')

@login_required(login_url='/login/')
def inventory_view(request):
    query = request.GET.get('q')
    searched = False
    found = False
    medicines = Medicine.objects.all()

    if query:
        searched = True
        medicines = Medicine.objects.filter(name__icontains=query)
        if medicines.exists():
            found = True
    
    return render(request, 'core/inventory.html', {
        'medicines': medicines,
        'searched': searched,
        'found': found,
        'query': query,
    })

@login_required(login_url='/login/')
def generate_bill(request):
    medicines = Medicine.objects.all()
    context = {'medicines': medicines}

    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        medicine_ids = request.POST.getlist('medicine_ids')  # getlist for multiple select
        quantities_raw = request.POST.getlist('quantities')  # quantities for each selected medicine

        context.update({'patient_name': patient_name})

        if not medicine_ids:
            context['error'] = "Please select at least one medicine."
            return render(request, 'core/generate_bill.html', context)

        try:
            selected_medicines = Medicine.objects.filter(id__in=medicine_ids)

            total_amount = 0
            bill_items_data = []

            for i, med in enumerate(selected_medicines):
                quantity_str = quantities_raw[i] if i < len(quantities_raw) else '0'
                quantity = int(quantity_str)

                if quantity <= 0:
                    context['error'] = f"Quantity for {med.name} must be greater than zero."
                    return render(request, 'core/generate_bill.html', context)

                if quantity > med.quantity:
                    context['error'] = f"Not enough quantity for {med.name}."
                    return render(request, 'core/generate_bill.html', context)

                amount = med.price * quantity
                total_amount += amount
                bill_items_data.append({'medicine': med, 'quantity': quantity})

            # Create the bill
            bill = Bill.objects.create(
                patient_name=patient_name,
                amount_paid=total_amount,
                date=timezone.now()
            )

            # Create bill items and update stock
            for item in bill_items_data:
                BillItem.objects.create(
                    bill=bill,
                    medicine=item['medicine'],
                    quantity=item['quantity']
                )
                item['medicine'].quantity -= item['quantity']
                item['medicine'].save()

            return redirect('bill_details', bill_id=bill.id)

        except ValueError:
            context['error'] = "Invalid quantity value."
            return render(request, 'core/generate_bill.html', context)

    return render(request, 'core/generate_bill.html', context)


@login_required(login_url='/login/')
def bill_details(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    items = BillItem.objects.filter(bill=bill).select_related('medicine')

    return render(request, 'core/bill_details.html', {
        'patient_name': bill.patient_name,
        'total_amount': bill.amount_paid,
        'items': items,
        'bill': bill
    })


@login_required(login_url='/login/')
def download_pdf(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    items = BillItem.objects.filter(bill=bill).select_related('medicine')
    template_path = 'core/bill_pdf.html'

    context = {
        'bill': bill,
        'items': items,
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bill_{bill_id}.pdf"'

    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('PDF generation failed.<pre>' + html + '</pre>')

    return response


@login_required(login_url='/login/')
def bill_success(request):
    return render(request, 'core/bill_success.html')


@login_required(login_url='/login/')
def bill_history(request):
    bills = Bill.objects.order_by('-date')  # Most recent first
    paginator = Paginator(bills, 10)  # 10 bills per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/bill_history.html', {'page_obj': page_obj})
