from django.shortcuts import render, redirect

from .forms import TicketForm


# def ticket(request):
#     if request.method == 'POST':
#         form = TicketForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('ticket:ticket')
#     else:
#         form = TicketForm()
#     return render(request, 'forms/ticket.html', {'form': form})


def ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('ticket:ticket')

    else:
        form = TicketForm()

    return render(request, 'forms/ticket.html', {'form': form})
